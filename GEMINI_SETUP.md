# Google Gemini Setup (100% FREE!)

## 🎉 Great News!

You're now using **Google Gemini** instead of OpenAI! Gemini is:
- ✅ **Completely FREE**
- ✅ **1,500 requests/day** (enough for 300-500 discoveries!)
- ✅ **No credit card required**
- ✅ **Similar quality to GPT-4**
- ✅ **Fast and reliable**

## 🚀 Get Your Free API Key (2 minutes)

### Step 1: Go to Google AI Studio
Open this link: **https://aistudio.google.com/app/apikey**

### Step 2: Sign In
- Use your Google account
- Any Gmail account works!

### Step 3: Create API Key
1. Click **"Create API key"** button
2. Choose **"Create API key in new project"** (recommended)
3. Copy the key (starts with `AIza...`)

### Step 4: Add to .env File
1. Open `.env` file (it's already open in your editor)
2. Find the line:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
3. Replace with your actual key:
   ```
   GOOGLE_API_KEY=AIzaSy...your_actual_key
   ```
4. Save the file (Ctrl+S)

## ✅ That's It!

Once you've added the key and saved:
1. I'll restart the backend
2. Run the test to verify everything works
3. You'll have a fully functional discovery system - FOR FREE!

## 📊 What You Get

### Free Tier Limits
- **1,500 requests per day**
- **15 requests per minute**
- **1 million tokens per minute**

### What This Means for You
- ~300-500 company discoveries per day
- ~9,000-15,000 discoveries per month
- All completely FREE!

## 🆚 Gemini vs OpenAI

| Feature | Google Gemini | OpenAI GPT-4 |
|---------|--------------|--------------|
| **Cost** | FREE | $5-10/month minimum |
| **Daily Limit** | 1,500 requests | Pay per use |
| **Quality** | Excellent (similar to GPT-4) | Excellent |
| **Speed** | Fast | Fast |
| **Credit Card** | Not required | Required |
| **Best For** | Free tier users | High-volume production |

## 🔒 Security

- Your API key is stored securely in .env file
- Never committed to git (.gitignore protects it)
- Only used by your backend server
- Not exposed to frontend

## 💡 Pro Tips

### Monitor Your Usage
Check your usage at: https://aistudio.google.com/app/apikey
- See requests per day
- Track remaining quota
- View usage history

### Rate Limits
- If you hit the 15/minute limit, the system will automatically retry
- 1,500/day is very generous for your use case
- Resets every 24 hours

### Upgrade if Needed
If you ever need more:
- Gemini Pro: Pay-as-you-go pricing
- Still much cheaper than OpenAI
- But free tier should be plenty!

## 🆘 Troubleshooting

### "API key not valid"
- Make sure you copied the entire key
- Check for extra spaces
- Verify it starts with `AIza`

### "Quota exceeded"
- You've hit the 1,500/day limit
- Wait 24 hours for reset
- Or create another Google account

### Key not working?
- Make sure you saved the .env file
- Restart the backend
- Run test: `python test_discovery.py`

## 🎯 Next Steps

After adding your Gemini key:
1. Save .env file
2. Let me know - I'll restart backend
3. Run full test
4. Start discovering companies for FREE!

**Ready?** Go get your key at: https://aistudio.google.com/app/apikey
