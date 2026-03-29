from pydantic import BaseModel

class LoginUserRequest(BaseModel):
    Email: str
    Password: str