from pydantic import BaseModel
from typing import List, Dict, Any


class Audit(BaseModel):
    duplicateIds: List[int]
    futureDates: List[str]
    invalidEmails: List[str]
    unknownStatuses: List[str]
    recordsNeedingReview: List[int]


class JsonRepairResponse(BaseModel):
    repairedJson: List[Dict[str, Any]]
    normalizedRecords: List[Dict[str, Any]]
    audit: Audit