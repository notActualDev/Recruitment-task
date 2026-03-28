from fastapi import APIRouter, Depends
from Services.DependencyProvider import GetLlmJsonRepairService
from Models.JsonRepairRequest import JsonRepairRequest
from Models.JsonRepairResponse import JsonRepairResponse
from Services.LlmJsonRepairService import LlmJsonRepairService
from Services.AdminTokenService import RequireAdminToken

router = APIRouter(prefix="/JsonRepair")

# @router.post("/Repair")
# def RepairJson():
#     return {"ok": True}

@router.post("/Repair", response_model=JsonRepairResponse)
def RepairJson(
    request: JsonRepairRequest,
    service: LlmJsonRepairService = Depends(GetLlmJsonRepairService),
    _: None = Depends(RequireAdminToken)
):
    return {"ok": True}
    # result = service.repair_json(request.corruptedJson)
    #
    # return result