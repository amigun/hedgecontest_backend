from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.queries import Query, Score
from src.db.models.users import User


class RatingsOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_user_scores_by_id(self, id):
        user = self.session.query(User).filter(User.id == id).one()
        query = self.session.query(Query).filter(Query.email == user.email).one()

        scores = self.session.query(Score).filter(Score.id_query == query.id).all()

        summation = 0

        for score in scores:
            summation += score.sum_score

        return summation

    def get_rating(self):
        users = self.session.query(User).all()

        rating = []

        for user in users:
            rating.append({'email': user.email, 'score': self.get_user_scores_by_id(user.id)})

        return sorted(rating, key=lambda item: item['score'], reverse=True)
