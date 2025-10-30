from fastapi import APIRouter

# وارد کردن روترهای کاربران و آیتم‌ها که قبلاً تعریف کرده‌ایم
from backend.api.api_v1.endpoints import users, items

# ایجاد روتر اصلی API نسخه 1
api_router = APIRouter()

# ------------------- اتصال روترها -------------------

# اتصال روتر کاربران به مسیر اصلی "/users"
# تگ "users" در مستندات Swagger/OpenAPI استفاده می‌شود.
api_router.include_router(users.router, prefix="/users", tags=["users"])

# اتصال روتر آیتم‌ها به مسیر اصلی "/items"
# تگ "items" در مستندات Swagger/OpenAPI استفاده می‌شود.
api_router.include_router(items.router, prefix="/items", tags=["items"])

# در آینده، روترهای اضافی مانند Auth، Health Check و... می‌توانند به همین ترتیب اضافه شوند.

# مثال:
# from backend.api.api_v1.endpoints import login
# api_router.include_router(login.router, tags=["login"])
