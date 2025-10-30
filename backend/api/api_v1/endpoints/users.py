from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# وارد کردن توابع CRUD و مدل‌ها
# توجه: فرض می‌کنیم crud_user، UserCreate، UserInDB و UserUpdate قبلاً تعریف شده‌اند.
from backend.crud import crud_user
from backend.schemas.user import UserCreate, UserInDB, UserUpdate
from backend.api import deps # وابستگی‌ها (get_db)

router = APIRouter()


# ------------------- مسیر (Endpoint) برای لیست کردن کاربران -------------------
@router.get("/", response_model=List[UserInDB])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    دریافت تمام کاربران با قابلیت صفحه‌بندی (Pagination).
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return users


# ------------------- مسیر برای ایجاد کاربر جدید -------------------
@router.post("/", response_model=UserInDB)
async def create_user(
    *,
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    ایجاد یک کاربر جدید.
    """
    # بررسی می‌کنیم که آیا کاربری با این ایمیل از قبل وجود دارد یا خیر
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # ایجاد و ذخیره کاربر در دیتابیس (تابع create از CRUD استفاده می‌کند)
    user = await crud_user.create(db, obj_in=user_in)
    return user


# ------------------- مسیر برای دریافت یک کاربر خاص -------------------
@router.get("/{user_id}", response_model=UserInDB)
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    دریافت یک کاربر خاص با استفاده از ID.
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


# ------------------- مسیر برای به‌روزرسانی کاربر -------------------
@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    *,
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    به‌روزرسانی اطلاعات یک کاربر.
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    # به‌روزرسانی و ذخیره تغییرات
    user = await crud_user.update(db, db_obj=user, obj_in=user_in)
    return user


# ------------------- مسیر برای حذف کاربر -------------------
@router.delete("/{user_id}", response_model=UserInDB)
async def delete_user(
    *,
    user_id: int,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    حذف یک کاربر.
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # حذف کاربر
    user = await crud_user.remove(db, id=user_id)
    return user
