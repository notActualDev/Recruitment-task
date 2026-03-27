import datetime
import secrets
from datetime import timedelta

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
import bcrypt


app = FastAPI()

# tokeny w RAM
admin_tokens = {}

frontend_url = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

TOKEN_LIFETIME = timedelta(minutes=15)


@app.post("/admin/login")
def admin_login(password: str):

    stored_hash = os.getenv("ADMIN_PASSWORD_HASH", "").strip()

    if not stored_hash:
        raise HTTPException(status_code=500, detail="Admin hash not configured")

    if not bcrypt.checkpw(password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid password")

    now = datetime.utcnow()

    # 1️⃣ usuwanie wygasłych tokenów
    expired_tokens = [
        token for token, expiration in admin_tokens.items()
        if expiration < now
    ]

    for token in expired_tokens:
        del admin_tokens[token]

    # 2️⃣ jeśli jest ważny token → użyj go
    for token, expiration in admin_tokens.items():
        if expiration >= now:

            # przedłużamy jego ważność
            new_expiration = now + TOKEN_LIFETIME
            admin_tokens[token] = new_expiration

            return {
                "token": token,
                "expiration": new_expiration.isoformat()
            }

    # 3️⃣ jeśli nie ma żadnego → tworzymy nowy
    token = secrets.token_hex(32)
    expiration = now + TOKEN_LIFETIME

    admin_tokens[token] = expiration

    return {
        "token": token,
        "expiration": expiration.isoformat()
    }