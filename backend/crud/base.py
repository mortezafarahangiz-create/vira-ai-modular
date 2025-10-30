from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.db.base_class import Base # فرض می‌کنیم Base مدل SQLAlchemy از اینجا وارد می‌شود

# تعریف TypeVar برای ORM Model و Schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    یک کلاس پایه برای CRUD (Create, Read, Update, Delete) که 
    عملیات رایج دیتابیس را به صورت جنریک (Generic) و ناهمگام (Asynchronous) پیاده‌سازی می‌کند.

    ویژگی‌ها:
    * model: کلاس مدل SQLAlchemy (مثلاً User یا Item)
    """

    def __init__(self, model: Type[ModelType]):
        """
        :param model: کلاس مدل SQLAlchemy که عملیات CRUD برای آن انجام می‌شود.
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        واکشی یک رکورد بر اساس ID.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        واکشی چندین رکورد.
        """
        stmt = select(self.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        ایجاد یک رکورد جدید.
        """
        # تبدیل Pydantic Schema به دیکشنری
        obj_in_data = jsonable_encoder(obj_in, exclude_unset=True)
        # ایجاد نمونه مدل SQLAlchemy
        db_obj = self.model(**obj_in_data) 
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        بروزرسانی یک رکورد موجود.
        """
        obj_data = jsonable_encoder(db_obj)
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Pydantic Schema را به دیکشنری تبدیل می‌کند و فقط فیلدهای Set شده را در نظر می‌گیرد
            update_data = obj_in.model_dump(exclude_unset=True)

        # ادغام داده‌های موجود با داده‌های به‌روزرسانی
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """
        حذف یک رکورد بر اساس ID.
        """
        # ابتدا رکورد را واکشی می‌کنیم تا آن را برگردانیم
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        obj = result.scalars().first()
        
        if not obj:
            return None

        # اجرای دستور حذف
        await db.delete(obj)
        await db.commit()
        return obj # شیء حذف شده را برمی‌گرداند
