from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    Id: int
    Email: str
    PasswordHash: str
    CreatedAt: datetime