from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.auth.access import access_log
from app.routes.api import router as api_router
from app.routes.auth import router as auth_router
from app.routes.index import router as index_router
from app.utils.logging import configure_logging
from app.utils.validation import request_validation_exception_handler

configure_logging()
load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret",
    https_only=False,
    same_site="lax",
)


@app.middleware("http")
async def access_logging(request: Request, call_next):
    return await access_log(request, call_next)


@app.exception_handler(RequestValidationError)
def handle_request_validation_error(request: Request, exc: RequestValidationError):
    return request_validation_exception_handler(exc)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")
app.include_router(index_router)
