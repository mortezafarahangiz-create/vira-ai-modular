import os
from typing import List, Optional

from pydantic import AnyHttpUrl, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ------------------- کلاس تنظیمات (Settings) -------------------
class Settings(BaseSettings):
    """
    تنظیمات اصلی پروژه که از متغیرهای محیطی (Environment Variables)
    یا فایل .env خوانده می‌شوند.
    """
    
    # تنظیمات مدل‌سازی Pydantic
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
        case_sensitive=True
    )

    # 1. تنظیمات عمومی
    PROJECT_NAME: str = "FastAPI Base Project"
    API_V1_STR: str = "/api/v1"

    # 2. تنظیمات امنیت و توکن
    SECRET_KEY: str = os.getenv("SECRET_KEY", "YOUR_SECURE_SECRET_KEY_GOES_HERE_CHANGE_ME")
    # زمان انقضای توکن دسترسی (بر حسب دقیقه) - برای مثال 60 دقیقه
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 روز

    # 3. تنظیمات CORS (ارتباط فرانت‌اند و بک‌اند)
    # اگر فرانت‌اند در دامنه دیگری باشد، آن را اینجا اضافه کنید.
    # به عنوان مثال: ["http://localhost:3000", "https://yourfrontend.com"]
    # استفاده از "*" برای محیط توسعه (Development) است.
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=["http://localhost:3000", "http://localhost:8000"], 
        # این مقدار برای پایداری در Pydantic Field تعریف شده است
        validate_default=True
    )
    
    # 4. تنظیمات دیتابیس PostgreSQL
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app_db")
    
    # فیلد محاسباتی برای ساخت URI کامل دیتابیس
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        ساخت URI اتصال به دیتابیس PostgreSQL برای SQLAlchemy
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg", # استفاده از درایور asyncpg برای عملیات غیرهمزمان
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=5432, # پورت پیش‌فرض PostgreSQL
            path=f"{self.POSTGRES_DB}",
        )


settings = Settings()
