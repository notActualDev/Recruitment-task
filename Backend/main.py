import secrets

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


@app.post("/admin/login")
def admin_login(password: str):

    stored_hash = os.getenv("ADMIN_PASSWORD_HASH", "").strip()

    if not stored_hash:
        raise HTTPException(status_code=500, detail="Admin hash not configured")

    password_bytes = password.encode()
    stored_hash_bytes = stored_hash.encode()

    if not bcrypt.checkpw(password_bytes, stored_hash_bytes):
        raise HTTPException(status_code=401, detail="Invalid password")

    # generujemy token
    token = secrets.token_hex(32)

    # zapis w RAM
    admin_tokens[token] = True

    return {
        "token": token
    }