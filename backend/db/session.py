from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

# -----------------------------------------------------------------
# تعریف موتور اتصال (Engine)
# -----------------------------------------------------------------
# با استفاده از رشته اتصال (SQLALCHEMY_DATABASE_URI) که از تنظیمات (settings)
# خوانده می‌شود، یک موتور اتصال ناهمگام (Async Engine) ایجاد می‌شود.
# این موتور مسئول ارتباط با دیتابیس (در اینجا PostgreSQL) است.
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True  # اطمینان از زنده بودن اتصال قبل از استفاده
)

# -----------------------------------------------------------------
# تعریف سازنده نشست دیتابیس (Sessionmaker)
# -----------------------------------------------------------------
# این بخش یک کلاس سازنده برای نشست‌های دیتابیس ایجاد می‌کند.
# 1. autocommit=False: تضمین می‌کند که تراکنش‌ها به صورت خودکار commit نشوند و نیاز به فراخوانی دستی commit باشد.
# 2. autoflush=False: تضمین می‌کند که اشیا قبل از فراخوانی query به صورت خودکار به دیتابیس ارسال نشوند.
# 3. bind=engine: نشست‌ها را به موتور اتصال تعریف شده بالا متصل می‌کند.
# 4. class_=AsyncSession: نوع نشست را به عنوان نشست ناهمگام (AsyncSession) تعریف می‌کند.
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)


# -----------------------------------------------------------------
# تابع کمکی برای تزریق وابستگی (Dependency Injection) در FastAPI
# -----------------------------------------------------------------
async def get_db() -> AsyncSession:
    """
    تابع جنریتور برای دریافت یک نشست دیتابیس ناهمگام (AsyncSession).
    
    این تابع برای استفاده به عنوان یک Dependency در FastAPI طراحی شده است.
    از الگوی Context Manager استفاده می‌کند تا تضمین کند نشست پس از اتمام
    کار (حتی در صورت بروز خطا) به درستی بسته شود.
    """
    db = AsyncSessionLocal()
    try:
        # نشست ایجاد شده را yield می‌کند
        yield db
    finally:
        # پس از اتمام کار، نشست را می‌بندد
        await db.close()

# -----------------------------------------------------------------
# نکته مهم:
# این فایل به متغیر settings.SQLALCHEMY_DATABASE_URI که در
# backend/core/config.py تعریف خواهد شد، وابستگی دارد.
# -----------------------------------------------------------------
