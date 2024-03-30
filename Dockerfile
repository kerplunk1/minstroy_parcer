FROM python:3.12.2-bullseye

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt install nano mc -qy

WORKDIR /api

COPY requirements.txt . 

RUN pip install -r requirements.txt

RUN alembic init alembic

COPY env.py ./alembic

EXPOSE 8000/tcp

EXPOSE 5432/tcp

