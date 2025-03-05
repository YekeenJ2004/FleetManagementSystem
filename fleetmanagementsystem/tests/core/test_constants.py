import pytest
from fleetmanagementsystem.core.constants import (
    VEHICLE_TYPES, TAX_TYPES, FUEL_TYPES, TAX_STATUS, SERVICE_STATUS,
    COLUMN_NAMES, SQL_MAPPINGS, VEHICLE_POPUP_FIELDS,
    VEHICLE_CLASS_MAPPINGS, FILTER_RANGE_FIELDS, FILTER_OPTIONS,
    FIELD_OPTIONS
)


class TestConstants:
    """Test suite for validating the constants module."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup any necessary resources for the tests."""
        self.expected_vehicle_types = [
            "Sedan", "Hatchback", "SUV", "Coupe", "Convertible",
            "Minivan", "Pickup Truck", "Cargo Van", "Box Truck"
        ]
        self.expected_tax_types = ["Taxed", "Tax Exempt", "SORN", "Untaxed"]
        self.expected_fuel_types = [
            "Diesel", "Petrol", "Electricity", "Hybrid"
        ]
        self.expected_tax_status = ["Paid", "Unpaid"]
        self.expected_service_status = ["Done", "Pending"]
        self.expected_column_names = [
            "Select", "Type", "Registration Number", "Tax Status",
            "Tax Due Date", "Tax Type", "Service Due Date",
            "Service Status", "Fuel Type", "Manufacture Year"
        ]

    def test_vehicle_types(self):
        """Test if VEHICLE_TYPES contains expected vehicle types."""
        assert isinstance(VEHICLE_TYPES, list)
        for vehicle in self.expected_vehicle_types:
            assert vehicle in VEHICLE_TYPES
        assert len(VEHICLE_TYPES) > 10

    def test_tax_types(self):
        """Ensure tax types are correctly defined."""
        assert isinstance(TAX_TYPES, list)
        for tax in self.expected_tax_types:
            assert tax in TAX_TYPES
        assert len(TAX_TYPES) > 3

    def test_fuel_types(self):
        """Verify fuel types contain expected values."""
        assert isinstance(FUEL_TYPES, list)
        for fuel in self.expected_fuel_types:
            assert fuel in FUEL_TYPES
        assert len(FUEL_TYPES) > 3

    def test_tax_status(self):
        """Check that tax status contains only valid options."""
        assert TAX_STATUS == self.expected_tax_status

    def test_service_status(self):
        """Check service status options."""
        assert SERVICE_STATUS == self.expected_service_status

    def test_column_names(self):
        """Ensure column names are defined correctly."""
        assert COLUMN_NAMES == self.expected_column_names

    def test_sql_mappings(self):
        """Ensure SQL mappings correctly map fields to database column
        names."""
        assert isinstance(SQL_MAPPINGS, dict)
        assert SQL_MAPPINGS["Type"] == "Type"
        assert SQL_MAPPINGS["Tax Status"] == "TaxStatus"
        assert "Fuel Type" in SQL_MAPPINGS
        assert len(SQL_MAPPINGS) == 9

    def test_vehicle_popup_fields(self):
        """Check that vehicle popup fields define valid input fields."""
        assert isinstance(VEHICLE_POPUP_FIELDS, list)

        for label, widget_type, _ in VEHICLE_POPUP_FIELDS:
            assert isinstance(label, str)
            assert callable(widget_type)

    def test_vehicle_class_mappings(self):
        """Ensure vehicle class mappings correctly map fields to class
        attributes."""
        assert isinstance(VEHICLE_CLASS_MAPPINGS, dict)
        assert VEHICLE_CLASS_MAPPINGS["Type"] == "vehicle_type"
        assert VEHICLE_CLASS_MAPPINGS["RegistrationNumber"] == "reg_number"
        assert len(VEHICLE_CLASS_MAPPINGS) == 9

    def test_filter_range_fields(self):
        """Ensure filter range fields are correctly structured."""
        assert isinstance(FILTER_RANGE_FIELDS, list)
        for field in FILTER_RANGE_FIELDS:
            assert len(field) == 4
            assert isinstance(field[1], str)
            assert isinstance(field[2], int)
            assert isinstance(field[3], int)

    def test_filter_options(self):
        """Ensure filter options contain expected values."""
        assert isinstance(FILTER_OPTIONS, dict)
        assert "Type" in FILTER_OPTIONS
        assert "All" in FILTER_OPTIONS["Type"]
        assert "ASC" in FILTER_OPTIONS["Order Direction"]
        assert "DESC" in FILTER_OPTIONS["Order Direction"]

    def test_field_options(self):
        """Ensure field options are structured properly."""
        assert isinstance(FIELD_OPTIONS, dict)
        assert "Type" in FIELD_OPTIONS
        assert "Tax Type" in FIELD_OPTIONS
        assert "Fuel Type" in FIELD_OPTIONS
        assert "Diesel" in FIELD_OPTIONS["Fuel Type"]
