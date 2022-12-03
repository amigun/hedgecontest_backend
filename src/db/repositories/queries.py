import sqlalchemy.exc
from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.queries import Query, Score, AcceptedQuery
from src.db.models.users import User


class QueriesOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def create_query(self, full_name, email, post, job_place, topic_work, title_work, annotation, file):
        if self.get_query_by_email(email) == {'result': 'Записи не найдено'}:
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
                self.session.commit()

                return {'result': 'Заявка успешно создана!'}
            except sqlalchemy.exc.IntegrityError:
                return {'result': 'Заявка от этого пользователя уже была подана ранее'}
        else:
            return {'result': 'Заявка от этого пользователя уже была подана ранее'}

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

    def get_accepted_query_by_id(self, id):
        try:
            return self.session.query(AcceptedQuery).filter(AcceptedQuery.id == id).one()
        except sqlalchemy.exc.NoResultFound:
            return {'result': 'Записи не найдено'}

    def get_accepted_query_by_email(self, email):
        try:
            return self.session.query(AcceptedQuery).filter(AcceptedQuery.email == email).one()
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

    def delete_query(self, query):
        old_query = self.get_query_by_email(query.email)
        self.session.delete(old_query)
        self.session.commit()

        return {'result': 'Заявка удалена!'}

    def accept_query(self, query):
        if self.get_accepted_query_by_email(query.email):
            try:
                self.session.add(AcceptedQuery(

                    full_name=query.full_name,
                    email=query.email,
                    post=query.post,
                    job_place=query.job_place,
                    topic_work=query.topic_work,
                    title_work=query.title_work,
                    annotation=query.annotation,
                    file=query.file
                ))

                self.delete_query(query)

                self.session.commit()

                return {'result': 'Заявка одобрена!'}
            except sqlalchemy.exc.IntegrityError:
                return {'result': 'Заявка от этого пользователя уже была одобрена ранее'}
        else:
            return {'result': 'Заявка от этого пользователя уже была одобрена ранее'}
