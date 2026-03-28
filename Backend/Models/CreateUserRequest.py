from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    Email: str
    PasswordHash: str