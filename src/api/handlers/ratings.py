from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from src.api.dependencies.common import Timing
from src.api.dependencies.users import Need
from src.db.repositories.ratings import RatingsOperation
from src.db.repositories.steps import StepsOperation

router = APIRouter()


@router.get('/get_ratings')
def get_ratings(ratings_operation: RatingsOperation = Depends(), steps_operation: StepsOperation = Depends()):
    if steps_operation.get_status() == 'finishing':
        return ratings_operation.get_rating()
    else:
        return {'result': 'Рейтинг недоступен'}


@router.get('/get_rating/{id}')
def get_rating(id: int, ratings_operation: RatingsOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['user', 'expert', 'admin'], authorize.get_raw_jwt()):
        return ratings_operation.get_user_scores_by_id(id)
    else:
        return HTTPException(status_code=401, detail='Нету прав доступа')
