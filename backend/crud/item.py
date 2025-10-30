from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# وارد کردن اجزای مورد نیاز
from backend.models.item import Item # مدل دیتابیسی
from backend.schemas.item import ItemCreate, ItemUpdate # اسکیماهای ورودی
from backend.crud.base import CRUDBase # کلاس پایه CRUD

# -----------------------------------------------------------------
# کلاس CRUD مخصوص مدل Item
# -----------------------------------------------------------------
class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    
    # ------------------- متدهای خواندن (Read) -------------------
    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        دریافت لیست چندگانه آیتم‌ها بر اساس شناسه مالک (Owner ID).
        
        :param db: نشست دیتابیس (AsyncSession)
        :param owner_id: شناسه کاربری مالک آیتم‌ها
        :param skip: تعداد رکوردهایی که باید نادیده گرفته شوند (برای صفحه‌بندی)
        :param limit: حداکثر تعداد رکوردهایی که باید برگردانده شوند (برای صفحه‌بندی)
        :return: لیستی از آبجکت‌های Item
        """
        # ساخت کوئری: انتخاب آیتم‌هایی که owner_id آن‌ها با شناسه ورودی برابر است.
        result = await db.execute(
            select(self.model)
            .where(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

# -----------------------------------------------------------------
# ایجاد یک نمونه از کلاس CRUDItem برای استفاده آسان در بخش‌های مختلف پروژه
# -----------------------------------------------------------------
item = CRUDItem(Item)
