import sqlite3
from typing import List, Tuple, Any
import logging


class DatabaseManager:
    """
    A class for managing database connections and executing queries.

    This class provides methods for interacting with a SQLite database,
    including executing queries and closing the database connection.
    """
    def __init__(self, db_path: str) -> None:
        """
        Initialize the DatabaseManager with the path to the database file.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_query(
        self,
        query: str,
        params: Tuple[Any, ...] = (),
        raise_exceptions: bool = False
    ) -> List[Tuple[Any, ...]]:
        """
        Execute a query on the database.

        Args:
            query (str): The SQL query to execute.
            params (Tuple[Any, ...]): A tuple of parameters to bind to the
            query.
            Defaults to an empty tuple.
            raise_exceptions (bool): Whether to raise exceptions if a
            database error occurs. Defaults to False.

        Returns:
            List[Tuple[Any, ...]]: The result of the query as a list of tuples.
            Returns an empty list on error.
        """
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            if raise_exceptions:
                raise
            return []

    def close(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()
