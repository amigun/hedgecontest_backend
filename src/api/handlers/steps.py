from fastapi import APIRouter

router = APIRouter()


@router.get('/get_status')
def get_status():
    return {'result': 'Ожидается запуск'}


@router.post('/set_deadline/{step}')
def set_deadline(step: str):
    step_deadline = step

    return step_deadline
