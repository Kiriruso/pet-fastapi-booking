FROM python:3.11

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir /booking
WORKDIR /booking
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-dev

COPY . .

RUN chmod a+x /booking/docker/*.sh