# Deployment Guide - Prospector AI

## Quick Deploy Options

### Option 1: Vercel (Frontend) + Railway (Backend) - RECOMMENDED
**Best for:** Quick deployment, free tier available
**Time:** 15-20 minutes

#### Backend on Railway
1. **Sign up**: https://railway.app
2. **New Project** → Deploy from GitHub
3. **Connect your repo** or upload code
4. **Set environment variables**:
   ```
   GOOGLE_API_KEY=your_key
   TAVILY_API_KEY=your_key
   ```
5. **Railway will auto-detect** Python and install requirements
6. **Get your backend URL**: e.g., `https://your-app.railway.app`

#### Frontend on Vercel
1. **Sign up**: https://vercel.com
2. **Import Project** from GitHub
3. **Framework**: Next.js (auto-detected)
4. **Root Directory**: `web`
5. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```
6. **Deploy** - Done in 2 minutes!
7. **Get your URL**: e.g., `https://prospector-ai.vercel.app`

**Update Frontend API URL:**
```typescript
// In web/app/page.tsx, replace:
const response = await fetch("http://localhost:8000/api/v1/research", {
// With:
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/research`, {
```

---

### Option 2: Render (Full Stack)
**Best for:** One-platform deployment
**Time:** 20-25 minutes

#### Deploy Backend
1. **Sign up**: https://render.com
2. **New Web Service**
3. **Connect repository**
4. **Settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. **Add environment variables**
6. **Deploy** - Get URL

#### Deploy Frontend
1. **New Static Site** on Render
2. **Settings**:
   - **Build Command**: `cd web && npm install && npm run build`
   - **Publish Directory**: `web/out`
3. **Deploy**

---

### Option 3: Docker + Any Cloud (AWS, GCP, DigitalOcean)
**Best for:** Full control, production-grade
**Time:** 30-60 minutes

#### Create Dockerfiles

**Backend Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile**:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY web/package*.json ./
RUN npm install

COPY web/ ./
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app ./

EXPOSE 3000
CMD ["npm", "start"]
```

**Deploy to**:
- AWS ECS/Fargate
- Google Cloud Run
- DigitalOcean App Platform
- Azure Container Instances

---

## Environment Variables Required

### Backend (.env)
```bash
# AI APIs
GOOGLE_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key_optional

# Search APIs
TAVILY_API_KEY=your_tavily_key
SERPAPI_API_KEY=your_serpapi_key_optional
BRAVE_API_KEY=your_brave_key_optional

# CORS (add your frontend domain)
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## Update CORS in Backend

Edit `app/main.py`:
```python
origins = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app",  # Add your deployed frontend
]
```

---

## Custom Domain Setup

### Vercel (Frontend)
1. Go to **Project Settings** → **Domains**
2. Add your domain: `prospector.yourdomain.com`
3. Update DNS records as instructed
4. SSL auto-configured ✅

### Railway (Backend)
1. Go to **Settings** → **Domains**
2. Add custom domain: `api.prospector.yourdomain.com`
3. Update DNS CNAME record
4. SSL auto-configured ✅

---

## Quick Start After Deployment

### Test Your Deployed App
1. Visit your frontend URL
2. Try researching: `stripe.com`
3. Check if API is responding
4. Monitor logs for errors

### Share Your App
```
🎯 Prospector AI
AI-powered B2B research in 70 seconds

Try it: https://your-app.vercel.app
```

---

## Monitoring & Logs

### Railway
- View logs in **Deployments** tab
- Set up alerts for errors
- Monitor API usage

### Vercel
- View logs in **Deployments** tab
- Check performance metrics
- Monitor bandwidth

---

## Cost Estimates (Monthly)

### Free Tier
- **Vercel**: Free (100GB bandwidth, unlimited requests)
- **Railway**: $5/month credit (good for hobby projects)
- **Render**: Free (750 hours/month, sleeps after inactivity)
- **API costs**: ~$10-20 (Gemini free tier, Tavily 1000 searches)

### Production (Low Traffic: 1000 requests/month)
- **Hosting**: $10-20/month
- **APIs**: $20-50/month
- **Total**: ~$30-70/month

### Production (Medium Traffic: 10,000 requests/month)
- **Hosting**: $50-100/month
- **APIs**: $100-200/month
- **Total**: ~$150-300/month

---

## Recommended: Start with Railway + Vercel

**Why?**
- ✅ Fastest to deploy (15 mins)
- ✅ Free tier available
- ✅ Auto-scaling
- ✅ SSL included
- ✅ Git-based deployment
- ✅ Easy to upgrade later

**Next Steps:**
1. Push code to GitHub
2. Deploy backend to Railway (5 mins)
3. Deploy frontend to Vercel (5 mins)
4. Update API URL in frontend
5. Test and share! 🚀

---

## Need Help?

Check these guides:
- Railway: https://docs.railway.app
- Vercel: https://vercel.com/docs
- Render: https://render.com/docs

Or ping me for deployment support!
