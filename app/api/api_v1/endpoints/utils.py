from fastapi import APIRouter, Depends
from pydantic import EmailStr
from starlette.status import HTTP_201_CREATED

from app.api.utils.security import get_current_active_superuser
from app.models.msg import Msg
from app.models.user import UserInDB
from app.utils import send_test_email

router = APIRouter()


@router.post("/test-email/", response_model=Msg, status_code=HTTP_201_CREATED)
async def test_email(
    email_to: EmailStr,
    # pylint: disable=unused-argument
    current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email task sent"}
