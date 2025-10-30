from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.core.config import settings
from backend.models.user import User
from backend.schemas.token import TokenPayload

# تعریف طرح امنیتی OAuth2PasswordBearer
# این مشخص می‌کند که توکن از کدام نقطه پایانی (endpoint) دریافت می‌شود.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

# ----------------------------------------------------
# توابع کمکی برای دریافت کاربر جاری
# ----------------------------------------------------

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> User:
    """
    اعتبارسنجی توکن JWT و بازگرداندن شیء کاربر متناظر.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # رمزگشایی (Decode) توکن
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        # اگر رمزگشایی یا اعتبارسنجی مدل Pydantic شکست خورد
        raise credentials_exception

    # پیدا کردن کاربر در دیتابیس بر اساس ID موجود در توکن
    user_statement = select(User).where(User.id == token_data.sub)
    result = await db.execute(user_statement)
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
        
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    اطمینان از فعال بودن کاربر جاری.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    اطمینان از فعال بودن و مدیر ارشد بودن کاربر جاری.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403, 
            detail="The user doesn't have enough privileges"
        )
    return current_user

# این بخش برای رفع خطای Imports از user.py در اینجا اضافه می‌شود.
# در حالت عادی، ماژول CRUD در لایه API نباید مستقیماً import شود، 
# اما برای استفاده از تابع is_superuser در اینجا ضروری است.
from backend import crud 
