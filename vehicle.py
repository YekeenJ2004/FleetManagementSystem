from datetime import datetime

class Vehicle:
    def __init__(self, vehicle_type, reg_number, tax_status, tax_type, tax_due_date, service_date, fuel_type, manufacture_year):
        self.vehicle_type = vehicle_type
        self.reg_number = reg_number
        self.tax_status = tax_status
        self.tax_type = tax_type
        self.tax_due_date = tax_due_date
        self.service_date = service_date
        self.fuel_type = fuel_type
        self.manufacture_year = manufacture_year
