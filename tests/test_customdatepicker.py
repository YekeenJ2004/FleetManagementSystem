import pytest
import tkinter as tk
from tkinter import ttk
from utils.customdatepicker import CustomDatePicker
from appmessage import AppMessage

class TestCustomDatePicker:
    """Test suite for the CustomDatePicker class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Fixture to set up the tkinter root and a date picker instance before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent the root window from showing
        self.date_picker = CustomDatePicker(self.root)

    def test_initialization(self):
        """Test that the date picker initializes correctly."""
        assert isinstance(self.date_picker, CustomDatePicker)
        assert isinstance(self.date_picker.entry, ttk.Combobox)
        assert self.date_picker.get() != ""  # Should be initialized to today's date

    def test_set_date_to_current(self):
        """Ensure the date picker correctly sets the current date."""
        self.date_picker.set_date_to_current()
        assert self.date_picker.get() != ""  # It should have a date value

    def test_insert_date(self):
        """Verify that inserting a date updates the displayed value."""
        self.date_picker.insert(0, "2024-05-10")
        assert self.date_picker.get() == "2024-05-10"

    def test_get_date(self):
        """Ensure the get() method retrieves the correct value."""
        self.date_picker.insert(0, "2023-12-25")
        assert self.date_picker.get() == "2023-12-25"

    def test_delete_date(self):
        """Ensure deleting a date clears the input field."""
        self.date_picker.insert(0, "2025-01-01")
        self.date_picker.delete()
        assert self.date_picker.get() == ""

    def test_open_date_picker(self):
        """Ensure the date picker popup opens properly."""
        self.date_picker.open_date_picker()
        assert hasattr(self.date_picker, "popup")  # Popup should be created
        assert isinstance(self.date_picker.popup, tk.Toplevel)

    def test_set_valid_date(self):
        """Test setting a valid date manually."""
        self.date_picker.set_date("2024-06-15")
        assert self.date_picker.get() == "2024-06-15"

    def test_set_invalid_date_fallback(self):
        """Ensure that an invalid date falls back to today's date."""
        initial_date = self.date_picker.get()
        self.date_picker.set_date("invalid-date")
        assert self.date_picker.get() != "invalid-date"
        assert self.date_picker.get() == initial_date  # Should revert to previous valid date

    def test_update_days(self):
        """Test updating days based on selected month."""
        picker = CustomDatePicker(self.root)
        picker.open_date_picker()  # Ensure `day_dropdown` exists
        picker.month_var.set("Feb")
        picker.update_days()
        assert "28" in picker.day_dropdown["values"]  # Feb has 28 days normally

    def test_update_days_leap_year(self):
        """Ensure February handles leap years properly."""
        self.date_picker.year_var.set(2024)  # Leap year
        self.date_picker.month_var.set("Feb")
        self.date_picker.update_days()
        assert "29" in self.date_picker.day_dropdown["values"]  # Should allow Feb 29 in leap years

    def test_error_handling(self, monkeypatch):
        """Ensure error handling works correctly."""
        picker = CustomDatePicker(self.root)

        def mock_show(level, title, message):
            self.captured_message = (level, title, message)

        monkeypatch.setattr(AppMessage, "show", mock_show)

        picker.set_date("invalid-date")  # This should trigger error handling
        assert self.captured_message[0] == "error"
        assert "Failed to set date" in self.captured_message[1]

    @pytest.fixture(scope="class", autouse=True)
    def teardown(self):
        """Ensure the Tkinter root is properly destroyed after tests."""
        yield
        self.root.destroy()

