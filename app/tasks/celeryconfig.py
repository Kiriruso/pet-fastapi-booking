from celery import Celery

from app.settings import service_redis_settings

celery = Celery(
    main="tasks", broker=service_redis_settings.redis_url, include=["app.tasks.tasks"]
)
