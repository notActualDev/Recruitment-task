import sqlite3
import os


class DatabaseService:

    def __init__(self):

        db_directory = os.getenv("DB_PATH", "/app/data")
        db_file = os.path.join(db_directory, "database.db")

        os.makedirs(db_directory, exist_ok=True)

        self.connection = sqlite3.connect(
            db_file,
            check_same_thread=False,
            timeout=30
        )

        self.connection.row_factory = sqlite3.Row

        self._ConfigureDatabase()

    def _ConfigureDatabase(self):

        cursor = self.connection.cursor()

        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")

        self.connection.commit()

    def GetConnection(self):
        return self.connection