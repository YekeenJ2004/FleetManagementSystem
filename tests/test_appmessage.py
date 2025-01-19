import pytest
from tkinter import messagebox
from appmessage import AppMessage
import logging


class TestAppMessage:
    """Test suite for the AppMessage class."""

    @pytest.fixture(autouse=True)
    def setup_mock_messagebox(self, monkeypatch):
        """Mock the tkinter messagebox methods."""
        self.messagebox_calls = []

        def mock_showinfo(title, msg):
            self.messagebox_calls.append(("info", title, msg))

        def mock_showerror(title, msg):
            self.messagebox_calls.append(("error", title, msg))

        def mock_showwarning(title, msg):
            self.messagebox_calls.append(("warning", title, msg))

        monkeypatch.setattr(messagebox, "showinfo", mock_showinfo)
        monkeypatch.setattr(messagebox, "showerror", mock_showerror)
        monkeypatch.setattr(messagebox, "showwarning", mock_showwarning)

    @pytest.fixture(autouse=True)
    def setup_mock_logging(self, monkeypatch):
        """Mock the logging methods."""
        self.log_calls = []

        def mock_info(msg):
            self.log_calls.append(("info", msg))

        def mock_error(msg):
            self.log_calls.append(("error", msg))

        def mock_warning(msg):
            self.log_calls.append(("warning", msg))

        monkeypatch.setattr(logging, "info", mock_info)
        monkeypatch.setattr(logging, "error", mock_error)
        monkeypatch.setattr(logging, "warning", mock_warning)

    def test_show_info_message(self):
        """Test displaying an info message."""
        AppMessage.show("info", "Test info message")
        assert self.log_calls == [("info", "Test info message")]
        assert self.messagebox_calls == [("info", "Information", "Test info message")]

    def test_show_error_message(self):
        """Test displaying an error message."""
        AppMessage.show("error", "Test error message", error="Details")
        assert self.log_calls == [("error", "Test error messageDetails")]
        assert self.messagebox_calls == [("error", "Error", "Test error message")]

    def test_show_warning_message(self):
        """Test displaying a warning message."""
        AppMessage.show("warning", "Test warning message")
        assert self.log_calls == [("warning", "Test warning message")]
        assert self.messagebox_calls == [("warning", "Warning", "Test warning message")]

    def test_invalid_message_type(self):
        """Test handling an invalid message type."""
        with pytest.raises(ValueError, match="Invalid message type. Use 'info' or 'error'."):
            AppMessage.show("invalid", "Invalid message type")
