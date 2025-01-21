import sqlite3
from typing import List, Tuple, Any
import logging

class DatabaseManager:
    def __init__(self, db_path: str) -> None:
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, params: Tuple[Any, ...] = (), raise_exceptions: bool = False) -> List[Tuple[Any, ...]]:
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
        self.connection.close()
