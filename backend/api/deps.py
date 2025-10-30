from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

# AsyncSessionLocal را از فایل session.py وارد می‌کنیم
# فرض بر این است که backend/db/session.py قبلاً ایجاد شده است
from backend.db.session import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    توابع وابستگی برای تزریق نشست دیتابیس (AsyncSession) به روترها.

    این تابع یک نشست دیتابیس را ایجاد کرده، آن را به تابع روتر تحویل می‌دهد
    و پس از پایان کار، نشست را بسته یا خطاها را مدیریت می‌کند.
    """
    db = AsyncSessionLocal()
    try:
        # نشست دیتابیس را به تابع روتر تحویل می‌دهد
        yield db
    finally:
        # در نهایت، مطمئن می‌شود که نشست دیتابیس بسته شود
        await db.close()

# در آینده، توابع وابستگی برای احراز هویت (Authentication) نیز به این فایل اضافه خواهند شد.
