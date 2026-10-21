# 🎯 Prospector AI

AI-powered GTM intelligence that turns 4 hours of sales research into 60 seconds.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)

## ✨ Features

- **🔍 Deep Company Research** - Analyze websites, job postings, news, and tech signals in 60 seconds
- **📊 Intent Scoring** - AI-powered 0-100 score based on buying signals
- **💡 Gap Analysis** - Identify pain points and objections automatically
- **✍️ Outreach Generation** - AI-crafted personalized messages ready to send
- **🎯 Lead Discovery** - Find companies matching your ICP
- **📈 Analytics Dashboard** - Track performance and research history
- **⚙️ API Management** - Test and configure all integrations from UI

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### 1. Clone & Install

```bash
git clone <your-repo>
cd prospector-ai

# Install Python dependencies
pip install -r requirements.txt

# Install Frontend dependencies
cd web
npm install
cd ..
```

### 2. Configure API Keys

Create `.env` file in the root:

```env
# Required
GOOGLE_API_KEY=your_google_gemini_key_here
TAVILY_API_KEY=your_tavily_key_here

# Optional (for additional search capacity)
SERPAPI_API_KEY=your_serpapi_key_here
BRAVE_API_KEY=your_brave_key_here
```

**Get Free API Keys:**
- Google Gemini: https://makersuite.google.com/app/apikey (1,500 requests/day FREE)
- Tavily Search: https://tavily.com (1,000 searches/month FREE)

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd web
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📖 Usage

### Research a Company

1. Go to **Overview** page
2. Enter company URL (e.g., `stripe.com`)
3. Click **Research**
4. Get results in ~60 seconds:
   - Intent Score (0-100)
   - Buying Signals
   - Pain Points
   - Outreach Messages

### View Analytics

1. Go to **Analytics** page
2. See:
   - Total researches
   - Average scores
   - Top industries
   - Recent activity

### Manage Settings

1. Go to **Settings** page
2. View API key status
3. Test connections
4. Update preferences

## 🏗️ Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library

### Backend
- **FastAPI** - Python web framework
- **LangChain** - AI agent orchestration
- **Google Gemini** - Free AI model (1,500 calls/day)
- **Tavily API** - Web search

### Storage
- **File-based JSON** - Simple persistence (no external DB needed)

## 📂 Project Structure

```
prospector-ai/
├── app/
│   ├── agents/          # AI agents (research, discovery)
│   ├── api/             # FastAPI routes
│   ├── database/        # Data storage
│   ├── models/          # Pydantic models
│   ├── scrapers/        # Search integrations
│   └── utils/           # Helpers
├── web/
│   ├── app/             # Next.js pages
│   ├── components/      # React components
│   └── lib/             # Utilities
├── .env                 # API keys (create this)
└── requirements.txt     # Python deps
```

## 💰 Cost

**$0/month** on free tiers:
- Google Gemini: 1,500 requests/day FREE
- Tavily Search: 1,000 searches/month FREE
- Hosting: Run locally or deploy free

## 🔧 Configuration

### Research Depth

Configure in Settings:
- **Quick** (30s) - Basic signals
- **Standard** (60s) - Full analysis (default)
- **Deep** (2-3min) - Comprehensive research

### Discovery Limits

Set max companies to discover: 5, 10, 20, or 50

## 📊 API Endpoints

### Research
```bash
POST /api/v1/research
{
  "company_url": "stripe.com",
  "research_depth": "standard"
}
```

### Analytics
```bash
GET /api/v1/analytics
# Returns: metrics, usage, recent researches
```

### Settings
```bash
GET /api/v1/settings
# Returns: current settings, API status

PUT /api/v1/settings
{
  "research_depth": "standard",
  "discovery_limit": 10
}
```

## 🐛 Troubleshooting

### "Not Configured" in Settings
- Check `.env` file exists in root
- Verify API keys are correct
- Restart backend server

### Empty Discovery Results
- Check backend logs for errors
- Verify Tavily API key is working
- Try broader ICP descriptions

### Low Intent Scores
- Normal for companies with limited public data
- Try bigger companies (Stripe, Notion, etc.)
- Score reflects actual available signals

## 🤝 Contributing

Contributions welcome! Open an issue or submit a PR.

## 📝 License

MIT License - feel free to use for commercial projects

## 🙏 Acknowledgments

Built with:
- Google Gemini (free AI)
- Tavily (web search)
- shadcn/ui (components)
- Next.js & FastAPI

---

**Built by [Your Name]** | [Twitter](https://twitter.com/yourhandle) | #buildinpublic

**Star ⭐ this repo if you found it helpful!**
