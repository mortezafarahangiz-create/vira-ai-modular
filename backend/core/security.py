from datetime import datetime, timedelta
from typing import Optional, Any
from passlib.context import CryptContext
from jose import jwt

# ماژول تنظیمات را وارد می‌کنیم. این ماژول را در گام بعدی ایجاد خواهیم کرد.
from backend.core.config import settings

# ----------------------------------------------------------------------
# تنظیمات پسورد
# ----------------------------------------------------------------------

# تعریف متد هشینگ برای پسوردها.
# استفاده از bcrypt برای هش کردن پسوردها که امن و استاندارد است.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """پسورد خام (plain_password) را با پسورد هش شده ذخیره شده در دیتابیس مقایسه می‌کند."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """یک پسورد خام را هش می‌کند و برای ذخیره در دیتابیس آماده می‌سازد."""
    return pwd_context.hash(password)

# ----------------------------------------------------------------------
# توابع JWT (JSON Web Token)
# ----------------------------------------------------------------------

def create_access_token(
    subject: Any, expires_delta: Optional[timedelta] = None
) -> str:
    """
    یک توکن دسترسی JWT ایجاد می‌کند.
    
    :param subject: شناسه کاربری (user_id) یا داده اصلی که می‌خواهیم درون توکن باشد.
    :param expires_delta: مدت زمان انقضا (اختیاری). اگر داده نشود از تنظیمات استفاده می‌شود.
    :return: رشته توکن JWT رمزنگاری شده.
    """
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # استفاده از زمان انقضای تعریف شده در فایل تنظیمات (config.py)
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # داده‌هایی که باید درون توکن رمزنگاری شوند. 'sub' برای 'subject' و 'exp' برای 'expiration' استاندارد هستند.
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # رمزنگاری توکن با استفاده از کلید مخفی و الگوریتم مشخص شده در تنظیمات
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt
