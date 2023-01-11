FROM python:3.10.9-alpine3.16

# Copy dependency files and code
COPY poetry.lock /temp/poetry.lock
COPY pyproject.toml /temp/pyproject.toml

WORKDIR /temp

# Install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY service /web-app/service
WORKDIR /web-app/service

EXPOSE 8000

RUN adduser --disabled-password service-user

USER service-user