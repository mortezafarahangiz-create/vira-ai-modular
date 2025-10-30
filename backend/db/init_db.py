from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.config import settings
from backend.crud.crud_user import user as crud_user
from backend.schemas.user import UserCreate

# تابعی برای مقداردهی اولیه دیتابیس
async def init_db(db: AsyncSession) -> None:
    """
    اطمینان از وجود کاربر مدیر ارشد (Superuser) در دیتابیس.
    اگر کاربری با ایمیل مدیر ارشد وجود نداشته باشد، آن را ایجاد می‌کند.
    """
    
    # تلاش برای پیدا کردن کاربر مدیر ارشد با ایمیل تعریف شده در تنظیمات
    # ما از متد get_by_email که در CRUD نوشتیم استفاده می‌کنیم.
    superuser = await crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)

    if not superuser:
        # اگر مدیر ارشد وجود نداشت، شیء UserCreate را برای ایجاد آن آماده می‌کنیم.
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            full_name="Superuser Admin"  # یک نام پیش‌فرض برای سادگی
        )
        
        # ایجاد کاربر جدید با استفاده از متد create در CRUD
        try:
            superuser = await crud_user.create(db, obj_in=user_in)
            print(f"--- کاربر مدیر ارشد با ایمیل {settings.FIRST_SUPERUSER_EMAIL} ایجاد شد. ---")
        except Exception as e:
            # اگر خطایی در حین ایجاد رخ داد (مثلاً مشکل اتصال به دیتابیس)، آن را گزارش می‌کنیم.
            print(f"خطا در ایجاد کاربر مدیر ارشد: {e}")
