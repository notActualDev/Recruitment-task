class HardwareRepository:

    def __init__(self, database_service):

        self.connection = database_service.GetConnection()

        self._EnsureTable()

    def _EnsureTable(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Hardware (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Brand TEXT,
            PurchaseDate TEXT,
            Status TEXT NOT NULL,
            AssignedTo TEXT,
            Notes TEXT,
            History TEXT
        )
        """)

        self.connection.commit()

    def ReplaceAllRecords(self, records):

        cursor = self.connection.cursor()

        # usuwamy stare rekordy
        cursor.execute("DELETE FROM Hardware")

        for r in records:

            cursor.execute(
                """
                INSERT INTO Hardware
                (Name, Brand, PurchaseDate, Status, AssignedTo, Notes, History)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r.Name,
                    r.Brand,
                    r.PurchaseDate,
                    r.Status,
                    r.AssignedTo,
                    r.Notes,
                    r.History
                )
            )

        self.connection.commit()