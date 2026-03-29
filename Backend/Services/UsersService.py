import bcrypt
import secrets
from datetime import datetime, timedelta
from Database.UsersRepository import UsersRepository


class UsersService:

    def __init__(self, usersRepository: UsersRepository):
        self.repo = usersRepository

        # token -> { email, expiration }
        self.activeTokens = {}

        self.tokenLifetime = timedelta(minutes=15)


    def Login(self, email: str, password: str):

        user = self.repo.GetUserByEmail(email)

        if not user:
            return None

        if not bcrypt.checkpw(
            password.encode(),
            user.password_hash.encode()
        ):
            return None

        token = secrets.token_hex(32)

        expiration = datetime.utcnow() + self.tokenLifetime

        # zapisujemy email razem z tokenem
        self.activeTokens[token] = {
            "email": email,
            "expiration": expiration
        }

        return token


    def ValidateToken(self, token: str):

        tokenData = self.activeTokens.get(token)

        if not tokenData:
            return False

        expiration = tokenData["expiration"]

        if expiration < datetime.utcnow():
            del self.activeTokens[token]
            return False

        return True


    def GetEmailByToken(self, token: str):

        tokenData = self.activeTokens.get(token)

        if not tokenData:
            return None

        expiration = tokenData["expiration"]

        if expiration < datetime.utcnow():
            del self.activeTokens[token]
            return None

        return tokenData["email"]