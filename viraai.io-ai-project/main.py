# این فایل برای تست عملکرد صحیح API هوش مصنوعی در app.py ساخته شده است.
# این تستر یک درخواست POST به سرور FastAPI در حال اجرا می‌فرستد.

import requests
import os
import json

# آدرس لوکال هاست (سرور آزمایشی که قرار است در ادامه اجرا کنیم)
# نکته مهم: در محیط سرور (VPS)، برای اتصال لوکال از 0.0.0.0 استفاده می‌کنیم

API_ENDPOINT = "http://localhost:8000/answer"
# سوالی که برای مدل هوش مصنوعی ارسال می‌کنیم
TEST_QUESTION = "Write a short, engaging sentence about the future of space exploration."

def run_test():
    """تابع اجرای تست اتصال به API."""
    print("--- شروع تست اتصال به API هوش مصنوعی ---")
    print(f"سوال آزمایشی: {TEST_QUESTION}")

    try:
        # ارسال درخواست POST به API
        # سرور uvicorn باید در ترمینال دیگری در حال اجرا باشد.
        response = requests.post(API_ENDPOINT, json={"question": TEST_QUESTION}, timeout=20)

        # بررسی کد وضعیت HTTP
        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "پاسخ متنی در خروجی JSON یافت نشد.")

            print("\n✅ اتصال موفقیت‌آمیز بود! (کد 200)")
            print(f"پاسخ هوش مصنوعی: {answer}")

        elif response.status_code == 500:
            # خطای 500 معمولاً به دلیل مشکل در توکن یا مدل است
            try:
                error_detail = response.json().get("detail", "خطای داخلی ناشناخته.")
            except json.JSONDecodeError:
                error_detail = response.text
                
            print("\n❌ خطای سرور داخلی (کد 500)")
            print(f"جزئیات خطا: {error_detail}")

            # اگر توکن درست نباشد، این خطا نمایش داده می‌شود
            if "HF_API_TOKEN" in error_detail or "Authorization" in error_detail:
                print("🛑 مشکل: توکن Hugging Face (HF_API_TOKEN) در فایل .env لود نشده یا اشتباه است.")

        else:
            # سایر خطاها (مثل 404 که قبلاً داشتیم)
            print(f"\n⚠️ خطای غیرمنتظره (کد {response.status_code})")
            print(f"جزئیات پاسخ: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n🛑 خطای اتصال: سرور FastAPI در حال اجرا نیست.")
        print(f"لطفاً مطمئن شوید دستور 'uvicorn app:app --host 0.0.0.0 --port 8000 --reload' در ترمینال دیگری فعال است.")
    except Exception as e:
        print(f"\n❌ خطای عمومی در اجرای تست: {e}")

    print("\n--- پایان تست ---")

if __name__ == "__main__":
    run_test()
