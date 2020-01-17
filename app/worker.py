from pydantic import EmailStr
from raven import Client

from app.core import config
from app.core.celery_app import celery_app
from app.utils import send_test_email

client_sentry = Client(config.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str):
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def task_send_test_email(email_to: EmailStr):
    send_test_email(email_to)
    return f"email to {email_to} has been sent"
