from fastapi import APIRouter, Depends
from Services.DependencyProvider import GetLlmJsonRepairService
from Models.JsonRepairRequest import JsonRepairRequest
from Services.LlmJsonRepairService import LlmJsonRepairService
from Services.AdminTokenService import RequireAdminToken

router = APIRouter(prefix="/JsonRepair")


@router.post("/Repair")
def RepairJson(
    request: JsonRepairRequest,
    service: LlmJsonRepairService = Depends(GetLlmJsonRepairService),
    _: None = Depends(RequireAdminToken)
):
    result = service.repair_json(request.corruptedJson)

    return result