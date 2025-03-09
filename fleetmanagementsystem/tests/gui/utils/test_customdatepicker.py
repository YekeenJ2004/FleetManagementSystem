import pytest
from tkinter import ttk, Tk, Toplevel
from fleetmanagementsystem.gui.utils.customdatepicker import CustomDatePicker
from fleetmanagementsystem.gui.utils.appmessage import AppMessage
from typing import Generator, List, Tuple


class TestCustomDatePicker:
    """Test suite for the CustomDatePicker class."""

    @pytest.fixture(autouse=True)
    def setup(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> Generator[None, None, None]:
        """Fixture to set up the tkinter root and a date picker instance
        before each test."""
        self.root = Tk()
        self.root.withdraw()  # Prevent the root window from showing
        self.date_picker = CustomDatePicker(self.root)

        # ✅ Manually create `day_dropdown` since `open_date_picker()` is mocked
        self.date_picker.day_dropdown = ttk.Combobox(
            self.root, state="readonly"
        )

        # ✅ Mock `open_date_picker()` to prevent UI popups
        monkeypatch.setattr(
            CustomDatePicker, "open_date_picker", lambda *args: None
        )

        # ✅ Mock `AppMessage.show()` to prevent blocking popups
        self.captured_messages: List[Tuple[str, str, str]] = []

        def mock_show(level: str, title: str, message: str = "") -> None:
            """Mock AppMessage.show() to capture the message."""
            self.captured_messages.append((level, title, message))

        monkeypatch.setattr(AppMessage, "show", mock_show)

        yield
        self.root.destroy()

    def test_open_date_picker_creates_popup(self, monkeypatch):
        """Ensure `open_date_picker` creates a popup window properly."""

        monkeypatch.undo()

        assert not hasattr(self.date_picker, "popup"), \
            "Popup should not exist before calling `open_date_picker`."

        self.date_picker.open_date_picker()  # ✅ Call the actual method

        assert hasattr(self.date_picker, "popup"), "Popup should be created."
        assert isinstance(self.date_picker.popup, Toplevel), \
            "Popup should be an instance of Toplevel."

    # ✅ Core Initialization Tests
    def test_initialization(self) -> None:
        """Test that the date picker initializes correctly."""
        assert isinstance(self.date_picker, CustomDatePicker)
        assert isinstance(self.date_picker.entry, ttk.Combobox)
        assert self.date_picker.get() != ""

    def test_set_date_to_current(self) -> None:
        """Ensure the date picker correctly sets the current date."""
        self.date_picker.set_date_to_current()
        assert self.date_picker.get() != ""  # It should have a date value

    # ✅ Date Manipulation Tests
    def test_insert_date(self) -> None:
        """Verify that inserting a date updates the displayed value."""
        self.date_picker.insert(0, "2024-05-10")
        assert self.date_picker.get() == "2024-05-10"

    def test_get_date(self) -> None:
        """Ensure the get() method retrieves the correct value."""
        self.date_picker.insert(0, "2023-12-25")
        assert self.date_picker.get() == "2023-12-25"

    def test_delete_date(self) -> None:
        """Ensure deleting a date clears the input field."""
        self.date_picker.insert(0, "2025-01-01")
        self.date_picker.delete()
        assert self.date_picker.get() == ""

    def test_set_valid_date(self) -> None:
        """Test setting a valid date manually."""
        self.date_picker.set_date("2024-06-15")
        assert self.date_picker.get() == "2024-06-15"

    def test_set_invalid_date_fallback(self) -> None:
        """Ensure that an invalid date falls back to today's date."""
        initial_date = self.date_picker.get()
        self.date_picker.set_date("invalid-date")
        assert self.date_picker.get() != "invalid-date"
        assert self.date_picker.get() == initial_date

    # ✅ Month & Day Updates
    def test_update_days(self) -> None:
        """Test updating days based on selected month."""
        self.date_picker.month_var.set("Feb")
        self.date_picker.update_days()
        assert "28" in self.date_picker.day_dropdown["values"]

    def test_update_days_leap_year(self) -> None:
        """Ensure February handles leap years properly."""
        self.date_picker.year_var.set(2024)  # Leap year
        self.date_picker.month_var.set("Feb")
        self.date_picker.update_days()
        assert "29" in self.date_picker.day_dropdown["values"]

    # ✅ Error Handling Tests
    def test_error_handling(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure error handling works correctly and prevents popups."""
        self.captured_message = None  # Initialize before assignment
        picker = CustomDatePicker(self.root)

        def mock_show(level: str, title: str, message: str) -> None:
            """Mock AppMessage.show() to capture the message."""
            self.captured_message = (level, title, message)

        monkeypatch.setattr(AppMessage, "show", mock_show)

        picker.set_date("invalid-date")  # This should trigger error handling

        # ✅ Ensure AppMessage.show was called correctly
        assert self.captured_message is not None, \
            "AppMessage.show was not called"
        assert self.captured_message[0] == "error"
        assert "Invalid date format!" in self.captured_message[1]

    def test_day_selection_updates_entry(self) -> None:
        """Ensure selecting a day updates the entry field."""
        self.date_picker.day_var.set(15)
        self.date_picker.set_date()
        assert "15" in self.date_picker.get()

    def test_year_selection_updates_entry(self) -> None:
        """Ensure selecting a year updates the entry field."""
        self.date_picker.year_var.set(2025)
        self.date_picker.set_date()
        assert "2025" in self.date_picker.get()

    def test_update_days_with_full_date_selection(self) -> None:
        """Ensure that changing month, year, and day correctly updates
        the selection."""
        self.date_picker.year_var.set(2024)
        self.date_picker.month_var.set("Mar")
        self.date_picker.day_var.set(10)
        self.date_picker.set_date()
        assert self.date_picker.get() == "2024-03-10"
