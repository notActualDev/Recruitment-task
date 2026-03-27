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

class AdminLoginRequest(BaseModel):
    password: str


class AdminLoginResponse(BaseModel):
    success: bool


@app.post("/admin/login", response_model=AdminLoginResponse)
def admin_login(request: AdminLoginRequest):

    # hash zapisany w Railway Environment Variables
    stored_hash = os.getenv("ADMIN_PASSWORD_HASH")

    if stored_hash is None:
        return {"success": False}

    # bcrypt działa na bytes
    password_bytes = request.password.encode("utf-8")
    stored_hash_bytes = stored_hash.encode("utf-8")

    # porównanie bcrypt
    is_valid = bcrypt.checkpw(password_bytes, stored_hash_bytes)

    return {"success": is_valid}