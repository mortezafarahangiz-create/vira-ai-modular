from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# وارد کردن توابع CRUD و مدل‌های Pydantic
# ما از مدل‌های ItemCreate، ItemInDB و ItemUpdate که قبلاً تعریف شده‌اند، استفاده می‌کنیم.
from backend.crud import crud_item
from backend.schemas.item import ItemCreate, ItemInDB, ItemUpdate
from backend.api import deps # وابستگی‌های دیتابیس (get_db)

router = APIRouter()

# ------------------- مسیر (Endpoint) برای لیست کردن آیتم‌ها -------------------
@router.get("/", response_model=List[ItemInDB])
async def read_items(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    دریافت تمام آیتم‌ها با قابلیت صفحه‌بندی (Pagination).
    """
    items = await crud_item.get_multi(db, skip=skip, limit=limit)
    return items


# ------------------- مسیر برای ایجاد آیتم جدید -------------------
@router.post("/", response_model=ItemInDB)
async def create_item(
    *,
    item_in: ItemCreate,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    ایجاد یک آیتم جدید.
    """
    # ایجاد و ذخیره آیتم در دیتابیس با استفاده از تابع CRUD
    item = await crud_item.create(db, obj_in=item_in)
    return item


# ------------------- مسیر برای دریافت یک آیتم خاص -------------------
@router.get("/{item_id}", response_model=ItemInDB)
async def read_item_by_id(
    item_id: int,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    دریافت یک آیتم خاص با استفاده از ID.
    """
    item = await crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


# ------------------- مسیر برای به‌روزرسانی آیتم -------------------
@router.put("/{item_id}", response_model=ItemInDB)
async def update_item(
    *,
    item_id: int,
    item_in: ItemUpdate,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    به‌روزرسانی اطلاعات یک آیتم.
    """
    item = await crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )
    
    # به‌روزرسانی و ذخیره تغییرات
    item = await crud_item.update(db, db_obj=item, obj_in=item_in)
    return item


# ------------------- مسیر برای حذف آیتم -------------------
@router.delete("/{item_id}", response_model=ItemInDB)
async def delete_item(
    *,
    item_id: int,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    حذف یک آیتم.
    """
    item = await crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # حذف آیتم
    item = await crud_item.remove(db, id=item_id)
    return item
