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