# PET-Project Booking

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi)
![FastAPI](https://img.shields.io/badge/FastAPI-04988b?style=flat&logo=fastapi&color=white)
![Docker](https://img.shields.io/badge/Docker-E5F2FC?style=flat&logo=docker&color=%23E5F2FC)

## Описание

Небольшой Backend проект написанный на FastAPI с применением архитектуры REST.

Основное окружение проекта:
- FastAPI
- Uvicorn + Gunicorn
- PostgreSQL
- SQLAlchemy + Alembic
- Redis
- Celery + Flower
- SQLAdmin
- Sentry

Для разрабокти:
- Pytest
- Ruff
- Pyright

## Установка

### Poetry

Для установки потребуется [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer).

Сначала клонируйте проект и перейдите в корневую директорию:

```bash
git clone https://github.com/Kiriruso/pet-fastapi-booking.git
cd pet-fastapi-booking
```

А затем запустите следующий скрипт для установки проекта:

```bash
poetry install --without dev
```

Для разработки замените флаг `--without` на `--with`

>Для создания виртуального окружения в директории проекта внесите изменения в конфигурацию [poetry](https://python-poetry.org/docs/configuration/#virtualenvspath)
```bash
poetry config virtualenvs.in-project = true
poetry config virtualenvs.path = "{project-dir}\\<your path>"
```

### Pip

Клонируйте проект, разверните виртуальное окружение `python -m venv venv` и запустите следующий скрипт:
```bash
pip install -r requirements.txt
```

## Сборка образа и запуск контейнера

Для сборки проекта потребуется добавить файл с переменными окружения `.env`:
```ini
APP_MODE='DEV'
APP_LOG_LEVEL='INFO'
APP_SENTRY_DSN=<your sentry dsn>

AUTH_SECRET_KEY=<your secret key>
AUTH_ALGORITHM=<your crypt algorithm>

DB_HOST=<host>
DB_PORT=5432
DB_USERNAME=<username>
DB_PASSWORD=<password>
DB_NAME=<database name>

DB_TEST_HOST=<host>
DB_TEST_PORT=5432
DB_TEST_USERNAME=<username>
DB_TEST_PASSWORD=<password>
DB_TEST_NAME=<test database name>

REDIS_HOST=<host>
REDIS_PORT=6379

GMAIL_SMTP_HOST='smtp.gmail.com'
GMAIL_SMTP_PORT=465
GMAIL_SMTP_USERNAME=<smtp username>
GOOGLE_APP_SECRET=<google app secret>
```

А также соответствующий файл `.env-non-dev` для поднятия всего проекта через `docker compose`:
```ini
# Содержимое .env файла...
# Кроме переменных окружения для тестовой базы с префиксом DB_TEST

# Добавить дополнительно для образа PostgreSQL
POSTGRES_DB=<database name>
POSTGRES_USER='postgres'
POSTGRES_PASSWORD=<password>
```

### Docker only

Достаточно иметь установленный Docker и в директории проекта запустить скрипт:
```bash
docker build -t <image name> .
```

После сборки можно поднять контейнер:
```bash
docker run -d -p <port>:8000 --name <container name>
```

Документация будет доступна по ссылке http://localhost:8000/docs.

>Без поднятия остальных контейнеров эндпоинты работают некорректно.

>Порт 8000 &ndash; стандартный для uvicorn, чтобы изменить это в файле `docker/app.sh` замените `--bind=0.0.0.0:8000` на нужное вам значение.  

#### Сборка образа без poetry

Потребуется отредактировать `Dockerfile` следующим образом:
```dockerfile
FROM python:3.11

RUN mkdir /booking
WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /booking/docker/*.sh
```

### Docker-compose

Для поднятия всего приложения нужно запустить сборку через `docker compose`:
```bash
docker compose build
```

А затем поднять все контейнеры:
```bash
docker compose run
```

После чего FastAPI приложение будет доступно по ссылке http://localhost:8000 (если порт не был сконфигурирован иначе).

Дополнительно:
- Flower доступен по ссылке http://localhost:5555