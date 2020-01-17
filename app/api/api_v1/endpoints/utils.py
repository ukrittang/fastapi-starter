from fastapi import APIRouter, Depends
from pydantic import EmailStr
from starlette.status import HTTP_201_CREATED

from app.api.utils.security import get_current_active_superuser
from app.core.celery_app import celery_app
from app.models.msg import Msg
from app.models.user import UserInDB

router = APIRouter()


@router.post("/test-celery/", response_model=Msg, status_code=HTTP_201_CREATED)
def test_celery(
    msg: Msg,
    # pylint: disable=unused-argument
    current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=Msg, status_code=HTTP_201_CREATED)
async def test_email(
    email_to: EmailStr,
    # pylint: disable=unused-argument
    current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test emails.
    """
    celery_app.send_task("app.worker.task_send_test_email", args=["ukrit.tang@gmail.com"])
    return {"msg": "Test email task sent"}
