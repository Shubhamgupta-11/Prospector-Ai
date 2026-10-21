"""
Multi-API Search Manager
Intelligently routes searches across Tavily, SerpAPI, and Brave Search
for maximum accuracy and reliability with automatic failover.
"""

import os
import logging
from typing import List, Dict, Optional
from enum import Enum
import asyncio
import aiohttp

logger = logging.getLogger(__name__)


class SearchProvider(Enum):
    """Available search providers"""
    TAVILY = "tavily"
    SERPAPI = "serpapi"
    BRAVE = "brave"


class MultiSearchManager:
    """
    Manages multiple search APIs with intelligent routing and failover.
    
    Strategy:
    1. Primary: Tavily (best for AI agents)
    2. Fallback: SerpAPI (highest accuracy, Google results)
    3. Backup: Brave Search (privacy-focused, independent index)
    
    Features:
    - Automatic failover on errors
    - Rate limit handling
    - Result deduplication
    - Quality scoring
    - No data leakage (all requests direct to providers)
    """
    
    def __init__(self):
        # Initialize API clients
        self.tavily_key = os.getenv("TAVILY_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")
        self.brave_key = os.getenv("BRAVE_API_KEY")
        
        # Track which APIs are available
        self.available_providers = []
        if self.tavily_key and self.tavily_key != "your_tavily_api_key_here":
            self.available_providers.append(SearchProvider.TAVILY)
            logger.info("✓ Tavily API configured")
        
        if self.serpapi_key and self.serpapi_key != "your_serpapi_api_key_here":
            self.available_providers.append(SearchProvider.SERPAPI)
            logger.info("✓ SerpAPI configured")
        
        if self.brave_key and self.brave_key != "your_brave_api_key_here":
            self.available_providers.append(SearchProvider.BRAVE)
            logger.info("✓ Brave Search configured")
        
        if not self.available_providers:
            logger.warning("⚠️  No search APIs configured. Please add API keys to .env")
        
        # Initialize Tavily client if available
        self.tavily_client = None
        if SearchProvider.TAVILY in self.available_providers:
            try:
                from tavily import TavilyClient
                self.tavily_client = TavilyClient(api_key=self.tavily_key)
            except Exception as e:
                logger.error(f"Failed to initialize Tavily client: {e}")
                self.available_providers.remove(SearchProvider.TAVILY)
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        preferred_provider: Optional[SearchProvider] = None
    ) -> List[Dict[str, str]]:
        """
        Execute search with intelligent provider selection and failover.
        
        Args:
            query: Search query
            limit: Maximum number of results
            preferred_provider: Optionally specify preferred provider
            
        Returns:
            List of search results with title, url, content, score
        """
        if not self.available_providers:
            logger.error("No search providers available")
            return []
        
        # Determine search order
        if preferred_provider and preferred_provider in self.available_providers:
            search_order = [preferred_provider] + [
                p for p in self.available_providers if p != preferred_provider
            ]
        else:
            # Default priority: Tavily > SerpAPI > Brave
            search_order = [
                p for p in [SearchProvider.TAVILY, SearchProvider.SERPAPI, SearchProvider.BRAVE]
                if p in self.available_providers
            ]
        
        # Try each provider in order
        for provider in search_order:
            try:
                logger.info(f"Searching with {provider.value}: '{query}'")
                
                if provider == SearchProvider.TAVILY:
                    results = await self._search_tavily(query, limit)
                elif provider == SearchProvider.SERPAPI:
                    results = await self._search_serpapi(query, limit)
                elif provider == SearchProvider.BRAVE:
                    results = await self._search_brave(query, limit)
                else:
                    continue
                
                if results:
                    logger.info(f"✓ {provider.value} returned {len(results)} results")
                    return results
                else:
                    logger.warning(f"⚠️  {provider.value} returned no results, trying next provider")
            
            except Exception as e:
                logger.error(f"❌ {provider.value} failed: {str(e)}, trying next provider")
                continue
        
        logger.error("All search providers failed")
        return []
    
    async def _search_tavily(self, query: str, limit: int) -> List[Dict[str, str]]:
        """Search using Tavily API"""
        if not self.tavily_client:
            raise ValueError("Tavily client not initialized")
        
        try:
            response = self.tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=limit,
            )
            
            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0),
                    'provider': 'tavily'
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Tavily search error: {str(e)}")
            raise
    
    async def _search_serpapi(self, query: str, limit: int) -> List[Dict[str, str]]:
        """Search using SerpAPI (Google Search)"""
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'q': query,
                    'api_key': self.serpapi_key,
                    'num': limit,
                    'engine': 'google'
                }
                
                async with session.get(
                    'https://serpapi.com/search',
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        raise ValueError(f"SerpAPI returned status {response.status}")
                    
                    data = await response.json()
                    
                    results = []
                    for result in data.get('organic_results', [])[:limit]:
                        results.append({
                            'title': result.get('title', ''),
                            'url': result.get('link', ''),
                            'content': result.get('snippet', ''),
                            'score': result.get('position', 999),  # Lower position = higher score
                            'provider': 'serpapi'
                        })
                    
                    return results
        
        except Exception as e:
            logger.error(f"SerpAPI search error: {str(e)}")
            raise
    
    async def _search_brave(self, query: str, limit: int) -> List[Dict[str, str]]:
        """Search using Brave Search API"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Accept': 'application/json',
                    'X-Subscription-Token': self.brave_key
                }
                
                params = {
                    'q': query,
                    'count': limit
                }
                
                async with session.get(
                    'https://api.search.brave.com/res/v1/web/search',
                    headers=headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        raise ValueError(f"Brave Search returned status {response.status}")
                    
                    data = await response.json()
                    
                    results = []
                    for result in data.get('web', {}).get('results', [])[:limit]:
                        results.append({
                            'title': result.get('title', ''),
                            'url': result.get('url', ''),
                            'content': result.get('description', ''),
                            'score': 1.0,  # Brave doesn't provide scores
                            'provider': 'brave'
                        })
                    
                    return results
        
        except Exception as e:
            logger.error(f"Brave Search error: {str(e)}")
            raise
    
    async def multi_search(
        self,
        query: str,
        limit: int = 5,
        use_all_providers: bool = False
    ) -> List[Dict[str, str]]:
        """
        Search across multiple providers and merge results for highest accuracy.
        
        Args:
            query: Search query
            limit: Maximum results to return
            use_all_providers: If True, query all providers and merge results
            
        Returns:
            Deduplicated and ranked results from multiple providers
        """
        if not use_all_providers:
            # Use standard failover logic
            return await self.search(query, limit)
        
        # Query all available providers in parallel
        tasks = []
        for provider in self.available_providers:
            if provider == SearchProvider.TAVILY:
                tasks.append(self._search_tavily(query, limit))
            elif provider == SearchProvider.SERPAPI:
                tasks.append(self._search_serpapi(query, limit))
            elif provider == SearchProvider.BRAVE:
                tasks.append(self._search_brave(query, limit))
        
        # Execute all searches concurrently
        results_lists = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Merge and deduplicate results
        all_results = []
        seen_urls = set()
        
        for results in results_lists:
            if isinstance(results, Exception):
                logger.error(f"Provider failed: {results}")
                continue
            
            if not results:
                continue
            
            for result in results:
                url = result['url'].lower().strip()
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(result)
        
        # Sort by score (higher is better for Tavily, lower is better for SerpAPI)
        # Normalize scoring
        for result in all_results:
            if result.get('provider') == 'serpapi':
                # SerpAPI uses position (lower is better), convert to score
                result['normalized_score'] = 1.0 / (result['score'] + 1)
            else:
                result['normalized_score'] = result['score']
        
        all_results.sort(key=lambda x: x.get('normalized_score', 0), reverse=True)
        
        logger.info(f"Multi-search merged {len(all_results)} unique results from {len(self.available_providers)} providers")
        
        return all_results[:limit]
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [p.value for p in self.available_providers]
    
    def is_provider_available(self, provider: SearchProvider) -> bool:
        """Check if a specific provider is available"""
        return provider in self.available_providers
