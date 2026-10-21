# 🎯 START HERE - Prospector AI

## Welcome! Your AI Research Assistant is Ready

This tool does **4 hours of prospect research in 60 seconds**. Let's get you up and running!

---

## ⚡ Quick Launch (Choose One)

### Option 1: Double-Click Start (Easiest)
1. **Get OpenAI API Key**: https://platform.openai.com/api-keys
2. **Edit `.env` file**: Paste your key next to `OPENAI_API_KEY=`
3. **Double-click** `start_backend.bat` (wait 5 seconds)
4. **Double-click** `start_frontend.bat` 
5. **Open**: http://localhost:8501
6. **Try**: Enter `chat360.io` and click Research

### Option 2: Command Line
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your OpenAI key to .env file

# 3. Start backend (Terminal 1)
uvicorn app.main:app --reload

# 4. Start frontend (Terminal 2)
streamlit run frontend/app.py

# 5. Open http://localhost:8501
```

---

## ✅ What You Get

### Input
- Any company URL (e.g., `chat360.io`, `stripe.com`, `notion.so`)

### Output (in 60 seconds)
- ✅ **Intent Score (0-100)** - How likely they are to buy
- ✅ **Gap Analysis** - AI identifies what they're missing
- ✅ **3 Personalized Messages** - Ready to send
- ✅ **Hiring Signals** - What roles they're hiring
- ✅ **News & Funding** - Recent events
- ✅ **Tech Stack** - What tools they use
- ✅ **All Sources** - Fully cited

---

## 📁 File Guide

| File | Purpose |
|------|---------|
| `start_backend.bat` | Launch the API server |
| `start_frontend.bat` | Launch the web interface |
| `QUICKSTART.md` | 5-minute setup guide |
| `SETUP.md` | Detailed setup instructions |
| `README.md` | Project documentation |
| `.env` | **YOUR API KEYS GO HERE** |
| `requirements.txt` | Python dependencies |

---

## 🚀 Ready to Showcase?

### Demo Flow (2 minutes)
1. Open UI: http://localhost:8501
2. Enter: `chat360.io`
3. Click: **Research**
4. Show while processing: "It's scraping their website, careers page, news..."
5. Show results:
   - Intent Score: 72/100
   - Primary Gap: "Enterprise credibility gap"
   - Messages: 3 personalized variants
6. Click through tabs: Score Breakdown → Gaps → Messages → Sources

### Best Demo Companies
- `chat360.io` - Indian SaaS, good results
- `stripe.com` - Well-known, lots of data  
- `notion.so` - Popular, strong insights
- `intercom.com` - Enterprise SaaS

---

## 🔧 Prerequisites

**Required:**
- ✅ Python 3.10+
- ✅ OpenAI API Key ([get one](https://platform.openai.com/api-keys))

**Optional (but recommended):**
- Tavily API Key for better search ([get one](https://tavily.com))

**Cost:**
- ~$0.02-0.05 per company research
- OpenAI GPT-4o-mini model (cheapest, fast)

---

## 🎬 Quick Test

After starting both servers, test the API:

```bash
# Test health
curl http://localhost:8000/health

# Test research
curl -X POST http://localhost:8000/api/v1/research ^
  -H "Content-Type: application/json" ^
  -d "{\"company_url\":\"chat360.io\"}"
```

Or double-click `TEST_API.bat`

---

## 📊 Architecture

```
You (Browser)
    ↓
Streamlit Frontend (localhost:8501)
    ↓
FastAPI Backend (localhost:8000)
    ↓
┌────────────┬──────────────┬─────────────┐
│            │              │             │
Research   Web Scraper   Tavily Search
Agent      (BS4 + aiohttp)    API
(GPT-4)
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Error: "ModuleNotFoundError"
pip install -r requirements.txt

# Error: "Port already in use"
uvicorn app.main:app --reload --port 8001
```

### Frontend shows "Backend Offline"
1. Make sure backend is running (check Terminal 1)
2. Look for: "Uvicorn running on http://127.0.0.1:8000"
3. Test: http://localhost:8000/health (should return JSON)

### "OPENAI_API_KEY not found"
1. Check `.env` file exists in project root
2. Make sure line reads: `OPENAI_API_KEY=sk-your-actual-key`
3. Restart backend after editing

### Research takes forever
- First request is always slower (cold start ~60s)
- Subsequent requests: ~30-40s
- Use "quick" mode in sidebar for faster results
- Check internet connection

---

## 📚 Documentation

- **QUICKSTART.md** - Get running in 5 minutes
- **SETUP.md** - Detailed setup walkthrough
- **README.md** - Full project documentation
- **docs/PRD.md** - Product requirements (what & why)
- **API Docs** - http://localhost:8000/docs (after starting backend)

---

## 🎯 Next Steps

1. ✅ Get it running (follow Quick Launch above)
2. ✅ Research 3-5 test companies
3. ✅ Review the generated messages
4. ✅ Try the API at http://localhost:8000/docs
5. ✅ Customize for your needs:
   - Edit prompts in `app/agents/research_agent.py`
   - Adjust scoring in `_calculate_intent_score()`
   - Add custom data sources

---

## 💡 Use Cases

### For Founders
- Research prospects before cold outreach
- Qualify leads automatically
- Write personalized messages at scale

### For Sales Teams
- Pre-research prospects (50/day → 50/hour)
- Prioritize leads by intent score
- A/B test message angles

### For RevOps
- Integrate via REST API
- Batch process prospect lists
- Enrich CRM data automatically

### For Developers
- Fork and customize
- Add custom scrapers
- Build plugins/extensions

---

## 🌟 What Makes This Special

| Feature | Prospector AI | Manual Research | Other Tools |
|---------|--------------|-----------------|-------------|
| **Time** | 60 seconds | 4 hours | N/A |
| **Cost** | $0.02 | $50+ (SDR time) | $500/mo subscription |
| **Quality** | AI-powered gaps | Limited by time | Just data, no insights |
| **Privacy** | Self-hosted | N/A | Cloud-only |
| **Customizable** | Open source | N/A | Closed source |

---

## 📞 Need Help?

1. **Read the logs** - Terminal shows detailed errors
2. **Check health** - http://localhost:8000/health
3. **Review docs** - All .md files in project root
4. **GitHub Issues** - Report bugs
5. **API Docs** - http://localhost:8000/docs

---

## 🎉 You're Ready!

Just need 2 things:
1. ✅ OpenAI API Key in `.env` file
2. ✅ Run `start_backend.bat` and `start_frontend.bat`

Then open http://localhost:8501 and start researching! 🚀

---

**Pro Tip:** Start with well-known SaaS companies (Stripe, Notion, Intercom) to see best results. They have rich public data, careers pages, and news coverage.

Good luck with your showcase! ⭐
