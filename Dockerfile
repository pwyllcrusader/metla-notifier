FROM mcr.microsoft.com/playwright/python:latest

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install -U pip \
    && pip install poetry

WORKDIR /usr/src/app

COPY . .

RUN POETRY_VIRTUALENVS_CREATE=false poetry install

RUN playwright install chromium

ENTRYPOINT [ "poetry", "run", "python", "./ma2tg.py" ]
