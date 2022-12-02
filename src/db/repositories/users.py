import sqlalchemy.exc
from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.users import User
from src.services.utils import get_password_hash


class UsersOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_user(self, email) :
        try:
            return self.session.query(User).filter(User.email==email).one()
        except sqlalchemy.exc.NoResultFound:
            return None

    def create_user(self, email, password):
        self.session.add(User(email=email, hashed_password=password))  # add hash_password
        self.session.commit()
