VEHICLE_TYPES = ["Sedan", "Hatchback", "SUV", "Coupe", "Convertible", "Minivan",
                "Pickup Truck", "Cargo Van", "Box Truck", "Bus", "Motorcycle", "Scooter",
                "Bicycle", "Semi-Truck", "Dump Truck", "Bulldozer", "Fire Truck", "Crane",
                "ATV", "Forklift", "Snowmobile", "Speedboat", "Yacht", "Ferry", "Helicopter"]
TAX_TYPES = ["Taxed", "Tax Exempt", "SORN", "Untaxed", "First-Year Rate", "Reduced Rate","Historic", "Disabled", "Agricultural Vehicle", "Exported"]
FUEL_TYPES = ["Diesel", "Petrol", "Electricity", "Hybrid", "Kerosene", "Jet Fuel", "Hydrogen", "Solar", "Other"]
TAX_STATUS = ["Paid", "Unpaid"]
COLUMN_NAMES = ["Select", "Type", "Registration Number", "Tax Status","Tax Due Date" ,"Tax Type", "Service Date", "Fuel Type", "Manufacture Year"]
SQL_MAPPINGS = {
    "Type": "Type",
    "Registration Number": "RegistrationNumber",
    "Tax Status": "TaxStatus",
    "Tax Type": "TaxType",
    "Fuel Type": "FuelType"
}
MAPPINGS  = { "Type": "vehicle_type","RegistrationNumber":  "reg_number", "TaxStatus" :"tax_status", "TaxType": "tax_type", "TaxDueDate":"tax_due_date", "ServiceDate":"service_date", "FuelType": "fuel_type", "ManufactureYear":"manufacture_year"}
ASCII_ART = r"""
         ______ __  __  _____
        |  ____|  \/  |/ ____|
        | |__  | \  / | (___
        |  __| | |\/| |\___ \
        | |    | |  | |____) |
        |_|    |_|  |_|_____/
        """