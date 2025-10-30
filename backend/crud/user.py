from typing import Any, Dict, Optional, List, Type
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

# وارد کردن مدل SQLAlchemy (مدل دیتابیس)
from backend.models import User as UserModel
# وارد کردن شمای Pydantic (مدل ورودی/خروجی)
from backend.schemas.user import UserCreate, UserUpdate

# وارد کردن ابزار هش کردن پسورد
from backend.core.security import get_password_hash

# ----------------------------------------------------------------------
# کلاس اصلی CRUD برای کاربر
# ----------------------------------------------------------------------

# این کلاس توابع مورد نیاز برای تعامل با مدل UserModel در دیتابیس را فراهم می‌کند.
class CRUDUser:
    
    # ------------------------------------------------------------------
    # خواندن اطلاعات (Read Operations)
    # ------------------------------------------------------------------

    # دریافت یک کاربر بر اساس شناسه (ID)
    def get_by_id(self, db: Session, user_id: int) -> Optional[UserModel]:
        """کاربر را بر اساس شناسه (ID) از دیتابیس دریافت می‌کند."""
        # استفاده از select جدید SQLAlchemy 2.0
        stmt = select(UserModel).where(UserModel.id == user_id)
        return db.scalar(stmt)

    # دریافت یک کاربر بر اساس ایمیل (Email)
    def get_by_email(self, db: Session, email: str) -> Optional[UserModel]:
        """کاربر را بر اساس ایمیل از دیتابیس دریافت می‌کند."""
        stmt = select(UserModel).where(UserModel.email == email)
        return db.scalar(stmt)

    # دریافت تمام کاربران
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[UserModel]:
        """لیستی از کاربران را با قابلیت صفحه بندی دریافت می‌کند."""
        stmt = select(UserModel).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    # ------------------------------------------------------------------
    # ایجاد (Create Operation)
    # ------------------------------------------------------------------

    # ایجاد یک کاربر جدید
    def create(self, db: Session, *, obj_in: UserCreate) -> UserModel:
        """یک کاربر جدید با پسورد هش شده در دیتابیس ایجاد می‌کند."""
        
        # هش کردن پسورد قبل از ذخیره سازی
        hashed_password = get_password_hash(obj_in.password)
        
        # تبدیل شمای ورودی به یک دیکشنری برای ساخت مدل دیتابیس
        # obj_in.model_dump() شامل تمامی فیلدها به جز password است
        obj_in_data = obj_in.model_dump(exclude_unset=True, exclude={'password'})
        
        # ساخت مدل جدید با پسورد هش شده و سایر اطلاعات
        db_obj = UserModel(
            **obj_in_data,
            hashed_password=hashed_password
        )
        
        # افزودن به سشن و ذخیره در دیتابیس
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ------------------------------------------------------------------
    # به‌روزرسانی (Update Operation)
    # ------------------------------------------------------------------
    
    # به‌روزرسانی اطلاعات یک کاربر
    def update(
        self, db: Session, *, db_obj: UserModel, obj_in: UserUpdate
    ) -> UserModel:
        """اطلاعات یک کاربر موجود را به‌روزرسانی می‌کند."""
        
        # تبدیل مدل دیتابیس به دیکشنری
        obj_data = db_obj.__dict__
        # تبدیل شمای ورودی (UserUpdate) به دیکشنری و حذف فیلدهای تنظیم نشده (None)
        update_data = obj_in.model_dump(exclude_unset=True)

        # اگر پسورد جدیدی در ورودی وجود داشته باشد، آن را هش کرده و جایگزین می‌کنیم
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            update_data["hashed_password"] = hashed_password
            # حذف پسورد خام از داده‌های به‌روزرسانی
            del update_data["password"]

        # به‌روزرسانی فیلدهای مدل دیتابیس با داده‌های جدید
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ------------------------------------------------------------------
    # حذف (Delete Operation)
    # ------------------------------------------------------------------

    # حذف یک کاربر
    def remove(self, db: Session, *, user_id: int) -> Optional[UserModel]:
        """یک کاربر را بر اساس شناسه از دیتابیس حذف می‌کند."""
        
        # پیدا کردن کاربر
        db_obj = self.get_by_id(db, user_id=user_id)
        
        if db_obj:
            # حذف کاربر
            db.delete(db_obj)
            db.commit()
        
        return db_obj

    # ------------------------------------------------------------------
    # توابع کمکی برای احراز هویت
    # ------------------------------------------------------------------

    # احراز هویت با ایمیل و پسورد (بدون commit به دیتابیس)
    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[UserModel]:
        """کاربر را بر اساس ایمیل و پسورد احراز هویت می‌کند."""
        user = self.get_by_email(db, email=email)
        
        if not user:
            return None
            
        # در اینجا نیاز به تابع verify_password داریم که در فایل security.py تعریف خواهد شد
        # اما برای جلوگیری از وابستگی چرخشی، آن را در همان جایی که استفاده می‌شود، import می‌کنیم
        from backend.core.security import verify_password
        
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
        
    # بررسی اینکه آیا کاربر مدیر (Superuser) است یا خیر
    def is_superuser(self, user: UserModel) -> bool:
        """بررسی می‌کند که آیا کاربر دارای مجوز مدیر است یا خیر."""
        return user.is_superuser
    
# ----------------------------------------------------------------------
# ایجاد نمونه اصلی CRUD
# ----------------------------------------------------------------------
# این شیء برای استفاده آسان در هر جای برنامه در دسترس قرار می‌گیرد.
user = CRUDUser()
