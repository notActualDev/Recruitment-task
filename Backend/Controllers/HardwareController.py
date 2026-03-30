from fastapi import APIRouter, Depends, HTTPException, Header

from Services.AdminTokenService import RequireAdminToken
from Services.DependencyProvider import GetHardwareRepository, GetHardwareService

from Models.CreateHardwareRequest import CreateHardwareRequest
from Models.UpdateHardwareRequest import UpdateHardwareRequest
from Models.Hardware import Hardware

from Database.HardwareRepository import HardwareRepository
from Services.HardwareService import HardwareService


router = APIRouter(prefix="/Hardware")


@router.get("/GetAllHardware")
def GetAllHardware(
    repo: HardwareRepository = Depends(GetHardwareRepository),
    _: None = Depends(RequireAdminToken)
):
    return repo.GetAllHardware()


@router.get("/GetHardwareById/{hardwareId}")
def GetHardwareById(
    hardwareId: int,
    repo: HardwareRepository = Depends(GetHardwareRepository),
    _: None = Depends(RequireAdminToken)
) -> Hardware:

    hardware = repo.GetHardwareById(hardwareId)

    if not hardware:
        raise HTTPException(status_code=404, detail="Hardware not found")

    return hardware


@router.post("/CreateHardware")
def CreateHardware(
    request: CreateHardwareRequest,
    repo: HardwareRepository = Depends(GetHardwareRepository),
    _: None = Depends(RequireAdminToken)
):

    hardwareId = repo.InsertHardware(request)

    return {"Id": hardwareId}


@router.put("/UpdateHardware/{hardwareId}")
def UpdateHardware(
    hardwareId: int,
    request: UpdateHardwareRequest,
    repo: HardwareRepository = Depends(GetHardwareRepository),
    _: None = Depends(RequireAdminToken)
):

    existing = repo.GetHardwareById(hardwareId)

    if not existing:
        raise HTTPException(status_code=404, detail="Hardware not found")

    repo.UpdateHardware(hardwareId, request)

    return {"Success": True}


@router.delete("/DeleteHardware/{hardwareId}")
def DeleteHardware(
    hardwareId: int,
    repo: HardwareRepository = Depends(GetHardwareRepository),
    _: None = Depends(RequireAdminToken)
):

    existing = repo.GetHardwareById(hardwareId)

    if not existing:
        raise HTTPException(status_code=404, detail="Hardware not found")

    repo.DeleteHardware(hardwareId)

    return {"Success": True}


# =========================
# USER ENDPOINT
# =========================

@router.get("/GetAllAvailableHardwareForUserToken")
def GetAllAvailableHardwareForUserToken(
    service: HardwareService = Depends(GetHardwareService),
    user_token: str = Header(None)
):

    result = service.GetAllAvailableHardwareForUserToken(user_token)

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid user token")

    return result


@router.get("/GetHardwareAssignedToUserToken")
def GetHardwareAssignedToUserToken(
    service: HardwareService = Depends(GetHardwareService),
    user_token: str = Header(None)
):

    result = service.GetHardwareAssignedToUserToken(user_token)

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid user token")

    return result