FROM python:3.11-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk update && apk upgrade
RUN apk add --no-cache \
    postgresql-client \
    bash \
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --prefer-binary -r /code/requirements.txt

COPY ./app /code/app
COPY ./DB_Queries.sql /code/
COPY ./init_db.sh /code/

ENV PGADDRESS=localhost
ENV PGUSER=Mehrdad
ENV PGPASSWORD=password
ENV PGPORT=5433
ENV PGNAME=profiles

ENV APPPORT=8084
ENV APPHOST=0.0.0.0
ENV AUTHSERVICEADDR=example.com

CMD uvicorn app.main:app --host $APPHOST --port $APPPORT
