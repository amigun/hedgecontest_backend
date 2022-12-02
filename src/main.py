from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.routes import router
from src.core import authjwt
from src.db import common

app = FastAPI()


# TODO: переместить в src/api/handlers/users
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(router)
