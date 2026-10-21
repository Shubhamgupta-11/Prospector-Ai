# Prospector AI — Product Requirements Document (PRD)

**Version:** 1.0
**Author:** Shubham Gupta
**Last Updated:** October 3, 2026
**Status:** Draft → Approved
**License:** MIT (Open Source)
**Repository:** github.com/[your-handle]/prospector-ai

---

## 1. Product Vision

### 1.1 Problem Statement

Cold outreach in B2B is broken. Sales teams spend 60–70% of their time on manual research — reading company websites, scanning job postings, checking LinkedIn, reading news — just to write one personalized message. Most of this research is repetitive, unstructured, and never reused.

The result: SDRs send 50–100 messages a day that feel generic, because doing real research at scale is humanly impossible.

### 1.2 Solution

**Prospector AI** is an open-source, AI-powered GTM intelligence tool that automates the entire prospect research pipeline.

**Input:** A company name or website URL.
**Output:** Deep company research, buying intent score, identified pain points/gaps, and a hyper-personalized outreach message — delivered in under 60 seconds.

### 1.3 One-Liner

> *"The AI research assistant that does 4 hours of prospect research in 60 seconds."*

### 1.4 Key Differentiators

| What Exists Today | Prospector AI |
|:---|:---|
| ZoomInfo/Apollo — gives you contact data, not intelligence | Gives you **why** to reach out, not just **who** |
| ChatGPT — you manually prompt it for each company | Fully automated pipeline, no prompting needed |
| Clay — powerful but expensive (\$500+/mo) and closed-source | Open-source, self-hostable, free to run |
| SDR manually researching — 30 min per company | 60 seconds per company, fully automated |

---

## 2. Target Users

### 2.1 Primary Personas

#### Persona 1: The Solo Founder (India / Global)
- **Who:** Early-stage founder doing their own outreach
- **Pain:** Can't afford a sales team. Spending evenings manually researching prospects
- **Need:** Automated research that helps them write messages that actually get replies
- **Quote:** *"I know personalisation works but I don't have time to research 50 companies a week"*

#### Persona 2: The GTM Engineer / RevOps Lead
- **Who:** Technical person responsible for outbound infrastructure at a B2B startup
- **Pain:** Building outbound workflows across multiple tools (Apollo + Clay + ChatGPT + CRM)
- **Need:** One unified pipeline that handles research → scoring → messaging
- **Quote:** *"I want to plug this into our existing stack via API"*

#### Persona 3: The SDR / BDR
- **Who:** Sales rep doing 50+ outreach messages per day
- **Pain:** Spending hours on LinkedIn research to write "personalized" messages that still feel generic
- **Need:** Pre-researched company briefs with ready-to-send message drafts
- **Quote:** *"If this saves me 2 hours a day on research, I'll use it every morning"*

### 2.2 Secondary Personas
- **VC Analysts** — researching portfolio companies and market landscapes
- **Freelance Consultants** — prospecting for new clients
- **Job Seekers** — researching companies before cold outreach to hiring managers

---

## 3. User Stories

### 3.1 Core User Stories (Phase 1 — MVP)

| ID | As a... | I want to... | So that... | Priority |
|:---|:---|:---|:---|:---|
| US-01 | Founder | Enter a company URL and get a full research brief in 60 seconds | I can understand the company without spending 30 minutes reading their website | P0 |
| US-02 | Founder | See an intent score (0-100) for each company | I can prioritize which prospects to reach out to first | P0 |
| US-03 | Founder | Get a personalized outreach message draft | I can send it immediately or tweak it before sending | P0 |
| US-04 | SDR | See identified pain points and gaps for a company | I know exactly what angle to lead with in my outreach | P0 |
| US-05 | SDR | See the sources and citations for all research | I can verify the information before using it | P0 |
| US-06 | GTM Engineer | Access all features via REST API | I can integrate this into our existing sales stack | P1 |

### 3.2 Growth User Stories (Phase 2)

| ID | As a... | I want to... | So that... | Priority |
|:---|:---|:---|:---|:---|
| US-07 | SDR | Upload a CSV of 50 companies and get all of them researched | I can batch-process my entire prospect list | P1 |
| US-08 | Founder | See a company's top 3 competitors auto-detected | I understand the competitive landscape before reaching out | P1 |
| US-09 | GTM Engineer | Define an ICP and auto-score companies against it | I can filter leads by fit before researching them | P1 |
| US-10 | SDR | Export enriched leads to CSV or Notion | I can move data into my CRM without copy-pasting | P1 |

### 3.3 Advanced User Stories (Phase 3)

| ID | As a... | I want to... | So that... | Priority |
|:---|:---|:---|:---|:---|
| US-11 | Founder | Set up monitoring alerts for target companies | I get notified when they raise funding, hire, or launch something | P2 |
| US-12 | SDR | Get 3 different outreach angles per company | I can A/B test messaging approaches | P2 |
| US-13 | GTM Engineer | See a full pipeline dashboard with all researched companies | I can manage my entire outbound from one place | P2 |

---

## 4. Feature Specifications

### 4.1 Phase 1: Core Pipeline (MVP)

#### F-01: Company Research Engine
**Description:** Given a company URL or name, automatically research and extract structured intelligence.

**Data Points Collected:**

```yaml
Company Profile:
  - Name, URL, Logo
  - Industry / Sector
  - Headquarters / Location
  - Founded Year
  - Company Size (employees)
  - One-line description (auto-generated)

Business Intelligence:
  - What they sell (products/services)
  - Target customers / ICP
  - Key value propositions (from website)
  - Recent blog posts / content themes
  - Tech stack (detected via BuiltWith / Wappalyzer logic)

Hiring Signals:
  - Active job postings (titles + departments)
  - Hiring velocity (how many roles open)
  - Key roles being hired (signals pain areas)

News & Events:
  - Recent funding rounds
  - Press coverage (last 6 months)
  - Product launches / announcements
  - Leadership changes

Public Commitments:
  - Stated goals (from About page, annual reports, press)
  - ESG / sustainability commitments
  - Partnership announcements
```

**Data Sources:**
| Source | Method | Data Extracted |
|:---|:---|:---|
| Company website | BeautifulSoup + Playwright | About, Products, Careers, Blog |
| Google Search | Tavily API | Recent news, press, funding |
| Job boards | Scraper (careers page) | Active job postings |
| LinkedIn (public) | Tavily search | Company size, description |
| Crunchbase (if available) | Tavily search | Funding data |

**Acceptance Criteria:**
- [ ] Returns structured JSON with all data points within 60 seconds
- [ ] Handles companies with minimal web presence gracefully (partial results, not errors)
- [ ] Cites every data point with its source URL
- [ ] Works for companies across India, US, EU markets

---

#### F-02: Intent Scoring Engine
**Description:** Score each company's buying intent from 0-100 based on detected signals.

**Scoring Framework:**

```yaml
Signal Categories (Total = 100):

  Hiring Signals (0-25 points):
    - Hiring for roles relevant to your product: +15
    - High hiring velocity (10+ open roles): +5
    - Hiring senior/leadership roles (scaling): +5

  Funding & Growth (0-20 points):
    - Raised funding in last 6 months: +10
    - Series A/B (growth stage, has budget): +5
    - Revenue growth indicators in press: +5

  Technology Gaps (0-20 points):
    - Using competitor products (detected): +10
    - No solution detected for the problem you solve: +10

  Public Commitments vs Capability (0-25 points):
    - Stated goal with no visible execution plan: +15
    - Regulatory pressure requiring action: +10

  Timing Signals (0-10 points):
    - Fiscal year start (budget available): +5
    - Recent leadership change (new initiatives): +5
```

**Output:**
```json
{
  "overall_score": 72,
  "breakdown": {
    "hiring_signals": {"score": 20, "max": 25, "evidence": ["Hiring 'Enterprise Sales Lead' — scaling outbound"]},
    "funding_growth": {"score": 15, "max": 20, "evidence": ["Backed by $150M group"]},
    "tech_gaps": {"score": 17, "max": 20, "evidence": ["No G2 reviews — trust gap in enterprise sales"]},
    "commitment_gap": {"score": 15, "max": 25, "evidence": ["Claims enterprise clients but weak market positioning"]},
    "timing": {"score": 5, "max": 10, "evidence": ["WhatsApp pricing change impacts client base"]}
  },
  "recommendation": "HIGH PRIORITY — Strong fit with multiple active signals"
}
```

**Acceptance Criteria:**
- [ ] Score is deterministic for the same input data
- [ ] Every score component includes human-readable evidence
- [ ] Scores update if company data changes on re-research

---

#### F-03: Gap Identifier (AI Analysis)
**Description:** LLM analyzes all collected data to identify the specific operational or strategic gap the prospect is facing.

**Prompt Architecture:**
```
System: You are a B2B sales strategist. Given company research data,
identify the #1 gap between what this company has publicly committed
to and what their current operations/tools can actually deliver.

Be specific. Don't say "they need better marketing."
Say "they've committed to enterprise sales but have zero G2 reviews,
which means enterprise buyers can't validate them during procurement."

Always cite your evidence.
```

**Output Format:**
```yaml
Primary Gap:
  title: "Enterprise credibility gap"
  description: "Chat360 targets enterprise buyers (Ford, Honda, Unilever)
    but has near-zero presence on G2/Capterra. Enterprise procurement
    teams require third-party validation before shortlisting vendors.
    This gap likely causes deal loss at the evaluation stage."
  evidence:
    - "G2 profile has <5 reviews vs competitor Gupshup with 200+"
    - "Enterprise clients listed on website but no public case studies"
  severity: "HIGH"
  
Secondary Gaps:
  - title: "Positioning diffusion"
    description: "Selling across 6 categories simultaneously..."
  - title: "Missing pricing narrative"
    description: "WhatsApp pricing change impacts clients..."
```

**Acceptance Criteria:**
- [ ] Identifies at least 1 primary and 2 secondary gaps
- [ ] Every gap is backed by specific evidence from the research
- [ ] Gaps are actionable (a salesperson can reference them in outreach)

---

#### F-04: Personalized Message Generator
**Description:** Generates a hyper-personalized outreach message based on identified gaps and company research.

**Message Rules (Hardcoded):**
1. Never start with "I hope this message finds you well"
2. Never use "I noticed your company..." without citing something specific
3. Lead with the prospect's problem, not your product
4. Keep under 150 words
5. End with a low-friction CTA (question, not a meeting request)
6. Match tone: professional but conversational (not corporate)

**Output:**
```yaml
Message Variants:
  - type: "gap-based"
    message: |
      Hey [Name],
      
      I was looking at Chat360's positioning and noticed something
      interesting — you've got Ford and Unilever on your client
      roster, but your G2 profile is nearly empty. In enterprise
      procurement, that's usually where deals quietly die.
      
      Has this come up in your sales cycles? Curious if you've
      thought about a systematic approach to solving this.

  - type: "timing-based"  
    message: |
      Hey [Name],
      
      With Meta's WhatsApp pricing change hitting on Oct 1, your
      clients are about to see their chatbot costs spike. The
      platforms that help businesses optimize message flows are
      going to win the next 6 months.
      
      Is Chat360 building anything around this?

  - type: "curiosity-based"
    message: |
      Hey [Name],
      
      Quick question — I've been mapping the Indian conversational
      AI space and I can't figure out Chat360's positioning.
      You've got enterprise logos but you're selling across 6
      categories. Is that intentional or is the GTM still evolving?
```

**Acceptance Criteria:**
- [ ] Generates 3 message variants (gap-based, timing-based, curiosity-based)
- [ ] Each message references specific research findings
- [ ] Messages are under 150 words
- [ ] No generic phrases or filler

---

#### F-05: Streamlit Dashboard (UI)
**Description:** Web-based UI for interacting with the tool.

**Screens:**

##### Screen 1: Home / Search
```
┌─────────────────────────────────────────────────┐
│  🔍 PROSPECTOR AI                               │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │ Enter company URL or name...            │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  [ Research This Company ]                      │
│                                                 │
│  Recent Searches:                               │
│  • chat360.io — Score: 72 — 2 hrs ago           │
│  • gupshup.io — Score: 58 — 1 day ago           │
│  • bitespeed.co — Score: 81 — 3 days ago        │
└─────────────────────────────────────────────────┘
```

##### Screen 2: Research Results
```
┌─────────────────────────────────────────────────┐
│  ← Back                                        │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │ CHAT360                                  │   │
│  │ Conversational AI Platform | Pune, India │   │
│  │ 50-200 employees | Backed by $150M group │   │
│  │                                          │   │
│  │ Intent Score: ████████░░ 72/100          │   │
│  │ Recommendation: HIGH PRIORITY            │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌─── TABS ─────────────────────────────────┐   │
│  │ [Overview] [Signals] [Gaps] [Messages]   │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌─── SCORE BREAKDOWN ──────────────────────┐   │
│  │ Hiring Signals:    ████████░░  20/25     │   │
│  │ Funding & Growth:  ██████░░░░  15/20     │   │
│  │ Tech Gaps:         ████████░░  17/20     │   │
│  │ Commitment Gap:    ██████░░░░  15/25     │   │
│  │ Timing:            ██████████   5/10     │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌─── IDENTIFIED GAPS ──────────────────────┐   │
│  │ 🔴 PRIMARY: Enterprise credibility gap   │   │
│  │    Zero G2 reviews vs competitor 200+    │   │
│  │    Source: g2.com/products/chat360       │   │
│  │                                          │   │
│  │ 🟡 SECONDARY: Positioning diffusion      │   │
│  │    Selling across 6 categories...        │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌─── OUTREACH MESSAGES ────────────────────┐   │
│  │ [Gap-Based] [Timing-Based] [Curiosity]   │   │
│  │                                          │   │
│  │ Hey [Name],                              │   │
│  │ I was looking at Chat360's positioning   │   │
│  │ and noticed something interesting...     │   │
│  │                                          │   │
│  │ [ 📋 Copy Message ] [ ✏️ Edit ]          │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌─── SOURCES ──────────────────────────────┐   │
│  │ 📎 chat360.io/about — scraped Oct 3      │   │
│  │ 📎 g2.com/chat360 — scraped Oct 3        │   │
│  │ 📎 inc42.com/chat360-funding — Oct 1     │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

##### Screen 3: Batch Processing (Phase 2)
```
┌─────────────────────────────────────────────────┐
│  📊 BATCH RESEARCH                              │
│                                                 │
│  [ Upload CSV ] or paste company list:          │
│  ┌─────────────────────────────────────────┐    │
│  │ chat360.io                              │    │
│  │ gupshup.io                              │    │
│  │ bitespeed.co                            │    │
│  │ interakt.shop                           │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  [ Research All (4 companies) ]                 │
│                                                 │
│  ┌─── RESULTS TABLE ────────────────────────┐   │
│  │ Company    │ Score │ Top Gap    │ Status  │   │
│  │ Chat360    │ 72    │ G2 reviews │ ✅ Done │   │
│  │ Gupshup    │ 58    │ Pricing    │ ✅ Done │   │
│  │ BiteSpeed  │ 81    │ Scale      │ ⏳ ...  │   │
│  │ Interakt   │ --    │ --         │ 🔄 Queue│   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  [ Export to CSV ] [ Export to Notion ]          │
└─────────────────────────────────────────────────┘
```

---

## 5. Technical Architecture

### 5.1 System Architecture Diagram

```
                    ┌──────────────┐
                    │   Frontend   │
                    │  (Streamlit) │
                    └──────┬───────┘
                           │ HTTP
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    │   Backend    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     ┌──────────────┐ ┌────────┐ ┌───────────┐
     │  LangChain   │ │ SQLite │ │ ChromaDB  │
     │  Agent Layer │ │   DB   │ │  Vectors  │
     └──────┬───────┘ └────────┘ └───────────┘
            │
   ┌────────┼────────────┐
   ▼        ▼            ▼
┌──────┐ ┌────────┐ ┌──────────┐
│ LLM  │ │ Tavily │ │ Scrapers │
│ API  │ │ Search │ │ (BS4 +   │
│      │ │  API   │ │Playwright│
└──────┘ └────────┘ └──────────┘
```

### 5.2 API Contract (REST)

#### POST /api/v1/research
Research a single company.

**Request:**
```json
{
  "company_url": "https://chat360.io",
  "company_name": "Chat360",  // optional, auto-detected from URL
  "research_depth": "standard",  // "quick" | "standard" | "deep"
  "seller_context": {  // optional — improves message relevance
    "product": "GTM automation platform",
    "target_persona": "Head of Sales",
    "value_prop": "Automate prospect research in 60 seconds"
  }
}
```

**Response:**
```json
{
  "id": "res_abc123",
  "status": "completed",
  "company": {
    "name": "Chat360",
    "url": "https://chat360.io",
    "industry": "Conversational AI / SaaS",
    "location": "Pune, India",
    "size": "50-200 employees",
    "description": "Omnichannel agentic AI chatbot platform",
    "founded": "2020",
    "funding": "Backed by $150M group (no external VC)"
  },
  "signals": {
    "hiring": [
      {"title": "Enterprise Sales Lead", "department": "Sales", "signal": "Scaling outbound sales"}
    ],
    "news": [
      {"title": "WhatsApp pricing impacts chatbot platforms", "date": "2026-10-01", "url": "..."}
    ],
    "tech_stack": ["WhatsApp API", "Web Widgets", "Voice AI"],
    "competitors_detected": ["Gupshup", "BiteSpeed", "Interakt"]
  },
  "intent_score": {
    "overall": 72,
    "breakdown": { ... },
    "recommendation": "HIGH PRIORITY"
  },
  "gaps": {
    "primary": {
      "title": "Enterprise credibility gap",
      "description": "...",
      "evidence": ["..."],
      "severity": "HIGH"
    },
    "secondary": [ ... ]
  },
  "outreach_messages": [
    {"type": "gap-based", "message": "..."},
    {"type": "timing-based", "message": "..."},
    {"type": "curiosity-based", "message": "..."}
  ],
  "sources": [
    {"url": "https://chat360.io/about", "scraped_at": "2026-10-03T12:00:00Z"}
  ],
  "metadata": {
    "research_time_seconds": 47,
    "tokens_used": 12500,
    "cost_usd": 0.03
  }
}
```

#### POST /api/v1/batch
Research multiple companies (Phase 2).

#### GET /api/v1/research/{id}
Retrieve a previous research result.

#### GET /api/v1/history
List all past research sessions.

---

## 6. Data Models

```python
# company.py
class Company(BaseModel):
    id: str
    name: str
    url: str
    industry: str | None
    location: str | None
    size: str | None
    description: str | None
    founded: str | None
    funding: str | None
    tech_stack: list[str]
    competitors: list[str]

# signals.py
class HiringSignal(BaseModel):
    title: str
    department: str
    signal: str  # human-readable interpretation

class NewsSignal(BaseModel):
    title: str
    date: str
    url: str
    relevance: str

class Signals(BaseModel):
    hiring: list[HiringSignal]
    news: list[NewsSignal]
    tech_stack: list[str]
    competitors_detected: list[str]

# scoring.py
class ScoreBreakdown(BaseModel):
    category: str
    score: int
    max_score: int
    evidence: list[str]

class IntentScore(BaseModel):
    overall: int  # 0-100
    breakdown: list[ScoreBreakdown]
    recommendation: str  # "HIGH PRIORITY" | "MEDIUM" | "LOW"

# gaps.py
class Gap(BaseModel):
    title: str
    description: str
    evidence: list[str]
    severity: str  # "HIGH" | "MEDIUM" | "LOW"

class GapAnalysis(BaseModel):
    primary: Gap
    secondary: list[Gap]

# outreach.py
class OutreachMessage(BaseModel):
    type: str  # "gap-based" | "timing-based" | "curiosity-based"
    message: str
    word_count: int
    references: list[str]  # which research points it references

# research.py (aggregate)
class ResearchResult(BaseModel):
    id: str
    status: str
    company: Company
    signals: Signals
    intent_score: IntentScore
    gaps: GapAnalysis
    outreach_messages: list[OutreachMessage]
    sources: list[Source]
    metadata: ResearchMetadata
```

---

## 7. Non-Functional Requirements

| Requirement | Target | Notes |
|:---|:---|:---|
| **Response Time** | < 60 seconds per company | Standard depth research |
| **Quick Mode** | < 20 seconds | Skips deep scraping, uses cached/search data only |
| **Availability** | 99% uptime (self-hosted) | Depends on LLM API availability |
| **Cost Per Research** | < $0.05 USD | ~12K tokens per research at GPT-4o rates |
| **Concurrency** | 5 parallel researches | Async pipeline with rate limiting |
| **Data Privacy** | No data sent to third parties beyond LLM APIs | All research stored locally |
| **Caching** | 24-hour cache per company | Avoid redundant API calls |
| **Error Handling** | Graceful degradation | Partial results if one source fails |

---

## 8. Success Metrics

### 8.1 Product Metrics
| Metric | Target (MVP) | How to Measure |
|:---|:---|:---|
| Research accuracy | > 85% of data points verified | Manual audit of 20 companies |
| Time saved per prospect | > 25 minutes | Compare manual vs tool research |
| Message quality | 3/5 messages deemed "sendable" by user | User feedback rating |
| Intent score accuracy | > 70% correlation with actual conversion | Track which scored leads convert |

### 8.2 Open Source Metrics
| Metric | Target (3 months) | Target (6 months) |
|:---|:---|:---|
| GitHub Stars | 100 | 500 |
| Contributors | 3 | 10 |
| Forks | 20 | 75 |
| Weekly active users | 50 | 200 |

---

## 9. Open Source Strategy

### 9.1 License
**MIT License** — Maximum adoption, no restrictions.

### 9.2 Repository Structure
```
prospector-ai/
├── README.md              # Project overview, demo GIF, quick start
├── LICENSE                 # MIT
├── CONTRIBUTING.md         # Contribution guidelines
├── CHANGELOG.md            # Version history
├── .env.example            # Required API keys template
├── docker-compose.yml      # One-command setup
├── Makefile                # Common commands (make run, make test)
│
├── docs/
│   ├── PRD.md              # This document
│   ├── ARCHITECTURE.md     # Technical deep dive
│   ├── API.md              # API reference
│   └── DEPLOYMENT.md       # Self-hosting guide
│
├── app/                    # Backend (FastAPI + LangChain)
├── frontend/               # Streamlit dashboard
├── tests/                  # Test suite
└── examples/               # Example outputs and demo scripts
```

### 9.3 README.md Structure
```markdown
# 🔍 Prospector AI
> The AI research assistant that does 4 hours of prospect research in 60 seconds.

[Demo GIF here]

## Features
- Company research in 60 seconds
- Intent scoring (0-100)
- Gap identification
- Personalized outreach generation
- REST API for integrations
- Batch processing

## Quick Start
    docker-compose up
    # Open http://localhost:8501

## API Usage
    curl -X POST http://localhost:8000/api/v1/research \
      -d '{"company_url": "https://example.com"}'

## Built With
Python, FastAPI, LangChain, OpenAI, ChromaDB, Streamlit

## Contributing
See CONTRIBUTING.md

## License
MIT
```

---

## 10. Phased Roadmap

### Phase 1: MVP (Week 1–2)
| Day | What to Build | Deliverable |
|:---|:---|:---|
| Day 1-2 | Project setup, FastAPI scaffold, data models | Running API skeleton |
| Day 3-4 | Website scraper + Tavily search integration | Company data extraction working |
| Day 5-6 | LangChain research agent + scoring engine | Research pipeline end-to-end |
| Day 7-8 | Gap identifier + message generator | Full pipeline complete |
| Day 9-10 | Streamlit dashboard | UI working with full flow |
| Day 11-12 | Testing, error handling, caching | Stable MVP |
| Day 13-14 | README, docs, Docker setup, deploy | Published on GitHub |

**MVP Demo:** Research chat360.io end-to-end → show company card, score, gaps, and message.

### Phase 2: Intelligence Layer (Week 3–4)
- Batch processing (CSV upload)
- RAG-powered follow-up questions
- Competitor auto-detection
- ICP matching
- CSV/Notion export

### Phase 3: Agentic Features (Week 5–6)
- Multi-agent research planning (LangGraph)
- Deep dive agent (autonomous follow-up research)
- 3-variant message generation
- Monitoring alerts
- Pipeline dashboard

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|:---|:---|:---|
| Website scraping blocked (rate limiting, CAPTCHAs) | Incomplete data | Fallback to search API results; respect robots.txt; implement delays |
| LLM hallucinations in gap analysis | Incorrect insights | Require citations for every claim; add confidence scores |
| High API costs at scale | Expensive to run | Caching layer; quick mode; token-efficient prompts |
| LinkedIn scraping blocked | Missing company data | Use only public search results, never direct LinkedIn scraping |
| Low open-source adoption | Wasted effort | Focus on README quality, demo GIF, one-command Docker setup |

---

> [!IMPORTANT]
> **Before starting development, confirm:**
> 1. Which LLM API? (OpenAI / Claude / Gemini)
> 2. Tavily API key ready?
> 3. Start Phase 1, Day 1 today?
