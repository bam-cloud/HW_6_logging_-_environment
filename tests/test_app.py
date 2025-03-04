"""Tests for the App class."""

import logging
import os
from unittest.mock import patch
import pytest

from app import App

"""_summary_"""
def test_app_get_environment_variable():
    app = App()

    # Mock the environment variables using patch
    with patch.dict(os.environ, {'ENVIRONMENT': 'DEVELOPMENT'}):
        app.load_environment_variables()

        # Retrieve the current environment setting
        current_env = app.get_environment_variable('ENVIRONMENT')

        # Assert that the current environment is one of the expected values
        assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

# Run the test
test_app_get_environment_variable()


def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit

#def test_app_start_unknown_command(capfd, monkeypatch):
 #   """Test how the REPL handles an unknown command before exiting."""
  #  # Simulate user entering an unknown command followed by 'exit'
  #  inputs = iter(['unknown_command', 'exit'])
   # monkeypatch.setattr('builtins.input', lambda _: next(inputs))
   
def test_app_start_unknown_command(caplog):
    app = App()

    # Capture logs
    with caplog.at_level(logging.ERROR):
        with pytest.raises(KeyError, match="Unknown command"):
            app.command_handler.execute_command("invalid_command")  # Use an invalid command

    # Assert the log contains the expected error message
    assert "Unknown command" in caplog.text, f"Expected error message, but got: {caplog.text}"

    app = App()

    with pytest.raises(SystemExit):
        app.start()

    # Optionally, check for specific exit code or message
    # assert excinfo.value.code == expected_exit_code

     # Capture both stdout and stderr
    captured = capfd.readouterr()

    # Verify that the unknown command was handled as expected
    assert "No such command: unknown_command" in captured.err, f"Expected error message, but got: {captured.err}"

    # Assert that the 'Exiting...' message is in stdout
    assert "Exiting..." in captured.out, f"Expected 'Exiting...', but got: {captured.out}"
