from pydantic import BaseModel


class Query(BaseModel):
    full_name: str
    post: str
    job_place: str
    topic_work: str
    title_work: str
    annotation: str
    file: str
