from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI

from app.api.client import router as client
from app.api.login import router as login

load_dotenv()

app = FastAPI()

app.include_router(login)

api_router = APIRouter(prefix="/api", tags=["api"])
app.include_router(api_router)
api_router.include_router(client)
