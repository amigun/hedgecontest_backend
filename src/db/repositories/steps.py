import datetime

import sqlalchemy.exc
from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.steps import Step


class StepsOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def set_deadlines(self, waiting, receiving, expertise, finishing):
        try:
            waiting_dl = self.session.query(Step).filter(Step.name == 'waiting').one()
            receiving_dl = self.session.query(Step).filter(Step.name == 'receiving').one()
            expertise_dl = self.session.query(Step).filter(Step.name == 'expertise').one()
            finishing_dl = self.session.query(Step).filter(Step.name == 'finishing').one()

            self.session.delete(waiting_dl)
            self.session.delete(receiving_dl)
            self.session.delete(expertise_dl)
            self.session.delete(finishing_dl)
            self.session.commit()
        except sqlalchemy.exc.NoResultFound:
            pass

        waiting = datetime.datetime.strptime(waiting, "%Y-%m-%d").date()
        receiving = datetime.datetime.strptime(receiving, "%Y-%m-%d").date()
        expertise = datetime.datetime.strptime(expertise, "%Y-%m-%d").date()
        finishing = datetime.datetime.strptime(finishing, "%Y-%m-%d").date()

        self.session.add(Step(
            name='waiting',
            deadline=waiting
        ))
        self.session.add(Step(
            name='receiving',
            deadline=receiving
        ))
        self.session.add(Step(
            name='expertise',
            deadline=expertise
        ))
        self.session.add(Step(
            name='finishing',
            deadline=finishing
        ))

        self.session.commit()

    def get_deadlines(self):
        waiting = self.session.query(Step).filter(Step.name == 'waiting').one()
        receiving = self.session.query(Step).filter(Step.name == 'receiving').one()
        expertise = self.session.query(Step).filter(Step.name == 'expertise').one()
        finishing = self.session.query(Step).filter(Step.name == 'finishing').one()

        return {'waiting': waiting.deadline, 'receiving': receiving.deadline, 'expertise': expertise.deadline, 'finishing': finishing.deadline}

    def get_status(self):
        deadlines = self.get_deadlines()

        # waiting_dt = datetime.datetime.strptime(deadlines['waiting'], '%Y-%m-%d')
        # receiving_dt = datetime.datetime.strptime(deadlines['receiving'], '%Y-%m-%d')
        # expertise_dt = datetime.datetime.strptime(deadlines['expertise'], '%Y-%m-%d')
        # finishing_dt = datetime.datetime.strptime(deadlines['finishing'], '%Y-%m-%d')

        waiting_dt = deadlines['waiting']
        receiving_dt = deadlines['receiving']
        expertise_dt = deadlines['expertise']
        finishing_dt = deadlines['finishing']

        now = datetime.date.today()

        if now <= waiting_dt:
            return 'waiting'
        elif now <= receiving_dt:
            return 'receiving'
        elif now <= expertise_dt:
            return 'expertise'
        else:
            return 'finishing'
