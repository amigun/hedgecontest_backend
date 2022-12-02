from fastapi import Depends, HTTPException, APIRouter
from fastapi_jwt_auth import AuthJWT

from src.models.schemas.users import User

router = APIRouter()


@router.post('/login')
def login(user: User, authorize: AuthJWT = Depends()):
    if user.username != 'test' or user.password != 'test':
        raise HTTPException(status_code=401, detail='Почта или пароль неверны!')

    access_token = authorize.create_access_token(subject=user.username)
    return {'access_token': access_token}


@router.get('/user')
def user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {'user': current_user}
