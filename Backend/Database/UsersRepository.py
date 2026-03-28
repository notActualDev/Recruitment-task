from Models.User import User

class UsersRepository:
    def __init__(self, databaseService):
        self.DatabaseService = databaseService
        self.EnsureTable()

    def EnsureTable(self):
        with self.DatabaseService.GetConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def CreateUser(self, email: str, passwordHash: str) -> int:
        with self.DatabaseService.GetConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO Users (email, password_hash)
            VALUES (?, ?)
            """, (email, passwordHash))
            conn.commit()
            return cursor.lastrowid

    def GetUserById(self, userId: int) -> User | None:
        with self.DatabaseService.GetConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, email, password_hash, created_at
            FROM Users
            WHERE id = ?
            """, (userId,))
            row = cursor.fetchone()
            if not row:
                return None
            return User(Id=row["id"], Email=row["email"], PasswordHash=row["password_hash"], CreatedAt=row["created_at"])

    def GetUserByEmail(self, email: str) -> User | None:
        with self.DatabaseService.GetConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, email, password_hash, created_at
            FROM Users
            WHERE email = ?
            """, (email,))
            row = cursor.fetchone()
            if not row:
                return None
            return User(Id=row["id"], Email=row["email"], PasswordHash=row["password_hash"], CreatedAt=row["created_at"])

    def GetAllUsers(self) -> list[User]:
        with self.DatabaseService.GetConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, email, password_hash, created_at
            FROM Users
            ORDER BY id
            """)
            rows = cursor.fetchall()
            return [User(Id=row["id"], Email=row["email"], PasswordHash=row["password_hash"], CreatedAt=row["created_at"]) for row in rows]