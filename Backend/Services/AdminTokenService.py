from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException, Header


class AdminTokenService:

    def __init__(self, lifetime_minutes: int = 15):
        self.tokens = {}
        self.token_lifetime = timedelta(minutes=lifetime_minutes)

    def GetOrCreateToken(self):

        now = datetime.utcnow()

        expired = [
            token for token, expiration in self.tokens.items()
            if expiration < now
        ]

        for token in expired:
            del self.tokens[token]

        for token, expiration in self.tokens.items():
            if expiration >= now:
                new_exp = now + self.token_lifetime
                self.tokens[token] = new_exp
                return token, new_exp

        token = secrets.token_hex(32)
        expiration = now + self.token_lifetime

        self.tokens[token] = expiration

        return token, expiration


token_service = AdminTokenService()


def RequireAdminToken(admin_token: str = Header()):

    expiration = token_service.tokens.get(admin_token)

    if not expiration:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    if expiration < datetime.utcnow():
        del token_service.tokens[admin_token]
        raise HTTPException(status_code=401, detail="Token expired")