from fastapi import APIRouter

from app.api.client import router as client
from app.api.group.parent import router as group_parent
from app.api.group.user import router as group_user
from app.api.groups import router as group
from app.api.user import router as user

router = APIRouter(tags=["api"])

router.include_router(client)
router.include_router(group)
router.include_router(group_parent)
router.include_router(group_user)
router.include_router(user)
