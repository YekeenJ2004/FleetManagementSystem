import logging
from typing import Optional
from customtypes import TaxStatus, TaxType, ServiceStatus, FuelType, VehicleType


class Vehicle:
    """
    Represents a vehicle with various attributes such as type, registration number,
    tax status, fuel type, and manufacture year.

    Attributes:
        vehicle_type (str): The type of the vehicle (e.g., SUV, Sedan).
        reg_number (str): The registration number of the vehicle.
        tax_status (str): The tax status of the vehicle (e.g., Paid, Unpaid).
        tax_type (str): The type of tax applicable to the vehicle.
        tax_due_date (Optional[str]): The due date for tax payment (format: YYYY-MM-DD).
        service_status (str): The service status of the vehicle (e.g., Due, Completed).
        service_due_date (Optional[str]): The due date for vehicle service (format: YYYY-MM-DD).
        fuel_type (str): The type of fuel used by the vehicle (e.g., Petrol, Diesel).
        manufacture_year (int): The year the vehicle was manufactured.
    """
    def __init__(
        self,
        vehicle_type: VehicleType,
        reg_number: str,
        tax_status: TaxStatus,
        tax_type: TaxType,
        tax_due_date: Optional[str],
        service_status: ServiceStatus,
        service_due_date: Optional[str],
        fuel_type: FuelType,
        manufacture_year: int,
    ) -> None:
        """
        Initializes a Vehicle instance and validates input types.

        Args:
            vehicle_type (str): The type of the vehicle (e.g., SUV, Sedan).
            reg_number (str): The registration number of the vehicle.
            tax_status (str): The tax status of the vehicle (e.g., Paid, Unpaid).
            tax_type (str): The type of tax applicable to the vehicle.
            tax_due_date (Optional[str]): The due date for tax payment (format: YYYY-MM-DD).
            service_status (str): The service status of the vehicle (e.g., Piad, Pending).
            service_due_date (Optional[str]): The due date for vehicle service (format: YYYY-MM-DD).
            fuel_type (str): The type of fuel used by the vehicle (e.g., Petrol, Diesel).
            manufacture_year (int): The year the vehicle was manufactured.

        Raises:
            TypeError: If any input parameter is not of the expected type.
        """
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
