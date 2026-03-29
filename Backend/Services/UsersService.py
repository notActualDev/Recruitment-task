import bcrypt
import secrets
from datetime import datetime, timedelta
from Database.UsersRepository import UsersRepository


class UsersService:

    def __init__(self, usersRepository: UsersRepository):
        self.repo = usersRepository

        # token -> expiration
        self.activeTokens = {}

        self.tokenLifetime = timedelta(minutes=15)


    def Login(self, email: str, password: str):

        user = self.repo.GetUserByEmail(email)

        if not user:
            return None

        if not bcrypt.checkpw(
            password.encode(),
            user.PasswordHash.encode()
        ):
            return None

        token = secrets.token_hex(32)

        expiration = datetime.utcnow() + self.tokenLifetime

        self.activeTokens[token] = expiration

        return token


    def ValidateToken(self, token: str):

        expiration = self.activeTokens.get(token)

        if not expiration:
            return False

        if expiration < datetime.utcnow():
            del self.activeTokens[token]
            return False

        return True