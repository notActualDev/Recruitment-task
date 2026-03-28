from pydantic import BaseModel


class AdminLoginResponse(BaseModel):

    Token: str
    Expiration: str