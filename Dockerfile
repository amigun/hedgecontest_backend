FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir hedgecontest/
COPY . hedgecontest/
WORKDIR hedgecontest/

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]