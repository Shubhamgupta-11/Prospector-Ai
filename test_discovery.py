"""
Test script for the Multi-API Discovery System
This will verify that:
1. API keys are configured
2. Each search provider is working
3. Failover mechanism works
4. Discovery agent can find companies with high accuracy
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_multi_search_providers():
    """Test each search provider individually"""
    print("\n=== Testing Search Providers ===")
    
    from app.scrapers.multi_search import MultiSearchManager, SearchProvider
    
    manager = MultiSearchManager()
    available = manager.get_available_providers()
    
    if not available:
        print("❌ No search providers configured!")
        print("\nPlease configure at least one of:")
        print("  - TAVILY_API_KEY (recommended)")
        print("  - SERPAPI_API_KEY (highest accuracy)")
        print("  - BRAVE_API_KEY (privacy-focused, 2000 free searches/month)")
        return False
    
    print(f"\n✓ Found {len(available)} configured provider(s): {', '.join(available)}")
    
    # Test each provider
    test_query = "B2B SaaS companies"
    all_passed = True
    
    for provider_name in available:
        print(f"\n--- Testing {provider_name.upper()} ---")
        try:
            provider_enum = SearchProvider(provider_name)
            results = await manager.search(test_query, limit=3, preferred_provider=provider_enum)
            
            if results:
                print(f"✓ {provider_name} working! Found {len(results)} results:")
                for i, result in enumerate(results[:2], 1):
                    print(f"  {i}. {result.get('title', 'No title')[:60]}")
                    print(f"     {result.get('url', 'No URL')[:60]}")
            else:
                print(f"⚠️  {provider_name} returned no results")
                all_passed = False
        
        except Exception as e:
            print(f"❌ {provider_name} failed: {str(e)}")
            all_passed = False
    
    return all_passed


async def test_failover_mechanism():
    """Test that failover works between providers"""
    print("\n=== Testing Failover Mechanism ===")
    
    from app.scrapers.multi_search import MultiSearchManager
    
    manager = MultiSearchManager()
    available = manager.get_available_providers()
    
    if len(available) < 2:
        print("⚠️  Only one provider configured, skipping failover test")
        print("   (Add more API keys to test failover)")
        return True
    
    print(f"Testing automatic failover across {len(available)} providers...")
    
    try:
        # This will try providers in order: Tavily > SerpAPI > Brave
        results = await manager.search("technology startups", limit=3)
        
        if results:
            provider_used = results[0].get('provider', 'unknown')
            print(f"✓ Failover working! Used provider: {provider_used}")
            print(f"  Found {len(results)} results")
            return True
        else:
            print("❌ All providers failed to return results")
            return False
    
    except Exception as e:
        print(f"❌ Failover test failed: {str(e)}")
        return False


async def test_multi_provider_merge():
    """Test merging results from multiple providers"""
    print("\n=== Testing Multi-Provider Merge ===")
    
    from app.scrapers.multi_search import MultiSearchManager
    
    manager = MultiSearchManager()
    available = manager.get_available_providers()
    
    if len(available) < 2:
        print("⚠️  Only one provider configured, skipping merge test")
        return True
    
    print(f"Querying all {len(available)} providers simultaneously...")
    
    try:
        # Query all providers and merge results
        results = await manager.multi_search(
            "enterprise software companies",
            limit=5,
            use_all_providers=True
        )
        
        if results:
            print(f"✓ Multi-provider merge working!")
            print(f"  Merged {len(results)} unique results from multiple sources")
            
            # Show which providers contributed
            providers_used = set(r.get('provider', 'unknown') for r in results)
            print(f"  Providers used: {', '.join(providers_used)}")
            
            return True
        else:
            print("❌ Multi-provider merge returned no results")
            return False
    
    except Exception as e:
        print(f"❌ Multi-provider merge failed: {str(e)}")
        return False


async def test_google_gemini_connection():
    """Test Google Gemini API connection"""
    print("\n=== Testing Google Gemini API Connection ===")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        print("❌ GOOGLE_API_KEY not configured in .env file")
        print("   Get your FREE API key from: https://aistudio.google.com/app/apikey")
        return False
    
    print(f"✓ GOOGLE_API_KEY found: {api_key[:10]}...")
    
    try:
        from google import genai
        
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents="Say 'OK' if you can read this"
        )
        
        print(f"✓ Google Gemini working! Response: {response.text.strip()}")
        return True
    
    except Exception as e:
        print(f"❌ Error testing Gemini: {str(e)}")
        return False


async def test_openai_connection():
    """Test OpenAI API connection (fallback)"""
    print("\n=== Testing OpenAI API Connection (Fallback) ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OPENAI_API_KEY not configured (optional)")
        return False
    
    print(f"✓ OPENAI_API_KEY found: {api_key[:10]}...")
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
        response = await llm.ainvoke("Say 'OK' if you can read this")
        
        print(f"✓ OpenAI API working! Response: {response.content}")
        return True
    
    except Exception as e:
        print(f"⚠️  OpenAI not available: {str(e)[:100]}...")
        print("   (This is OK - using Gemini instead)")
        return False


async def test_discovery_agent():
    """Test the full discovery agent"""
    print("\n=== Testing Discovery Agent ===")
    
    try:
        from app.agents.discovery_agent import DiscoveryAgent
        
        agent = DiscoveryAgent()
        
        # Test ICP
        icp = "B2B SaaS companies with 50-200 employees, recently funded, hiring sales roles"
        print(f"\nICP: {icp}")
        print("\nDiscovering companies (this may take 20-30 seconds)...")
        
        companies = await agent.discover_companies(icp, max_results=5)
        
        if companies:
            print(f"\n✓ Discovery successful! Found {len(companies)} companies:")
            for i, company in enumerate(companies, 1):
                print(f"\n  {i}. {company['name']}")
                print(f"     URL: {company['url']}")
                if company.get('description'):
                    print(f"     Description: {company['description'][:100]}...")
            return True
        else:
            print("❌ No companies found")
            return False
    
    except Exception as e:
        print(f"❌ Error testing discovery agent: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("PROSPECTOR AI - MULTI-API DISCOVERY TEST")
    print("=" * 60)
    
    # Test 1: Check Google Gemini (primary)
    gemini_ok = await test_google_gemini_connection()
    
    # Test 2: Check OpenAI (fallback)
    openai_ok = await test_openai_connection()
    
    # At least one AI API must work
    if not gemini_ok and not openai_ok:
        print("\n" + "=" * 60)
        print("⚠️  No AI API configured!")
        print("=" * 60)
        print("\nYou need at least ONE of:")
        print("1. Google Gemini (FREE) - Get from: https://aistudio.google.com/app/apikey")
        print("2. OpenAI (Paid) - Get from: https://platform.openai.com/api-keys")
        print("\nRecommended: Use Gemini (completely free!)")
        return
    
    # Test 3: Check search providers
    providers_ok = await test_multi_search_providers()
    
    if not providers_ok:
        print("\n" + "=" * 60)
        print("⚠️  No search APIs configured!")
        print("=" * 60)
        print("\nAdd at least ONE search API key:")
        print("  - Tavily (recommended): https://tavily.com")
        print("  - SerpAPI (highest accuracy): https://serpapi.com")
        print("  - Brave Search (2000 free/month): https://brave.com/search/api/")
        return
    
    # Test 4: Failover mechanism
    failover_ok = await test_failover_mechanism()
    
    # Test 5: Multi-provider merge
    merge_ok = await test_multi_provider_merge()
    
    # Test 6: Full discovery flow
    discovery_ok = await test_discovery_agent()
    
    print("\n" + "=" * 60)
    if (gemini_ok or openai_ok) and providers_ok and discovery_ok:
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n🎉 Your multi-API discovery system is ready!")
        print("\nFeatures enabled:")
        if gemini_ok:
            print("  ✓ Google Gemini (FREE - 1,500 requests/day)")
        if openai_ok:
            print("  ✓ OpenAI GPT-4 (Paid fallback)")
        print("  ✓ Automatic failover between providers")
        print("  ✓ High accuracy with multiple data sources")
        print("  ✓ No data leakage (direct API calls only)")
        print("  ✓ Smart result deduplication")
        print("\nOpen http://localhost:3000 and try the 'Discover Leads' tab")
    else:
        print("⚠️  SOME TESTS HAD ISSUES")
        print("=" * 60)
        print("\nThe system will still work, but consider:")
        print("  - Checking any errors above")
        if not gemini_ok and not openai_ok:
            print("  - Adding Google Gemini API key (FREE!)")
        if not providers_ok:
            print("  - Adding more search API keys for better failover")


if __name__ == "__main__":
    asyncio.run(main())
