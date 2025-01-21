import logging


class Vehicle:
    def __init__(self, vehicle_type, reg_number, tax_status, tax_type, tax_due_date, service_status, service_due_date, fuel_type, manufacture_year):
        attributes = {
            "vehicle_type": (vehicle_type, str),
            "reg_number": (reg_number, str),
            "tax_status": (tax_status, str),
            "tax_type": (tax_type, str),
            "tax_due_date": (tax_due_date, (str, type(None))),
            "service_status": (service_status, str),
            "service_due_date": (service_due_date, (str, type(None))),
            "fuel_type": (fuel_type, str),
            "manufacture_year": (manufacture_year, int)
        }

        for attr_name, (value, expected_type) in attributes.items():
            try:
                if not isinstance(value, expected_type):
                    raise TypeError(f"{attr_name} must be of type {expected_type.__name__}")
            except TypeError as e:
                # Handle the error: log, re-raise, or provide custom behavior
                logging.error(f"Error initializing Vehicle: {e}")
                raise

        # Assign attributes
        self.vehicle_type = vehicle_type
        self.reg_number = reg_number
        self.tax_status = tax_status
        self.tax_type = tax_type
        self.tax_due_date = tax_due_date
        self.service_due_date = service_due_date
        self.service_status = service_status
        self.fuel_type = fuel_type
        self.manufacture_year = manufacture_year
