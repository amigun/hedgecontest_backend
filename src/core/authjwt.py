from fastapi_jwt_auth import AuthJWT

from src.core.settings import Settings


@AuthJWT.load_config
def get_config():
    return Settings()
