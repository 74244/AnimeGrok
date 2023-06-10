FROM python:3.11.3-slim-buster

ENV  \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.3.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN pip3 install "poetry-core==1.4.0" "poetry==$POETRY_VERSION" && poetry --version

WORKDIR /animegrok

COPY ./poetry.lock ./pyproject.toml /animegrok/
RUN poetry install --no-root

COPY . /animegrok
