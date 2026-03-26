from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # pozwól na wszystkie domeny
    allow_credentials=True,
    allow_methods=["*"],   # wszystkie metody (GET, POST itd.)
    allow_headers=["*"],   # wszystkie nagłówki
)

@app.get("/")
def root():
    return {"message": "Hello World"}