import sqlite3
from fleetmanagementsystem.core.vehicle import Vehicle
from typing import List, Tuple, Any
import logging


class VehicleManager:
    """
    A manager for handling operations related to vehicles in the database.

    Attributes:
        conn (sqlite3.Connection): SQLite database connection object.
    """
    def __init__(self, db_name: str = "fleet_management.db") -> None:
        """
        Initializes the VehicleManager and ensures the table structure is created.

        Args:
            db_name (str): Name of the database file. Defaults to 'fleet_management.db'.
        """
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self) -> None:
        """
        Creates the Vehicles table if it does not already exist.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Vehicles (
                VehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
                Type TEXT,
                RegistrationNumber TEXT UNIQUE,
                TaxStatus TEXT,
                TaxDueDate DATE,
                TaxType TEXT,
                ServiceDueDate DATE,
                ServiceStatus TEXT,
                FuelType TEXT,
                ManufactureYear INTEGER
            )
        """)
        self.conn.commit()

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """
        Adds a new vehicle to the database.

        Args:
            vehicle (Vehicle): A Vehicle object containing vehicle details.

        Raises:
            sqlite3.Error: If there is an error during the insertion process.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Vehicles (Type, RegistrationNumber, TaxStatus, TaxDueDate, TaxType, ServiceDueDate, ServiceStatus, FuelType, ManufactureYear)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (vehicle.vehicle_type, vehicle.reg_number, vehicle.tax_status, vehicle.tax_due_date, vehicle.tax_type, vehicle.service_due_date, vehicle.service_status, vehicle.fuel_type, vehicle.manufacture_year))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            raise

    def remove_vehicle(self, reg_number: str) -> None:
        """
        Removes a vehicle from the database by its registration number.

        Args:
            reg_number (str): The registration number of the vehicle to remove.

        Raises:
            sqlite3.Error: If there is an error during the deletion process.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Vehicles WHERE RegistrationNumber = ?", (reg_number,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def update_vehicle(self, reg_number: str, **kwargs: Any) -> None:
        """
        Updates details of a specific vehicle in the database.

        Args:
            reg_number (str): The registration number of the vehicle to update.
            **kwargs: Column-value pairs to update in the database.

        Raises:
            sqlite3.Error: If there is an error during the update process.
        """
        try:
            cursor = self.conn.cursor()
            for key, value in kwargs.items():
                cursor.execute(f"UPDATE Vehicles SET {key} = ? WHERE RegistrationNumber = ?", (value, reg_number))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def search_vehicles(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        """
        Searches for vehicles in the database using a custom SQL query.

        Args:
            query (str): The SQL query to execute.
            params (Tuple[Any, ...]): Parameters to use in the SQL query.

        Returns:
            List[Tuple[Any, ...]]: Results from the query.

        Raises:
            sqlite3.Error: If there is an error during the query execution.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return []
