from fastapi import APIRouter, Depends

from src.db.repositories.ratings import RatingsOperation

router = APIRouter()


@router.get('/get_ratings')
def get_ratings(ratings_operation: RatingsOperation = Depends()):
    return ratings_operation.get_rating()
