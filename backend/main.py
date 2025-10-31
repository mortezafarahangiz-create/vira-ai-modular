from fastapi import FastAPI
from datetime import datetime

# ایجاد یک نمونه از برنامه FastAPI
# عنوان و توضیحات برای مستندات Swagger/Redoc استفاده می‌شود.
app = FastAPI(
    title="VIRA-AI Modular Backend",
    description="سرویس‌های ماژولار هوش مصنوعی و مدیریت داده.",
    version="1.0.0"
)

# ----------------------------------------------------------------------
# 1. مسیر اصلی / Health Check
# ----------------------------------------------------------------------
@app.get("/", tags=["سیستم"], summary="بررسی سلامت برنامه")
async def root():
    """
    بررسی می‌کند که آیا سرویس در حال اجرا است یا خیر.
    این مسیر به‌عنوان Health Check برای محیط‌های استقرار استفاده می‌شود.
    """
    return {
        "status": "online",
        "service": "VIRA-AI Backend",
        "timestamp": datetime.now().isoformat()
    }

# ----------------------------------------------------------------------
# 2. ماژول‌های آینده‌ی هوش مصنوعی (Future AI Modules)
# ----------------------------------------------------------------------

# در آینده، ماژول‌های هوش مصنوعی را در اینجا تعریف یا ایمپورت خواهیم کرد:
# @app.post("/ai/process-image")
# async def process_image():
#     # منطق پردازش تصویر
#     pass

# @app.get("/data/user-profiles")
# async def get_user_profiles():
#     # منطق مدیریت پایگاه داده
#     pass
