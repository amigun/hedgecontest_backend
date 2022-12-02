from fastapi import Depends

from src.db.repositories.users import create_user


def registration(email, password, user=Depends(create_user)):
    pass
