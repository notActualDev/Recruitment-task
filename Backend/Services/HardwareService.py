from Database.HardwareRepository import HardwareRepository
from Services.UsersService import UsersService


class HardwareService:

    def __init__(
        self,
        hardwareRepository: HardwareRepository,
        usersService: UsersService
    ):
        self.repo = hardwareRepository
        self.usersService = usersService


    def GetAllAvailableHardwareForUserToken(self, token: str):

        if not token:
            return None

        # walidacja tokena usera
        if not self.usersService.ValidateToken(token):
            return None

        # pobranie sprzętu
        hardware = self.repo.GetAvailableHardware()

        return hardware

    def GetHardwareAssignedToUserToken(self, token: str):

        if not token:
            return None

        # token → email
        email = self.usersService.GetEmailFromToken(token)

        if not email:
            return None

        # pobranie sprzętu przypisanego do usera
        hardware = self.repo.GetHardwareAssignedToEmail(email)

        return hardware