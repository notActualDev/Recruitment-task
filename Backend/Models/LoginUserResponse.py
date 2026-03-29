from pydantic import BaseModel

class LoginUserResponse(BaseModel):
    Token: str