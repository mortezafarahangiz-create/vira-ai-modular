from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, String, Text, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ایمپورت کردن کلاس پایه (Base) که قبلا تعریف کردیم
from backend.db.base import Base

# -----------------------------------------------------------------
# مدل User: برای ذخیره اطلاعات کاربران
# -----------------------------------------------------------------
class User(Base):
    """
    مدل SQLAlchemy برای نگهداری اطلاعات کاربران.
    جدول مربوطه به صورت خودکار 'user' نامیده می شود.
    """
    
    # ایمیل کاربر - باید منحصر به فرد باشد و به عنوان نام کاربری استفاده می شود
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="ایمیل منحصر به فرد کاربر"
    )
    
    # پسورد هش شده - از نوع String برای ذخیره هش امن
    hashed_password: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="پسورد هش شده کاربر"
    )
    
    # نام و نام خانوادگی کاربر
    full_name: Mapped[Optional[str]] = mapped_column(
        String(255), 
        nullable=True,
        comment="نام کامل کاربر"
    )
    
    # پرچم وضعیت فعال بودن کاربر
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True,
        comment="وضعیت فعال بودن حساب کاربری"
    )
    
    # پرچم وضعیت مدیر بودن کاربر
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, 
        default=False,
        comment="تعیین می کند آیا کاربر مدیر است یا خیر"
    )

    # رابطه (Relationship) با مدل APIToken
    tokens: Mapped[list["APIToken"]] = relationship(
        "APIToken",
        back_populates="user",
        cascade="all, delete-orphan", # حذف توکن‌ها با حذف کاربر
        comment="توکن‌های API مرتبط با این کاربر"
    )

# -----------------------------------------------------------------
# مدل APIToken: برای ذخیره توکن‌های احراز هویت
# -----------------------------------------------------------------
class APIToken(Base):
    """
    مدل SQLAlchemy برای نگهداری توکن‌های API یا Refresh Token ها.
    جدول مربوطه به صورت خودکار 'apitoken' نامیده می شود.
    """
    
    # توکن اصلی - باید یکتا و ایندکس شده باشد
    token: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="مقدار توکن API"
    )
    
    # تاریخ انقضای توکن
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        comment="زمان انقضای توکن"
    )
    
    # کلید خارجی برای اتصال به جدول کاربر
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), 
        nullable=False,
        comment="کلید خارجی به کاربر مالک توکن"
    )
    
    # رابطه (Relationship) با مدل User
    user: Mapped["User"] = relationship(
        "User", 
        back_populates="tokens",
        comment="کاربر مالک این توکن"
    )
