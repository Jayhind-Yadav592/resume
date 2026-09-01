# Production Deployment Runbook — ResumeForge AI

This guide covers production deployment on **Render** and **Railway**.

---

## 1. Environment Variables Checklist

Ensure the following environment variables are set in your platform dashboard:

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Strong Django secret key | `generate-a-cryptographically-random-string` |
| `ALLOWED_HOSTS` | Comma-separated allowed host domains | `resumeforge.onrender.com,yourdomain.com` |
| `DATABASE_URL` | Managed PostgreSQL connection URI | `postgresql://user:pass@host:5432/dbname` |
| `CELERY_BROKER_URL` | Redis URI for Celery task queuing | `redis://default:pass@redis-host:6379/0` |
| `CELERY_RESULT_BACKEND` | Redis URI for Celery results | `redis://default:pass@redis-host:6379/0` |
| `CELERY_TASK_ALWAYS_EAGER` | Run Celery tasks synchronously (for dev only) | `False` |
| `GROQ_API_KEY` | API Key from Groq Cloud | `gsk_...` |
| `GROQ_MODEL` | AI model to execute analysis & interviews | `llama-3.3-70b-versatile` |
| `RAZORPAY_KEY_ID` | Razorpay Key ID | `rzp_live_...` |
| `RAZORPAY_KEY_SECRET` | Razorpay Key Secret | `...` |
| `RAZORPAY_WEBHOOK_SECRET` | Razorpay Webhook Secret | `...` |
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origins | `https://resumeforge.ai,http://localhost:3000` |

---

## 2. Deploying on Render

### Step A: Provision Managed Databases
1. Create a **PostgreSQL** instance on Render (Name: `resumeforge-db`). Copy the *Internal Database URL*.
2. Create a **Redis** instance on Render (Name: `resumeforge-redis`). Copy the *Internal Redis URL*.

### Step B: Create Web Service (Django + Gunicorn)
1. In Render Dashboard, click **New +** -> **Web Service**.
2. Connect your Git repository.
3. Configure the service:
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install "setuptools<70" && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**:
     ```bash
     gunicorn resumeforge.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
     ```
4. Under **Advanced Settings**, add the environment variables listed above (setting `DATABASE_URL` and `CELERY_BROKER_URL` from Step A).

### Step C: Create Background Worker (Celery Worker)
1. In Render Dashboard, click **New +** -> **Background Worker**.
2. Connect the same repository.
3. Configure the worker:
   - **Build Command**: `pip install "setuptools<70" && pip install -r requirements.txt`
   - **Start Command**:
     ```bash
     celery -A resumeforge worker -l INFO --concurrency=4
     ```
4. Attach the exact same environment variables.

---

## 3. Deploying on Railway

1. Click **New Project** -> **Deploy from GitHub repo**.
2. Add **PostgreSQL** and **Redis** plugins from the Railway architecture canvas.
3. In your Web service settings:
   - **Build Command**: `pip install "setuptools<70" && pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `python manage.py migrate && gunicorn resumeforge.wsgi:application --bind 0.0.0.0:$PORT --workers 3`
4. Add a secondary service in the same project for Celery:
   - **Start Command**: `celery -A resumeforge worker -l INFO`
5. Railway will automatically link `${{Postgres.DATABASE_URL}}` and `${{Redis.REDIS_URL}}`.

---

## 4. Setting up Razorpay Webhook in Production

1. Navigate to **Razorpay Dashboard** -> **Settings** -> **Webhooks**.
2. Add Webhook URL: `https://<YOUR-DOMAIN>/api/v1/billing/webhook/`
3. Enter your `RAZORPAY_WEBHOOK_SECRET`.
4. Select active events:
   - `payment.captured`
   - `order.paid`
   - `subscription.activated`
   - `subscription.cancelled`
