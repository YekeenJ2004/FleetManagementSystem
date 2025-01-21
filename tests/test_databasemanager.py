import pytest
import sqlite3
from databasemanager import DatabaseManager


class TestDatabaseManager:
    @pytest.fixture
    def db_manager(self, tmp_path):
        """Fixture to initialize the DatabaseManager with a temporary database."""
        db_path = tmp_path / "test.db"
        manager = DatabaseManager(str(db_path))
        yield manager
        manager.close()

    @pytest.fixture
    def setup_table(self, db_manager):
        """Fixture to set up a sample table for testing."""
        db_manager.execute_query(
            """
            CREATE TABLE IF NOT EXISTS Vehicles (
                VehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Type TEXT
            )
            """
        )

    def test_execute_query_insert_and_select(self, db_manager, setup_table):
        """Test inserting and selecting data."""
        # Insert data
        insert_query = "INSERT INTO Vehicles (Name, Type) VALUES (?, ?)"
        db_manager.execute_query(insert_query, ("CarA", "SUV"))
        db_manager.execute_query(insert_query, ("CarB", "Sedan"))

        # Select data
        select_query = "SELECT * FROM Vehicles"
        result = db_manager.execute_query(select_query)
        assert len(result) == 2
        assert result[0][1] == "CarA"
        assert result[0][2] == "SUV"
        assert result[1][1] == "CarB"
        assert result[1][2] == "Sedan"

    def test_execute_query_invalid_query(self, db_manager):
        """Test handling of an invalid query."""
        invalid_query = "SELECT * FROM NonExistentTable"
        result = db_manager.execute_query(invalid_query)
        assert result == []  # Should return an empty list

    def test_execute_query_with_params(self, db_manager, setup_table):
        """Test executing a query with parameters."""
        insert_query = "INSERT INTO Vehicles (Name, Type) VALUES (?, ?)"
        db_manager.execute_query(insert_query, ("CarC", "Truck"))

        select_query = "SELECT * FROM Vehicles WHERE Type = ?"
        result = db_manager.execute_query(select_query, ("Truck",))
        assert len(result) == 1
        assert result[0][1] == "CarC"
        assert result[0][2] == "Truck"

    def test_close_connection(self, db_manager):
        """Test closing the database connection."""
        db_manager.close()
        with pytest.raises(sqlite3.ProgrammingError):
            db_manager.execute_query("SELECT 1", raise_exceptions=True)
