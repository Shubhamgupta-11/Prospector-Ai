# 🚀 Prospector AI - Setup Guide

## Step-by-Step Setup

### 1. Get Your API Keys

#### OpenAI API Key (Required)
1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)
6. **Save it somewhere safe - you won't see it again!**

#### Tavily API Key (Optional but Recommended)
1. Go to https://tavily.com
2. Sign up for free account
3. Get your API key from dashboard
4. Copy the key (starts with `tvly-...`)

### 2. Install Python Dependencies

```bash
# Make sure you're in the project directory
cd prospector-ai

# Install all required packages
pip install -r requirements.txt
```

This will install:
- FastAPI (backend framework)
- Streamlit (frontend UI)
- LangChain + OpenAI (AI)
- BeautifulSoup4 + aiohttp (web scraping)
- Tavily (search API)
- And other dependencies

### 3. Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env

# Now edit .env file and add your keys:
```

Edit `.env` file:
```
OPENAI_API_KEY=sk-your-actual-key-here
TAVILY_API_KEY=tvly-your-actual-key-here
```

**Important:** Never commit the `.env` file to git!

### 4. Test Backend

```bash
# Start the FastAPI backend
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test it:** Open http://localhost:8000 in your browser
- You should see: `{"status": "online", "message": "Prospector AI API is running"}`

**Check health:** http://localhost:8000/health
- Should show: `{"status": "healthy", "openai_configured": true, ...}`

### 5. Test Frontend

Open a **new terminal** (keep backend running):

```bash
# Start Streamlit
streamlit run frontend/app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Open:** http://localhost:8501

### 6. Run Your First Research

1. In the Streamlit UI, enter a company URL: `chat360.io`
2. Click "🔍 Research"
3. Wait 30-60 seconds
4. Explore the results!

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'X'"
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists in project root
- Check that you have `OPENAI_API_KEY=sk-...` in `.env`
- Restart the backend after adding keys

### Backend not responding
- Check terminal for errors
- Make sure port 8000 is not in use by another app
- Try: `uvicorn app.main:app --reload --port 8001`

### Frontend can't connect to backend
- Make sure backend is running on port 8000
- Check sidebar in Streamlit - should show "✅ Backend Connected"
- If offline, restart backend

### Slow research times
- First request is always slower (cold start)
- Network speed affects scraping
- Tavily API makes it faster - make sure it's configured

### API costs too high
- Switch to `gpt-4o-mini` in `research_agent.py` (default)
- Use `research_depth: "quick"` for faster/cheaper research
- Each research costs ~$0.02-0.05

## 🎯 Next Steps

Once everything is working:

1. **Try different companies:**
   - SaaS companies work best
   - Companies with careers pages give better results
   - More public information = better analysis

2. **Explore the API:**
   - Visit http://localhost:8000/docs
   - Try the interactive API documentation
   - Test with Postman/curl

3. **Customize for your needs:**
   - Edit prompts in `app/agents/research_agent.py`
   - Adjust scoring weights
   - Add custom data sources

4. **Integrate with your stack:**
   - Use the REST API from your CRM
   - Batch process CSV lists
   - Build custom workflows

## 📞 Need Help?

- **Check logs:** Terminal output shows detailed errors
- **API docs:** http://localhost:8000/docs
- **GitHub Issues:** Report bugs
- **PRD:** Read `docs/PRD.md` for complete documentation

## ✅ Verification Checklist

- [ ] Python 3.10+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenAI API key configured in `.env`
- [ ] Tavily API key configured (optional)
- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:8501
- [ ] Can research a test company successfully
- [ ] Results display correctly

You're ready to showcase! 🎉
