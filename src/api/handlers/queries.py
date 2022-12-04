from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from starlette import status
from starlette.requests import Request

from src.api.dependencies.common import Timing
from src.api.dependencies.users import Need
from src.db.repositories.queries import QueriesOperation
from src.db.repositories.steps import StepsOperation
from src.db.repositories.users import UsersOperation
from src.models.schemas.queries import Query, Score

router = APIRouter()


@router.post('/create_query', status_code=status.HTTP_201_CREATED)
def create_query(query: Query, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends(), steps_operation: StepsOperation = Depends()):  # add email from jwt token
    authorize.jwt_optional()
    if steps_operation.get_status() == 'receiving':

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
    else:
        return {'result': 'Время подачи заявки вышло'}


@router.get('/get_queries')
def get_queries(queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['admin'], authorize.get_raw_jwt()):

        return queries_operation.get_queries()


@router.get('/get_query_by_id/{id}')
def get_query_by_id(id: int, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['admin'], authorize.get_raw_jwt()):

        print(queries_operation.get_query_by_id(id))
        return queries_operation.get_query_by_id(id)


@router.get('/get_query_by_email/{email}')
def get_query_by_email(email: str, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['admin'], authorize.get_raw_jwt()):

        return queries_operation.get_query_by_email(email)


@router.post('/set_score_by_id/')
def set_score_by_id(data: Score, authorize: AuthJWT = Depends(), queries_operation: QueriesOperation = Depends(), user_operations: UsersOperation = Depends(), need: Need = Depends(), steps_operation: StepsOperation = Depends()):
    authorize.jwt_optional()
    if steps_operation.get_status() == 'expertise':
        if need.need(['expert'], authorize.get_raw_jwt()):

            id_expert = user_operations.get_user(authorize.get_jwt_subject().split(':')[0]).id

            return queries_operation.set_score_by_id(id_expert, data)
    else:
        return {'result': 'Время выставления оценок вышло'}


@router.post('/accept_query/{id}')
def accept_query(id: int, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(),
                 need: Need = Depends()):
    query = queries_operation.get_query_by_id(id)
    return queries_operation.accept_query(query)


@router.delete('/delete_query/{id}')
def delete_query(id: int, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(),
                     need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['admin'], authorize.get_raw_jwt()):
        query = queries_operation.get_query_by_id(id)

        return queries_operation.delete_query(query)
    else:
        return HTTPException(status_code=401, detail='Нету прав доступа')


@router.get('/get_accepted_queries')
def get_accepted_queries(queries_operations: QueriesOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['expert'], authorize.get_raw_jwt()):
        return queries_operations.get_accepted_queries()
    else:
        return {'result': 'Недостаточно прав'}


@router.get('/get_accepted_query_by_id/{id}')
def get_accepted_query_by_id(id: int, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(), need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['expert'], authorize.get_raw_jwt()):
        return queries_operation.get_accepted_query_by_id(id)
    else:
        return {'result': 'Недостаточно прав'}


@router.get('/get_accepted_query_by_email/{email}')
def get_accepted_query_by_id(email: str, queries_operation: QueriesOperation = Depends(), authorize: AuthJWT = Depends(),
                             need: Need = Depends()):
    authorize.jwt_optional()
    if need.need(['expert'], authorize.get_raw_jwt()):
        return queries_operation.get_accepted_query_by_id(email)
    else:
        return {'result': 'Недостаточно прав'}
