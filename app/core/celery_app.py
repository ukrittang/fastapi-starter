from celery import Celery

from app.core import config

celery_app = Celery("worker", broker=config.REDIS_URI)

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.task_send_test_email": "main-queue",
}
