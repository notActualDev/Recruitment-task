from fastapi import APIRouter, Depends, HTTPException
from Services.AdminTokenService import RequireAdminToken
from Services.DependencyProvider import GetUsersRepository
from Models.CreateUserRequest import CreateUserRequest
from Models import User
from Database.UsersRepository import UsersRepository
import bcrypt
from Models.Users import LoginUserRequest
from Models.Users import LoginUserResponse

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
        raise HTTPException(status_code=404, detail="Users not found")

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

###

from Services.DependencyProvider import GetUsersService
from Services.UsersService import UsersService


@router.post("/Login", response_model=LoginUserResponse)
def Login(
    request: LoginUserRequest,
    usersService: UsersService = Depends(GetUsersService)
):

    token = usersService.Login(
        request.Email,
        request.Password
    )

    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return LoginUserResponse(Token=token)