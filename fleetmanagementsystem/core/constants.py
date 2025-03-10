import tkinter as tk
from tkinter import ttk
from fleetmanagementsystem.gui.utils.customdatepicker import CustomDatePicker

# List of vehicle types
VEHICLE_TYPES = [
    "Sedan", "Hatchback", "SUV", "Coupe", "Convertible", "Minivan",
    "Pickup Truck", "Cargo Van", "Box Truck", "Bus", "Motorcycle",
    "Scooter", "Bicycle", "Semi-Truck", "Dump Truck", "Bulldozer",
    "Fire Truck", "Crane", "ATV", "Forklift", "Snowmobile",
    "Speedboat", "Yacht", "Ferry", "Helicopter"
]

# List of tax types
TAX_TYPES = [
    "Taxed", "Tax Exempt", "SORN", "Untaxed", "First-Year Rate",
    "Reduced Rate", "Historic", "Disabled", "Agricultural Vehicle",
    "Exported"
]

# List of fuel types
FUEL_TYPES = [
    "Diesel", "Petrol", "Electricity", "Hybrid", "Kerosene", "Jet Fuel",
    "Hydrogen", "Solar", "Other"
]

# List of tax statuses
TAX_STATUS = ["Paid", "Unpaid"]

# List of service statuses
SERVICE_STATUS = ["Done", "Pending"]

# Column names for the vehicle table
COLUMN_NAMES = [
    "Select", "Type", "Registration Number", "Tax Status", "Tax Due Date",
    "Tax Type", "Service Due Date", "Service Status",
    "Fuel Type", "Manufacture Year"
]

# SQL mappings for vehicle attributes
SQL_MAPPINGS = {
    "Type": "Type",
    "Registration Number": "RegistrationNumber",
    "Tax Status": "TaxStatus",
    "Tax Type": "TaxType",
    "Fuel Type": "FuelType",
    "Manufacture Year": "ManufactureYear",
    "Tax Due Date": "TaxDueDate",
    "Service Due Date": "ServiceDueDate",
    "Service Status": "ServiceStatus"
}

# Fields for the vehicle popup
VEHICLE_POPUP_FIELDS = [
    ("Type",
        lambda parent: ttk.Combobox(
            parent, values=VEHICLE_TYPES, state="readonly"
        ),
     ""),
    ("Registration Number", tk.Entry, ""),
    ("Tax Status",
        lambda parent: ttk.Combobox(
            parent, values=TAX_STATUS, state="readonly"
        ),
     ""),
    ("Tax Due Date",
        lambda parent: CustomDatePicker(parent),
     ""),
    ("Tax Type",
     lambda parent: ttk.Combobox(parent, values=TAX_TYPES, state="readonly"),
     ""),
    (
        "Service Due Date",
        lambda parent: CustomDatePicker(parent),
        ""
    ),
    ("Service Status",
     lambda parent: ttk.Combobox(
         parent, values=SERVICE_STATUS, state="readonly"
     ),
     ""),
    ("Fuel Type",
     lambda parent: ttk.Combobox(parent, values=FUEL_TYPES, state="readonly"),
     ""),
]

# Mappings for vehicle class attributes
VEHICLE_CLASS_MAPPINGS = {
    "Type": "vehicle_type",
    "RegistrationNumber": "reg_number",
    "TaxStatus": "tax_status",
    "TaxType": "tax_type",
    "TaxDueDate": "tax_due_date",
    "ServiceDueDate": "service_due_date",
    "ServiceStatus": "service_status",
    "FuelType": "fuel_type",
    "ManufactureYear": "manufacture_year"
}

# Fields for filter ranges
FILTER_RANGE_FIELDS = [
    ("Year From", "Year From", 2, 4), ("To", "Year To", 2, 6),
    ("Tax Due Date From", "Tax Due Date From", 2, 0),
    ("To", "Tax Due Date To", 2, 2),
    ("Service Date From", "Service Date From", 3, 0),
    ("To", "Service Date To", 3, 2)
]

# Options for filters
FILTER_OPTIONS = {
    "Type": VEHICLE_TYPES + ["All"],
    "Tax Type": TAX_TYPES + ["All"],
    "Tax Status": TAX_STATUS + ["All"],
    "Fuel Type": FUEL_TYPES + ["All"],
    "Service Status": SERVICE_STATUS + ["All"],
    "Order By": [
        "Manufacture Year", "Tax Due Date",
        "Service Due Date", "Registration Number"
    ],
    "Order Direction": ["ASC", "DESC"]
}

# Options for fields
FIELD_OPTIONS = {
    "Type": VEHICLE_TYPES,
    "Tax Type": TAX_TYPES,
    "Tax Status": TAX_STATUS,
    "Fuel Type": FUEL_TYPES,
    "Service Status": SERVICE_STATUS
}

# ASCII art for the application
ASCII_ART = r"""
         ______ __  __  _____
        |  ____|  \/  |/ ____|
        | |__  | \  / | (___
        |  __| | |\/| |\___ \
        | |    | |  | |____) |
        |_|    |_|  |_|_____/
        """
