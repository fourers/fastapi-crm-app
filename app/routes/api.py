from fastapi import APIRouter

from app.api.client import router as client
from app.api.group import router as group
from app.api.user import router as user

router = APIRouter(tags=["api"])

router.include_router(client)
router.include_router(group)
router.include_router(user)
