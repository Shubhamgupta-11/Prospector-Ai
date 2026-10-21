# Multi-API Discovery Setup Guide

## Overview

Your discovery system now uses **3 search APIs** with intelligent routing for:
- ✅ **Higher Accuracy**: Results from multiple sources
- ✅ **Automatic Failover**: If one API fails, others take over
- ✅ **No Data Leakage**: All requests go directly to providers (not through proxies)
- ✅ **Smart Deduplication**: Removes duplicate companies
- ✅ **Cost Optimization**: Uses free tiers efficiently

## Search Providers

### 1. Tavily API (Primary - Already Configured!)
**Status**: ✓ You've already added this key
- **Best for**: AI agents, structured data
- **Free tier**: 1,000 searches/month
- **Accuracy**: ★★★★☆ (4/5)
- **Get key**: https://tavily.com

### 2. SerpAPI (Optional - Highest Accuracy)
**Recommended**: Add this for best results
- **Best for**: Google search results (highest accuracy)
- **Free tier**: 100 searches/month
- **Accuracy**: ★★★★★ (5/5)
- **Get key**: https://serpapi.com
- **Setup time**: 2 minutes

**How to get SerpAPI key:**
1. Go to https://serpapi.com
2. Click "Register" (top right)
3. Verify your email
4. Go to "Dashboard" → "API Key"
5. Copy your key (starts with a long string of letters/numbers)

### 3. Brave Search API (Optional - Best Free Tier)
**Recommended**: Add this for maximum free searches
- **Best for**: Independent results, privacy
- **Free tier**: 2,000 searches/month (no credit card!)
- **Accuracy**: ★★★★☆ (4/5)
- **Get key**: https://brave.com/search/api/
- **Setup time**: 2 minutes

**How to get Brave Search key:**
1. Go to https://brave.com/search/api/
2. Click "Get Started"
3. Sign up (no credit card required!)
4. Go to dashboard and copy your API key

## Configuration

### Step 1: Open .env file
```bash
# Location: c:\Users\my277\ntra\prospector-ai\.env
```

### Step 2: Add Your Keys

**Current (only Tavily):**
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_key_here  # ✓ Already added!
SERPAPI_API_KEY=your_serpapi_api_key_here
BRAVE_API_KEY=your_brave_api_key_here
```

**Recommended (all 3 for best results):**
```env
OPENAI_API_KEY=sk-proj-abc123xyz...
TAVILY_API_KEY=tvly-12345...          # ✓ You have this
SERPAPI_API_KEY=abc123xyz...          # Add this (100 free searches/month)
BRAVE_API_KEY=BSA123xyz...            # Add this (2000 free searches/month)
```

### Step 3: Save the file

### Step 4: Restart Backend
```bash
# Stop current backend (Ctrl+C in terminal)
# Then restart:
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Testing Your Setup

### Quick Test (2 minutes)
```bash
python test_discovery.py
```

**Expected Output:**
```
=== Testing OpenAI API Connection ===
✓ OPENAI_API_KEY found
✓ OpenAI API working!

=== Testing Search Providers ===
✓ Found 3 configured provider(s): tavily, serpapi, brave

--- Testing TAVILY ---
✓ tavily working! Found 3 results

--- Testing SERPAPI ---
✓ serpapi working! Found 3 results

--- Testing BRAVE ---
✓ brave working! Found 3 results

=== Testing Failover Mechanism ===
✓ Failover working! Used provider: tavily

=== Testing Multi-Provider Merge ===
✓ Multi-provider merge working!
  Merged 8 unique results from multiple sources
  Providers used: tavily, serpapi, brave

=== Testing Discovery Agent ===
✓ Discovery successful! Found 5 companies

✓ ALL TESTS PASSED!
```

## How the Routing Works

### Scenario 1: Single Provider (Current - Only Tavily)
```
User searches → Tavily API → Results
```

### Scenario 2: With Failover (Tavily + SerpAPI)
```
User searches → Try Tavily
             → If Tavily fails → Try SerpAPI
             → Return first successful results
```

### Scenario 3: Multi-Provider (All 3 - Recommended!)
```
User searches → Query all 3 APIs simultaneously
             → Merge results
             → Remove duplicates
             → Rank by relevance
             → Return best results
```

## Cost Breakdown (Monthly)

### Option 1: Tavily Only (Current)
- Free searches: 1,000/month
- Discoveries possible: ~100-200/month
- Cost: $0 (free tier)

### Option 2: Tavily + SerpAPI
- Free searches: 1,100/month (1000 + 100)
- Discoveries possible: ~110-220/month
- Higher accuracy with Google results
- Cost: $0 (free tiers)

### Option 3: All Three (Recommended!)
- Free searches: 3,100/month (1000 + 100 + 2000)
- Discoveries possible: ~300-600/month
- **Best accuracy** with result deduplication
- Automatic failover if one API fails
- Cost: $0 (free tiers)

## Security & Privacy

✅ **No Data Leakage**
- All requests go directly to API providers
- No intermediate proxies or caching
- Your searches are private to each provider

✅ **API Key Security**
- Keys stored in .env file (not committed to git)
- Never exposed in frontend
- Each provider gets only their own key

✅ **HTTPS Only**
- All API calls use encrypted HTTPS
- No plaintext transmission

## Troubleshooting

### "No search providers configured"
**Solution**: Add at least one search API key to .env file

### "Provider failed" errors
**Solution**: 
1. Check API key is correct (no extra spaces)
2. Verify key is active on provider dashboard
3. Check free tier quota not exceeded

### "All providers failed"
**Solution**:
1. Check internet connection
2. Verify all API keys are valid
3. Try running test script: `python test_discovery.py`

### Low quality results
**Solution**: Add more providers for better accuracy
- With 1 provider: Good
- With 2 providers: Better (failover)
- With 3 providers: Best (merged results)

## API Key Quick Links

| Provider | Sign Up | Dashboard | Free Tier |
|----------|---------|-----------|-----------|
| Tavily | [tavily.com](https://tavily.com) | [app.tavily.com](https://app.tavily.com) | 1,000/month |
| SerpAPI | [serpapi.com](https://serpapi.com) | [serpapi.com/dashboard](https://serpapi.com/dashboard) | 100/month |
| Brave | [brave.com/search/api](https://brave.com/search/api/) | [api.search.brave.com](https://api.search.brave.com) | 2,000/month |

## Next Steps

1. **Now**: System works with Tavily (your current setup)
2. **Optional**: Add SerpAPI for highest accuracy
3. **Optional**: Add Brave for 2000 extra free searches/month

**To test current setup:**
```bash
python test_discovery.py
```

**To add more keys:**
1. Get API keys from links above
2. Add to .env file
3. Restart backend
4. Run test again

Your system will automatically detect and use all configured providers!
