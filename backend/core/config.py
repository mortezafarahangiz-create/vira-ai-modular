import os
from typing import Any, Optional
from pydantic import Field, HttpUrl, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
# در محیط توسعه، این کار به شما کمک می‌کند متغیرها را جدا از کد نگه دارید.
load_dotenv()

# ----------------------------------------------------------------------
# کلاس تنظیمات
# ----------------------------------------------------------------------
# این کلاس تمامی متغیرهای مورد نیاز برنامه را از متغیرهای محیطی می‌خواند.

class Settings(BaseSettings):
    
    # ------------------------------------------------------------------
    # تنظیمات عمومی پروژه
    # ------------------------------------------------------------------
    
    # نام برنامه که در جاهای مختلفی مثل داکیومنت‌ها استفاده می‌شود.
    PROJECT_NAME: str = "FastAPI Persian Template"
    
    # لیستی از آدرس‌هایی که مجاز به برقراری ارتباط (CORS) هستند.
    # به صورت پیش‌فرض، تمامی آدرس‌ها مجاز هستند (امنیت کمتر، انعطاف بیشتر)
    BACKEND_CORS_ORIGINS: list[str] = ["*"] 
    
    # ------------------------------------------------------------------
    # تنظیمات امنیتی (JWT)
    # ------------------------------------------------------------------
    
    # کلید محرمانه برای امضای توکن‌های JWT.
    # این مقدار باید به شدت محرمانه و تصادفی باشد.
    # اگر در محیط تعریف نشده باشد، یک کلید پیش‌فرض (فقط برای توسعه) استفاده می‌شود.
    # در محیط تولید (Production) حتماً باید تنظیم شود.
    SECRET_KEY: str = Field(
        default="YOUR_ULTRA_SECRET_KEY_GOES_HERE_CHANGE_ME",
        validation_alias="SECRET_KEY"
    )

    # الگوریتم رمزنگاری برای JWT (استاندارد HS256)
    ALGORITHM: str = "HS256"
    
    # مدت زمان انقضای توکن دسترسی (بر حسب دقیقه)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 هفته
    
    # ------------------------------------------------------------------
    # تنظیمات دیتابیس (PostgreSQL)
    # ------------------------------------------------------------------
    
    # متغیرهای اتصال به دیتابیس
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app_db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    # رشته اتصال به دیتابیس (DB URI)
    # این خاصیت به صورت computed (محاسبه شده) است و توسط BaseSettings مدیریت می‌شود.
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """رشته اتصال نهایی به دیتابیس را برمی‌گرداند."""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ------------------------------------------------------------------
    # تنظیمات مدل برای Pydantic
    # ------------------------------------------------------------------
    
    model_config = SettingsConfigDict(
        # اجازه می‌دهد فیلدها را از متغیرهای محیطی با پیشوند "MYAPP_" بخواند
        # برای مثال: MYAPP_SECRET_KEY
        env_prefix='MYAPP_',
        # استفاده از .env
        env_file=('.env', '.env.prod'),
        # اجازه می‌دهد که متغیرها بدون تنظیم صریح در محیط، مقادیر پیش‌فرض بگیرند
        extra="allow",
        # حروف بزرگ/کوچک در متغیرهای محیطی مهم نیستند
        case_sensitive=False
    )

# ----------------------------------------------------------------------
# ایجاد نمونه اصلی تنظیمات
# ----------------------------------------------------------------------
# این شیء برای استفاده در هر جای برنامه در دسترس قرار می‌گیرد.
settings = Settings()
