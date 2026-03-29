from pydantic import BaseModel, Field
from typing import Optional, Literal


class CreateHardwareRequest(BaseModel):

    Name: Optional[str] = None
    Brand: Optional[str] = None

    PurchaseDate: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )

    Status: Literal[
        "Available",
        "In Use",
        "Repair",
        "Unknown"
    ]

    AssignedTo: Optional[str] = None
    Notes: Optional[str] = None
    History: Optional[str] = None