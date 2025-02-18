import pytest
import logging
from tkinter import ttk, Tk
from appmessage import AppMessage
from utils.customdatepicker import CustomDatePicker
from tkfiltermanager import TkFilterManager

class MockWidget:
    def __init__(self, value="All"):
        self.value = value
    
    def get(self):
        return self.value
    
    def set(self, value):
        self.value = value
    
    def delete(self):
        self.set("All")  # Ensuring reset behavior is consistent

class MockAppMessage:
    @staticmethod
    def show(msg_type, message):
        print(f"[{msg_type.upper()}]: {message}")

class TestTkFilterManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.root = Tk()
        self.root.withdraw()  # Hide the Tkinter window
        self.filters = {
            "Year From": MockWidget("2025-01-01"),
            "Year To": MockWidget("2020-01-01"),
            "FuelType": MockWidget("Gasoline"),
            "Order By": MockWidget("ManufactureYear"),
            "Order Direction": MockWidget("ASC"),
            "Custom Date": MockWidget("2025-01-01")  # Mocking CustomDatePicker
        }
        self.filter_manager = TkFilterManager(self.filters)
    
    def test_handle_invalid_range(self, monkeypatch):
        monkeypatch.setattr(AppMessage, "show", lambda *args, **kwargs: None)  # Suppress popups
        self.filter_manager.handle_invalid_range("Year From", "Year To")
        assert True  # Just verifying execution, assuming no exception is raised

    def test_clear_filters(self):
        self.filter_manager.clear_filters()
        assert self.filters["Order By"].get() == "ManufactureYear"
        assert self.filters["Order Direction"].get() == "ASC"
        assert self.filters["FuelType"].get() == "All"  # Ensuring reset behavior
        assert self.filters["Year From"].get() == ""
        assert self.filters["Year To"].get() == ""
        assert self.filters["Custom Date"].get() == "All"  # Ensuring custom date is reset