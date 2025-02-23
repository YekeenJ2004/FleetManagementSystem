import tkinter as tk
from tkinter import ttk
from gui.utils.customdatepicker import CustomDatePicker
from core.vehiclemanager import VehicleManager
from gui.tkfiltermanager import TkFilterManager
from core.constants import (
    COLUMN_NAMES, ASCII_ART, FILTER_RANGE_FIELDS, FILTER_OPTIONS
)
import datetime
from gui.vehiclepopup import VehiclePopup
from gui.utils.appmessage import AppMessage
from typing import List, Any, Optional
import logging
from gui.utils.tooltip import ToolTip


class FleetApp:
    """
    Fleet Management System application.

    This class handles the main GUI components, user interactions, and
    integrates with the `VehicleManager` and `FilterManager`
    for backend operations.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the Fleet Management System.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.manager = VehicleManager()
        self.root = root
        self.root.title("Fleet Management System")

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create and layout the widgets for the application.
        """
        try:
            current_year = datetime.datetime.now().year
            year_options = [int(year) for year in range(
                current_year - 50, current_year + 1)]

            # Top frame for ASCII art, buttons, and search functionality
            self.top_frame = tk.Frame(self.root)
            self.top_frame.pack(fill=tk.X, pady=10)

            # Create a canvas for the main content
            # and attach a horizontal scrollbar
            self.canvas = tk.Canvas(self.root)
            self.canvas.pack(fill=tk.BOTH, expand=True)

            self.scrollbar_x = ttk.Scrollbar(
                self.root, orient=tk.HORIZONTAL, command=self.canvas.xview
            )
            self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

            # Create a frame inside the canvas to hold all content
            self.content_frame = tk.Frame(self.canvas)
            self.content_frame.pack(fill=tk.BOTH, expand=True)

            self.canvas.create_window((0, 0), window=self.content_frame)

            self.content_frame.bind(
                "<Configure>", lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")))
            self.content_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
            )

            # ASCII art on the left
            tk.Label(
                self.top_frame, text=ASCII_ART, font=("Courier", 12),
                justify=tk.LEFT
            ).pack(side=tk.LEFT, padx=10)

            # Right frame for buttons and search
            self.top_right_frame = tk.Frame(self.top_frame)
            self.top_right_frame.pack(side=tk.RIGHT, padx=10)

            # Add Vehicle, List All Vehicles, and Delete Selected buttons
            tk.Button(
                self.top_right_frame, text="Add Vehicle",
                command=self.open_add_vehicle_popup
            ).pack(side=tk.LEFT, padx=5)
            tk.Button(
                self.top_right_frame, text="List All Vehicles",
                command=self.list_all_vehicles
            ).pack(side=tk.LEFT, padx=5)
            tk.Button(
                self.top_right_frame, text="Delete Selected",
                command=self.bulk_delete
            ).pack(side=tk.LEFT, padx=5)

            # Search bar and button
            self.filters = {}
            self.filters["Search"] = tk.Entry(self.top_right_frame, width=30)
            self.filters["Search"].pack(side=tk.LEFT, padx=(10, 5))
            tk.Button(
                self.top_right_frame, text="Search", command=self.apply_filters
            ).pack(side=tk.LEFT)

            # Filter frame
            self.filter_frame = tk.Frame(self.content_frame)
            self.filter_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

            for i, (field, options) in enumerate(FILTER_OPTIONS.items()):
                tk.Label(self.filter_frame, text=field).grid(
                    row=0, column=i * 2
                )
                combo = ttk.Combobox(
                    self.filter_frame, values=options, state="readonly"
                )
                if field in ["Order By", "Order Direction"]:
                    combo.set(options[0])
                combo.grid(row=0, column=i * 2 + 1)
                self.filters[field] = combo

            # Add range filters
            for label, var, row, col in FILTER_RANGE_FIELDS:
                tk.Label(self.filter_frame, text=label).grid(
                    row=row, column=col
                )
                if "Date" in var:
                    date_picker = CustomDatePicker(
                        self.filter_frame,
                    )
                    date_picker.delete()
                    date_picker.grid(row=row, column=col + 1)
                    self.filters[var] = date_picker
                else:
                    combo = ttk.Combobox(
                        self.filter_frame,
                        values=year_options,
                        state="readonly"
                    )
                    combo.set("")
                    combo.grid(row=row, column=col + 1)
                    self.filters[var] = combo

            # Apply and Clear filter buttons
            tk.Button(
                self.filter_frame,
                text="Apply Filters",
                command=self.apply_filters
            ).grid(row=0, column=len(FILTER_OPTIONS) * 2, padx=10)
            tk.Button(
                self.filter_frame,
                text="Clear Filters",
                command=self.clear_filters
            ).grid(
                row=0,
                column=len(FILTER_OPTIONS) * 2 + 1,
                padx=10
            )

            # Add Info Icon with Tooltip
            info_icon = tk.Label(
                self.filter_frame, text="ℹ️", font=("Arial", 12),
                fg="blue", cursor="hand2"
            )
            info_icon.grid(
                row=0, column=len(FILTER_OPTIONS) * 2 + 2, padx=10, sticky="e"
            )

            # Attach Tooltip to Info Icon
            self.filter_tooltip = ToolTip(
                info_icon,
                text=("Double-click a row to edit a vehicle.\n"
                      "Click the checkbox to select a vehicle for deletion."),
                max_width=250  # Adjust tooltip width if needed
            )

            # Bind Events for Tooltip
            info_icon.bind(
                "<Enter>", lambda event: self.filter_tooltip.show_tooltip(
                    event)
            )
            info_icon.bind(
                "<Leave>", lambda event: self.filter_tooltip.hide_tooltip(
                    event)
            )

            # Frame for Treeview and scrollbar
            self.tree_frame = tk.Frame(self.root)
            self.tree_frame.pack(fill=tk.BOTH, expand=True)

            # Treeview for listing vehicles
            self.tree = ttk.Treeview(
                self.tree_frame, columns=COLUMN_NAMES, show="headings",
                height=20
            )
            self.tree.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 10)
            )

            # Define headings
            self.tree.heading("Select", text="Select")
            for col in self.tree["columns"][1:]:
                self.tree.heading(col, text=col)

            # Bind events
            self.tree.bind(
                "<Double-1>", lambda event: self.edit_vehicle_popup(event)
            )
            self.tree.bind("<Button-1>", self.toggle_checkbox)
        except Exception as e:
            logging.error(f"Error: {e}")

    def vehicle_popup(
        self, mode: str, vehicle_data: Optional[List[Any]] = None
    ) -> None:
        """
        Open a popup window for adding or editing a vehicle.

        Args:
            mode (str): The mode of the popup ("add" or "edit").
            vehicle_data (Optional[List[Any]]): Data for the vehicle to edit.
        """
        try:
            VehiclePopup(
                self.root, self.manager, self.list_all_vehicles,
                mode, vehicle_data
            )
        except Exception as e:
            AppMessage.show("error", str(e), e)

    def open_add_vehicle_popup(self) -> None:
        """
        Open a popup window for adding a new vehicle.
        """
        logging.info("Opening Add Vehicle Popup")
        self.vehicle_popup("add")

    def edit_vehicle_popup(self, event: tk.Event) -> None:
        """Open a popup window for editing an existing vehicle.

        Args:
            event (tk.Event): The event object containing information
                about the click event.
        """
        try:
            item = self.tree.identify_row(event.y)
            if not item:
                return

            values = self.tree.item(item, "values")

            if len(values) < 3:
                AppMessage.show(
                    "error", "Invalid row data. Cannot edit vehicle."
                )
                return

            reg_number = values[2]

            vehicle = self.manager.search_vehicles(
                "SELECT * FROM Vehicles WHERE RegistrationNumber = ?",
                (reg_number,)
            )

            if not vehicle:
                AppMessage.show("error", "Vehicle not found")
                return

            self.vehicle_popup("edit", vehicle[0])
        except Exception as e:
            AppMessage.show(
                "error", "Error at opening vehicle popup at root level", e
            )

    def apply_filters(self) -> None:
        """
        Apply the selected filters and update the vehicle list.
        """
        try:
            filter_manager = TkFilterManager(self.filters)
            query, values = filter_manager.apply_filters()
            logging.info(query, values)
            records = self.manager.search_vehicles(query, values)
            self.update_treeview(records)
        except ValueError as e:
            AppMessage.show("error", str(e), e)

    def clear_filters(self) -> None:
        """
        Clear all filters and reset the vehicle list.
        """
        filter_manager = TkFilterManager(self.filters)
        filter_manager.clear_filters()
        self.list_all_vehicles()

    def list_all_vehicles(self) -> None:
        """
        Fetch and display all vehicles.
        """
        records = self.manager.search_vehicles("SELECT * FROM Vehicles")
        self.update_treeview(records)

    def update_treeview(self, records: List[List[Any]]) -> None:
        """
        Update the treeview with given records.

        Args:
            records (List[List[Any]]): The records to display in the treeview.
        """
        try:
            self.tree.delete(*self.tree.get_children())
            for record in records:
                if not self.tree.exists(record[2]):  # Ensure unique iid
                    self.tree.insert(
                        "", "end", iid=record[2], values=("☐", *record[1:])
                    )
        except Exception as e:
            AppMessage.show("error", str(e), e)

    def toggle_checkbox(self, event: tk.Event) -> None:
        """
        Toggles the checkbox state (checked/unchecked) for the clicked row
        in the Treeview.

        Args:
            event (tk.Event): The event object containing information
                about the click event.
        """
        try:
            # Identify the row and column clicked
            region = self.tree.identify("region", event.x, event.y)
            if region == "cell":
                item = self.tree.identify_row(event.y)
                col = self.tree.identify_column(event.x)
                if col == "#1":  # Checkbox column
                    current_value = self.tree.item(item, "values")[0]
                    new_value = "☑" if current_value == "☐" else "☐"
                    values = (new_value, *self.tree.item(item, "values")[1:])
                    self.tree.item(item, values=values)
        except Exception as e:
            AppMessage.show("error", str(e), e)

    def bulk_delete(self) -> None:
        """
        Delete selected vehicles from the database
        and refresh the vehicle list.
        """
        try:
            selected = []
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[0] == "☑":
                    selected.append(self.tree.item(item, "values")[2])

            if not selected:
                AppMessage.show(
                    "warning", "No vehicles selected for deletion."
                )
                return

            for reg in selected:
                self.manager.remove_vehicle(reg)
            AppMessage.show(
                "info", "Selected vehicle(s) deleted successfully!"
            )
            self.list_all_vehicles()
        except Exception as e:
            AppMessage.show("error", str(e), e)
