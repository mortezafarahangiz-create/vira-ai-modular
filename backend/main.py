from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import AsyncDB
from backend.core.security import create_access_token

# Note: منطق احراز هویت (Authentication) و تولید توکن (Token)
# در گام‌های بعدی و بعد از تعریف شمای Pydantic اضافه خواهد شد.

router = APIRouter()


@router.post("/access-token")
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncDB
):
    """
    دریافت توکن دسترسی OAuth2 از طریق نام کاربری و رمز عبور.
    """
    # TODO: در اینجا باید کاربر با استفاده از email و password تایید شود.
    # user = authenticate_user(db, email=form_data.username, password=form_data.password)
    # اگر کاربر پیدا نشد یا رمز عبور اشتباه بود:
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Incorrect username or password",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    
    # فعلاً یک پاسخ موقت برمی‌گردانیم
    return {
        "access_token": "DUMMY_TOKEN_FOR_NOW",
        "token_type": "bearer",
    }
