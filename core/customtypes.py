from typing import Literal

VehiclePopupAction = Literal["add", "edit"]

TaxStatus = Literal["Paid", "Unpaid"]

TaxType = Literal[
    "Taxed", "Tax Exempt", "SORN", "Untaxed", "First-Year Rate",
    "Reduced Rate", "Historic", "Disabled", "Agricultural Vehicle",
    "Exported"
]

ServiceStatus = Literal["Done", "Pending"]

FromRange = Literal["Year From", "Tax Due Date From", "Service Date From"]
ToRange = Literal["Year To", "Tax Due Date To", "Service Date To"]
RangeField = Literal["ManufactureYear", "TaxDueDate", "ServiceDate"]
FuelType = Literal[
    "Diesel", "Petrol", "Electricity", "Hybrid", "Kerosene", "Jet Fuel",
    "Hydrogen", "Solar", "Other"
]

VehicleType = Literal[
    "Sedan", "Hatchback", "SUV", "Coupe", "Convertible", "Minivan",
    "Pickup Truck", "Cargo Van", "Box Truck", "Bus", "Motorcycle",
    "Scooter", "Bicycle", "Semi-Truck", "Dump Truck", "Bulldozer",
    "Fire Truck", "Crane", "ATV", "Forklift", "Snowmobile",
    "Speedboat", "Yacht", "Ferry", "Helicopter"
]
