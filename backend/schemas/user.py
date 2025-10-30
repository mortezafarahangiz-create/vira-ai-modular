from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Forward Reference برای جلوگیری از Import Cycle
# ما به شمای Item نیاز داریم تا لیست آیتم‌های یک کاربر را نمایش دهیم.
# این شمای آیتم در فایل schemas/item.py تعریف خواهد شد.
class Item(BaseModel):
    # این فقط یک تعریف موقت است. جزئیات دقیق در schemas/item.py می‌آید.
    title: str
    class Config:
        from_attributes = True

# ----------------- Base Schemas -----------------

class UserBase(BaseModel):
    """
    ویژگی‌های مشترک برای خواندن و نوشتن (ایمیل و نام)
    """
    email: EmailStr = Field(..., example="user@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")


class UserCreate(UserBase):
    """
    مدل برای ایجاد یک کاربر جدید (نیاز به رمز عبور).
    """
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    """
    مدل برای به‌روزرسانی اختیاری اطلاعات کاربر (رمز عبور و نام).
    """
    email: Optional[EmailStr] = None # اجازه به‌روزرسانی ایمیل
    password: Optional[str] = Field(None, min_length=8) # رمز عبور جدید
    full_name: Optional[str] = None


# ----------------- Response Schemas -----------------

class User(UserBase):
    """
    مدل نمایش داده‌های کاربر به مشتری (شامل ID و وضعیت‌ها).
    این مدل برای پاسخ‌های API استفاده می‌شود.
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    # لیست آیتم‌هایی که این کاربر مالک آن‌هاست (رابطه One-to-Many)
    # توجه: باید به صورت یک لیست از شمای Item تعریف شود.
    items: List[Item] = [] 

    # تنظیمات Pydantic برای سازگاری با SQLAlchemy
    class Config:
        """
        اجازه می‌دهد که مدل Pydantic از ORM (SQLAlchemy) Object Mapping بسازد.
        """
        from_attributes = True
