from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------------
# تنظیمات اصلی
# ----------------------------------------------------------------------

# این قسمت باید با توجه به تنظیمات پروژه شما تغییر کند.
# برای شروع و سادگی، از SQLite در یک فایل به نام 'app.db' استفاده می کنیم.
# برای پروژه های جدی تر، بهتر است از PostgreSQL یا MySQL استفاده شود.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Engine اصلی دیتابیس
# connect_args={'check_same_thread': False} فقط برای SQLite در FastAPI نیاز است.
# این اجازه می دهد که چندین درخواست در یک زمان با یک اتصال کار کنند.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# تعریف SessionLocal
# این کلاس هر بار که نیاز به تعامل با دیتابیس داریم، یک Session ایجاد می کند.
# autocommit=False: یعنی تغییرات باید صراحتاً با commit() ذخیره شوند.
# autoflush=False: از فراخوانی flush به طور خودکار قبل از commit جلوگیری می کند.
# bind=engine: اتصال به Engine تعریف شده را مشخص می کند.
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# ----------------------------------------------------------------------
# تابع Dependency برای استفاده در مسیرهای FastAPI
# ----------------------------------------------------------------------

def get_db() -> Generator:
    """
    Dependency Helper برای مسیرهای FastAPI.
    یک سشن دیتابیس جدید باز می کند و پس از اتمام درخواست آن را می بندد.
    """
    db = SessionLocal()
    try:
        # yield باعث می شود که کد بعد از اتمام درخواست (یا وقوع خطا) اجرا شود (فاز cleanup)
        yield db
    finally:
        # در نهایت، سشن دیتابیس بسته می شود.
        db.close()
