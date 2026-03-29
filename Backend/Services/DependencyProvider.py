from Database.DatabaseService import DatabaseService
from Database.UsersRepository import UsersRepository
from Database.HardwareRepository import HardwareRepository
from Services.LlmJsonRepairService import LlmJsonRepairService


database_service = DatabaseService()

users_repository = UsersRepository(database_service)

hardware_repository = HardwareRepository(database_service)

llm_json_repair_service = LlmJsonRepairService()


def GetUsersRepository():
    return users_repository


def GetLlmJsonRepairService():
    return llm_json_repair_service

def GetHardwareRepository():
    return hardware_repository

