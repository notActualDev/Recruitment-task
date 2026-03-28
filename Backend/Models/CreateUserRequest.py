from pydantic import BaseModel


class CreateUserRequest(BaseModel):

    Email: str
    Password: str