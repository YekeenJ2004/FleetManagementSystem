from constants import SQL_MAPPINGS
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from appmessage import AppMessage


class FilterManager:
    def __init__(self, filters):
        self.filters = filters

    def apply_filters(self):
        """Build the SQL WHERE clause and values based on the filters."""
        where_clauses = []
        values = []

        def add_range_filter(field_from, field_to, db_field):
            """Add range filter for date or year fields."""
            from_value = self.filters.get(field_from, "").get()
            to_value = self.filters.get(field_to, "").get()

            # Skip adding conditions if both range fields are empty
            if not from_value and not to_value:
                return  

            if from_value and to_value and to_value < from_value:
                AppMessage.show("error", f"'{field_to}' cannot be earlier than '{field_from}'.")
            if from_value:
                where_clauses.append(f'"{db_field}" >= ?')
                values.append(from_value)
            if to_value:
                where_clauses.append(f'"{db_field}" <= ?')
                values.append(to_value)

        # Search Bar
        search_query = self.filters.get("Search", "").get().strip()
        if search_query:
            search_fields = ["Type", "RegistrationNumber", "TaxStatus", "FuelType"]
            where_clauses.append(" OR ".join([f'"{field}" LIKE ?' for field in search_fields]))
            values.extend([f"%{search_query}%"] * len(search_fields))

        # Range Filters
        add_range_filter("Year From", "Year To", "ManufactureYear")
        add_range_filter("Tax Due Date From", "Tax Due Date To", "TaxDueDate")
        add_range_filter("Service Date From", "Service Date To", "ServiceDate")

        # Dropdown Filters
        for field, widget in self.filters.items():
            if field not in ["Year From", "Year To", "Tax Due Date From", "Tax Due Date To", "Service Date From", "Service Date To", "Search"]:
                value = widget.get()
                if value and value != "All":
                    where_clauses.append(f'"{SQL_MAPPINGS[field]}" = ?')
                    values.append(value)

        query = "SELECT * FROM Vehicles"
        if where_clauses:
            query += f" WHERE {' AND '.join(where_clauses)}"
        print(query)
        return query, values

    def clear_filters(self):
        """Reset all filters to their default values."""
        for field, widget in self.filters.items():
            if isinstance(widget, ttk.Combobox):
                widget.set("All")  # Reset dropdowns to "All"
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)  # Clear search bar
            elif isinstance(widget, DateEntry):
                widget.delete(0, tk.END)  # Clear date picker
