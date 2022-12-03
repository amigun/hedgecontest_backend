from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from starlette import status

from src.db.repositories.queries import QueriesOperation
from src.db.repositories.users import UsersOperation
from src.models.schemas.queries import Query, Score

router = APIRouter()


@router.post('/create_query', status_code=status.HTTP_201_CREATED)
def create_query(query: Query, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends()):  # add email from jwt token
    authorize.jwt_optional()

    try:
        email = authorize.get_jwt_subject().split(':')[0]
    except AttributeError:
        return HTTPException(status_code=401, detail="Пользователь не авторизован")

    return queries_operation.create_query(
        query.full_name,
        email,
        query.post,
        query.job_place,
        query.topic_work,
        query.title_work,
        query.annotation,
        query.file
    )


@router.get('/get_queries')
def get_queries(queries_operation: QueriesOperation = Depends()):
    return queries_operation.get_queries()


@router.get('/get_query_by_id/{id}')
def get_query_by_id(id: int, queries_operation: QueriesOperation = Depends()):
    return queries_operation.get_query_by_id(id)


@router.get('/get_query_by_email/{email}')
def get_query_by_email(email: str, queries_operation: QueriesOperation = Depends()):
    return queries_operation.get_query_by_email(email)


@router.post('/set_score_by_id/')
def set_score_by_id(data: Score, authorize: AuthJWT = Depends(), queries_operation: QueriesOperation = Depends(), user_operations: UsersOperation = Depends()):
    authorize.jwt_required()
    id_expert = user_operations.get_user(authorize.get_jwt_subject().split(':')[0]).id

    return queries_operation.set_score_by_id(id_expert, data)


@router.post('/accept_query/{id}')
def accept_query(id: int, queries_operation: QueriesOperation = Depends()):
    query = queries_operation.get_query_by_id(id)
    return queries_operation.accept_query(query)


@router.delete('/delete_query/{id}')
def delete_query(id: int, queries_operation: QueriesOperation = Depends()):
    query = queries_operation.get_query_by_id(id)
    return queries_operation.delete_query(query)
