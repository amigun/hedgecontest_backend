from pydantic import BaseModel


class StepsDeadlines(BaseModel):
    waiting: str
    receiving: str
    expertise: str
    finishing: str
