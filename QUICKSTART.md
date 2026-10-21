# ⚡ Prospector AI - Quick Start (5 Minutes)

## 🎯 Get Running in 3 Steps

### Step 1: Install Dependencies (2 min)
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys (1 min)
1. Get OpenAI API key: https://platform.openai.com/api-keys
2. Edit `.env` file and paste your key:
```
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Launch (1 min)

**Option A: Double-click to start** (Windows)
- `start_backend.bat` - Start backend (Terminal 1)
- `start_frontend.bat` - Start frontend (Terminal 2)

**Option B: Manual start**
```bash
# Terminal 1 - Backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend  
streamlit run frontend/app.py
```

### Step 4: Open & Test
1. Go to: **http://localhost:8501**
2. Enter: `chat360.io`
3. Click "Research"
4. Wait 30-60 seconds
5. 🎉 Done!

---

## 🎬 Demo Script for Showcase

### The Pitch (30 seconds)
"This is Prospector AI - an open-source tool that does 4 hours of B2B prospect research in 60 seconds. Watch this..."

### The Demo (2 minutes)

1. **Enter URL**: `chat360.io`
   - "I just enter any company URL..."

2. **Click Research**
   - "It's now scraping their website, job postings, recent news, and analyzing everything with GPT-4..."

3. **Show Intent Score** (while processing)
   - "It will calculate a 0-100 buying intent score based on 5 factors..."

4. **Results appear** (30-60 sec later)
   - **Score**: "Here's the intent score - 72/100 - HIGH PRIORITY"
   - **Breakdown**: "See why: they're hiring for sales, have funding, gaps detected..."
   - **Gaps Tab**: "It identified this primary gap - enterprise credibility gap - they target big clients but have no reviews"
   - **Messages Tab**: "And it wrote 3 personalized outreach messages I can send right now"
   - **Sources**: "Everything is cited with sources"

5. **Try Another**
   - "Let me show you another company..." (pick from examples)

### Key Points to Emphasize
✅ **Fast**: 60 seconds vs 4 hours manual research  
✅ **Intelligent**: AI identifies gaps, not just data collection  
✅ **Actionable**: Ready-to-send personalized messages  
✅ **Open Source**: MIT license, self-hostable, free to use  
✅ **Production Ready**: Full REST API, documented, tested  

---

## 🚨 Troubleshooting

**Backend won't start?**
```bash
# Check if port 8000 is in use
# Try different port:
uvicorn app.main:app --reload --port 8001
```

**Frontend won't connect?**
- Make sure backend is running first
- Check sidebar: should show "✅ Backend Connected"
- Check backend health: http://localhost:8000/health

**"OPENAI_API_KEY not found"?**
- Make sure `.env` file exists in root folder
- Check the key starts with `sk-`
- Restart backend after adding key

**Research takes too long?**
- First request is always slower (cold start)
- Use "quick" research depth in sidebar
- Check your internet connection

---

## 💡 Best Companies to Demo

1. **chat360.io** - Great example with hiring, gaps
2. **stripe.com** - Well-known, lots of data
3. **notion.so** - Popular product, good results
4. **Any B2B SaaS** - Works best with:
   - Active careers page
   - Public about/blog
   - Clear positioning

---

## 📊 What to Show Investors/Users

### For Investors:
- Market size: Every B2B company needs this
- Differentiation: Open source + AI-powered gaps
- Traction potential: GitHub stars, usage
- Business model: Open core, enterprise features

### For Users:
- Time saved: Show 60 sec vs 4 hours
- Quality: Show personalized messages vs generic
- Trust: Show sources and citations
- Value: Mention cost per research (~$0.02)

### For Developers:
- Open source: Show GitHub repo
- API: Show /docs endpoint
- Extensible: Show code structure
- Self-hostable: Emphasize data privacy

---

## 🎯 Call to Action

After demo:
- **Users**: "Try it yourself - it's free and open source"
- **Developers**: "Star us on GitHub, PRs welcome"
- **Enterprises**: "We can help you integrate this into your sales stack"

---

Ready to showcase! 🚀
