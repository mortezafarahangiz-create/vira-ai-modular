from typing import Any
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

# -----------------------------------------------------------------
# کلاس پایه برای مدل‌های SQLAlchemy
# این کلاس شامل تنظیمات اولیه و ستون‌های مشترک برای همه جداول است.
# -----------------------------------------------------------------
class Base(DeclarativeBase):
    """
    کلاس پایه سفارشی برای تمام مدل‌های SQLAlchemy.
    این کلاس شامل ستون‌های مشترک مانند 'id'، 'created_at' و 'updated_at' است.
    """

    # 1. نام جدول (Table Name)
    # این متد به صورت خودکار نام کلاس را به حروف کوچک تبدیل کرده و به عنوان
    # نام جدول در دیتابیس استفاده می کند (مثلا User -> user، Item -> item).
    @declared_attr
    def __tablename__(cls) -> str:
        """تولید خودکار نام جدول از نام کلاس."""
        # تبدیل نام کلاس به حروف کوچک
        return cls.__name__.lower()

    # 2. ستون ID (کلید اصلی)
    # تمام جداول ما یک کلید اصلی با نام 'id' از نوع integer خواهند داشت.
    id: Mapped[int] = mapped_column(primary_key=True)

    # 3. ستون زمان ایجاد (Created At)
    # از نوع DateTime است و با استفاده از func.now() به صورت خودکار زمان ایجاد را ثبت می کند.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=func.now(), 
        nullable=False,
        comment="زمان ایجاد رکورد"
    )

    # 4. ستون زمان به‌روزرسانی (Updated At)
    # از نوع DateTime است و هر بار که رکورد به‌روزرسانی می شود، زمان آن را ثبت می کند.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=func.now(), 
        onupdate=func.now(),
        nullable=False,
        comment="زمان آخرین به روز رسانی رکورد"
    )
    
    # 5. نمایش شیء (Representation)
    # برای دیباگینگ بهتر، یک متد __repr__ ساده تعریف می کنیم.
    def __repr__(self) -> str:
        """نمایش ساده و مفید از شیء مدل."""
        return f"<{self.__class__.__name__}(id={self.id})>"
