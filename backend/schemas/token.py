from pydantic import BaseModel

# ----------------------------------------------------------------------
# کلاس‌های پایه برای توکن
# ----------------------------------------------------------------------

# Token: شمای اصلی که برای پاسخ API پس از احراز هویت موفق استفاده می‌شود.
class Token(BaseModel):
    # توکن دسترسی (Access Token) که کلاینت برای درخواست‌های محافظت شده استفاده می‌کند.
    access_token: str
    
    # نوع توکن، که معمولاً "bearer" است.
    token_type: str = "bearer"
    
    # Optional: اضافه کردن یک Refresh Token در صورت نیاز به مکانیزم طولانی‌تر
    # refresh_token: Optional[str] = None

# TokenPayload: شمای داده‌هایی که داخل خود توکن JWT رمزگذاری می‌شوند.
# این شامل شناسه کاربری (sub) و تاریخ انقضا (exp) است.
class TokenPayload(BaseModel):
    # sub (Subject): معمولاً شناسه کاربری (user_id) را نگه می‌دارد.
    sub: Optional[int] = None
    
    # exp (Expiration Time): زمان انقضای توکن (به صورت اختیاری برای برخی JWT ها)
    exp: Optional[int] = None
    
    # Optional: اضافه کردن نقش یا Scope کاربر (مثلاً 'admin' یا 'user')
    # scope: Optional[str] = None

    class Config:
        # Pydantic v2
        from_attributes = True 
