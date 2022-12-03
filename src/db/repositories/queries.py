import sqlalchemy.exc
from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.queries import Query


class QueriesOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def create_query(self, full_name, post, job_place, topic_work, title_work, annotation, file):
        self.session.add(Query(
            full_name=full_name,
            post=post,
            job_place=job_place,
            topic_work=topic_work,
            title_work=title_work,
            annotation=annotation,
            file=file
        ))
        self.session.commit()

    def get_queries(self):
        try:
            return self.session.query(Query).all()
        except Exception as e:
            print(e)

    def get_query(self, id):
        try:
            return self.session.query(Query).filter(Query.id == id).one()
        except sqlalchemy.exc.NoResultFound:
            return {'result': 'Записи не найдено'}
