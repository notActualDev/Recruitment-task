import sqlite3
import os
from pathlib import Path

class DatabaseService:

    def __init__(self):
        self.DbPath = os.getenv("DB_PATH", "/app/data/database.db")
        self.EnsureDatabaseDirectory()

    def EnsureDatabaseDirectory(self):
        Path(self.DbPath).parent.mkdir(parents=True, exist_ok=True)

    def GetConnection(self):
        conn = sqlite3.connect(
            self.DbPath,
            timeout=10,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn