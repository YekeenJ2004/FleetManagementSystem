import pytest
from tkinter import ttk, Tk
from tkcalendar import DateEntry
from filtermanager import FilterManager
from appmessage import AppMessage


class TestFilterManager:
    """Test suite for the FilterManager class."""

    @pytest.fixture
    def mock_filters(self, monkeypatch):
        """Set up a mock filters dictionary with tkinter widgets."""
        root = Tk()
        filters = {
            "Type": ttk.Combobox(root, values=["Sedan", "SUV", "All"], state="readonly"),
            "Year From": ttk.Combobox(root, values=["2020", "2021", "2022"], state="readonly"),
            "Year To": ttk.Combobox(root, values=["2020", "2021", "2022"], state="readonly"),
            "Tax Due Date From": DateEntry(root, date_pattern="yyyy-mm-dd"),
            "Tax Due Date To": DateEntry(root, date_pattern="yyyy-mm-dd"),
            "Service Date From": DateEntry(root, date_pattern="yyyy-mm-dd"),
            "Service Date To": DateEntry(root, date_pattern="yyyy-mm-dd"),
            "Search": ttk.Entry(root),
        }

        # Initialize widgets
        for key, widget in filters.items():
            if isinstance(widget, ttk.Combobox):
                widget.set("All")
            elif isinstance(widget, ttk.Entry):
                widget.delete(0, "end")
            elif isinstance(widget, DateEntry):
                widget.delete(0, "end")

        # Mock AppMessage.show for testing
        self.messages = []

        def mock_show(message_type, message, error=""):
            self.messages.append((message_type, message, error))

        monkeypatch.setattr(AppMessage, "show", mock_show)

        return filters

    def test_apply_filters_with_valid_data(self, mock_filters):
        """Test applying filters with valid data."""
        mock_filters["Type"].set("SUV")
        mock_filters["Year From"].set("2020")
        mock_filters["Year To"].set("2021")
        mock_filters["Search"].insert(0, "Example")

        manager = FilterManager(mock_filters)
        query, values = manager.apply_filters()

        assert "WHERE" in query
        assert set(values) == {"SUV", "2020", "2021", "%Example%"}

    def test_apply_filters_with_empty_filters(self, mock_filters):
        """Test applying filters with no filters set."""
        manager = FilterManager(mock_filters)
        query, values = manager.apply_filters()

        assert query == "SELECT * FROM Vehicles"
        assert values == []

    def test_clear_filters(self, mock_filters):
        """Test clearing all filters."""
        mock_filters["Type"].set("SUV")
        mock_filters["Year From"].set("2020")
        mock_filters["Search"].insert(0, "Example")

        manager = FilterManager(mock_filters)
        manager.clear_filters()

        assert mock_filters["Type"].get() == "All"
        assert mock_filters["Year From"].get() == "All"
        assert mock_filters["Search"].get() == ""
