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

    # =========================
    # DODANE METODY
    # =========================

    def GetAllHardware(self):

        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM Hardware")

        rows = cursor.fetchall()

        return rows


    def GetHardwareById(self, hardware_id):

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM Hardware WHERE id = ?",
            (hardware_id,)
        )

        return cursor.fetchone()


    def InsertHardware(self, hardware):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO Hardware
            (Name, Brand, PurchaseDate, Status, AssignedTo, Notes, History)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                hardware.Name,
                hardware.Brand,
                hardware.PurchaseDate,
                hardware.Status,
                hardware.AssignedTo,
                hardware.Notes,
                hardware.History
            )
        )

        self.connection.commit()

        return cursor.lastrowid


    def UpdateHardware(self, hardware_id, hardware):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE Hardware
            SET
                Name = ?,
                Brand = ?,
                PurchaseDate = ?,
                Status = ?,
                AssignedTo = ?,
                Notes = ?,
                History = ?
            WHERE id = ?
            """,
            (
                hardware.Name,
                hardware.Brand,
                hardware.PurchaseDate,
                hardware.Status,
                hardware.AssignedTo,
                hardware.Notes,
                hardware.History,
                hardware_id
            )
        )

        self.connection.commit()


    def DeleteHardware(self, hardware_id):

        cursor = self.connection.cursor()

        cursor.execute(
            "DELETE FROM Hardware WHERE id = ?",
            (hardware_id,)
        )

        self.connection.commit()


    def DeleteAllHardware(self):

        cursor = self.connection.cursor()

        cursor.execute("DELETE FROM Hardware")

        self.connection.commit()


    def CountHardware(self):

        cursor = self.connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM Hardware")

        result = cursor.fetchone()

        return result[0]