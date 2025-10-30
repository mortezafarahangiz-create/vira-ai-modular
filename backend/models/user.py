from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# از OAuth2PasswordBearer برای ساخت طرح احراز هویت مبتنی بر توکن استفاده می‌کنیم
from fastapi.security import OAuth2PasswordBearer 

# سشن دیتابیس را از ماژول database وارد می‌کنیم
from backend.core.database import get_async_session 

# طرح احراز هویت OAuth2
# این طرح مشخص می‌کند که توکن از طریق هدر Authorization (Bearer Token) ارسال می‌شود.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

# ------------------- وابستگی: دریافت سشن دیتابیس -------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    تابع تزریق وابستگی (Dependency) برای ارائه یک سشن دیتابیس غیرهمزمان (AsyncSession)
    به Endopintهای FastAPI.
    """
    async for session in get_async_session():
        # سشن را در اختیار endpoint قرار می‌دهد
        yield session

# تعریف یک نوع (Type) کوتاه‌تر برای استفاده در روترها
# Annotated[AsyncSession, Depends(get_db)]
AsyncDB = Annotated[AsyncSession, Depends(get_db)]


# ------------------- وابستگی: دریافت کاربر فعلی (در آینده) -------------------
# توجه: منطق احراز هویت در حال حاضر پیاده‌سازی نشده است.
# این توابع فقط برای ساختار آینده پروژه نگه داشته شده‌اند.

async def get_current_user_placeholder(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncDB,
):
    """
    وابستگی موقت برای احراز هویت.
    در آینده، منطق دیکد کردن JWT و واکشی کاربر از دیتابیس اینجا قرار می‌گیرد.
    """
    # در حال حاضر فقط توکن را دریافت می‌کنیم
    # منطق واقعی در فایل‌های security و CRUD قرار خواهد گرفت.
    return {"token_received": token}
