import tkinter as tk
from tkinter import ttk
from fleetmanagementsystem.gui.utils.customdatepicker import CustomDatePicker
import datetime
from fleetmanagementsystem.core.vehicle import Vehicle
from typing import Callable, Optional, Dict, Any
from fleetmanagementsystem.core.constants import (
    SQL_MAPPINGS,
    VEHICLE_CLASS_MAPPINGS,
    VEHICLE_POPUP_FIELDS,
    FIELD_OPTIONS,
)
from fleetmanagementsystem.gui.utils.appmessage import AppMessage
from fleetmanagementsystem.core.vehiclemanager import VehicleManager
from fleetmanagementsystem.core.customtypes import VehiclePopupAction


class VehiclePopup:
    """Popup window for adding or editing a vehicle."""

    def __init__(
        self,
        root: Any,
        manager: VehicleManager,
        list_all_vehicles: Callable[[], None],
        mode: VehiclePopupAction,
        vehicle_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        A popup window for adding or editing vehicle information.

        Attributes:
            root (tk.Tk): The root window.
            manager (VehicleManager): The manager instance for database
            operations.
            list_all_vehicles (Callable): Function to refresh the vehicle list
            in the main application.
            mode (str): The mode of the popup, either 'add' or 'edit'.
            vehicle_data (Optional[Dict[str, Any]]): Data of the vehicle being
                edited, if applicable.
        """
        self.root = root
        self.manager = manager
        self.list_all_vehicles = list_all_vehicles
        self.mode = mode
        self.vehicle_data = vehicle_data

        self.popup = tk.Toplevel(root)
        self.popup.title("Edit Vehicle" if mode == "edit" else "Add Vehicle")

        self.popup.transient(root)  # Make the popup window a transient child
        self.popup.grab_set()      # Direct all input events to the popup
        self.popup.focus_force()   # Bring the popup to focus

        self.current_year = datetime.datetime.now().year
        self.manufacture_years = [
            str(year)
            for year in range(self.current_year, self.current_year - 50, -1)
        ]

        self.inputs = {}
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create and layout the widgets in the popup window.
        """
        try:
            fields = VEHICLE_POPUP_FIELDS + [
                (
                    "Manufacture Year",
                    lambda parent: ttk.Combobox(
                        parent, values=self.manufacture_years, state="readonly"
                    ),
                    ""
                )
            ]

            if self.mode == "edit" and self.vehicle_data:
                for i, field in enumerate(fields):
                    fields[i] = (field[0], field[1], self.vehicle_data[i + 1])

            for i, (label, widget_type, initial_value) in enumerate(fields):
                tk.Label(self.popup, text=label).grid(row=i, column=0)

                if widget_type == CustomDatePicker:
                    widget_instance = CustomDatePicker(self.popup)
                    # Get the actual entry field
                    widget = widget_instance.entry
                else:
                    widget = widget_type(self.popup)

                widget.grid(row=i, column=1)

                if isinstance(widget, ttk.Combobox):
                    widget.set(initial_value)
                elif isinstance(widget, CustomDatePicker):
                    try:
                        widget.set_date(initial_value)
                    except ValueError:
                        # Fallback to today's date if the stored date is
                        # invalid
                        widget.set_date(datetime.date.today())
                else:
                    widget.insert(0, initial_value)

                self.inputs[label] = widget

            tk.Button(
                self.popup,
                text="Save Changes" if self.mode == "edit" else "Add Vehicle",
                command=self.save_changes
            ).grid(row=len(fields), column=0, pady=10)

            print("here")
            if self.mode == "edit":
                tk.Button(
                    self.popup,
                    text="Delete Vehicle",
                    command=self.delete_vehicle
                ).grid(row=len(fields), column=1, pady=10)
        except Exception as e:
            AppMessage.show("error", f"Failed to create widgets: {e}")

    def save_changes(self) -> None:
        """
        Save the changes made to the vehicle.

        This method validates the input data and either adds a new
        vehicle or updates an existing one in the database. It shows
        appropriate messages based on the success or failure of the operation.
        """
        try:
            updates = {}
            for label, widget in self.inputs.items():
                value = widget.get()

                # Validate each field based on its expected data type
                if label == "Manufacture Year":
                    if not value.isdigit():
                        raise ValueError(f"{label} must be a valid number.")
                    updates[label] = int(value)  # Convert to int
                elif label in ["Tax Due Date", "Service Date"]:  # Date fields
                    if not value:
                        raise ValueError(f"{label} cannot be empty.")
                    try:
                        # Ensure valid date format
                        datetime.datetime.strptime(value, "%Y-%m-%d")
                    except ValueError:
                        raise ValueError(
                            f"{label} must be in YYYY-MM-DD format."
                        )
                    updates[label] = value
                elif label in ["Type", "Tax Status", "Tax Type", "Fuel Type"]:
                    # Example: Check if value is in the predefined options
                    if value not in FIELD_OPTIONS[label]:
                        raise ValueError(f"{label} must be a valid option.")
                    updates[label] = value
                elif label == "Registration Number":  # String field
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(
                            f"{label} must be a non-empty string."
                        )
                    updates[label] = value.strip()
                else:
                    updates[label] = value

            # Map the field names for database or class object compatibility
            updates = {
                SQL_MAPPINGS[key]: value for key, value in updates.items()
            }

            if self.mode == "edit":
                self.manager.update_vehicle(self.vehicle_data[2], **updates)
                AppMessage.show("info", "Vehicle updated successfully!")
            else:
                updates = {
                    VEHICLE_CLASS_MAPPINGS[key]: value
                    for key, value in updates.items()
                }
                new_vehicle = Vehicle(**updates)
                self.manager.add_vehicle(new_vehicle)
                AppMessage.show("info", "Vehicle added successfully!")

            self.popup.destroy()
            self.list_all_vehicles()
        except ValueError as e:
            # Show specific validation error in a popup
            print(e)
            AppMessage.show("error", "Validation Error", e)
        except Exception as e:
            print(e)
            # Handle generic errors
            AppMessage.show("error", "Failed to save vehicle", e)

    def delete_vehicle(self) -> None:
        """
        Delete the current vehicle from the database.

        Displays appropriate success or error messages based on the outcome.
        """
        try:
            self.manager.remove_vehicle(self.vehicle_data[2])
            AppMessage.show("info", "Vehicle deleted successfully!")
            self.popup.destroy()
            self.list_all_vehicles()
        except Exception as e:
            AppMessage.show("error", "Failed to delete vehicle", e)
