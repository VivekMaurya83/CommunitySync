<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Groq LLM](https://img.shields.io/badge/Groq_LLM-FF6B35?style=for-the-badge&logo=meta&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)
![OpenCage](https://img.shields.io/badge/OpenCage-2ECC71?style=for-the-badge&logo=openstreetmap&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Twilio](https://img.shields.io/badge/Twilio-F22F46?style=for-the-badge&logo=twilio&logoColor=white)

<br/><br/>

# 🌍 CommunitySync

### Smart Resource Allocation & Volunteer Coordination System

*An AI-powered, full-stack disaster response platform that transforms unstructured crisis reports into prioritized, actionable assignments — matching the right volunteer to the right need, instantly. Powered by a hybrid NLP pipeline combining Groq LLM + rule-based extraction + OpenCage geocoding.*

<br/>

**Groq LLM + Rule-Based NLP** · **Volunteer Approval Workflow** · **OpenCage Geocoding** · **Task Lifecycle Tracking** · **Role-Based Access** · **Auto Notifications** · **Workload-Aware Matching** · **Interactive Audit Trails** · **Geospatial Intelligence** · **Gamification**

</div>

---

## 📑 Table of Contents

- [✨ Core Features](#-core-features)
- [🧠 Hybrid NLP Pipeline](#-hybrid-nlp-pipeline)
- [🔄 Task Lifecycle](#-task-lifecycle)
- [🛠 Tech Stack](#-tech-stack)
- [🏗 System Architecture](#-system-architecture)
- [📊 Role-Specific Features](#-role-specific-features)
- [📡 API Endpoints](#-api-endpoints)
- [🚀 Setup & Installation](#-setup--installation)
- [🔐 Environment Variables](#-environment-variables)
- [🌐 Production Deployment](#-production-deployment-guide) (Render + Neon PostgreSQL)
- [🗺 Usage Flow](#-usage-flow)
- [📁 Project Architecture](#-project-architecture)
- [🐛 Troubleshooting](#-troubleshooting)
- [🔭 Future Scope](#-future-scope)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

> **📖 Full Deployment Guide:** See [DEPLOYMENT.md](DEPLOYMENT.md) for complete step-by-step instructions on hosting with Render + Neon PostgreSQL

---

---

## ✨ Core Features at a Glance

| Feature | Description |
|---------|-------------|
| 🧠 **Hybrid NLP Pipeline** | 10-stage AI extraction: Preprocess → Summarize → Rule-based → Groq LLM → Geocoding → Scoring |
| 🛡️ **Gemini Pre-Validation** | Google Gemini 2.5 Flash validates reports before processing, reducing spam & false entries |
| 📄 **Multi-Format Upload** | PDF, DOCX, TXT with automatic text extraction & OCR preprocessing |
| 📍 **Smart Geocoding** | 3-tier location extraction with OpenCage API + LRU cache (256 entries) |
| 🤖 **Workload-Aware Matching** | Skill similarity (50%) + GPS proximity (35%) + ratings (15%) + workload penalty |
| 🔄 **5-Stage Task Lifecycle** | Pending → Assigned → Accepted → In Progress → Completed |
| ✅ **Volunteer Approval** | Admin review gate with auto email/WhatsApp onboarding |
| 🕒 **Audit Trails** | Complete task history with who, what, when, and resource tracking |
| 🗺️ **Geospatial Intelligence** | Interactive map with auto-clustering & heatmap visualization |
| 🏆 **Gamification** | Performance points, leaderboards, and achievement tracking |
| 📬 **Auto Notifications** | Email & WhatsApp alerts for assignments and updates |
| 🔐 **JWT + RBAC** | Role-based access control with account status gating |

---

### 🧠 **Hybrid NLP Pipeline Details**

**10-Stage Processing:**
1. **Preprocess** — 40+ slang normalization (khana→food, paani→water, etc.)
2. **Summarize** — Extract top 2-4 sentences by disaster-keyword density
3. **Rule-Based** — Multi-category detection (8 categories) + urgency + people count
4. **Groq LLM** — Async extraction via `llama-3.1-8b-instant` (15s timeout fallback)
5. **Merge** — Combine LLM + rules with confidence scoring (90/65/40)
6. **Geocode** — Convert locations to lat/lon with caching
7. **Score** — Priority calculation (0–100 scale)
8. **Match** — Workload-aware volunteer assignment
9. **Notify** — Email + WhatsApp dispatch
10. **Track** — Audit trail logging

**Graceful Degradation:** If Groq unavailable → falls back to rule-based extraction

---

### 🛡️ **Gemini Pre-Validation Layer (NEW)**

Ensures **only authentic, actionable disaster reports** are processed:
- **Asynchronous validation** via Google Gemini 2.5 Flash in JSON mode
- **Pre-pipeline gate** — validates before entering main NLP pipeline
- **Reduces spam** — Drastically cuts database pollution from false/duplicate entries
- **Fail-open fallback** — If Gemini unavailable, system allows reports to proceed

---

### 📍 **Location & Geocoding**

| Tier | Method |
|------|--------|
| 1️⃣ Primary | Groq LLM extraction |
| 2️⃣ Secondary | spaCy NER (GPE/LOC entities) |
| 3️⃣ Fallback | 20+ static city coordinates |

- **OpenCage API** with LRU cache prevents repeated API calls
- **Haversine distance** for GPS-based volunteer matching

---

### 🤖 **Smart Volunteer Matching**

**Composite Score:** 
- Jaccard Skill Similarity: **50%**
- Haversine Proximity: **35%**
- Performance Rating: **15%**
- Workload Penalty: Applied per active task

**Gate:** Only **approved** volunteers eligible

---

### 🔄 **Task Lifecycle & Volunteer Actions**

```
Pending ──[Admin Match]──> Assigned ──[Volunteer Accept]──> Accepted
                                                                ↓
                                                        In Progress ──> Completed
                                                        (with feedback)
```

- Volunteers must **explicitly accept** before work begins
- Real-time status tracking with animated badges
- 1-5 star ratings + comments on completion

---

### ✅ **Volunteer Approval Workflow**

| Step | Action | Notification |
|------|--------|--------------|
| 1. Signup | Volunteer registers | Status: `pending` |
| 2. Review | Admin approves/rejects | N/A |
| 3. Onboard | System sends credentials | Welcome Email + WhatsApp |
| 4. Access | Volunteer can now login | Auto-approved |

---

### 🕒 **Interactive Audit Trails**

Track every change:
- Who/when/what actions occurred
- Resource allocations & status transitions
- Volunteer feedback & ratings
- Complete task history

---

### 🗺️ **Geospatial Intelligence**

- **OpenStreetMap + React-Leaflet** integration
- **Auto-clustering** of crisis markers
- **Dynamic heatmap** showing high-priority zones
- **Real-time tracking** (future scope)

---

### 📬 **Notification System**

| Channel | Use Case |
|---------|----------|
| 📧 **Email** | Assignment alerts, welcome, password resets |
| 💬 **WhatsApp** | Real-time assignment notifications with details |

---

### 🏆 **Gamification**

- Performance points per completed task
- Leaderboard rankings
- Achievement history tracking
- Cross-org collaboration bonuses

---

### 🔐 **Security & Access Control**

- **JWT authentication** with configurable expiry
- **Account status gating** (pending/approved/rejected)
- **Frontend RBAC** via `<ProtectedRoute>` wrapper
- **URL hacking protection** → redirects to `/unauthorized`

---

## 🔄 Task Lifecycle

```
  ┌──────────┐    Admin assigns    ┌──────────┐   Volunteer accepts  ┌──────────┐
  │ PENDING  │ ─────────────────▶ │ ASSIGNED │ ─────────────────▶  │ ACCEPTED │
  └──────────┘                    └──────────┘                      └────┬─────┘
                                                                         │ Volunteer starts
                                                                         ▼
                                                                   ┌───────────┐
                                                                   │ IN PROGRESS│
                                                                   └─────┬──────┘
                                                                         │ Volunteer completes
                                                                         ▼
                                                                   ┌───────────┐
                                                                   │ COMPLETED  │
                                                                   └───────────┘
```

Each transition is validated server-side. Invalid transitions (e.g., jumping from `pending` to `in_progress`) return a `400 Bad Request`.

---

## 🛠 Tech Stack

| Layer | Tech |
|-------|------|
| **Frontend** | React 18, Tailwind CSS, Axios, React Router, Lucide Icons |
| **Backend** | FastAPI, Python 3.10, SQLAlchemy 2.0, Pydantic v2 |
| **Database** | PostgreSQL, pg8000 (pure Python driver) |
| **AI/NLP** | Groq LLM (llama-3.1-8b-instant), spaCy, Rule-based extraction |
| **Validation** | Google Gemini 2.5 Flash (pre-validation gate) |
| **Geocoding** | OpenCage API + LRU cache (256 entries) |
| **Auth** | JWT (python-jose), bcrypt (passlib) |
| **Email** | FastAPI-Mail (SMTP) |
| **SMS/WhatsApp** | Twilio API |
| **Testing** | Pytest, httpx, Faker |

---

## 🏗 System Architecture

**10-Stage AI Pipeline:**

```
Report Input
     ↓
[Gemini Pre-Validation] ← NEW: Reduces spam & false entries
     ↓
Preprocess (40+ slang mappings)
     ↓
Summarize (disaster keyword scoring)
     ↓
Rule-Based Extract (8 categories, urgency, people count)
     ↓
Groq LLM Extract (llama-3.1-8b-instant, 15s async timeout)
     ↓
Merge Results (LLM preferred, rule fallback)
     ↓
Geocode Location (OpenCage + 256-entry LRU cache)
     ↓
Score Priority (0-100 scale)
     ↓
Workload-Aware Match (Skill 50% + Distance 35% + Rating 15%)
     ↓
Notify Volunteer (Email + WhatsApp)
     ↓
Task Lifecycle Tracking (Pending → Assigned → Accepted → In Progress → Completed)
```

**Confidence Scores:**
- **90** = LLM successful extraction
- **65** = Rule-based with category matches
- **40** = Fallback only

---

## 📊 Role-Specific Dashboards

| Role | Key Features |
|------|-------------|
| **👑 Admin** | Full analytics (5-state lifecycle), category/urgency charts, volunteer metrics, NGO management, global audit trail, match/unassign controls |
| **🏢 NGO** | Needs overview, progress tracking, resource contribution, pool requests, volunteer dispatch, performance charts |
| **👤 Volunteer** | My Tasks, action buttons (Accept/Start/Complete), feedback submission, skills management, leaderboard, achievement history |

---

## 📡 API Endpoints

### 🔑 Auth & Profile
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | `POST` | Register (volunteers start `pending`) |
| `/auth/login` | `POST` | Authenticate → JWT (blocks unapproved) |
| `/auth/me` | `GET` | Get profile |
| `/auth/me` | `PUT` | Update profile |
| `/auth/forgot-password` | `POST` | Request reset email |
| `/auth/reset-password` | `POST` | Reset with token |

### 📋 Needs & Reporting
| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/api/upload-report` | `POST` | Auth | Text → Gemini validation → NLP pipeline |
| `/api/upload-file` | `POST` | Auth | PDF/DOCX/TXT → pipeline |
| `/api/needs` | `GET` | Auth | List all needs (filter by status/category) |
| `/api/needs/{id}` | `GET` | Auth | Get single need |

### 🤝 Matching & Tasks
| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/api/match/{need_id}` | `POST` | Admin/NGO | Auto-match approved volunteer |
| `/api/match/{need_id}/manual` | `POST` | Admin | Manual assign |
| `/api/match/{need_id}/unassign` | `POST` | Admin | Remove assignment |
| `/api/task/my-tasks` | `GET` | Volunteer | Get assigned tasks |
| `/api/task/{need_id}/accept` | `POST` | Volunteer | Accept → `accepted` |
| `/api/task/{need_id}/start` | `POST` | Volunteer | Start → `in_progress` |
| `/api/task/{need_id}/complete` | `POST` | Volunteer | Complete + rating → `completed` |

### 👥 Volunteer Management
| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/api/volunteers` | `GET` | Admin/NGO | List approved volunteers |
| `/api/volunteers/pending` | `GET` | Admin | List pending approvals |
| `/api/volunteer/{id}/approve` | `POST` | Admin | Approve (triggers welcome email + WhatsApp) |
| `/api/volunteer/{id}/reject` | `POST` | Admin | Reject |
| `/api/volunteer` | `POST` | Admin | Create (auto-approved) |
| `/api/volunteer/{id}` | `PUT` | Admin | Update |
| `/api/volunteer/{id}` | `DELETE` | Admin | Delete |

### 📊 Analytics
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard` | `GET` | Aggregated stats (5 lifecycle states) |

---

## 🚀 Setup & Installation

### Prerequisites
- **Python 3.10+** | **Node.js 18+** | **PostgreSQL 14+** | **C++ Build Tools** (Windows)

### Quick Start

**1. Clone & Setup Database**
```bash
git clone https://github.com/your-username/CommunitySync.git
cd CommunitySync

# Create database
psql -U postgres -c "CREATE DATABASE community_sync3;"
```

**2. Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create .env file (see Environment Variables section)
python scripts/setup_db.py
python add_admin.py
uvicorn main:app --reload
```

**3. Frontend Setup**
```bash
cd frontend
npm install --legacy-peer-deps
# Create .env file (see Environment Variables section)
npm start
```

**Backend:** http://127.0.0.1:8000 | **Docs:** http://127.0.0.1:8000/docs  
**Frontend:** http://localhost:3000

---

## 🔐 Environment Variables

### Backend `.env`
```env
# Database
DATABASE_URL=postgresql+pg8000://sync_admin:password@localhost:5432/community_sync3

# App Config
APP_TITLE=Smart Resource Allocation API
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]

# JWT
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=1440

# Email (Gmail + App Password)
EMAIL_USERNAME=your.email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE=+14155238886

# LLMs & APIs
GROQ_API_KEY=gsk_your_groq_key
OPENCAGE_API_KEY=your_opencage_key
```

### Frontend `.env`
```env
REACT_APP_API_URL=http://127.0.0.1:8000
```

**Get Free Keys:**
- 🤖 Groq: [console.groq.com](https://console.groq.com)
- 🗺️ OpenCage: [opencagedata.com](https://opencagedata.com/users/sign_up)
- 📧 Gmail: Use [App Password](https://support.google.com/accounts/answer/185833)
- 💬 Twilio: [Sandbox setup](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)

---

## 🗺 Usage Flow

### Upload & Process Crisis Report
```
Upload (Text/PDF) ─→ Gemini Validation ─→ Preprocess + Summarize
     ↓
Rule-Based Extract ─→ Groq LLM Extract ─→ Merge (LLM preferred)
     ↓
Geocode Location ─→ Priority Score (0-100) ─→ Dashboard (Pending)
     ↓
Admin Auto-Match ─→ Workload-Aware Algorithm ─→ Volunteer Assignment
     ↓
Email + WhatsApp Notification ─→ Status: Assigned
```

### Volunteer Task Management
```
Accept Assignment ─→ Accept (Status: Accepted) ─→ Start Work (In Progress)
     ↓
Complete Task ─→ Submit Rating + Feedback (1-5 stars) ─→ Status: Completed
     ↓
Performance Points Earned ─→ Leaderboard Updated
```

### Role-Based Actions
| Admin | NGO | Volunteer |
|:-----:|:---:|:---------:|
| ✅ Upload | ✅ Upload | ✅ Upload |
| ✅ View All Needs | ✅ View Needs | ❌ View Only My Tasks |
| ✅ Auto/Manual Match | ✅ Auto Match | ❌ Can't Match |
| ✅ Approve Volunteers | ❌ No Access | ❌ No Access |
| ❌ Accept Tasks | ❌ Accept Tasks | ✅ Accept/Complete |

---

## 📁 Project Architecture

```
CommunitySync/
├── backend/
│   ├── models/          # ORM models (User, Need, Volunteer, Task, Resource)
│   ├── routes/          # API endpoints (auth, needs, matching, tasks)
│   ├── services/        # Business logic (NLP, geocoding, matching, notifications)
│   ├── schemas/         # Pydantic validation schemas
│   ├── scripts/         # DB setup & migrations
│   ├── tests/           # Pytest test suites
│   ├── main.py          # FastAPI entry point
│   └── requirements.txt # Dependencies
│
├── frontend/
│   ├── src/
│   │   ├── pages/       # Dashboard, Needs, Volunteers, Login, etc.
│   │   ├── components/  # TopBar, Sidebar, TaskPanel, ProtectedRoute
│   │   ├── services/    # API wrappers (axios)
│   │   └── utils/       # Auth helpers, formatters
│   ├── package.json
│   └── tailwind.config.js
│
└── README.md
```

**Key Services:**
- `nlp_service.py` — Groq + rule-based extraction, confidence scoring
- `matching_service.py` — Workload-aware volunteer assignment
- `geocoding_service.py` — OpenCage + caching + fallback cities
- `email_service.py` — Assignment & welcome notifications
- `whatsapp_service.py` — Twilio WhatsApp alerts
- `validation_service.py` — Gemini pre-validation gate

## 🛠 Running the System

### Terminal 1: Backend
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
uvicorn main:app --reload
```
→ **http://127.0.0.1:8000** | Docs: **http://127.0.0.1:8000/docs**

### Terminal 2: Frontend
```bash
cd frontend
npm start
```
→ **http://localhost:3000**

---

## � Production Deployment Guide

Deploy on **Render** (Frontend + Backend) + **Neon PostgreSQL** (Database)

### 1️⃣ Neon PostgreSQL Setup

**Create Free Database:**
1. Go to [neon.tech](https://neon.tech) → Sign up
2. Create new project → Copy `DATABASE_URL`:
   ```
   postgresql://user:password@ep-xxx.us-east-1.neon.tech/community_sync?sslmode=require
   ```
3. Store this — you'll need it for Render backend

**Important:** Neon uses SSL by default. Your `DATABASE_URL` must include `?sslmode=require`

---

### 2️⃣ Backend on Render (FastAPI + EasyOCR)

**Create Web Service:**
1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo
3. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `communitysync-backend` |
| **Environment** | `Python` |
| **Region** | US (or closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r backend/requirements.txt && python -m spacy download en_core_web_sm` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free (for testing) or Starter+ (production) |

**Set Environment Variables in Render Dashboard:**
```env
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.neon.tech/community_sync?sslmode=require

APP_TITLE=CommunitySync
DEBUG=False
CORS_ORIGINS=["https://communitysync-frontend.onrender.com"]

JWT_SECRET=your-production-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=1440

EMAIL_USERNAME=your.email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587

TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE=+14155238886

GROQ_API_KEY=gsk_your_groq_key
OPENCAGE_API_KEY=your_opencage_key
GEMINI_API_KEY=your_gemini_api_key
```

**After Deployment:**
- ✅ Backend runs at: `https://communitysync-backend.onrender.com`
- ✅ API docs: `https://communitysync-backend.onrender.com/docs`

---

### 3️⃣ Frontend on Render (React Static Site)

**Build Production Bundle:**
```bash
cd frontend
npm run build
```
This creates `/frontend/build` folder

**Create Static Site:**
1. Go to [render.com](https://render.com) → New → Static Site
2. Connect your GitHub repo
3. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `communitysync-frontend` |
| **Branch** | `main` |
| **Build Command** | `cd frontend && npm install --legacy-peer-deps && npm run build` |
| **Publish Directory** | `frontend/build` |

**Add Environment Variable:**
```env
REACT_APP_API_URL=https://communitysync-backend.onrender.com
```

**After Deployment:**
- ✅ Frontend runs at: `https://communitysync-frontend.onrender.com`
- ✅ Routes automatically fallback to `index.html` for React Router

---

### 4️⃣ Database Migrations on Neon

After backend deploys, initialize database:

**Option A: Use Render Console**
```bash
cd backend && python scripts/setup_db.py
```

**Option B: Manual via psql**
```bash
psql postgresql://user:password@ep-xxx.us-east-1.neon.tech/community_sync

# Then run:
\i scripts/setup_db.sql
```

**Option C: Python Script (Recommended)**
```python
# scripts/init_production_db.py
from database import engine
from models import *

# Create all tables
metadata.create_all(bind=engine)
print("✅ Database initialized")
```

Run via Render webhook or manual trigger

---

### 5️⃣ Code Changes for Production

**Backend:**

**`backend/main.py`** — Update CORS:
```python
from fastapi.middleware.cors import CORSMiddleware

# Production CORS config
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    '["https://communitysync-frontend.onrender.com"]'
)

origins = json.loads(CORS_ORIGINS) if isinstance(CORS_ORIGINS, str) else CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**`backend/config.py`** — Production settings:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://localhost/community_sync"
    )
    # Ensure SSL for Neon
    if "neon.tech" in DATABASE_URL:
        if "?" not in DATABASE_URL:
            DATABASE_URL += "?sslmode=require"
    
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # ... other settings

settings = Settings()
```

**Frontend:**

**`frontend/.env.production`** — Create this file:
```env
REACT_APP_API_URL=https://communitysync-backend.onrender.com
```

**`frontend/src/services/api.js`** — Update base URL:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;
```

---

### 6️⃣ Critical Checklist ✅

| Item | Status | Notes |
|------|--------|-------|
| Neon database created | ⬜ | Copy `DATABASE_URL` with `?sslmode=require` |
| Render backend service created | ⬜ | Set all env vars, use `Start Command` from step 2 |
| Render frontend site created | ⬜ | Publish directory must be `frontend/build` |
| Database migrations run | ⬜ | Creates tables & enums |
| Admin account created | ⬜ | Run `python add_admin.py` via backend service |
| CORS configured correctly | ⬜ | Frontend URL matches `CORS_ORIGINS` |
| All API keys set | ⬜ | Groq, Gemini, OpenCage, Twilio, Gmail |
| `build` folder committed | ⬜ | Only needed if not using Render's build command |

---

### 7️⃣ Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| `SSL connection error` | Add `?sslmode=require` to `DATABASE_URL` |
| `CORS 403` | Check `CORS_ORIGINS` matches frontend URL |
| `API endpoint not found` | Backend URL in frontend `.env` must be https |
| `Build timeout` | Render free tier slow; use Starter+ ($12/mo) |
| `EasyOCR memory` | Disable OCR for free tier or use Starter+ |
| `Secrets not loading` | Restart service after adding env vars |
| `Database connection failed` | Test connection string via psql locally first |
| `WhatsApp not sending` | Ensure sandbox configured in Twilio Console |

---

### 8️⃣ Cost Breakdown (Monthly)

| Service | Plan | Cost |
|---------|------|------|
| Render Backend | Free | $0 (spins down after 15min inactivity) |
| Render Backend | Starter+ | $12 (always running, recommended) |
| Render Frontend | Free | $0 (static site) |
| Neon Database | Free | $0 (with limits) |
| **Total** | Free Tier | ~$0 (works for MVP) |
| **Total** | Production | ~$12/mo |

---

### 9️⃣ Optional: Custom Domain

1. Buy domain (GoDaddy, Namecheap, etc.)
2. In Render dashboard → Custom Domain
3. Add CNAME records pointing to Render's nameservers
4. SSL certificate auto-generates (free via Render)

Example: `https://communitysync.com`

---

### 🔟 Post-Deployment Verification

1. **Test Backend API:**
   ```bash
   curl https://communitysync-backend.onrender.com/docs
   ```
   Should show Swagger UI ✅

2. **Test Frontend:**
   ```bash
   curl https://communitysync-frontend.onrender.com
   ```
   Should return HTML ✅

3. **Test Database:**
   ```bash
   psql postgresql://user:password@ep-xxx.us-east-1.neon.tech/community_sync
   \dt  # List tables
   ```

4. **Test Login:**
   - Go to frontend URL
   - Login with admin credentials created
   - Should redirect to dashboard ✅

5. **Test Upload:**
   - Upload test crisis report
   - Should process through Gemini + Groq pipeline ✅
   - Check Render backend logs for errors

---

## �🐛 Troubleshooting

| Error | Solution |
|-------|----------|
| `Relation X does not exist` | Run `python scripts/setup_db.py` |
| `Connection Refused` (backend) | Check PostgreSQL running & `DATABASE_URL` correct |
| `Connection Refused` (frontend) | Ensure backend on port 8000 & `.env` configured |
| `Invalid Token` / `403` | Clear cookies or login again |
| `Account pending approval` | Admin must approve volunteer |
| Groq LLM timeout | Fallback to rule-based auto-kicks in |
| Email not sending | Verify Gmail app password in `.env` |
| WhatsApp not delivering | Recipient must opt-in via Twilio Sandbox |
| Geocoding failing | OpenCage key invalid; fallback cities used |
| `Module not found` | Run `pip install -r requirements.txt` or `npm install` |

---

## 🔭 Future Roadmap

| Feature | Description | Impact |
|---------|-------------|--------|
| 🤖 **Predictive Crisis AI** | Ingest weather + geopolitical feeds | Proactive need generation |
| 📍 **Real-Time Tracking** | WebSocket GPS on Leaflet/Mapbox | Live volunteer location |
| 🏢 **Multi-Tenant NGO** | Isolated workspaces + shared pools | Cross-org coordination |
| 📱 **Mobile App** | React Native offline-first | Field operations in low connectivity |
| 📈 **Analytics Dashboards** | Volunteer performance trends | Data-driven insights |
| 🌐 **Multilingual NLP** | Bengali, Tamil, Spanish, Swahili | Regional language support |
| 🔄 **Batch Upload** | Multiple reports with progress | Bulk reporting |
| 🔗 **WhatsApp Commands** | "accept 101" via WhatsApp | Alternative UI |
| 🤝 **Consensus Completion** | Multiple NGO sign-offs | Federated operations |
| 📦 **Smart Inventory** | Auto-dedup & quantity merge | Efficient resource management |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** your feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for communities that need it most.**

⭐ *Star this repo if you found it useful!* ⭐

**[Report Bug](https://github.com/your-username/CommunitySync/issues)** · **[Request Feature](https://github.com/your-username/CommunitySync/issues)**

</div>
