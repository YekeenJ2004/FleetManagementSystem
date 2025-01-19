import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from vehicle import Vehicle
from constants import VEHICLE_TYPES, TAX_STATUS, TAX_TYPES, FUEL_TYPES, SQL_MAPPINGS, VEHICLE_CLASS_MAPPINGS, SERVICE_STATUS

class VehiclePopup:
    """Popup window for adding or editing a vehicle."""

    def __init__(self, root, manager, list_all_vehicles, mode, vehicle_data=None):
        self.root = root
        self.manager = manager
        self.list_all_vehicles = list_all_vehicles
        self.mode = mode
        self.vehicle_data = vehicle_data

        self.popup = tk.Toplevel(root)
        self.popup.title("Edit Vehicle" if mode == "edit" else "Add Vehicle")

        self.current_year = datetime.datetime.now().year
        self.manufacture_years = [str(year) for year in range(self.current_year, self.current_year - 20, -1)]

        self.inputs = {}
        self.create_widgets()

    def create_widgets(self):
        fields = [
            ("Type", lambda parent: ttk.Combobox(parent, values=VEHICLE_TYPES, state="readonly"), ""),
            ("Registration Number", tk.Entry, ""),
            ("Tax Status", lambda parent: ttk.Combobox(parent, values=TAX_STATUS, state="readonly"), ""),
            ("Tax Due Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd'), ""),
            ("Tax Type", lambda parent: ttk.Combobox(parent, values=TAX_TYPES, state="readonly"), ""),
            ("Service Due Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd'), ""),
            ("Service Status", lambda parent: ttk.Combobox(parent, values=SERVICE_STATUS, state="readonly"), ""),
            ("Fuel Type", lambda parent: ttk.Combobox(parent, values=FUEL_TYPES, state="readonly"), ""),
            ("Manufacture Year", lambda parent: ttk.Combobox(parent, values=self.manufacture_years, state="readonly"), "")
        ]

        if self.mode == "edit" and self.vehicle_data:
            for i, field in enumerate(fields):
                fields[i] = (field[0], field[1], self.vehicle_data[i + 1])

        for i, (label, widget_type, initial_value) in enumerate(fields):
            tk.Label(self.popup, text=label).grid(row=i, column=0)
            widget = widget_type(self.popup)
            widget.grid(row=i, column=1)

            if isinstance(widget, ttk.Combobox):
                widget.set(initial_value)
            elif isinstance(widget, DateEntry):
                try:
                    widget.set_date(datetime.datetime.strptime(initial_value, "%Y-%m-%d").date() if initial_value else datetime.date.today())
                except ValueError:
                    widget.set_date(datetime.date.today())  # Fallback to today's date
            else:
                widget.insert(0, initial_value)

            self.inputs[label] = widget

        tk.Button(self.popup, text="Save Changes" if self.mode == "edit" else "Add Vehicle", command=self.save_changes).grid(row=len(fields), column=0, pady=10)

        if self.mode == "edit":
            tk.Button(self.popup, text="Delete Vehicle", command=self.delete_vehicle).grid(row=len(fields), column=1, pady=10)

    def save_changes(self):
        try:
            updates = {}
            for label, widget in self.inputs.items():
                value = widget.get()
                if label == "Manufacture Year" and not value.isdigit():
                    raise ValueError(f"{label} must be a valid number.")
                updates[label] = value
            updates = {SQL_MAPPINGS[key]: value for key, value in updates.items()}

            if self.mode == "edit":
                self.manager.update_vehicle(self.vehicle_data[2], **updates)
                messagebox.showinfo("Success", "Vehicle updated successfully!")
            else:
                updates = {VEHICLE_CLASS_MAPPINGS[key]: value for key, value in updates.items()}
                new_vehicle = Vehicle(**updates)
                self.manager.add_vehicle(new_vehicle)
                messagebox.showinfo("Success", "Vehicle added successfully!")

            self.popup.destroy()
            self.list_all_vehicles()
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to save vehicle: {e}")

    def delete_vehicle(self):
        try:
            self.manager.remove_vehicle(self.vehicle_data[2])
            messagebox.showinfo("Success", "Vehicle deleted successfully!")
            self.popup.destroy()
            self.list_all_vehicles()
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to delete vehicle: {e}")

# class VehiclePopup:
#     """Popup window for adding or editing a vehicle."""

#     def __init__(self, root, manager, list_all_vehicles, mode, vehicle_data=None):
#         """
#         Initializes the VehiclePopup.

#         Args:
#             root: Parent tkinter window.
#             manager: Instance of VehicleManager for database operations.
#             list_all_vehicles: Method to refresh vehicle list in the main app.
#             mode: "add" or "edit" mode.
#             vehicle_data: Vehicle data for editing (default: None).
#         """
#         self.root = root
#         self.manager = manager
#         self.list_all_vehicles = list_all_vehicles
#         self.mode = mode
#         self.vehicle_data = vehicle_data

#         self.popup = tk.Toplevel(root)
#         self.popup.title("Edit Vehicle" if mode == "edit" else "Add Vehicle")

#         self.current_year = datetime.datetime.now().year
#         self.manufacture_years = [str(year) for year in range(self.current_year, self.current_year - 20, -1)]

#         self.inputs = {}
#         self.create_widgets()

#     def create_widgets(self):
#         """Creates the widgets for the popup window."""
#         fields = [
#             ("Type", lambda parent: ttk.Combobox(parent, values=VEHICLE_TYPES, state="readonly"), ""),
#             ("Registration Number", tk.Entry, ""),
#             ("Tax Status", lambda parent: ttk.Combobox(parent, values=TAX_STATUS, state="readonly"), ""),
#             ("Tax Due Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd'), ""),
#             ("Tax Type", lambda parent: ttk.Combobox(parent, values=TAX_TYPES, state="readonly"), ""),
#             ("Service Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd'), ""),
#             ("Fuel Type", lambda parent: ttk.Combobox(parent, values=FUEL_TYPES, state="readonly"), ""),
#             ("Manufacture Year", lambda parent: ttk.Combobox(parent, values=self.manufacture_years, state="readonly"), "")
#         ]

#         # If editing, populate initial values
#         if self.mode == "edit" and self.vehicle_data:
#             for i, field in enumerate(fields):
#                 fields[i] = (field[0], field[1], self.vehicle_data[i + 1])

#         for i, (label, widget_type, initial_value) in enumerate(fields):
#             tk.Label(self.popup, text=label).grid(row=i, column=0)
#             widget = widget_type(self.popup)
#             widget.grid(row=i, column=1)

#             # Set initial value
#             if isinstance(widget, ttk.Combobox):
#                 widget.set(initial_value)
#             elif isinstance(widget, DateEntry):
#                 try:
#                     if initial_value:
#                         widget.set_date(datetime.datetime.strptime(initial_value, "%Y-%m-%d").date())
#                     else:
#                         widget.set_date(datetime.date.today())
#                 except (ValueError, TypeError):
#                     widget.set_date(datetime.date.today())  # Fallback to today's date
#             else:
#                 widget.insert(0, initial_value)

#             self.inputs[label] = widget

#         tk.Button(
#             self.popup,
#             text="Save Changes" if self.mode == "edit" else "Add Vehicle",
#             command=self.save_changes
#         ).grid(row=len(fields), column=0, pady=10)

#         if self.mode == "edit":
#             tk.Button(self.popup, text="Delete Vehicle", command=self.delete_vehicle).grid(row=len(fields), column=1, pady=10)

#     def save_changes(self):
#         """Handles saving vehicle data."""
#         try:
#             updates = {}
#             for label, widget in self.inputs.items():
#                 value = widget.get()
#                 if label == "Manufacture Year" and not value.isdigit():
#                     raise ValueError(f"{label} must be a valid number.")
#                 updates[label] = value
#             updates = {SQL_MAPPINGS[key]: value for key, value in updates.items()}
#             print(updates)

#             if self.mode == "edit":
#                 self.manager.update_vehicle(self.vehicle_data[2], **updates)
#                 messagebox.showinfo("Success", "Vehicle updated successfully!")
#             else:
#                 new_vehicle = Vehicle(**updates)
#                 self.manager.add_vehicle(new_vehicle)
#                 messagebox.showinfo("Success", "Vehicle added successfully!")

#             self.popup.destroy()
#             self.list_all_vehicles()
#         except Exception as e:
#             print(f"Error: {e}")  # Log error
#             messagebox.showerror("Error", f"Failed to save vehicle: {e}")

#     def delete_vehicle(self):
#         """Handles deleting vehicle data."""
#         try:
#             self.manager.remove_vehicle(self.vehicle_data[2])
#             messagebox.showinfo("Success", "Vehicle deleted successfully!")
#             self.popup.destroy()
#             self.list_all_vehicles()
#         except Exception as e:
#             print(f"Error: {e}")  # Log error
#             messagebox.showerror("Error", f"Failed to delete vehicle: {e}")