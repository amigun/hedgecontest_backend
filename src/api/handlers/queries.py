from fastapi import APIRouter, UploadFile, File, Depends
from starlette import status

from src.db.repositories.queries import QueriesOperation
from src.models.schemas.queries import Query

router = APIRouter()


@router.post('/create_query', status_code=status.HTTP_201_CREATED)
def create_query(query: Query, queries_operation: QueriesOperation = Depends()):  # add email from jwt token
    queries_operation.create_query(
        query.full_name,
        query.post,
        query.job_place,
        query.topic_work,
        query.title_work,
        query.annotation,
        query.file
    )

    return {'result': 'Заявка успешно создана!'}


@router.get('/get_queries')
def get_queries(queries_operation: QueriesOperation = Depends()):
    return queries_operation.get_queries()


@router.get('/get_query/{id}')
def get_query(id: int, queries_operation: QueriesOperation = Depends()):
    return queries_operation.get_query(id)
