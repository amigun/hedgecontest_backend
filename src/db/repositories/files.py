import sqlalchemy.exc
from fastapi import Depends

from src.core.db import Session
from src.db.common import get_database
from src.db.models.files import File


class FilesOperation:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_file(self, filename):
        try:
            return self.session.query(File).filter(File.file_path == f'files/{filename}').all()
        except sqlalchemy.exc.NoResultFound:
            return None

    def add_file(self, filename):
        self.session.add(File(file_path=f'files/{filename}'))
        self.session.commit()

        return self.session.query(File).filter(File.file_path == f'files/{filename}').one().id
