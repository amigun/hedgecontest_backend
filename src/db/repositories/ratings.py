from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.users import User


class RatingsOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_user_scores_by_id(self, id):
        user = self.session.query(User).filter(User.id == id).one()

