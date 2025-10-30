from typing import List, Optional, Union

# از pydantic-settings برای مدیریت ایمن تنظیمات استفاده می‌کنیم.
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, EmailStr, field_validator


class Settings(BaseSettings):
    """
    کلاس تنظیمات اصلی برنامه که مقادیر را از متغیرهای محیطی یا فایل .env می‌خواند.
    """

    # ----------------------------------------------------
    # تنظیمات پایگاه داده (PostgreSQL)
    # ----------------------------------------------------
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """ساخت URI دیتابیس PostgreSQL برای SQLAlchemy (استفاده از asyncpg)"""
        # توجه: از "postgresql+asyncpg" برای درایور آسنکرون استفاده می‌شود.
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # ----------------------------------------------------
    # تنظیمات امنیتی (JWT)
    # ----------------------------------------------------
    # کلید محرمانه برای امضای توکن‌ها (باید تصادفی و طولانی باشد)
    SECRET_KEY: str
    # مدت زمان انقضا توکن دسترسی به دقیقه (مثال: 60 دقیقه * 24 ساعت * 7 روز = 1 هفته)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 
    # الگوریتم رمزگذاری JWT
    SECURITY_ALGORITHM: str = "HS256"

    # ----------------------------------------------------
    # تنظیمات مدیر ارشد (Superuser)
    # ----------------------------------------------------
    # ایمیل و رمز عبور پیش‌فرض برای ایجاد اولین مدیر ارشد
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    
    # ----------------------------------------------------
    # تنظیمات CORS (دامنه‌های مجاز)
    # ----------------------------------------------------
    # لیست دامنه‌هایی که اجازه دسترسی به API را دارند.
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # این اعتبارسنجی کمک می‌کند تا مقادیر را هم به صورت لیست و هم به صورت رشته جدا شده با کاما قبول کنیم.
    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """تبدیل رشته‌های جدا شده با کاما به لیست URL‌های مجاز."""
        if isinstance(v, str) and not v.startswith("["):
            return [url.strip() for url in v.split(",")]
        elif isinstance(v, List):
            return [str(url).strip() for url in v]
        return v
    
    # ----------------------------------------------------
    # تنظیمات pydantic-settings
    # ----------------------------------------------------
    model_config = SettingsConfigDict(
        # تعیین فایل پیش‌فرض برای خواندن متغیرهای محیطی
        env_file=".env",
        # تعیین حساسیت به حروف بزرگ و کوچک در متغیرهای محیطی
        case_sensitive=True
    )

# ایجاد نمونه Singleton از تنظیمات
settings = Settings()
