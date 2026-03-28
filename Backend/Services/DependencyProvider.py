from Database.DatabaseService import DatabaseService
from Database.UsersRepository import UsersRepository


# singleton Database
database_service = DatabaseService()

# singleton Repository
users_repository = UsersRepository(database_service)


def GetUsersRepository():
    return users_repository