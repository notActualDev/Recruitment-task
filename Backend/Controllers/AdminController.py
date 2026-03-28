from fastapi import APIRouter, HTTPException
from Services.AdminTokenService import token_service
from Models.AdminLoginRequest import AdminLoginRequest
from Models.AdminLoginResponse import AdminLoginResponse
import os
import bcrypt

router = APIRouter(prefix="/Admin")


@router.post("/Login", response_model=AdminLoginResponse)
def AdminLogin(request: AdminLoginRequest):

    stored_hash = os.getenv("ADMIN_PASSWORD_HASH", "").strip()

    if not stored_hash:
        raise HTTPException(status_code=500, detail="Admin hash not configured")

    if not bcrypt.checkpw(request.Password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid password")

    token, expiration = token_service.GetOrCreateToken()

    return AdminLoginResponse(
        Token=token,
        Expiration=expiration.isoformat()
    )