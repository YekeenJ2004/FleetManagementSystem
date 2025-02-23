import pytest
from core.vehicle import Vehicle


class TestVehicle:
    def test_vehicle_initialization(self):
        """Test the Vehicle class initialization with valid data."""
        vehicle = Vehicle(
            vehicle_type="SUV",
            reg_number="ABC123",
            tax_status="Paid",
            tax_type="Full",
            tax_due_date="2025-01-01",
            service_status="On Schedule",
            service_due_date="2025-06-01",
            fuel_type="Diesel",
            manufacture_year=2020,
        )

        assert vehicle.vehicle_type == "SUV"
        assert vehicle.reg_number == "ABC123"
        assert vehicle.tax_status == "Paid"
        assert vehicle.tax_type == "Full"
        assert vehicle.tax_due_date == "2025-01-01"
        assert vehicle.service_status == "On Schedule"
        assert vehicle.service_due_date == "2025-06-01"
        assert vehicle.fuel_type == "Diesel"
        assert vehicle.manufacture_year == 2020

    def test_vehicle_invalid_data(self):
        """Test initialization with invalid data types."""
        with pytest.raises(TypeError):
            Vehicle(
                vehicle_type=None,
                reg_number=12345,  # Should be a string
                tax_status="Paid",
                tax_type="Full",
                tax_due_date="2025-01-01",
                service_status="On Schedule",
                service_due_date="2025-06-01",
                fuel_type="Diesel",
                manufacture_year="2020",  # Should be an integer
            )

    def test_vehicle_missing_fields(self):
        """Test initialization with missing required fields."""
        with pytest.raises(TypeError):
            Vehicle(
                vehicle_type="SUV",
                reg_number="ABC123",
                tax_status="Paid"
                # Missing other required fields
            )

    def test_vehicle_edge_cases(self):
        """Test the Vehicle class with edge cases."""
        vehicle = Vehicle(
            vehicle_type="",
            reg_number="",
            tax_status="",
            tax_type="",
            tax_due_date="",
            service_status="",
            service_due_date="",
            fuel_type="",
            manufacture_year=0,
        )

        assert vehicle.vehicle_type == ""
        assert vehicle.reg_number == ""
        assert vehicle.tax_status == ""
        assert vehicle.tax_type == ""
        assert vehicle.tax_due_date == ""
        assert vehicle.service_status == ""
        assert vehicle.service_due_date == ""
        assert vehicle.fuel_type == ""
        assert vehicle.manufacture_year == 0
