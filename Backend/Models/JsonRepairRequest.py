from pydantic import BaseModel


class JsonRepairRequest(BaseModel):
    corruptedJson: str