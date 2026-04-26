# Production Configuration for CommunitySync

## 🚀 Deployment Checklist

### Pre-Deployment (Local)
- [ ] Run `npm run build` in frontend
- [ ] Test locally with production build: `npm install -g serve && serve -s frontend/build`
- [ ] All environment variables set in `.env` files
- [ ] Database migrations tested locally
- [ ] No hardcoded credentials in code
- [ ] Git repo is clean and pushed to main branch

### Neon PostgreSQL
- [ ] Account created at neon.tech
- [ ] Database project created
- [ ] Connection string copied: `postgresql://...?sslmode=require`
- [ ] Test connection with psql locally
- [ ] Schema initialized (run setup_db.py)
- [ ] Admin user created

### Render Backend
- [ ] Service created (type: Web Service)
- [ ] Python environment selected
- [ ] Build command set correctly
- [ ] Start command set to: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] ALL environment variables added in Render dashboard
- [ ] Database URL includes `?sslmode=require`
- [ ] Service deployed and running (check status page)
- [ ] Swagger docs accessible at `/docs` endpoint
- [ ] Health check passing

### Render Frontend
- [ ] Service created (type: Static Site)
- [ ] Build command set: `cd frontend && npm install --legacy-peer-deps && npm run build`
- [ ] Publish directory set to: `frontend/build`
- [ ] Environment variable `REACT_APP_API_URL` set
- [ ] Service deployed (check build logs)
- [ ] Site loads in browser (no 404)

### Integration Testing
- [ ] Backend API responding: `curl https://[backend-url]/docs`
- [ ] Frontend loads: `https://[frontend-url]`
- [ ] Login works with admin credentials
- [ ] Upload form accessible from dashboard
- [ ] Groq API key valid (test extraction)
- [ ] Gemini API key valid (test validation)
- [ ] Email notifications sending (check logs)
- [ ] WhatsApp notifications working (test account)

### Post-Deployment
- [ ] Monitor Render dashboard for errors
- [ ] Check logs daily for first week
- [ ] Set up uptime monitoring (Render provides free)
- [ ] Configure custom domain (optional)
- [ ] Enable auto-deploy on git push
- [ ] Document all deployment secrets securely

---

## 📋 Environment Variables Reference

### Production Values for Render

```env
# Database (from Neon)
DATABASE_URL=postgresql://[user]:[password]@[host]/[db]?sslmode=require

# App Config
DEBUG=False
APP_TITLE=CommunitySync
CORS_ORIGINS=["https://communitysync-frontend.onrender.com"]

# Security (Generate new secret!)
JWT_SECRET=[generate-random-secure-string]
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=1440

# Email (Gmail App Password)
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=[app-specific-password]
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE=+1415...

# AI Services
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=...
OPENCAGE_API_KEY=...
```

---

## 🔐 How to Generate JWT_SECRET

```bash
# Linux/Mac
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Windows PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use online: https://generate-random.org/
```

---

## 📊 Render Deployment Architecture

```
                    ┌─────────────────────┐
                    │  Frontend (Render)  │
                    │  Static Site        │
                    │  React App          │
                    └──────────┬──────────┘
                               │
                               │ HTTPS
                               ▼
                    ┌─────────────────────┐
                    │  Backend (Render)   │
                    │  FastAPI Service    │
                    │  EasyOCR, Groq,     │
                    │  Gemini             │
                    └──────────┬──────────┘
                               │
                               │ SSL
                               ▼
                    ┌─────────────────────┐
                    │ Neon PostgreSQL     │
                    │ (eu-west-1)         │
                    │ Free Tier           │
                    └─────────────────────┘

Third-Party APIs:
- Groq API (LLM)
- Google Gemini API (Validation)
- OpenCage API (Geocoding)
- Twilio API (WhatsApp)
- SMTP (Email)
```

---

## ⚠️ Common Issues & Fixes

### 1. SSL Connection Error
**Problem:** `SSL: CERTIFICATE_VERIFY_FAILED`
**Fix:** Ensure DATABASE_URL includes `?sslmode=require`

### 2. CORS 403
**Problem:** Frontend requests blocked
**Fix:** Update `CORS_ORIGINS` in Render env var to match frontend URL exactly

### 3. Build Timeout
**Problem:** Build takes >15 min and times out
**Fix:** Use Render Starter+ ($12/mo) or reduce dependencies

### 4. EasyOCR Out of Memory
**Problem:** OCR feature crashes on free tier
**Fix:** Disable for free tier or upgrade to Starter+

### 5. Database Not Initializing
**Problem:** Tables don't exist on first deploy
**Fix:** Run `python scripts/setup_db.py` manually via Render console or webhook

### 6. Secrets Not Updating
**Problem:** Changed env var but app still uses old value
**Fix:** Restart the service in Render dashboard

---

## 🔄 CI/CD Setup (Auto-Deploy)

Enable in Render dashboard:
1. Connect GitHub repo
2. Set branch to `main`
3. Enable "Auto-Deploy" toggle
4. Every git push triggers deployment

---

## 📈 Monitoring & Logs

**View Logs in Render:**
```bash
# SSH into service (if shell access enabled)
# Or use Render dashboard → Service → Logs tab

# Check last 50 lines
tail -50 /var/log/app.log
```

**Set Up Uptime Monitor:**
- Render provides free uptime monitoring
- Add alerts for > 1% downtime

---

## 💾 Database Backups

Neon provides automatic backups on free tier:
- 7-day retention
- Automatic daily snapshots
- Access via Neon dashboard → Backups

---

## 🔐 Security Best Practices

1. **Never commit secrets** to git
2. **Use Render's env vars** for sensitive data
3. **Rotate JWT_SECRET** periodically
4. **Use SSL** for all connections (already done)
5. **Enable 2FA** on Render account
6. **Monitor logs** for suspicious activity
7. **Rate limit** API endpoints (optional)
8. **Backup database** regularly

---

## 📞 Support Links

- **Render Docs:** https://render.com/docs
- **Neon Docs:** https://neon.tech/docs/introduction
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **React Build:** https://create-react-app.dev/docs/deployment/
