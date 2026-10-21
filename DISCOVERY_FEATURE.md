# Lead Discovery & Enrichment Feature

## Overview
The Lead Discovery feature allows you to describe your Ideal Customer Profile (ICP) in natural language and have the AI automatically find companies matching those criteria before researching them in-depth.

## How It Works

### 1. Discovery Mode
- Navigate to the "Discover Leads" tab on the homepage
- Enter a natural language description of your ideal customer
- The system uses AI to:
  - Generate multiple targeted search queries from your ICP
  - Search for companies using Tavily API
  - Filter and rank results by ICP fit
  - Return a structured list of companies

### 2. Deep Research
- Each discovered company has a "Deep Research" button
- Clicking it triggers the full research pipeline:
  - Website scraping
  - News analysis
  - Hiring signals
  - Intent scoring
  - Gap analysis
  - Outreach message generation

## Backend Architecture

### New Files Created

**`app/agents/discovery_agent.py`**
- Main LangChain agent for company discovery
- Uses GPT-4 to interpret ICP and generate search queries
- Integrates with Tavily Search API
- AI-powered filtering and ranking

**`app/models/discovery.py`**
- Pydantic models for request/response
- `DiscoveryRequest`: ICP description + max results
- `DiscoveryResponse`: List of discovered companies
- `DiscoveredCompany`: Name, URL, description

**`app/api/discovery.py`**
- FastAPI endpoint: `POST /api/v1/discover`
- Handles discovery requests
- Returns structured JSON response

### Updated Files
- `app/main.py`: Registered discovery router
- `app/agents/__init__.py`: Exported DiscoveryAgent

## Frontend Architecture

### New Components

**`components/ui/table.tsx`**
- shadcn data table component
- Clean, minimalist design
- Used for displaying discovered companies

**`components/ui/skeleton.tsx`**
- Loading state component
- Displays while discovery is in progress

**`components/ui/textarea.tsx`**
- Multi-line input for ICP description
- Enterprise-grade styling

### Updated Files

**`app/page.tsx`**
- Added mode toggle: "Direct Research" vs "Discover Leads"
- Integrated discovery workflow
- Table view for discovered companies
- "Deep Research" button for each result
- Skeleton loaders during discovery

## Design Principles

✅ **Minimalist & Enterprise-Grade**
- No emojis (except Target icon for discover button)
- Clean table layout
- Professional typography
- Dark mode optimized

✅ **User Experience**
- Two distinct workflows in one interface
- Clear loading states
- Seamless transition from discovery to research
- Inline error handling

## Example ICP Descriptions

```
B2B SaaS companies with 50-200 employees, recently raised Series A funding, hiring for sales roles, based in San Francisco
```

```
Fintech startups in Europe, 20-100 employees, using React and Node.js, actively expanding to new markets
```

```
Enterprise software companies hiring DevOps engineers, revenue $10M-$50M, recently announced partnerships
```

## API Usage

### Discovery Endpoint

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/discover \
  -H "Content-Type: application/json" \
  -d '{
    "icp_description": "B2B SaaS startups in healthcare, 20-50 employees",
    "max_results": 10
  }'
```

**Response:**
```json
{
  "status": "success",
  "icp_description": "B2B SaaS startups in healthcare, 20-50 employees",
  "companies": [
    {
      "name": "HealthTech Co",
      "url": "https://healthtech.example.com",
      "description": "Healthcare SaaS platform..."
    }
  ],
  "total_found": 10
}
```

## Configuration

### Required API Keys
- `OPENAI_API_KEY`: For AI-powered query generation and filtering
- `TAVILY_API_KEY`: For company search

Both should be set in your `.env` file.

## Performance

- **Discovery Time**: 15-30 seconds for 10 companies
- **Accuracy**: Depends on ICP specificity and data availability
- **Cost**: ~$0.01-0.03 per discovery (OpenAI + Tavily)

## Future Enhancements

Potential improvements:
- Save ICP profiles for reuse
- Bulk research mode (research all discovered companies at once)
- Export discovered companies to CSV
- Advanced filters (revenue, employee count, location)
- Integration with LinkedIn, Crunchbase for richer data
- Company deduplication across multiple discoveries

## Troubleshooting

**No companies found?**
- Make ICP more specific but not too narrow
- Try different phrasing
- Ensure Tavily API key is configured

**Slow discovery?**
- Normal for first run (AI query generation)
- Subsequent runs are faster
- Reduce max_results for faster response

**Poor ICP matching?**
- Add more specific criteria
- Include industry keywords
- Mention hiring signals or tech stack
