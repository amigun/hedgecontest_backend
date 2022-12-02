from fastapi import APIRouter

from src.api.handlers import users, steps, queries

router = APIRouter()
router.include_router(users.router, tags=['users'])
router.include_router(steps.router, tags=['steps'])
router.include_router(queries.router, tags=['queries'])
