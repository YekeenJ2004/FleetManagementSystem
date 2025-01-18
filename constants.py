VEHICLE_TYPES = ["Sedan", "Hatchback", "SUV", "Coupe", "Convertible", "Minivan",
                "Pickup Truck", "Cargo Van", "Box Truck", "Bus", "Motorcycle", "Scooter",
                "Bicycle", "Semi-Truck", "Dump Truck", "Bulldozer", "Fire Truck", "Crane",
                "ATV", "Forklift", "Snowmobile", "Speedboat", "Yacht", "Ferry", "Helicopter"]
TAX_TYPES = ["Taxed", "Tax Exempt", "Untaxed"]
FUEL_TYPES = ["Diesel", "Petrol", "Electricity"]
TAX_STATUS = ["Paid", "Unpaid"]
COLUMN_NAMES = ["Select", "Type", "Registration Number", "Tax Status", "Tax Type", "Fuel Type", "Manufacture Year", "Tax Due Date", "Service Date"]
SQL_MAPPINGS = {
    "Type": "Type",
    "Registration Number": "RegistrationNumber",
    "Tax Status": "TaxStatus",
    "Tax Type": "TaxType",
    "Fuel Type": "FuelType"
}
ASCII_ART = r"""
         ______ __  __  _____
        |  ____|  \/  |/ ____|
        | |__  | \  / | (___
        |  __| | |\/| |\___ \
        | |    | |  | |____) |
        |_|    |_|  |_|_____/
        """