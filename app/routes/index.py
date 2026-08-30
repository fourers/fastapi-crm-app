from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

RESTRICTED_PATHS = [
    "api",
    "auth",
    "health",
]

router = APIRouter(include_in_schema=False)


@router.get("/{path:path}", name="index")
def index(path: str):
    if any([path == p or path.startswith(f"{p}/") for p in RESTRICTED_PATHS]):
        raise HTTPException(404)
    return FileResponse("frontend/dist/index.html")
