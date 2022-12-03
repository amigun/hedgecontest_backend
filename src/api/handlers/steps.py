from fastapi import APIRouter, Depends

from src.db.repositories.steps import StepsOperation
from src.models.schemas.steps import StepsDeadlines

router = APIRouter()


@router.get('/get_status')
def get_status():
    return {'result': 'Ожидается запуск'}


@router.post('/set_deadline')
def set_deadline(steps_deadlines: StepsDeadlines, steps_operations: StepsOperation = Depends()):
    pass
