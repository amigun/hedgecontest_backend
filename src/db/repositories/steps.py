from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database


class StepsOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def set_deadlines(self, waiting, receiving, expertise, finishing):
        pass
