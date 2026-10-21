import os
import logging
from typing import Optional
from tavily import TavilyClient

logger = logging.getLogger(__name__)


class TavilySearcher:
    """Search the web for company intelligence using Tavily"""
    
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            logger.warning("TAVILY_API_KEY not set, search features will be limited")
            self.client = None
        else:
            self.client = TavilyClient(api_key=api_key)
    
    async def search(self, query: str, limit: int = 5) -> list[dict]:
        """Generic search method for any query"""
        if not self.client:
            logger.warning("Tavily client not initialized, returning empty results")
            return []
        
        try:
            response = self.client.search(
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
                })
            
            return results
        except Exception as e:
            logger.error(f"Error performing search: {str(e)}")
            return []
    
    async def search_company_news(self, company_name: str, limit: int = 5) -> list[dict]:
        """Search for recent company news"""
        if not self.client:
            return []
        
        try:
            query = f'"{company_name}" news funding announcement launch'
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=limit,
                include_domains=["techcrunch.com", "venturebeat.com", "crunchbase.com", "linkedin.com"]
            )
            
            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0),
                })
            
            return results
        except Exception as e:
            logger.error(f"Error searching company news: {str(e)}")
            return []
    
    async def search_company_info(self, company_name: str, company_url: str) -> dict:
        """Search for general company information"""
        if not self.client:
            return {}
        
        try:
            # First search: General company info
            query = f'"{company_name}" company information industry location employees'
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=3,
            )
            
            # Aggregate information from results
            info = {
                'industry': None,
                'location': None,
                'size': None,
                'description': None,
                'funding': None,
            }
            
            for result in response.get('results', []):
                content = result.get('content', '').lower()
                title = result.get('title', '').lower()
                full_text = content + ' ' + title
                
                # Try to extract industry
                if not info['industry']:
                    if 'saas' in full_text or 'software as a service' in full_text:
                        info['industry'] = 'SaaS / Software'
                    elif 'fintech' in full_text or 'financial technology' in full_text:
                        info['industry'] = 'Fintech'
                    elif 'e-commerce' in full_text or 'ecommerce' in full_text:
                        info['industry'] = 'E-commerce'
                    elif 'artificial intelligence' in full_text or ' ai ' in full_text or 'machine learning' in full_text:
                        info['industry'] = 'AI / ML'
                
                # Try to extract location
                if not info['location']:
                    # Common patterns for location
                    import re
                    location_patterns = [
                        r'based in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                        r'headquartered in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                        r'located in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                    ]
                    for pattern in location_patterns:
                        match = re.search(pattern, result.get('content', ''))
                        if match:
                            info['location'] = match.group(1)
                            break
                
                # Try to extract size
                if not info['size']:
                    import re
                    size_patterns = [
                        r'(\d+[\+\-]?\s*(?:to\s+\d+)?\s*employees)',
                        r'team of (\d+[\+\-]?)',
                        r'(\d+[\+\-]?\s*people)',
                    ]
                    for pattern in size_patterns:
                        match = re.search(pattern, content)
                        if match:
                            info['size'] = match.group(0).strip()
                            break
            
            # Second search: Specific funding query
            try:
                funding_query = f'"{company_name}" funding raised investment Series valuation'
                funding_response = self.client.search(
                    query=funding_query,
                    search_depth="basic",
                    max_results=3,
                )
                
                for result in funding_response.get('results', []):
                    content = result.get('content', '')
                    title = result.get('title', '')
                    
                    # Look for funding mentions
                    import re
                    funding_patterns = [
                        r'raised \$[\d\.]+[MBK](?:illion)?',
                        r'Series [A-F] (?:funding )?(?:round )?(?:of )?\$[\d\.]+[MBK]',
                        r'valued at \$[\d\.]+[MBK](?:illion)?',
                        r'\$[\d\.]+[MBK] (?:in )?(?:funding|investment)',
                        r'(?:total|累计) (?:funding|raised) (?:of )?\$[\d\.]+[MBK]',
                    ]
                    
                    for pattern in funding_patterns:
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            info['funding'] = match.group(0)
                            logger.info(f"Found funding info: {info['funding']}")
                            break
                    
                    if info['funding']:
                        break
                
                # If still no funding, try to extract from Crunchbase-style content
                if not info['funding']:
                    for result in funding_response.get('results', []):
                        content = result.get('content', '')
                        if 'crunchbase' in result.get('url', '').lower() or 'funding' in content.lower():
                            # Extract first sentence with funding-related keywords
                            sentences = content.split('. ')
                            for sentence in sentences:
                                if any(kw in sentence.lower() for kw in ['raised', 'funding', 'investment', 'series', 'valuation']):
                                    info['funding'] = sentence.strip()[:150]
                                    logger.info(f"Found funding from context: {info['funding']}")
                                    break
                            if info['funding']:
                                break
                
            except Exception as e:
                logger.error(f"Error in funding search: {str(e)}")
            
            return info
        except Exception as e:
            logger.error(f"Error searching company info: {str(e)}")
            return {}
    
    async def search_competitors(self, company_name: str, industry: str) -> list[str]:
        """Search for company competitors"""
        if not self.client:
            return []
        
        try:
            query = f'"{company_name}" competitors alternatives {industry}'
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=3,
            )
            
            # Extract competitor names from results (simplified)
            competitors = []
            for result in response.get('results', []):
                content = result.get('content', '')
                # This would need more sophisticated NER in production
                # For now, just return empty list or mock data
            
            return competitors[:5]
        except Exception as e:
            logger.error(f"Error searching competitors: {str(e)}")
            return []
