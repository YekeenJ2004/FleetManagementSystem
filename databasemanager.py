import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        self.connection.close()
