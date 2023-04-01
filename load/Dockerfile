FROM python:3.11.1-slim-bullseye
LABEL maintainer="up-team"

ENV PYTHONUNBUFFERED 1

#RUN apt update

WORKDIR /load/app

#RUN apt install -y python3-dev build-essential default-libmysqlclient-dev && \
#RUN pip install --upgrade pip 

COPY app/requirements.txt /load/app/requirements.txt
RUN pip install -r /load/app/requirements.txt 

#COPY ./scripts /scripts
RUN adduser --disabled-password --no-create-home --gecos "" app 
USER app

#CMD ["bash"]