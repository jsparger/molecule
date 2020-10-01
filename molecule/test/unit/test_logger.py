#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import logging

from molecule import logger

# from molecule.util import strip_ansi_color

# @pytest.mark.parametrize(
#     "logger_method_name,expected_stdout,expected_stderr",
#     [
#         pytest.param("info", None, "foo", id="info"),
#         # ("out", None, "    foo\n",
#         pytest.param("warning", None, "foo", id="warning"),
#         pytest.param("error", None, "ERROR: foo", id="error"),
#         pytest.param("critical", None, "ERROR: foo", id="critical"),
#     ],
#     # indirect=["logger_method_name"],
# )
# def test_logger_methods(capsys, monkeypatch, logger_method_name, expected_stdout, expected_stderr):
#     monkeypatch.setenv("PY_COLORS", "1")
#     log = logger.get_logger(__name__)
#     getattr(log, logger_method_name)("foo")
#     stdout, stderr = capsys.readouterr()

#     if expected_stdout:
#         stdout_clean = strip_ansi_color(stdout)
#         # out method is not expected to add any ANSI
#         if logger_method_name != "out":
#             assert expected_stdout != stdout
#         assert expected_stdout == stdout_clean
#     if expected_stderr:
#         stderr_clean = strip_ansi_color(stderr)
#         assert expected_stderr in stderr_clean

#     monkeypatch.setenv("PY_COLORS", "0")


def test_markup_detection_pycolors0(monkeypatch):
    monkeypatch.setenv("PY_COLORS", "0")
    assert not logger.should_do_markup()


def test_markup_detection_pycolors1(monkeypatch):
    monkeypatch.setenv("PY_COLORS", "1")
    assert logger.should_do_markup()


def test_markup_detection_tty_yes(mocker):
    mocker.patch("sys.stdout.isatty", return_value=True)
    mocker.patch("os.environ", {"TERM": "xterm"})
    assert logger.should_do_markup()
    mocker.resetall()
    mocker.stopall()


def test_markup_detection_tty_no(mocker):
    mocker.patch("os.environ", {})
    mocker.patch("sys.stdout.isatty", return_value=False)
    assert not logger.should_do_markup()
    mocker.resetall()
    mocker.stopall()


def test_logger_class():
    class FooLogger(logging.getLoggerClass()):
        """stub logger that subclasses logging.getLoggerClass()."""

    logging.setLoggerClass(FooLogger)

    # this test throws RecursionError prior to bugfix
    assert FooLogger("foo")
