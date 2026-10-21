# API Keys Setup Guide

## Required API Keys

To use the Discovery feature, you need two API keys:

### 1. OpenAI API Key (Required)
**Used for:** AI-powered query generation, ICP filtering, gap analysis, and message generation

**How to get it:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-...`)
5. Paste it into `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Cost:** ~$0.01-0.05 per discovery (depending on ICP complexity)

### 2. Tavily API Key (Required for Discovery)
**Used for:** Web search to find companies matching ICP criteria

**How to get it:**
1. Go to https://tavily.com
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key (it starts with `tvly-...`)
5. Paste it into `.env` file:
   ```
   TAVILY_API_KEY=tvly-your-actual-key-here
   ```

**Cost:** Free tier includes 1,000 searches/month (enough for 100-200 discoveries)

## Configuration Steps

1. **Open the `.env` file** in the project root:
   ```
   c:\Users\my277\ntra\prospector-ai\.env
   ```

2. **Replace the placeholders** with your actual keys:
   ```env
   # Before (default)
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here

   # After (with your keys)
   OPENAI_API_KEY=sk-proj-abc123...
   TAVILY_API_KEY=tvly-xyz789...
   ```

3. **Save the file**

4. **Restart the backend** (if it's running):
   - Stop the backend server (Ctrl+C in terminal)
   - Start it again:
     ```bash
     python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
     ```

## Testing Your Setup

Run the test script to verify everything is working:

```bash
python test_discovery.py
```

**Expected output:**
```
=== Testing OpenAI API Connection ===
✓ OPENAI_API_KEY found: sk-proj-ab...
✓ OpenAI API working! Response: OK

=== Testing Tavily API Connection ===
✓ TAVILY_API_KEY found: tvly-12345...
✓ Search successful! Found 3 results:
  1. Company Name
     URL: https://example.com
     Content: Description...

=== Testing Discovery Agent ===
✓ Discovery successful! Found 5 companies:
  1. Company A
     URL: https://companya.com
  ...

✓ ALL TESTS PASSED!
```

## Troubleshooting

### "OPENAI_API_KEY not configured"
- Make sure you've replaced `your_openai_api_key_here` with your actual key
- Verify the key starts with `sk-`
- Check there are no extra spaces or quotes around the key

### "TAVILY_API_KEY not configured"
- Make sure you've replaced `your_tavily_api_key_here` with your actual key
- Verify the key starts with `tvly-`
- Check there are no extra spaces or quotes around the key

### "Invalid API key" error
- Your API key might be incorrect or expired
- Go back to the platform and generate a new key
- Make sure you copied the entire key

### "Rate limit exceeded"
- OpenAI: You may have exceeded your usage quota
- Tavily: Free tier has 1,000 searches/month limit
- Wait a bit or upgrade your plan

## Security Best Practices

⚠️ **Never commit API keys to version control**

The `.env` file is already in `.gitignore`, but double-check:
- Never share your `.env` file
- Never paste API keys in public channels
- Rotate keys if they're accidentally exposed
- Use environment variables in production (not `.env` files)

## Cost Estimates

**Per Discovery (10 companies):**
- OpenAI: $0.01-0.03 (GPT-4 mini)
- Tavily: 3-5 searches from free tier

**Per Deep Research (1 company):**
- OpenAI: $0.02-0.05
- Tavily: 2-3 searches

**Monthly costs** (assuming 50 discoveries + 50 deep research):
- OpenAI: ~$2-5
- Tavily: Free tier should be sufficient

## Next Steps

Once your API keys are configured and tested:

1. Start both servers:
   ```bash
   # Terminal 1 - Backend
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   
   # Terminal 2 - Frontend
   cd web
   npm run dev
   ```

2. Open http://localhost:3000

3. Click "Discover Leads" tab

4. Enter your ICP and start discovering!
