from fastapi import APIRouter

# وارد کردن روترهای فرعی (که هنوز آنها را نساخته‌ایم)
from backend.api.api_v1.endpoints import users, login, items 

# ایجاد روتر اصلی برای نسخه 1 API
api_router = APIRouter()

# ----------------------------------------------------
# اتصال روترهای فرعی به روتر اصلی
# ----------------------------------------------------

# 1. روتر احراز هویت (Login and Token Generation)
# پیشوند: /api/v1/login
api_router.include_router(login.router, prefix="/login", tags=["login"])

# 2. روتر کاربران (User Management)
# پیشوند: /api/v1/users
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 3. روتر آیتم‌ها (Item Management)
# پیشوند: /api/v1/items
api_router.include_router(items.router, prefix="/items", tags=["items"])

# توجه: روترهای login و items هنوز تعریف نشده‌اند. 
# در مراحل بعدی آن‌ها را خواهیم ساخت.
