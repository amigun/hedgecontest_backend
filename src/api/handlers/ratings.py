from fastapi import APIRouter

router = APIRouter()


@router.get('/get_ratings')
def get_ratings():
    pass
