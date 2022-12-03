from fastapi import APIRouter, Depends

from src.db.repositories.steps import StepsOperation
from src.models.schemas.steps import StepsDeadlines

router = APIRouter()


@router.get('/get_status')
def get_status():
    return {'result': 'Ожидается запуск'}


@router.post('/set_deadlines')
def set_deadline(steps_deadlines: StepsDeadlines, steps_operations: StepsOperation = Depends()):
    print(steps_deadlines)
    steps_operations.set_deadlines(steps_deadlines.waiting, steps_deadlines.receiving, steps_deadlines.expertise, steps_deadlines.finishing)

    return {'results': 'Дедлайны установлены'}


@router.get('/get_deadlines')
def get_deadlines(steps_operations: StepsOperation = Depends()):
    return steps_operations.get_deadlines()

