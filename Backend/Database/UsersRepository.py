from Models.User import User


class UsersRepository:

    def __init__(self, database_service):

        self.connection = database_service.GetConnection()

        self._EnsureTable()

    def _EnsureTable(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()

    def GetAllUsers(self):

        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM Users")

        rows = cursor.fetchall()

        return [User(**dict(row)) for row in rows]

    def GetUserById(self, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM Users WHERE id = ?",
            (user_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return User(**dict(row))

    def CreateUser(self, email, password_hash):

        cursor = self.connection.cursor()

        cursor.execute(
            "INSERT INTO Users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )

        self.connection.commit()

        return cursor.lastrowid