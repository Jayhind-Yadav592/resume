# ResumeForge AI — ATS Resume Scanner & AI Mock Interview SaaS

A production-grade, full-stack SaaS application built with **Django 5.x**, **Django REST Framework (DRF)**, **SimpleJWT**, **Groq AI (Llama-3.3-70b)**, **Celery & Redis**, and **Razorpay**.

Designed following strict Django **MVT (Model-View-Template)** separation with a decoupled **Service Layer** ("thin views, fat services").

---

## 🌟 Key Features

1. **AI ATS Resume Scoring**: Upload PDF resumes and evaluate them against any Job Description using Groq (`llama-3.3-70b-versatile`). Returns overall match percentage, keyword relevance, formatting compliance, missing keywords, and actionable suggestions.
2. **Turn-Based AI Mock Interviews**: Interactive 6-turn conversational interview sessions with role-specific opening questions, conversational memory, instant critique, and end-of-session comprehensive synthesis.
3. **Async Task Processing (Celery & Redis)**: Non-blocking background parsing and AI scoring with pollable status endpoints and Celery Beat scheduled weekly digests for Pro subscribers.
4. **Subscription Tiers & Razorpay**: Integrated Razorpay checkout, cryptographic HMAC-SHA256 signature verification, webhooks, and automatic Pro access management.
5. **Interactive UI & OpenAPI Docs**: Server-rendered public landing & web login pages with instant JWT local storage management, Swagger UI, and ReDoc documentation.

---

## 🏗️ Architecture & App Structure

```
AI Resume/
├── manage.py                     # Django management utility
├── Dockerfile                    # Multi-stage production Dockerfile
├── docker-compose.yml            # Web, DB, Redis, Celery Worker & Beat
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Production & test dependencies
├── DEPLOYMENT.md                 # Render & Railway deployment runbooks
├── resumeforge/                  # Project root package
│   ├── settings.py               # 12-factor configuration via django-environ
│   ├── urls.py                   # Root URL routing (MVT + API + Swagger)
│   ├── celery.py                 # Celery app & Celery Beat schedules
│   ├── wsgi.py                   # Production WSGI application
│   └── asgi.py                   # Production ASGI application
├── core/                         # Landing page, health check, shared utils
├── accounts/                     # Custom User, JWT authentication, permissions
├── resumes/                      # PDF upload, pdfplumber, Groq ATS scoring, Celery tasks
├── interviews/                   # Turn-based mock interview engine & Groq conversational turns
├── billing/                      # Subscription plans, Razorpay orders, signatures & webhooks
├── api/                          # Unified v1 router (/api/v1/) & OpenAPI documentation
├── templates/                    # Server-rendered HTML templates
│   ├── base.html                 # Base layout with Tailwind CSS & icons
│   ├── core/home.html            # Public landing page
│   ├── accounts/login.html       # Web login & registration page
│   └── emails/weekly_summary.html# Pro subscriber email digest template
└── tests/                        # Comprehensive pytest test suite (>=90% coverage)
```

---

## 🚀 Quickstart & Local Development

### 1. Prerequisites
- Python 3.11+
- Redis (optional for development; `CELERY_TASK_ALWAYS_EAGER=True` can be used)
- PostgreSQL or SQLite

### 2. Setup Environment
```bash
# Clone and enter the repository
cd "AI Resume"

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install "setuptools<70"
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

### 3. Run Migrations & Start Server
```bash
# Run database migrations
python manage.py migrate

# Start development server
python manage.py runserver
```
Visit:
- **Landing Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Web Login / Register**: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
- **Interactive Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Automated Tests

Run the complete test suite with coverage reporting:
```bash
pytest --cov=. --cov-report=term-missing
```

---

## 📡 API Reference Overview (`/api/v1/`)

### Authentication (`/api/v1/auth/`)
- `POST /api/v1/auth/register/`: Register a new user account & obtain JWT tokens.
- `POST /api/v1/auth/login/`: Authenticate credentials & retrieve access/refresh tokens.
- `POST /api/v1/auth/refresh/`: Refresh an expired access token.
- `GET  /api/v1/auth/me/`: Retrieve authenticated user profile.

### ATS Resume Scanning (`/api/v1/resumes/`)
- `POST /api/v1/resumes/upload/`: Upload PDF resume & Job Description. Starts async Groq scoring.
- `GET  /api/v1/resumes/scan/{id}/`: Retrieve complete ATS match breakdown.
- `GET  /api/v1/resumes/scan/{id}/status/`: Poll scan progress (`pending`, `processing`, `completed`, `failed`).

### AI Mock Interviews (`/api/v1/interviews/`)
- `POST /api/v1/interviews/start/`: Initialize mock interview session & get Question 1.
- `POST /api/v1/interviews/{session_id}/answer/`: Submit answer, get AI critique, advance to next question or final summary.
- `GET  /api/v1/interviews/{session_id}/`: Retrieve full conversational history and summary.

### Billing & Razorpay (`/api/v1/billing/`)
- `GET  /api/v1/billing/plans/`: List active subscription tiers.
- `GET  /api/v1/billing/my-subscription/`: View active subscription details.
- `POST /api/v1/billing/create-order/`: Create Razorpay payment order.
- `POST /api/v1/billing/verify-payment/`: Verify HMAC signature and activate Pro.
- `POST /api/v1/billing/webhook/`: Razorpay server-to-server webhook endpoint.

---

## 🐳 Docker Deployment

Run the complete stack (PostgreSQL, Redis, Web App, Celery Worker, Celery Beat) using Docker Compose:

```bash
docker-compose up --build
```
