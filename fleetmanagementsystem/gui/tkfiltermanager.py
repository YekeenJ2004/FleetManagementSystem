from tkinter import ttk
from gui.utils.appmessage import AppMessage
from gui.utils.customdatepicker import CustomDatePicker
import logging
from core.filtermanager import FilterManager


class TkFilterManager(FilterManager):
    """
    A subclass of FilterManager that integrates with Tkinter-specific
    components.
    """
    def handle_invalid_range(self, field_from: str, field_to: str) -> None:
        """
        Display an error message using Tkinter's AppMessage.
        """
        try:
            AppMessage.show(
                "error",
                f"'{field_to}' cannot be earlier than '{field_from}'."
            )
        except Exception as e:
            logging.error(f"Error displaying message: {e}")

    def clear_filters(self) -> None:
        """
        Reset all filters to their default values, including CustomDatePicker
        widgets.
        """
        try:
            for field, widget in self.filters.items():
                if field == "Order By":
                    widget.set("ManufactureYear")
                elif field == "Order Direction":
                    widget.set("ASC")
                elif isinstance(widget, ttk.Combobox):
                    widget.set("All")
                elif isinstance(widget, ttk.Entry):
                    widget.delete(0, "end")
                elif isinstance(widget, CustomDatePicker):
                    widget.delete()
        except Exception as e:
            logging.error(f"Error clearing filters in TkFilterManager: {e}")
