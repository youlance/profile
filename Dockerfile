FROM python:3.9-alpine

WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt

RUN apk update && apk upgrade
RUN apk add libpq-dev python3-dev postgresql-client
RUN apk add --no-cache bash\
                       pkgconfig \
                       gcc \
                       openldap \
                       libcurl \
                       gpgme-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*



RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r /code/requirements.txt

 
COPY ./app /code/app

ENV PGADDRESS=localhost
ENV PGUSER=Mehrdad
ENV PGPASSWORD=password
ENV PGPORT=5433
ENV PGNAME=profiles

ENV APPPORT=8084
ENV APPHOST=0.0.0.0
ENV AUTHSERVICEADDR=example.com


CMD uvicorn app.main:app --host $APPHOST --port $APPPORT
