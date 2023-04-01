FROM python:3.11.1-slim-bullseye
LABEL maintainer="up-team"

ENV PYTHONUNBUFFERED 1

RUN apt update

WORKDIR /load

#RUN apt install -y python3-dev build-essential default-libmysqlclient-dev && \
RUN pip install --upgrade pip 

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt 

#COPY ./scripts /scripts
RUN adduser --disabled-password --no-create-home --gecos "" app 
USER app

CMD ["run.sh"]