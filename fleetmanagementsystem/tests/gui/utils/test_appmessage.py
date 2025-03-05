import pytest
import logging
from tkinter import messagebox
from fleetmanagementsystem.gui.utils.appmessage import AppMessage


class TestAppMessage:
    @pytest.fixture(autouse=True)
    def setup_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Capture logging output for testing.

        Note:
            This fixture is used to capture logging output for testing
            purposes.

        Args:
            caplog: Pytest fixture to capture logging output.
        """
        caplog.set_level(logging.INFO)
        self.caplog = caplog

    def test_show_info_message(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test showing an info message and logging it.

        Args:
            monkeypatch: Pytest fixture to mock the messagebox.showinfo method.
        """
        self.logged_message: tuple[str, str] | None = None

        def mock_showinfo(title: str, message: str) -> None:
            self.logged_message = (title, message)

        monkeypatch.setattr(messagebox, "showinfo", mock_showinfo)

        AppMessage.show("info", "Test Information Message")

        assert self.logged_message == (
            "Information", "Test Information Message"
        )
        assert "Test Information Message" in self.caplog.text

    def test_show_error_message(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test showing an error message and logging it.

        Args:
            monkeypatch: Pytest fixture to mock the messagebox.showerror
            method.
        """
        self.logged_message: tuple[str, str] | None = None

        def mock_showerror(title: str, message: str) -> None:
            self.logged_message = (title, message)

        monkeypatch.setattr(messagebox, "showerror", mock_showerror)

        AppMessage.show("error", "Test Error Message", "TestError")

        assert self.logged_message == ("Error", "Test Error Message,TestError")
        assert "Test Error Message" in self.caplog.text
        assert "TestError" in self.caplog.text

    def test_show_warning_message(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test showing a warning message and logging it.

        Args:
            monkeypatch: Pytest fixture to mock the messagebox.showwarning
            method.
        """
        self.logged_message: tuple[str, str] | None = None

        def mock_showwarning(title: str, message: str) -> None:
            self.logged_message = (title, message)

        monkeypatch.setattr(messagebox, "showwarning", mock_showwarning)

        AppMessage.show("warning", "Test Warning Message", "TestWarning")

        assert self.logged_message == (
            "Warning", "Test Warning Message,TestWarning"
        )
        assert "Test Warning Message" in self.caplog.text
        assert "TestWarning" in self.caplog.text

    def test_invalid_message_type(self) -> None:
        """Test handling of an invalid message type."""
        with pytest.raises(ValueError, match="Invalid message type"):
            AppMessage.show("invalid", "This should fail")
