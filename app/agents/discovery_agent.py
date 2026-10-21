import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
import os

from app.scrapers.multi_search import MultiSearchManager
from app.utils.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class DiscoveryAgent:
    """Agent for discovering companies based on ICP criteria"""
    
    def __init__(self):
        self.searcher = MultiSearchManager()
        
        # Try Google Gemini first (free), fallback to OpenAI
        gemini_key = os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if gemini_key and gemini_key != "your_google_api_key_here":
            # Use Google Gemini (FREE!)
            self.client = GeminiClient(api_key=gemini_key)
            self.llm_type = "gemini"
            logger.info("✓ Using Google Gemini (FREE)")
        elif openai_key and openai_key != "your_openai_api_key_here":
            # Fallback to OpenAI
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.3,
                api_key=openai_key
            )
            self.llm_type = "openai"
            logger.info("✓ Using OpenAI GPT-4")
        else:
            raise ValueError("No AI API key configured. Add GOOGLE_API_KEY or OPENAI_API_KEY to .env")
    
    async def discover_companies(
        self,
        icp_description: str,
        max_results: int = 10
    ) -> List[Dict[str, str]]:
        """
        Discover companies matching the ICP description
        
        Args:
            icp_description: Natural language description of ideal customer profile
            max_results: Maximum number of companies to return
            
        Returns:
            List of companies with name and url
        """
        logger.info(f"Starting company discovery for ICP: {icp_description[:100]}...")
        
        try:
            # Step 1: Use AI to extract search queries from ICP
            search_queries = await self._generate_search_queries(icp_description)
            logger.info(f"Generated {len(search_queries)} search queries: {search_queries[:3]}")
            
            # Step 2: Execute searches across multiple queries
            all_companies = []
            for query in search_queries[:3]:  # Limit to 3 queries to avoid rate limits
                logger.info(f"Searching for: {query}")
                companies = await self._search_companies(query, limit=5)
                logger.info(f"Found {len(companies)} companies for query: {query}")
                all_companies.extend(companies)
            
            logger.info(f"Total companies before dedup: {len(all_companies)}")
            
            # Step 3: Deduplicate by URL
            seen_urls = set()
            unique_companies = []
            for company in all_companies:
                url = company['url'].lower()
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_companies.append(company)
            
            logger.info(f"Unique companies after dedup: {len(unique_companies)}")
            
            # If we have companies, filter by ICP, otherwise return what we have
            if unique_companies:
                filtered_companies = await self._filter_by_icp(
                    unique_companies,
                    icp_description,
                    max_results
                )
                logger.info(f"Filtered companies: {len(filtered_companies)}")
            else:
                filtered_companies = []
                logger.warning("No companies found from search")
            
            logger.info(f"Discovery complete: Found {len(filtered_companies)} companies")
            return filtered_companies[:max_results]
        
        except Exception as e:
            logger.error(f"Discovery failed: {str(e)}")
            raise
    
    async def _generate_search_queries(self, icp_description: str) -> List[str]:
        """Generate search queries from ICP description"""
        prompt = f"""You are a B2B lead generation expert. Given an Ideal Customer Profile (ICP), generate 3-5 specific search queries to find companies matching that profile.

ICP Description:
{icp_description}

Generate search queries that will find companies matching this ICP. Make them specific and actionable.

Examples:
- "SaaS companies hiring sales development reps"
- "B2B fintech startups San Francisco"
- "Enterprise software companies 50-200 employees"

Return ONLY the search queries, one per line, no numbering or extra text."""
        
        try:
            if self.llm_type == "gemini":
                content = self.client.generate_content(prompt)
            else:
                from langchain_core.prompts import ChatPromptTemplate
                prompt_template = ChatPromptTemplate.from_template(prompt)
                response = await self.llm.ainvoke(prompt_template.format_messages())
                content = response.content
            
            queries = [
                line.strip().strip('-').strip('*').strip()
                for line in content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            ]
            
            # Fallback if parsing fails
            if not queries:
                queries = [icp_description[:200]]
            
            logger.info(f"Generated {len(queries)} search queries")
            return queries
        
        except Exception as e:
            logger.error(f"Query generation failed: {str(e)}")
            # Fallback to using ICP directly
            return [icp_description[:200]]
    
    async def _search_companies(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """Search for companies using Tavily"""
        try:
            # Use Tavily to search for companies
            results = await self.searcher.search(query, limit=limit)
            
            companies = []
            for result in results:
                # Extract company name and URL
                url = result.get('url', '')
                title = result.get('title', '')
                
                # Try to extract company name from title or URL
                company_name = self._extract_company_name(title, url)
                
                if company_name and url:
                    companies.append({
                        'name': company_name,
                        'url': url,
                        'description': result.get('content', '')[:200]
                    })
            
            return companies
        
        except Exception as e:
            logger.error(f"Company search failed for query '{query}': {str(e)}")
            return []
    
    def _extract_company_name(self, title: str, url: str) -> str:
        """Extract company name from title or URL"""
        # Clean up title
        if title:
            # Remove common suffixes
            for suffix in [' - Home', ' | Home', ' - Official Site', ' | Official Site', '...']:
                title = title.replace(suffix, '')
            
            # Take first part before common separators
            for separator in ['|', '-', '—', ':']:
                if separator in title:
                    parts = title.split(separator)
                    if parts[0].strip():
                        return parts[0].strip()
            
            return title.strip()
        
        # Fallback to domain
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.replace('www.', '')
            name = domain.split('.')[0].capitalize()
            return name
        except:
            return 'Unknown Company'
    
    async def _filter_by_icp(
        self,
        companies: List[Dict[str, str]],
        icp_description: str,
        max_results: int
    ) -> List[Dict[str, str]]:
        """Use AI to filter and rank companies by ICP fit"""
        if not companies:
            return []
        
        # Create company list for prompt
        company_list = "\n".join([
            f"{i+1}. {c['name']} - {c['url']}\n   {c.get('description', 'No description')}"
            for i, c in enumerate(companies)
        ])
        
        prompt = f"""You are filtering a list of companies to find the best matches for an Ideal Customer Profile (ICP).

ICP Description:
{icp_description}

Companies Found:
{company_list}

Select the top {max_results} companies that BEST match this ICP. Consider:
- Industry relevance
- Company size indicators
- Business model fit
- Geographic location (if specified)
- Technology stack (if mentioned)

Return ONLY the numbers of the selected companies, comma-separated, in priority order.
Example: 3,7,1,9,2

If none match well, return the most promising ones anyway."""
        
        try:
            if self.llm_type == "gemini":
                content = self.client.generate_content(prompt)
            else:
                from langchain_core.prompts import ChatPromptTemplate
                prompt_template = ChatPromptTemplate.from_template(prompt)
                response = await self.llm.ainvoke(prompt_template.format_messages())
                content = response.content.strip()
            
            # Parse selected indices
            indices = []
            
            for part in content.split(','):
                try:
                    idx = int(part.strip()) - 1  # Convert to 0-based
                    if 0 <= idx < len(companies):
                        indices.append(idx)
                except:
                    continue
            
            # If parsing failed, return all companies
            if not indices:
                return companies[:max_results]
            
            # Return selected companies
            return [companies[i] for i in indices]
        
        except Exception as e:
            logger.error(f"ICP filtering failed: {str(e)}")
            # Return all companies if filtering fails
            return companies[:max_results]
