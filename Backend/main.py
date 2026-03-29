import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Controllers import JsonRepairController
from Controllers.AdminController import router as AdminRouter
from Controllers.UsersController import router as UsersRouter
from Controllers.JsonRepairController import router as HardwareRouter


app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AdminRouter)
app.include_router(UsersRouter)
app.include_router(JsonRepairController.router)
app.include_router(HardwareRouter)


@app.get("/")
def root():
    return {"message": "Hello World"}


