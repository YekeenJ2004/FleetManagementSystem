import pytest
import sqlite3
from fleetmanagementsystem.core.vehicle import Vehicle
from fleetmanagementsystem.core.vehiclemanager import VehicleManager


class TestVehicleManager:
    """Test suite for the VehicleManager class."""

    def setup_method(self) -> None:
        """Setup method to initialize the VehicleManager and database."""
        self.vehicle_manager = VehicleManager(db_name=":memory:")
        self.sample_vehicle = Vehicle(
            vehicle_type="SUV",
            reg_number="ABC123",
            tax_status="Paid",
            tax_due_date="2025-01-01",
            tax_type="Standard",
            service_due_date="2025-06-01",
            service_status="Pending",
            fuel_type="Petrol",
            manufacture_year=2020
        )

    def teardown_method(self) -> None:
        """Tear down method to close the database connection."""
        self.vehicle_manager.conn.close()

    def test_add_vehicle(self) -> None:
        """Test adding a vehicle to the database."""
        self.vehicle_manager.add_vehicle(self.sample_vehicle)
        result = self.vehicle_manager.search_vehicles("SELECT * FROM Vehicles")
        assert len(result) == 1
        assert result[0][1] == "SUV"

    def test_remove_vehicle(self) -> None:
        """Test removing a vehicle from the database."""
        self.vehicle_manager.add_vehicle(self.sample_vehicle)
        self.vehicle_manager.remove_vehicle(self.sample_vehicle.reg_number)
        result = self.vehicle_manager.search_vehicles("SELECT * FROM Vehicles")
        assert len(result) == 0

    def test_update_vehicle(self) -> None:
        """Test updating vehicle details in the database."""
        self.vehicle_manager.add_vehicle(self.sample_vehicle)
        self.vehicle_manager.update_vehicle(
            self.sample_vehicle.reg_number,
            TaxStatus="Unpaid",
            FuelType="Diesel"
        )
        result = self.vehicle_manager.search_vehicles(
            "SELECT TaxStatus, FuelType FROM Vehicles WHERE "
            "RegistrationNumber = ?",
            (self.sample_vehicle.reg_number,)
        )
        assert result[0] == ("Unpaid", "Diesel")

    def test_search_vehicles(self) -> None:
        """Test searching for vehicles using a query."""
        self.vehicle_manager.add_vehicle(self.sample_vehicle)
        result = self.vehicle_manager.search_vehicles(
            "SELECT * FROM Vehicles WHERE Type = ?", ("SUV",)
        )
        assert len(result) == 1
        assert result[0][1] == "SUV"

    def test_add_duplicate_vehicle(self) -> None:
        """Test adding a vehicle with a duplicate registration number."""
        self.vehicle_manager.add_vehicle(self.sample_vehicle)
        duplicate_vehicle = Vehicle(
            vehicle_type="Sedan",
            reg_number="ABC123",
            tax_status="Paid",
            tax_due_date="2026-01-01",
            tax_type="Standard",
            service_due_date="2026-06-01",
            service_status="Pending",
            fuel_type="Electric",
            manufacture_year=2021
        )
        with pytest.raises(sqlite3.IntegrityError):
            self.vehicle_manager.add_vehicle(duplicate_vehicle)
