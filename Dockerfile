FROM python:3.9


WORKDIR /code

 
COPY ./requirements.txt /code/requirements.txt

 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

 
COPY ./app /code/app


ENV PGUSER = Mehrdad
ENV PGPASSWORD = password
ENV PGPORT =  5433
ENV PGNAME = profiles

ENV APPPORT = 8084
ENV APPHOST = 0.0.0.0
 
CMD uvicorn app.main:app --host ${APPHOST} --port ${APPPORT}
