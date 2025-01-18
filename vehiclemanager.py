import sqlite3
from vehicle import Vehicle

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
                ServiceDate DATE,
                FuelType TEXT,
                ManufactureYear INTEGER
            )
        """)
        self.conn.commit()

    def add_vehicle(self, vehicle: Vehicle):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Vehicles (Type, RegistrationNumber, TaxStatus, TaxDueDate, TaxType, ServiceDate, FuelType, ManufactureYear)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (vehicle.vehicle_type, vehicle.reg_number, vehicle.tax_status, vehicle.tax_due_date, vehicle.tax_type, vehicle.service_date, vehicle.fuel_type, vehicle.manufacture_year))
        self.conn.commit()

    def remove_vehicle(self, reg_number):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Vehicles WHERE RegistrationNumber = ?", (reg_number,))
        self.conn.commit()

    def update_vehicle(self, reg_number, **kwargs):
        cursor = self.conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f"UPDATE Vehicles SET {key} = ? WHERE RegistrationNumber = ?", (value, reg_number))
        self.conn.commit()

    def search_vehicles(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
