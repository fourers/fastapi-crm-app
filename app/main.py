from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.client import router as client
from app.api.login import router as login

load_dotenv()

app = FastAPI()

app.include_router(client)
app.include_router(login)
