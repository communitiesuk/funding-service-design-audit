"""
Tests if expected logs are printed
"""
import logging
import sys

import pytest


@pytest.mark.usefixtures("flask_test_client")
class TestLogging:
    def test_print(self, capsys):
        """
        GIVEN a running application
        WHEN we print() or an error is sent to stderr
        THEN the message or error is outputted
        :param capsys:
        :return:
        """
        print("hello")
        sys.stderr.write("world\n")
        captured = capsys.readouterr()
        assert captured.out == "hello\n"
        assert captured.err == "world\n"
        print("next")
        captured = capsys.readouterr()
        assert captured.out == "next\n"

    def test_logging(self, caplog):
        """
        GIVEN a running flask application
        WHEN we user the app.logger
        THEN the message is logged in the correct format
        :param caplog:
        :return:
        """
        logging.error("This is an error")
        assert (
            caplog.text
            == "ERROR    root:test_logging.py:37 This is an error\n"
        )
