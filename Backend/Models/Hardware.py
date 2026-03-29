from pydantic import BaseModel
from typing import Optional
from typing import Literal


class Hardware(BaseModel):

    Id: int

    Name: Optional[str] = None
    Brand: Optional[str] = None
    PurchaseDate: Optional[str] = None

    Status: Literal[
        "Available",
        "In Use",
        "Repair",
        "Unknown"
    ]

    AssignedTo: Optional[str] = None
    Notes: Optional[str] = None
    History: Optional[str] = None