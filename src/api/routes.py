from fastapi import APIRouter

from src.api.handlers import users

router = APIRouter()
router.include_router(users.router, tags=['users'])
