FROM python:3.9

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update 
RUN apt-get install -y sudo 
RUN sudo pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

COPY . /usr/src/app/
