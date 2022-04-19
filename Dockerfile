FROM mcr.microsoft.com/playwright/python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip \
    && pip install poetry

WORKDIR /usr/src/app
COPY . .
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN playwright install chromium

ENTRYPOINT [ "poetry", "run", "python", "./ma2tg.py" ]
