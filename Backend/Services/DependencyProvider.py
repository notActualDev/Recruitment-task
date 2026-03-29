from Database.DatabaseService import DatabaseService
from Database.UsersRepository import UsersRepository
from Database.HardwareRepository import HardwareRepository
from Services.LlmJsonRepairService import LlmJsonRepairService
from Services.UsersService import UsersService



database_service = DatabaseService()

users_repository = UsersRepository(database_service)

users_service = UsersService(users_repository)

hardware_repository = HardwareRepository(database_service)

llm_json_repair_service = LlmJsonRepairService()


def GetUsersRepository():
    return users_repository

def GetUsersService():
    return users_service

def GetLlmJsonRepairService():
    return llm_json_repair_service

def GetHardwareRepository():
    return hardware_repository
