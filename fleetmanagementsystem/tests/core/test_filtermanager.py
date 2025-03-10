import pytest
from tkinter import ttk, Tk
from fleetmanagementsystem.gui.utils.customdatepicker import CustomDatePicker
from fleetmanagementsystem.core.filtermanager import FilterManager
from fleetmanagementsystem.gui.utils.appmessage import AppMessage


class TestFilterManager:
    """Test suite for the FilterManager class."""

    @pytest.fixture
    def mock_filters(self, monkeypatch):
        """Set up a mock filters dictionary with tkinter widgets."""
        root = Tk()
        filters = {
            "Type": ttk.Combobox(
                root, values=["Sedan", "SUV", "All"], state="readonly"
            ),
            "Year From": ttk.Combobox(
                root, values=["2020", "2021", "2022"], state="readonly"
            ),
            "Year To": ttk.Combobox(
                root, values=["2020", "2021", "2022"], state="readonly"
            ),
            "Tax Due Date From": CustomDatePicker(root),
            "Tax Due Date To": CustomDatePicker(root),
            "Service Date From": CustomDatePicker(root),
            "Service Date To": CustomDatePicker(root),
            "Search": ttk.Entry(root),
            "Order By": ttk.Combobox(
                root, values=["Type", "RegistrationNumber", "ManufactureYear"],
                state="readonly"
            ),
            "Order Direction": ttk.Combobox(
                root, values=["ASC", "DESC"], state="readonly"
            ),
        }

        # Initialize widgets
        for key, widget in filters.items():
            if key == "Order By":
                widget.set("ManufactureYear")
            elif key == "Order Direction":
                widget.set("ASC")  # Default Order Direction to ASC
            elif isinstance(widget, ttk.Combobox):
                widget.set("All")
            elif isinstance(widget, ttk.Entry):
                widget.delete(0, "end")
            elif isinstance(widget, CustomDatePicker):
                widget.delete()
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
        mock_filters["Order By"].set("Type")
        mock_filters["Order Direction"].set("ASC")

        manager = FilterManager(mock_filters)
        query, values = manager.apply_filters()

        assert "WHERE" in query
        assert "ORDER BY" in query
        assert "Type" in query
        assert "ASC" in query
        assert set(values) == {"SUV", "2020", "2021", "%Example%"}

    def test_apply_filters_with_order_by_only(self, mock_filters):
        """Test applying filters with only the Order By fields set."""
        mock_filters["Order By"].set("ManufactureYear")
        mock_filters["Order Direction"].set("DESC")

        manager = FilterManager(mock_filters)
        query, values = manager.apply_filters()

        assert "ORDER BY" in query
        assert '"ManufactureYear" DESC' in query
        assert values == []

    def test_apply_filters_with_empty_filters(self, mock_filters):
        """Test applying filters with no filters set."""
        manager = FilterManager(mock_filters)
        query, values = manager.apply_filters()

        assert query == 'SELECT * FROM Vehicles ORDER BY "ManufactureYear" ASC'
        assert values == []
