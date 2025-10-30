from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from backend.core.database import Base

# این چک تایپ برای جلوگیری از Import Cycle ضروری است
if TYPE_CHECKING:
    from .user import User # در آینده این مدل را خواهیم ساخت


class Item(Base):
    """
    مدل SQLAlchemy برای جدول 'items' در دیتابیس.
    هر آیتم متعلق به یک کاربر (owner) است.
    """
    __tablename__ = "items"

    # ستون‌های اصلی
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), index=True, nullable=False)
    description = Column(Text, nullable=True) # Text برای متن‌های طولانی
    
    # کلید خارجی (Foreign Key) که به جدول 'users' اشاره دارد
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # زمان‌بندی
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # تعریف رابطه (Relationship)
    # تعریف مالک آیتم (یک به یک با مدل User)
    owner: "User" = relationship("User", back_populates="items")

    def __repr__(self) -> str:
        """
        نمایش آبجکت در کنسول
        """
        return f"<Item id={self.id}, title={self.title}, owner_id={self.owner_id}>"
