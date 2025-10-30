from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# ----------------------------------------------------------------------
# کلاس پایه
# ----------------------------------------------------------------------

# BaseUser: فیلدهای مشترک که در ایجاد و به‌روزرسانی کاربر استفاده می‌شوند.
class BaseUser(BaseModel):
    # ایمیل کاربر
    email: EmailStr = Field(..., description="ایمیل کاربر")
    
    # نام کامل کاربر (اختیاری)
    full_name: Optional[str] = Field(None, description="نام کامل کاربر")
    
    # وضعیت فعال بودن (اختیاری، پیش‌فرض True)
    is_active: Optional[bool] = Field(True, description="وضعیت فعال بودن کاربر")
    
    # وضعیت مدیر بودن (اختیاری، پیش‌فرض False)
    is_superuser: Optional[bool] = Field(False, description="تعیین می‌کند آیا کاربر مدیر است یا خیر")
    
    class Config:
        # allow_population_by_field_name = True
        # به Pydantic اجازه می‌دهد تا مدل‌های SQLAlchemy را به اشیای Pydantic تبدیل کند
        from_attributes = True

# ----------------------------------------------------------------------
# کلاس‌های عملیاتی
# ----------------------------------------------------------------------

# UserCreate: شمای مورد نیاز برای ایجاد یک کاربر جدید (ورودی API)
class UserCreate(BaseUser):
    # پسورد کاربر - برای ایجاد الزامی است
    password: str = Field(..., description="پسورد کاربر")

# UserUpdate: شمای مورد نیاز برای به‌روزرسانی اطلاعات کاربر (ورودی API)
# پسورد در اینجا اختیاری است
class UserUpdate(BaseUser):
    # ایمیل را در به‌روزرسانی اختیاری می‌کنیم
    email: Optional[EmailStr] = Field(None, description="ایمیل کاربر")
    
    # برای به‌روزرسانی پسورد، اگر وارد شود
    password: Optional[str] = Field(None, description="پسورد جدید کاربر (اختیاری)")
    
    # در به‌روزرسانی می‌توان وضعیت is_superuser را تغییر نداد
    is_superuser: Optional[bool] = Field(None, description="تعیین می‌کند آیا کاربر مدیر است یا خیر")

# UserInDBBase: شمای اصلی برای نمایش اطلاعات کاربر (خروجی API)
# حاوی فیلدهایی از دیتابیس است که نباید در معرض دید قرار گیرند (مثل پسورد)
class UserInDBBase(BaseUser):
    id: Optional[int] = Field(None, description="شناسه منحصر به فرد کاربر")
    
    # فیلد is_active باید وجود داشته باشد اما is_superuser می تواند حذف شود اگر نمی خواهیم همیشه نشان دهیم.
    # در اینجا آن را نگه می داریم.

# ----------------------------------------------------------------------
# کلاس‌های نمایش
# ----------------------------------------------------------------------

# User: شمای خروجی API برای نمایش اطلاعات عمومی کاربر
class User(UserInDBBase):
    pass
    # از همین کلاس برای نمایش داده‌ها استفاده می‌کنیم.
    # در این مدل، فیلد 'hashed_password' از مدل SQLAlchemy وجود ندارد و Pydantic آن را حذف می کند.

# UserInDB: شمایی که شامل تمام فیلدهای دیتابیس است (فقط برای استفاده داخلی سرور)
class UserInDB(UserInDBBase):
    hashed_password: str = Field(..., description="پسورد هش شده کاربر")
