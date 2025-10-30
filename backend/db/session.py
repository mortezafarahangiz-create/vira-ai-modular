import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# وارد کردن شیء تنظیمات سراسری که در گام قبل تعریف شد
from backend.core.config import settings

# ----------------------------------------------------------------------
# پیکربندی SQLAlchemy
# ----------------------------------------------------------------------

# ایجاد موتور اتصال (Engine) به دیتابیس.
# از رشته اتصال کامل تعریف شده در config.py استفاده می‌شود.
# echo=False: برای جلوگیری از نمایش کوئری‌های SQL در کنسول. برای دیباگ کردن می‌تواند True شود.
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    pool_pre_ping=True,  # بررسی سلامت اتصال قبل از استفاده (برای اتصال‌های پایدار)
    echo=False
)

# ایجاد سازنده Session (جلسه) برای SQLAlchemy.
# Session محلی است که کوئری‌ها در آن اجرا می‌شوند.
# autocommit=False: تغییرات بلافاصله به دیتابیس ارسال نمی‌شوند و نیاز به commit دارند.
# autoflush=False: تغییرات به صورت خودکار به دیتابیس ارسال نمی‌شوند.
# bind=engine: این Session را به موتور اتصال ایجاد شده در بالا متصل می‌کند.
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# ----------------------------------------------------------------------
# تابع Dependency برای FastAPI
# ----------------------------------------------------------------------

def get_db():
    """
    Dependency Function برای استفاده در مسیرهای (Routes) FastAPI.
    
    این تابع یک Session دیتابیس جدید ایجاد کرده، آن را برای استفاده در اختیار 
    تابع مسیر (Path function) قرار می‌دهد و در نهایت، پس از اتمام کار،
    (چه موفقیت‌آمیز و چه با خطا) Session را می‌بندد تا منابع آزاد شوند.
    
    استفاده از try-finally تضمین می‌کند که Session حتماً بسته شود.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
