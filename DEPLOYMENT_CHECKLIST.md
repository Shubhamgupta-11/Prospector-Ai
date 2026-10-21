# Deployment Checklist

## ✅ Pre-Deployment Done
- [x] Updated tagline to "hours of research in 70 secs"
- [x] Created API configuration for production
- [x] Updated API calls to use environment variables
- [x] All features working locally

## 📝 Deploy to Railway + Vercel (15 mins)

### Step 1: Push to GitHub (if not already)
```bash
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/prospector-ai.git
git push -u origin main
```

### Step 2: Deploy Backend to Railway (5 mins)
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `prospector-ai` repository
5. Railway auto-detects Python
6. Add Environment Variables:
   ```
   GOOGLE_API_KEY=AIza...
   TAVILY_API_KEY=tvly-...
   ```
7. Click Deploy
8. **Copy your Railway URL**: `https://prospector-ai-production.up.railway.app`

### Step 3: Deploy Frontend to Vercel (5 mins)
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. **Root Directory**: `web`
5. Framework Preset: Next.js (auto-detected)
6. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
   ```
   (Use the URL from Step 2)
7. Click Deploy
8. **Copy your Vercel URL**: `https://prospector-ai.vercel.app`

### Step 4: Update CORS in Backend (2 mins)
1. Go to your code: `app/main.py`
2. Update origins:
   ```python
   origins = [
       "http://localhost:3000",
       "https://prospector-ai.vercel.app",  # Your Vercel URL
       "https://*.vercel.app",  # All Vercel preview deploys
   ]
   ```
3. Commit and push:
   ```bash
   git add app/main.py
   git commit -m "Add production CORS"
   git push
   ```
4. Railway will auto-redeploy

### Step 5: Test Your Live App
1. Visit your Vercel URL
2. Research a company: `stripe.com`
3. Check all features work:
   - [  ] Direct research
   - [ ] Discovery/ICP search
   - [ ] Export CSV
   - [ ] Generate Report
   - [ ] Score breakdown
   - [ ] Gap analysis
   - [ ] Outreach messages

## 🎯 Your Live URLs

**Frontend**: https://prospector-ai.vercel.app  
**Backend API**: https://prospector-ai-production.railway.app  
**API Docs**: https://prospector-ai-production.railway.app/docs

## 🔗 Share Links

### For Twitter:
```
🚀 Just launched Prospector AI

AI-powered B2B research that turns hours of work into 70 seconds.

✨ Features:
• Intent scoring
• Gap analysis  
• Personalized outreach
• Lead discovery

Try it: [YOUR_VERCEL_URL]

Built with AI in a week 🤯
```

### For Product Hunt (when ready):
```
Tagline: Hours of B2B research in 70 seconds

Description: Prospector AI analyzes companies in seconds, scoring buying intent, 
identifying gaps, and generating personalized outreach messages. 
Built for sales teams who want to move fast.
```

### For LinkedIn:
```
Excited to share Prospector AI 🎯

After seeing sales teams spend 4+ hours researching each prospect, 
I built an AI tool that does it in 70 seconds.

It scores buying intent, identifies gaps, and writes personalized messages.

Free tier available. Try it: [YOUR_URL]
```

## 📊 Monitor After Launch

### Railway Dashboard
- Check backend logs
- Monitor API response times
- Watch for errors

### Vercel Dashboard
- Check frontend analytics
- Monitor page load times
- Watch bandwidth usage

### API Usage
- Track Gemini API calls
- Monitor Tavily searches
- Watch for rate limits

## 🐛 Common Issues

### Issue: CORS Error
**Fix**: Make sure you added your Vercel URL to `origins` in `app/main.py`

### Issue: 502 Bad Gateway
**Fix**: Check Railway logs - backend might be starting up (takes ~30s first time)

### Issue: API calls failing
**Fix**: Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel

### Issue: Slow first load
**Expected**: Railway free tier sleeps after inactivity, first request wakes it up (~30s)

## 💰 Costs

### Current Setup (Free Tier)
- Railway: $5/month credit
- Vercel: Free unlimited
- Gemini API: Free tier (1500 requests/day)
- Tavily: Free tier (1000 searches/month)

**Total**: ~$0-5/month for hobby use

## 🚀 Next Steps

After deployment:
1. [ ] Test all features on live URL
2. [ ] Share on Twitter
3. [ ] Share on LinkedIn
4. [ ] Post demo video
5. [ ] Gather feedback
6. [ ] Add to portfolio
7. [ ] Consider custom domain

## Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Next.js Deployment: https://nextjs.org/docs/deployment

You got this! 🎉
