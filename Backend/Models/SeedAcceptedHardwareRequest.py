from pydantic import BaseModel
from typing import List
from Models.HardwareRecord import HardwareRecord


class SeedAcceptedHardwareRequest(BaseModel):

    Records: List[HardwareRecord]