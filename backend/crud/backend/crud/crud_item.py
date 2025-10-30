from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.base import CRUDBase
from backend.models.item import Item as ItemModel
from backend.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[ItemModel, ItemCreate, ItemUpdate]):
    """
    پیاده‌سازی CRUD اختصاصی برای مدل آیتم (Item).
    """

    async def get_multi_by_owner(
        self,
        db: AsyncSession,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ItemModel]:
        """
        واکشی چندین آیتم بر اساس owner_id.
        """
        # ساخت دستور SELECT با فیلتر where برای owner_id
        stmt = (
            select(self.model)
            .where(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        return result.scalars().all()


# ایجاد نمونه‌ای از کلاس CRUDItem برای استفاده در اندپوینت‌ها
# این نمونه را می‌توان به عنوان یک Singleton در کل برنامه استفاده کرد.
item = CRUDItem(ItemModel)
