# 🧠 ViraAI.io — پلتفرم هوش مصنوعی مولد

این مخزن شامل کد کامل پروژه ViraAI است که شامل بک‌اند (FastAPI) و فرانت‌اند (Next.js/React) می‌شود.

## 🚀 ساختار پروژه

/viraai/ ├── frontend/                 # Next.js 14 + TailwindCSS ├── backend/                  # FastAPI + PostgreSQL + AI Integration ├── docker-compose.yml        # مدیریت سرویس‌ها (Backend, Frontend, Postgres) ├── requirements.txt          # وابستگی‌های پایتون ├── .env.example              # متغیرهای محیطی └── README.md


## ⚙️ شروع سریع (تست لوکال)

1.  فایل `.env.example` را کپی کرده و به `.env` تغییر نام دهید و متغیرها را پر کنید.
2.  با استفاده از Docker Compose، تمامی سرویس‌ها (Backend و Postgres) را راه‌اندازی کنید:
    ```bash
    docker-compose up --build -d
    ```
3.  **دسترسی‌ها:**
    * **FastAPI Backend (API):** http://localhost:8000
    * **FastAPI Docs (Swagger):** http://localhost:8000/docs
    * **Next.js Frontend:** http://localhost:3000
