import sqlalchemy.exc
from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.queries import Query, Score
from src.db.models.users import User


class QueriesOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def create_query(self, full_name, email, post, job_place, topic_work, title_work, annotation, file):
        try:
            self.session.add(Query(
                full_name=full_name,
                email=email,
                post=post,
                job_place=job_place,
                topic_work=topic_work,
                title_work=title_work,
                annotation=annotation,
                file=file
            ))
        except sqlalchemy.exc.IntegrityError:
            return {'result': 'Заявка от этого пользователя уже была подана ранее'}
        self.session.commit()

    def get_queries(self):
        try:
            return self.session.query(Query).all()
        except Exception as e:
            print(e)

    def get_query_by_id(self, id):
        try:
            return self.session.query(Query).filter(Query.id == id).one()
        except sqlalchemy.exc.NoResultFound:
            return {'result': 'Записи не найдено'}

    def get_query_by_email(self, email):
        try:
            return self.session.query(Query).filter(Query.email == email).one()
        except sqlalchemy.exc.NoResultFound:
            return {'result': 'Записи не найдено'}

    def set_score_by_id(self, id, data):
        query = self.session.query(Query).filter(Query.id == data.id_query).one()
        user = self.session.query(User).filter(User.id == id).one()

        try:
            self.session.add(Score(
                id_query=query.id,
                id_expert=user.id,
                sum_score=data.sum_score
            ))
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return {'result': 'Работа уже была оценена ранее'}

        return {'result': 'Балл выставлен'}