from fastapi import APIRouter, Depends
from Services.DependencyProvider import GetLlmJsonRepairService, GetHardwareRepository
from Models.JsonRepairRequest import JsonRepairRequest
from Services.LlmJsonRepairService import LlmJsonRepairService
from Services.AdminTokenService import RequireAdminToken
from Models.SeedAcceptedHardwareRequest import SeedAcceptedHardwareRequest
from Database.HardwareRepository import HardwareRepository

router = APIRouter(prefix="/JsonRepair")


@router.post("/Repair")
def RepairJson(
        request: JsonRepairRequest,
        service: LlmJsonRepairService = Depends(GetLlmJsonRepairService),
        _: None = Depends(RequireAdminToken)
):
    result = service.repair_json(request.corruptedJson)

    return result


# @router.post("/SeedAcceptedRecords")
# def SeedAcceptedRecords(
#         request: SeedAcceptedHardwareRequest,
#         _: None = Depends(RequireAdminToken)
# ):
#     # DEBUG: zwracamy dokładnie ten sam JSON
#     return request



@router.post("/SeedAcceptedRecords")
def SeedAcceptedRecords(
        request: SeedAcceptedHardwareRequest,
        repo: HardwareRepository = Depends(GetHardwareRepository),
        _: None = Depends(RequireAdminToken)
):

    repo.ReplaceAllRecords(request.Records)

    return request
