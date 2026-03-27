from datetime import datetime, timedelta
import secrets


class AdminTokenService:

    def __init__(self, lifetime_minutes: int = 15):
        self.tokens = {}
        self.token_lifetime = timedelta(minutes=lifetime_minutes)

    def get_or_create_token(self):

        now = datetime.utcnow()

        # usuwanie wygasłych
        expired_tokens = [
            token for token, expiration in self.tokens.items()
            if expiration < now
        ]

        for token in expired_tokens:
            del self.tokens[token]

        # sprawdzenie czy jest aktywny
        for token, expiration in self.tokens.items():
            if expiration >= now:

                new_expiration = now + self.token_lifetime
                self.tokens[token] = new_expiration

                return token, new_expiration

        # tworzenie nowego
        token = secrets.token_hex(32)
        expiration = now + self.token_lifetime

        self.tokens[token] = expiration

        return token, expiration