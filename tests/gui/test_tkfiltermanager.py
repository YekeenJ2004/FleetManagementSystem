import pytest
from tkinter import ttk, Tk
from gui.utils.customdatepicker import CustomDatePicker
from gui.utils.appmessage import AppMessage
from gui.tkfiltermanager import TkFilterManager
from typing import List, Tuple, Generator


class TestTkFilterManager:
    """Test suite for the TkFilterManager class."""

    @pytest.fixture(autouse=True)
    def setup(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> Generator[None, None, None]:
        """Fixture to set up the Tkinter root and TkFilterManager instance.

        Args:
            monkeypatch: Pytest fixture to mock methods.
        """
        self.root = Tk()
        self.root.withdraw()  # Prevent GUI popups
        self.filter_manager = TkFilterManager(
            filters={}
        )  # Pass empty dictionary

        # Mock filters with different Tkinter widgets
        self.filter_manager.filters = {
            "Order By": ttk.Combobox(
                self.root, values=["ManufactureYear", "Model"]
            ),
            "Order Direction": ttk.Combobox(self.root, values=["ASC", "DESC"]),
            "Name": ttk.Entry(self.root),
            "Start Date": CustomDatePicker(self.root),
            "End Date": CustomDatePicker(self.root)
        }

        # Mock AppMessage to prevent blocking popups
        self.captured_messages: List[Tuple[str, str, str]] = []

        def mock_show(level: str, title: str, message: str = "") -> None:
            self.captured_messages.append((level, title, message))

        monkeypatch.setattr(AppMessage, "show", mock_show)
        yield
        self.root.destroy()

    def test_handle_invalid_range(self) -> None:
        """Test that handle_invalid_range() calls AppMessage.show()
        correctly."""
        self.filter_manager.handle_invalid_range("Start Date", "End Date")

        assert len(self.captured_messages) == 1
        assert self.captured_messages[0][0] == "error"
        assert "cannot be earlier than" in self.captured_messages[0][1]

    def test_clear_filters(self) -> None:
        """Test that clear_filters() resets all filter widgets correctly."""
        # Set some initial values
        self.filter_manager.filters["Order By"].set("Model")
        self.filter_manager.filters["Order Direction"].set("DESC")
        self.filter_manager.filters["Name"].insert(0, "Test Name")
        self.filter_manager.filters["Start Date"].insert(0, "2024-06-01")
        self.filter_manager.filters["End Date"].insert(0, "2024-06-15")

        self.filter_manager.clear_filters()

        assert self.filter_manager.filters["Order By"].get() == \
            "ManufactureYear"
        assert self.filter_manager.filters["Order Direction"].get() == "ASC"
        assert self.filter_manager.filters["Name"].get() == ""
        assert self.filter_manager.filters["Start Date"].get() == ""
        assert self.filter_manager.filters["End Date"].get() == ""
