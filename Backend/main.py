import datetime
import secrets
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
import bcrypt
from services.admin_token_service import AdminTokenService


app = FastAPI()
token_service = AdminTokenService(lifetime_minutes=15)

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

    token, expiration = token_service.get_or_create_token()

    return {
        "token": token,
        "expiration": expiration.isoformat()
    }