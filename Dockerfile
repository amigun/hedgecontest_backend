FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev

RUN sqlite database.sqlite3 "INSERT INTO users (email, hashed_password, role) VALUES (user, user, user)"
RUN sqlite database.sqlite3 "INSERT INTO users (email, hashed_password, role) VALUES (expert, expert, expert)"
RUN sqlite database.sqlite3 "INSERT INTO users (email, hashed_password, role) VALUES (admin, admin, admin)"

RUN mkdir hedgecontest/
COPY . hedgecontest/
WORKDIR hedgecontest/

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]