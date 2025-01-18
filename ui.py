import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from vehiclemanager import VehicleManager
from filtermanager import FilterManager
from vehicle import Vehicle
from tkinter import messagebox
from constants import SQL_MAPPINGS, COLUMN_NAMES, FUEL_TYPES, TAX_TYPES, VEHICLE_TYPES, ASCII_ART, TAX_STATUS, MAPPINGS
import datetime

current_year = datetime.datetime.now().year
manufacture_years = [str(year) for year in range(current_year, current_year - 20, -1)]

class FleetApp:
    def __init__(self, root):
        self.manager = VehicleManager()
        self.root = root
        self.root.title("Fleet Management System")

        self.create_widgets()

    def create_widgets(self):
        current_year = datetime.datetime.now().year
        year_options = [str(year) for year in range(current_year - 50, current_year + 1)]
        # Parent frame for ASCII art and buttons
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, pady=10)

        # Left frame for the ASCII art
        self.ascii_frame = tk.Frame(self.top_frame)
        self.ascii_frame.pack(side=tk.LEFT, padx=10)

        # Filter Frame
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(fill=tk.X, padx=10, pady=5)

        # ASCII art for "FMS"
        ascii_art = ASCII_ART

        # Display ASCII art in a Label
        ascii_label = tk.Label(
            self.ascii_frame, text=ascii_art, font=("Courier", 12),
            justify=tk.LEFT
        )
        ascii_label.pack()

        # Right frame for the buttons
        self.button_frame = tk.Frame(self.top_frame)
        self.button_frame.pack(side=tk.RIGHT, padx=10)

        # Add buttons to the right frame
        tk.Button(
            self.button_frame, text="Add Vehicle",
            command=self.open_add_vehicle_popup
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            self.button_frame, text="List All Vehicles",
            command=self.list_all_vehicles
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            self.button_frame, text="Delete Selected", command=self.bulk_delete
        ).grid(row=0, column=2, padx=5)

        # Add Search Bar below ASCII art and align to the right
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill=tk.X, padx=10, pady=5)

        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(fill=tk.X, padx=10, pady=5)

        filter_options = {
            "Type": VEHICLE_TYPES + ["All"],
            "Tax Type": TAX_TYPES + ["All"],
            "Tax Status": TAX_STATUS + ["All"],
            "Fuel Type": FUEL_TYPES + ["All"],
        }
        self.filters = {}

        for i, (field, options) in enumerate(filter_options.items()):
            tk.Label(self.filter_frame, text=field).grid(row=0, column=i * 2)
            combo = ttk.Combobox(self.filter_frame, values=options, state="readonly")
            combo.set("All")  # Default to "All"
            combo.grid(row=0, column=i * 2 + 1)
            self.filters[field] = combo

        # Add Search Button
        search_button = tk.Button(self.search_frame, text="Search", command=self.apply_filters)
        search_button.pack(side=tk.RIGHT)

        # Add Search Bar
        search_bar = tk.Entry(self.search_frame, width=30)
        search_bar.pack(side=tk.RIGHT, padx=(0, 10))
        self.filters["Search"] = search_bar

        tk.Label(self.filter_frame, text="Year From").grid(row=2, column=4)
        year_from = ttk.Combobox(self.filter_frame, values=year_options, state="readonly")
        year_from.set("")
        year_from.grid(row=2, column=5)
        self.filters["Year From"] = year_from

        tk.Label(self.filter_frame, text="To").grid(row=2, column=6)
        year_to = ttk.Combobox(self.filter_frame, values=year_options, state="readonly")
        year_from.set("")
        year_to.grid(row=2, column=7)
        self.filters["Year To"] = year_to

        # Add Tax Due Date range filters
        tk.Label(self.filter_frame, text="Tax Due Date From").grid(row=2, column=0)
        tax_due_date_from = DateEntry(self.filter_frame, date_pattern='yyyy-mm-dd')
        tax_due_date_from.grid(row=2, column=1)
        tax_due_date_from.delete(0, tk.END)  # Set initial value to empty
        self.filters["Tax Due Date From"] = tax_due_date_from

        tk.Label(self.filter_frame, text="To").grid(row=2, column=2)
        tax_due_date_to = DateEntry(self.filter_frame, date_pattern='yyyy-mm-dd')
        tax_due_date_to.grid(row=2, column=3)
        tax_due_date_to.delete(0, tk.END)  # Set initial value to empty
        self.filters["Tax Due Date To"] = tax_due_date_to

        # Add Service Date range filters
        tk.Label(self.filter_frame, text="Service Date From").grid(row=3, column=0)
        service_date_from = DateEntry(self.filter_frame, date_pattern='yyyy-mm-dd')
        service_date_from.grid(row=3, column=1)
        service_date_from.delete(0, tk.END)  # Set initial value to empty
        self.filters["Service Date From"] = service_date_from

        tk.Label(self.filter_frame, text="To").grid(row=3, column=2)
        service_date_to = DateEntry(self.filter_frame, date_pattern='yyyy-mm-dd')
        service_date_to.grid(row=3, column=3)
        service_date_to.delete(0, tk.END)  # Set initial value to empty
        self.filters["Service Date To"] = service_date_to

        # Add filter button
        tk.Button(self.filter_frame, text="Apply Filters", command=self.apply_filters).grid(row=0, column=len(filter_options) * 2, padx=10)
        tk.Button(self.filter_frame, text="Clear Filters", command=self.clear_filters).grid(row=0, column=len(filter_options) * 2 + 1, padx=10)

        # Treeview for listing vehicles
        self.tree = ttk.Treeview(
            self.root,
            columns=COLUMN_NAMES,
            show="headings"
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define headings
        self.tree.heading("Select", text="Select")
        for col in self.tree["columns"][1:]:
            self.tree.heading(col, text=col)

        # Bind events
        self.tree.bind("<Double-1>", self.edit_vehicle_popup)
        self.tree.bind("<Button-1>", self.toggle_checkbox)

    def open_add_vehicle_popup(self):
        """Opens a popup window for adding a new vehicle."""
        self.vehicle_popup("add")
        # popup = tk.Toplevel(self.root)
        # popup.title("Add Vehicle")

        # # Field labels and widget types
        # fields = [
        #     ("Type", lambda parent: ttk.Combobox(parent, values=VEHICLE_TYPES)),
        #     ("Registration Number", tk.Entry),
        #     ("Tax Status", lambda parent: ttk.Combobox(parent, values=["Paid", "Unpaid"])),
        #     ("Tax Type", lambda parent: ttk.Combobox(parent, values=TAX_TYPES)),
        #     ("Tax Due Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd')),
        #     ("Service Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd')),
        #     ("Fuel Type", lambda parent: ttk.Combobox(parent, values=FUEL_TYPES)),
        #     ("Manufacture Year", tk.Entry)
        # ]

        # # Dictionary to store input widgets
        # inputs = {}

        # # Create labels and input widgets dynamically
        # for i, (label, widget_type) in enumerate(fields):
        #     tk.Label(popup, text=label).grid(row=i, column=0)
        #     widget = widget_type(popup)
        #     widget.grid(row=i, column=1)
        #     inputs[label] = widget

        #     # Set default values for dropdowns (if applicable)
        #     if label == "Type":
        #         widget.set("Sedan")
        #     elif label == "Fuel Type":
        #         widget.set("Diesel")

        def add_vehicle():
            try:
                # Create a Vehicle object using field values
                print(inputs)
                vehicle = Vehicle(
                    vehicle_type=inputs["Type"].get(),
                    reg_number=inputs["Registration Number"].get(),
                    tax_due_date=inputs["Tax Due Date"].get(),
                    tax_type=inputs["Tax Type"].get(),
                    tax_status=inputs["Tax Status"].get(),
                    service_date=inputs["Service Date"].get(),
                    fuel_type=inputs["Fuel Type"].get(),
                    manufacture_year=int(inputs["Manufacture Year"].get())
                )

                # Add the vehicle to the database
                self.manager.add_vehicle(vehicle)
                messagebox.showinfo("Success", "Vehicle added successfully!")

                # Update the vehicle list
                self.list_all_vehicles()

                # Close the popup
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add vehicle: {e}")

        # Add and Cancel buttons
        tk.Button(popup, text="Add Vehicle", command=add_vehicle).grid(row=len(fields), column=0, pady=10)
        tk.Button(popup, text="Cancel", command=popup.destroy).grid(row=len(fields), column=1, pady=10)

    def apply_filters(self):
        """Apply the selected filters and update the vehicle list."""
        try:
            filter_manager = FilterManager(self.filters)
            query, values = filter_manager.apply_filters()
            records = self.manager.search_vehicles(query, values)
            self.update_treeview(records)
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def clear_filters(self):
        """Clear all filters and reset the vehicle list."""
        filter_manager = FilterManager(self.filters)
        filter_manager.clear_filters()
        self.list_all_vehicles()

    def list_all_vehicles(self):
        """Fetch and display all vehicles."""
        records = self.manager.search_vehicles("SELECT * FROM Vehicles")
        self.update_treeview(records)

    def update_treeview(self, records):
        """Update the treeview with given records."""
        self.tree.delete(*self.tree.get_children())
        for record in records:
            if not self.tree.exists(record[2]):  # Ensure unique iid
                self.tree.insert("", "end", iid=record[2], values=("☐", *record[1:]))

    def toggle_checkbox(self, event):
        """
        Toggles the checkbox state (checked/unchecked) for the clicked row in the Treeview.

        Args:
            event: The event object containing information about the click event.
        """
        """Toggles the checkbox state (checked/unchecked) for the clicked row in the Treeview."""
        # Identify the row and column clicked
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            col = self.tree.identify_column(event.x)
            if col == "#1":  # Checkbox column
                current_value = self.tree.item(item, "values")[0]
                new_value = "☑" if current_value == "☐" else "☐"
                self.tree.item(item, values=(new_value, *self.tree.item(item, "values")[1:]))

    def bulk_delete(self):
        selected = []
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == "☑":
                selected.append(self.tree.item(item, "values")[2])  # Registration Number

        if not selected:
            messagebox.showwarning("No Selection", "No vehicles selected for deletion.")
            return

        for reg in selected:
            self.manager.remove_vehicle(reg)
        messagebox.showinfo("Success", "Selected vehicles deleted successfully!")
        self.list_all_vehicles()

    def edit_vehicle_popup(self, event):
        """Opens a popup window for editing an existing vehicle."""
        item = self.tree.identify_row(event.y)
        if not item:
            return

        reg_number = self.tree.item(item, "values")[2]  # Get Registration Number
        vehicle = self.manager.search_vehicles("SELECT * FROM Vehicles WHERE RegistrationNumber = ?", (reg_number,))
        print(vehicle)
        if not vehicle:
            messagebox.showerror("Error", "Vehicle not found.")
            return

        vehicle = vehicle[0]  # Extract the record
        self.vehicle_popup("edit", vehicle)
        
    def vehicle_popup(self, mode, vehicle_data=None):
        """Generalized popup window for adding or editing a vehicle."""
        popup = tk.Toplevel(self.root)
        popup.title("Edit Vehicle" if mode == "edit" else "Add Vehicle")

        current_year = datetime.datetime.now().year
        manufacture_years = [str(year) for year in range(current_year, current_year - 20, -1)]

        # Fields configuration
        fields = [
            ("Type", lambda parent: ttk.Combobox(parent, values=VEHICLE_TYPES, state="readonly"), ""),
            ("Registration Number", tk.Entry, ""),
            ("Tax Status", lambda parent: ttk.Combobox(parent, values=TAX_STATUS, state="readonly"), ""),
            ("Tax Due Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd'), ""),
            ("Tax Type", lambda parent: ttk.Combobox(parent, values=TAX_TYPES, state="readonly"), ""),
            ("Service Date", lambda parent: DateEntry(parent, date_pattern='yyyy-mm-dd'), ""),
            ("Fuel Type", lambda parent: ttk.Combobox(parent, values=FUEL_TYPES, state="readonly"), ""),
            ("Manufacture Year", lambda parent: ttk.Combobox(parent, values=manufacture_years, state="readonly"), "")
        ]

        # If editing, populate initial values
        if mode == "edit" and vehicle_data:
            for i, field in enumerate(fields):
                fields[i] = (field[0], field[1], vehicle_data[i + 1])

        inputs = {}

        # Create labels and input widgets dynamically
        for i, (label, widget_type, initial_value) in enumerate(fields):
            tk.Label(popup, text=label).grid(row=i, column=0)
            widget = widget_type(popup)
            widget.grid(row=i, column=1)

            # Set initial value
            if isinstance(widget, ttk.Combobox):
                widget.set(initial_value)
            elif isinstance(widget, DateEntry):
                try:
                    if initial_value:
                        widget.set_date(initial_value)
                    else:
                        widget.set_date(datetime.date.today())
                except ValueError:
                    widget.set_date(datetime.date.today())  # Fallback to today's date for invalid values
            else:
                widget.insert(0, initial_value)

            inputs[label] = widget

        def save_changes():
            try:
                updates = {
                    "Type": inputs["Type"].get(),
                    "RegistrationNumber": inputs["Registration Number"].get(),
                    "TaxStatus": inputs["Tax Status"].get(),
                    "TaxType": inputs["Tax Type"].get(),
                    "TaxDueDate": inputs["Tax Due Date"].get(),
                    "ServiceDate": inputs["Service Date"].get(),
                    "FuelType": inputs["Fuel Type"].get(),
                    "ManufactureYear": int(inputs["Manufacture Year"].get())
                }

                if mode == "edit":
                    self.manager.update_vehicle(vehicle_data[2], **updates)
                    messagebox.showinfo("Success", "Vehicle updated successfully!")
                else:
                    updated_keys = {MAPPINGS[key]: value for key, value in updates.items()}
                    new_vehicle = Vehicle(**updated_keys)
                    self.manager.add_vehicle(new_vehicle)
                    messagebox.showinfo("Success", "Vehicle added successfully!")

                popup.destroy()
                self.list_all_vehicles()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save vehicle: {e}")

        def delete_vehicle():
            if mode == "edit":
                try:
                    self.manager.remove_vehicle(vehicle_data[2])
                    messagebox.showinfo("Success", "Vehicle deleted successfully!")
                    popup.destroy()
                    self.list_all_vehicles()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete vehicle: {e}")

        # Add Save and Delete buttons
        tk.Button(popup, text="Save Changes" if mode == "edit" else "Add Vehicle", command=save_changes).grid(row=len(fields), column=0, pady=10)

        if mode == "edit":
            tk.Button(popup, text="Delete Vehicle", command=delete_vehicle).grid(row=len(fields), column=1, pady=10)    
    


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = FleetApp(root)
    root.mainloop()