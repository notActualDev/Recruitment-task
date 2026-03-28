from pydantic import BaseModel

class AdminLoginRequest(BaseModel):

    Password: str