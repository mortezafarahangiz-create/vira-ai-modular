from typing import Any, Dict, Optional, Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# وارد کردن مدل‌ها و شمای Pydantic
from backend.models.user import User as UserModel
from backend.schemas.user import UserCreate, UserUpdate
from backend.crud.base import CRUDBase

# وارد کردن توابع امنیتی (که باید بعداً در فایل security.py تعریف شوند)
# فرض می‌کنیم توابع زیر در یک ماژول امنیتی وجود دارند:
from backend.core.security import get_password_hash, verify_password 


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    """
    پیاده‌سازی CRUD اختصاصی برای مدل کاربر (User).
    """
    
    # ----------------- متدهای واکشی اختصاصی -----------------

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[UserModel]:
        """
        واکشی یک کاربر بر اساس آدرس ایمیل.
        """
        stmt = select(self.model).where(self.model.email == email)
        result = await db.execute(stmt)
        return result.scalars().first()

    # ----------------- متدهای ایجاد و به‌روزرسانی -----------------

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> UserModel:
        """
        ایجاد یک کاربر جدید با هش کردن رمز عبور.
        """
        # هش کردن رمز عبور قبل از ذخیره در دیتابیس
        hashed_password = get_password_hash(obj_in.password)
        
        # ساخت دیکشنری از داده‌های ورودی
        obj_in_data = obj_in.model_dump()
        obj_in_data["hashed_password"] = hashed_password
        
        # حذف رمز عبور ساده از دیکشنری قبل از ساخت مدل
        del obj_in_data["password"] 
        
        # ساخت و ذخیره مدل
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: UserModel,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        """
        به‌روزرسانی اطلاعات کاربر، با هش کردن مجدد رمز عبور در صورت وجود.
        """
        # اگر ورودی Pydantic Schema بود
        if isinstance(obj_in, UserUpdate):
            update_data = obj_in.model_dump(exclude_unset=True)
        # اگر ورودی دیکشنری بود
        else:
            update_data = obj_in

        # مدیریت رمز عبور: اگر رمز عبور جدیدی ارسال شده، آن را هش کن
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["hashed_password"] = hashed_password
            del update_data["password"]
        elif "password" in update_data:
            # اگر password به صراحت None یا رشته خالی بود، آن را از به‌روزرسانی حذف کن
            del update_data["password"]
            
        # فراخوانی متد update کلاس پایه
        # ما باید مطمئن شویم که فقط فیلدهای مورد نظر به‌روزرسانی شوند.
        # متد update در CRUDBase این کار را انجام می‌دهد.
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


    # ----------------- متد احراز هویت (Auth) -----------------
    
    def authenticate(self, db_obj: UserModel, password: str) -> bool:
        """
        بررسی می‌کند که آیا رمز عبور ارائه شده با رمز عبور هش شده در دیتابیس مطابقت دارد یا خیر.
        """
        if not db_obj:
            return False
            
        return verify_password(password, db_obj.hashed_password)


    # ----------------- متدهای نقش و مجوز (Authorization) -----------------

    def is_superuser(self, user: UserModel) -> bool:
        """
        بررسی می‌کند که آیا کاربر دارای مجوز سوپریوزر است یا خیر.
        """
        return user.is_superuser


# ایجاد نمونه‌ای از کلاس CRUDUser برای استفاده در اندپوینت‌ها
# این نمونه را می‌توان به عنوان یک Singleton در کل برنامه استفاده کرد.
user = CRUDUser(UserModel)
