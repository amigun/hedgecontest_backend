from fastapi import Depends, HTTPException, APIRouter, status
from fastapi_jwt_auth import AuthJWT

from src.db.repositories.users import UsersOperation
from src.models.schemas.users import User
from src.services.utils import get_password_hash, verify_password

router = APIRouter()


@router.post('/login')
def login(user: User, authorize: AuthJWT = Depends()):
    if user.username != 'test' or user.password != 'test':
        raise HTTPException(status_code=401, detail='Почта или пароль неверны!')

    access_token = authorize.create_access_token(subject=user.username)
    return {'access_token': access_token}


@router.post('/registration', status_code=status.HTTP_201_CREATED)
def registration(user: User, authorize: AuthJWT = Depends(), users_operation: UsersOperation = Depends()):
    if users_operation.get_user(user.username) is False:
        users_operation.create_user(user.username, user.password)
        return {'result': 'Пользователь успешно создан'}
    else:
        return {'result': 'Пользователь с таким email уже существует!'}


@router.get('/user')
def user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {'user': current_user}
