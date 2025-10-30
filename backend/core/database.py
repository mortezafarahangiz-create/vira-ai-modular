from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.core.config import settings

# ------------------- ساختار اصلی مدل‌های دیتابیس -------------------
class Base(DeclarativeBase):
    """
    کلاس پایه اصلی برای مدل‌های SQLAlchemy (ORM) ما.
    تمام مدل‌های دیتابیس (مانند User و Item) از این کلاس ارث می‌برند.
    """
    pass

# ------------------- پیکربندی اتصال به دیتابیس -------------------

# ساخت موتور اتصال غیرهمزمان (Async Engine)
# از URI ساخته شده در config.py استفاده می‌کند.
async_engine = create_async_engine(
    url=str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True, # در محیط توسعه (Development)، کوئری‌های SQL را نمایش می‌دهد
    future=True, # از سینتکس جدید SQLAlchemy 2.0 استفاده می‌کند
)

# تعریف سازنده سشن (Session Maker) برای ایجاد سشن‌های جدید
# expire_on_commit=False: از منقضی شدن آبجکت‌ها بعد از هر commit جلوگیری می‌کند.
async_session_maker = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# ------------------- تابع وابستگی برای دریافت سشن -------------------
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    یک سشن دیتابیس غیرهمزمان جدید ایجاد می‌کند و آن را در اختیار
    Endopintهای FastAPI قرار می‌دهد (از طریق Dependency Injection).
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            # نیازی به commit کردن در اینجا نیست، زیرا هر endpoint به صورت
            # خودکار وظیفه commit را در پایان عملیات موفقیت‌آمیز بر عهده می‌گیرد.
            await session.close()
