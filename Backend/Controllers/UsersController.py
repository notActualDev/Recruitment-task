from fastapi import APIRouter, Depends, HTTPException
from Services.AdminTokenService import RequireAdminToken
from Services.DependencyProvider import GetUsersRepository
from Models.CreateUserRequest import CreateUserRequest
from Models.User import User
from Database.UsersRepository import UsersRepository
import bcrypt

router = APIRouter(prefix="/Users")


@router.get("/GetAllUsers")
def GetAllUsers(
    repo: UsersRepository = Depends(GetUsersRepository),
    _: None = Depends(RequireAdminToken)
):
    return repo.GetAllUsers()


@router.get("/GetUserById/{userId}")
def GetUserById(
    userId: int,
    repo: UsersRepository = Depends(GetUsersRepository),
    _: None = Depends(RequireAdminToken)
) -> User:

    user = repo.GetUserById(userId)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/CreateUser")
def CreateUser(
    request: CreateUserRequest,
    repo: UsersRepository = Depends(GetUsersRepository),
    _: None = Depends(RequireAdminToken)
):

    password_hash = bcrypt.hashpw(
        request.Password.encode(),
        bcrypt.gensalt()
    ).decode()

    userId = repo.CreateUser(
        request.Email,
        password_hash
    )

    return {"Id": userId}