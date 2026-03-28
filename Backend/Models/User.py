from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):

    id: int
    email: str
    password_hash: str
    created_at: datetime