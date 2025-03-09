from typing import Literal

# Define a type for the actions that can be performed in the VehiclePopup
VehiclePopupAction = Literal["add", "edit"]

# Define a type for the tax status of a vehicle
TaxStatus = Literal["Paid", "Unpaid"]

# Define a type for the different types of tax that can be applied to a vehicle
TaxType = Literal[
    "Taxed", "Tax Exempt", "SORN", "Untaxed", "First-Year Rate",
    "Reduced Rate", "Historic", "Disabled", "Agricultural Vehicle",
    "Exported"
]

# Define a type for the service status of a vehicle
ServiceStatus = Literal["Done", "Pending"]

# Define types for the range fields used in filtering
FromRange = Literal["Year From", "Tax Due Date From", "Service Date From"]
ToRange = Literal["Year To", "Tax Due Date To", "Service Date To"]
RangeField = Literal["ManufactureYear", "TaxDueDate", "ServiceDate"]

# Define a type for the different types of fuel that a vehicle can use
FuelType = Literal[
    "Diesel", "Petrol", "Electricity", "Hybrid", "Kerosene", "Jet Fuel",
    "Hydrogen", "Solar", "Other"
]

# Define a type for the different types of vehicles
VehicleType = Literal[
    "Sedan", "Hatchback", "SUV", "Coupe", "Convertible", "Minivan",
    "Pickup Truck", "Cargo Van", "Box Truck", "Bus", "Motorcycle",
    "Scooter", "Bicycle", "Semi-Truck", "Dump Truck", "Bulldozer",
    "Fire Truck", "Crane", "ATV", "Forklift", "Snowmobile",
    "Speedboat", "Yacht", "Ferry", "Helicopter"
]
