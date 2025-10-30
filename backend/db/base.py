# این فایل به عنوان یک "نقطه مرکزی" برای وارد کردن (import) 
# تمام اجزای مرتبط با مدل‌های دیتابیس (SQLAlchemy ORM) عمل می‌کند.
# این کار برای اطمینان از اینکه Base کلاس والد، از وجود تمام مدل‌های فرزند آگاه است، ضروری است 
# و به ابزارهای Migration (مانند Alembic) کمک می‌کند تا جداول مورد نیاز را شناسایی کنند.

# 1. وارد کردن کلاس پایه اصلی (Base Class)
from .base_class import Base 

# 2. وارد کردن تمامی مدل‌های SQLAlchemy تعریف شده:
# هر مدلی که تعریف می‌شود، باید در اینجا import گردد.

# وارد کردن مدل User که در backend/models/user.py تعریف شده است.
from backend.models.user import User  

# وارد کردن مدل Item که در backend/models/item.py تعریف شده است.
from backend.models.item import Item 
