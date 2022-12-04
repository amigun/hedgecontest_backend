from fastapi import Depends, HTTPException, APIRouter, status
from fastapi_jwt_auth import AuthJWT

from src.db.repositories.users import UsersOperation
from src.models.schemas.users import User
from src.services.utils import get_password_hash, verify_password
from src.api.dependencies.users import Need

router = APIRouter()


@router.post('/registration', status_code=status.HTTP_201_CREATED)
def registration(user: User, authorize: AuthJWT = Depends(), users_operation: UsersOperation = Depends()):
    if users_operation.get_user(user.username) is None:
        return users_operation.create_user(user.username, user.password, 'user')
    else:
        return {'result': 'Пользователь с таким email уже существует!'}


@router.post('/login')
def login(user: User, authorize: AuthJWT = Depends(), users_operation: UsersOperation = Depends()):
    user_object = users_operation.get_user(user.username)
    if user_object:
        if user_object.email != user.username or user_object.hashed_password != user.password:  # add hash_password
            raise HTTPException(status_code=401, detail='Почта или пароль неверны!')

        access_token = authorize.create_access_token(subject=f'{user.username}:{user_object.role}')
        return {'access_token': access_token}


@router.get('/get_user/{email}')
def get_user(email: str, users_operation: UsersOperation = Depends(), need: Need = Depends(), authorize: AuthJWT = Depends()):
    authorize.jwt_optional()
    if need.need(['expert', 'admin'], authorize.get_raw_jwt()):
        user_object = users_operation.get_user(email)

        if user_object:
            return {
                'id': user_object.id,
                'email': user_object.email,
                'role': user_object.role
            }
        else:
            return {'result': 'Пользователь с таким email не найден!'}
    else:
        return HTTPException(status_code=401, detail='Нету прав доступа')


@router.get('/user')
def user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {'user': current_user}


@router.post('/reg_start')
def ref_start(users_operation: UsersOperation = Depends()):
    users_operation.register_users()
    return 'ok'