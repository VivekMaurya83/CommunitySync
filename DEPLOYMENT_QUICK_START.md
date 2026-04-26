# 🚀 Deployment Quick Start (5 Steps)

## Step 1: Neon Database (2 min)

```
1. Go to neon.tech → Sign up
2. Create database project
3. Copy DATABASE_URL (includes ?sslmode=require)
4. Save it somewhere safe
```

**Example URL:**
```
postgresql://user:password@ep-cool-wave-123.us-east-1.neon.tech/community_sync?sslmode=require
```

---

## Step 2: Render Backend (5 min)

```
1. Go to render.com → New Web Service
2. Connect GitHub repo
3. Configure:
   - Name: communitysync-backend
   - Build: pip install -r backend/requirements.txt && python -m spacy download en_core_web_sm
   - Start: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Set Environment Variables:**
```
DATABASE_URL = [paste from Neon]
GROQ_API_KEY = [from console.groq.com]
GEMINI_API_KEY = [from ai.google.dev]
OPENCAGE_API_KEY = [from opencagedata.com]
JWT_SECRET = [generate new: python -c "import secrets; print(secrets.token_urlsafe(32))"]
TWILIO_ACCOUNT_SID = [from twilio.com]
TWILIO_AUTH_TOKEN = [from twilio.com]
TWILIO_PHONE = [your twilio number]
EMAIL_USERNAME = [your gmail]
EMAIL_PASSWORD = [gmail app password]
CORS_ORIGINS = ["https://communitysync-frontend.onrender.com"]
DEBUG = False
```

**Deploy!** → Wait 3-5 min → Check `/docs`

---

## Step 3: Render Frontend (3 min)

```
1. Go to render.com → New Static Site
2. Connect GitHub repo
3. Configure:
   - Name: communitysync-frontend
   - Build: cd frontend && npm install --legacy-peer-deps && npm run build
   - Publish: frontend/build
```

**Set Environment Variable:**
```
REACT_APP_API_URL = https://communitysync-backend.onrender.com
```

**Deploy!** → Wait 2-3 min → Check frontend URL

---

## Step 4: Initialize Database (2 min)

**Option A: Via Render Console**
```bash
cd backend
python scripts/init_production_db.py
```

**Option B: Via psql**
```bash
psql postgresql://user:pwd@host/db?sslmode=require < backend/scripts/setup_db.sql
```

This creates tables and admin user.

---

## Step 5: Test Everything (3 min)

```bash
# Test backend API
curl https://communitysync-backend.onrender.com/docs

# Test frontend
https://communitysync-frontend.onrender.com

# Test login
Email: admin@communitysync.com
Password: [the one you set during init]

# Test upload
Try uploading a test crisis report
```

---

## ✅ Done! You're Live

| Component | URL |
|-----------|-----|
| **Frontend** | https://communitysync-frontend.onrender.com |
| **API** | https://communitysync-backend.onrender.com |
| **API Docs** | https://communitysync-backend.onrender.com/docs |
| **Database** | Neon Console |

---

## 🆘 If Something Breaks

1. **Backend won't deploy?**
   - Check build logs in Render dashboard
   - Ensure all env vars are set
   - Try increasing instance type to Starter+

2. **Frontend shows blank page?**
   - Check browser console for errors
   - Verify `REACT_APP_API_URL` is set
   - Clear cache & rebuild: `npm run build`

3. **Database connection error?**
   - Verify `?sslmode=require` in DATABASE_URL
   - Test locally first with: `psql [your-url]`
   - Check Neon status page

4. **API returning 403?**
   - CORS issue — verify frontend URL in backend `CORS_ORIGINS`
   - Clear browser cookies
   - Restart backend service

5. **Need Help?**
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide
   - Check Render logs: Service → Logs
   - Check Neon logs: Database → Logs

---

## 💡 Pro Tips

- **Free tier works** for MVP/testing
- **Upgrade to Starter+** ($12/mo) for production
- **Enable auto-deploy** in Render (git push → auto deploy)
- **Monitor logs** daily first week
- **Backup database** via Neon dashboard
- **Use custom domain** for professional look

---

## 📊 Expected Costs

| Service | Free | Starter+ |
|---------|------|----------|
| Render Backend | $0 | $12/mo |
| Render Frontend | $0 | - |
| Neon Database | $0 | $0 |
| **Total** | **$0** | **$12/mo** |

---

**Total setup time: ~15 minutes**  
**Estimated cost: $0-12/month**  
**Availability: 99.9%+**

Happy deploying! 🎉
