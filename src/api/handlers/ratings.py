from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from src.api.dependencies.users import Need
from src.db.repositories.ratings import RatingsOperation

router = APIRouter()


@router.get('/get_ratings')
def get_ratings(ratings_operation: RatingsOperation = Depends()):
    return ratings_operation.get_rating()


@router.get('/get_rating/{id}')
def get_rating(id: int, ratings_operation: RatingsOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['user', 'expert', 'admin'], authorize.get_raw_jwt()):
        return ratings_operation.get_user_scores_by_id(id)
    else:
        return HTTPException(status_code=401, detail='Нету прав доступа')
