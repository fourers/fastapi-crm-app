from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.api.client import router as client
from app.api.login import router as login
from app.api.user import router as user

load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret",
    https_only=False,
    same_site="lax",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(login)

api_router = APIRouter(prefix="/api", tags=["api"])
app.include_router(api_router)
api_router.include_router(client)
api_router.include_router(user)
