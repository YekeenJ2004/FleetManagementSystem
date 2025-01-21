import sqlite3
from vehicle import Vehicle
import logging


class VehicleManager:
    def __init__(self, db_name="fleet_management.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
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

    def add_vehicle(self, vehicle: Vehicle):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Vehicles (Type, RegistrationNumber, TaxStatus, TaxDueDate, TaxType, ServiceDueDate, ServiceStatus, FuelType, ManufactureYear)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (vehicle.vehicle_type, vehicle.reg_number, vehicle.tax_status, vehicle.tax_due_date, vehicle.tax_type, vehicle.service_due_date, vehicle.service_status, vehicle.fuel_type, vehicle.manufacture_year))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def remove_vehicle(self, reg_number):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Vehicles WHERE RegistrationNumber = ?", (reg_number,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def update_vehicle(self, reg_number, **kwargs):
        try:
            cursor = self.conn.cursor()
            for key, value in kwargs.items():
                cursor.execute(f"UPDATE Vehicles SET {key} = ? WHERE RegistrationNumber = ?", (value, reg_number))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def search_vehicles(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return []
