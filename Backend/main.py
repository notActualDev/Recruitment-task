from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
import bcrypt


app = FastAPI()

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

    stored_hash = os.getenv("ADMIN_PASSWORD_HASH")

    if not stored_hash:
        return {"error": "ADMIN_PASSWORD_HASH not set"}

    password_bytes = password.encode("utf-8")

    # debug: generujemy hash z przesłanego hasła
    generated_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # sprawdzenie
    is_valid = bcrypt.checkpw(password_bytes, stored_hash.encode())

    return {
        "received_password": password,
        "generated_hash": generated_hash.decode(),
        "stored_hash": stored_hash,
        "success": is_valid
    }