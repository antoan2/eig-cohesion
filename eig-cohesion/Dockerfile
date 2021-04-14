FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./

CMD gunicorn --bind=0.0.0.0:$PORT app:server"
