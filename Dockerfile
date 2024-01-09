FROM mcr.microsoft.com/playwright/python:latest

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt install ca-certificates

RUN pip install -U pip \
    && pip install poetry

WORKDIR /usr/src/app

COPY . .

RUN poetry install


RUN playwright install --with-deps chromium

ENTRYPOINT [ "poetry", "run", "python", "./ma2tg.py" ]
