from fastapi import APIRouter, Depends

from src.db.repositories.steps import StepsOperation
from src.models.schemas.steps import StepsDeadlines

router = APIRouter()


@router.get('/get_status')
def get_status(steps_operations: StepsOperation = Depends()):
    pairs = {
        'waiting': 'Ожидается запуск',
        'receiving': 'Прием заявок',
        'expertise': 'Независимая экспертиза',
        'finishing': 'Завершение конкурса'
    }

    return {'result': pairs[steps_operations.get_status()]}


@router.post('/set_deadlines')
def set_deadline(steps_deadlines: StepsDeadlines, steps_operations: StepsOperation = Depends()):
    print(steps_deadlines)
    steps_operations.set_deadlines(steps_deadlines.waiting, steps_deadlines.receiving, steps_deadlines.expertise, steps_deadlines.finishing)

    return {'results': 'Дедлайны установлены'}


@router.get('/get_deadlines')
def get_deadlines(steps_operations: StepsOperation = Depends()):
    return steps_operations.get_deadlines()

