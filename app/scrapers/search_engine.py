from typing import Dict, List, Optional
import os
from datetime import datetime


class SearchEngine:
    """Search engine integration for company research"""
    
    def __init__(self):
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')
        self.use_tavily = bool(self.tavily_api_key and self.tavily_api_key != 'your_tavily_api_key_here')
    
    def search_company_news(self, company_name: str, days: int = 180) -> List[Dict]:
        """Search for recent company news and press coverage"""
        
        if self.use_tavily:
            return self._search_with_tavily(company_name, "news funding press release")
        else:
            return self._get_fallback_news(company_name)
    
    def search_company_info(self, company_name: str, domain: str) -> Dict:
        """Search for general company information"""
        
        if self.use_tavily:
            results = self._search_with_tavily(company_name, "company information about")
            
            # Extract useful information
            info = {
                'industry': self._extract_industry(results),
                'size': self._extract_company_size(results),
                'location': self._extract_location(results),
                'founded': self._extract_founded_year(results),
                'funding': self._extract_funding(results),
            }
            return info
        else:
            return self._get_fallback_info(company_name)
    
    def search_competitors(self, company_name: str, industry: str) -> List[str]:
        """Search for company competitors"""
        
        if self.use_tavily:
            query = f"{company_name} competitors alternatives in {industry}"
            results = self._search_with_tavily(company_name, query)
            return self._extract_competitors(results, company_name)
        else:
            return []
    
    def _search_with_tavily(self, company_name: str, query: str) -> List[Dict]:
        """Execute search using Tavily API"""
        try:
            from tavily import TavilyClient
            
            client = TavilyClient(api_key=self.tavily_api_key)
            
            response = client.search(
                query=f"{company_name} {query}",
                max_results=5,
                include_answer=True
            )
            
            results = []
            if response.get('results'):
                for result in response['results']:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('url', ''),
                        'content': result.get('content', ''),
                        'score': result.get('score', 0),
                    })
            
            return results
            
        except Exception as e:
            print(f"Tavily search error: {str(e)}")
            return []
    
    def _get_fallback_news(self, company_name: str) -> List[Dict]:
        """Fallback news when API not available"""
        return [
            {
                'title': f"{company_name} - Company Information",
                'date': datetime.now().strftime('%Y-%m-%d'),
                'url': f"https://www.google.com/search?q={company_name}+news",
                'relevance': "General company information",
                'source': "Web Search"
            }
        ]
    
    def _get_fallback_info(self, company_name: str) -> Dict:
        """Fallback company info when API not available"""
        return {
            'industry': 'Technology / SaaS',
            'size': 'Not available',
            'location': 'Not available',
            'founded': 'Not available',
            'funding': 'Not available',
        }
    
    def _extract_industry(self, results: List[Dict]) -> str:
        """Extract industry from search results"""
        # Simple keyword matching
        text = ' '.join([r.get('content', '') for r in results]).lower()
        
        industries = {
            'saas': 'SaaS / Software',
            'software': 'Software / Technology',
            'fintech': 'Financial Technology',
            'e-commerce': 'E-commerce',
            'ai': 'Artificial Intelligence',
            'healthcare': 'Healthcare',
            'education': 'Education Technology',
            'marketing': 'Marketing Technology',
        }
        
        for keyword, industry in industries.items():
            if keyword in text:
                return industry
        
        return 'Technology'
    
    def _extract_company_size(self, results: List[Dict]) -> str:
        """Extract company size from search results"""
        import re
        
        text = ' '.join([r.get('content', '') for r in results])
        
        # Look for employee count patterns
        patterns = [
            r'(\d+[\+\-]\d+)\s+employees',
            r'(\d+)\s+to\s+(\d+)\s+employees',
            r'team\s+of\s+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return f"{match.group(1)} employees"
        
        return "Not available"
    
    def _extract_location(self, results: List[Dict]) -> str:
        """Extract location from search results"""
        import re
        
        text = ' '.join([r.get('content', '') for r in results])
        
        # Common location patterns
        pattern = r'(?:based in|located in|headquartered in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        match = re.search(pattern, text)
        
        if match:
            return match.group(1)
        
        return "Not available"
    
    def _extract_founded_year(self, results: List[Dict]) -> str:
        """Extract founding year from search results"""
        import re
        
        text = ' '.join([r.get('content', '') for r in results])
        
        # Look for founding year
        pattern = r'(?:founded in|established in|started in)\s+(\d{4})'
        match = re.search(pattern, text, re.I)
        
        if match:
            return match.group(1)
        
        return "Not available"
    
    def _extract_funding(self, results: List[Dict]) -> str:
        """Extract funding information from search results"""
        import re
        
        text = ' '.join([r.get('content', '') for r in results])
        
        # Look for funding patterns
        patterns = [
            r'raised\s+\$(\d+(?:\.\d+)?[MBK])',
            r'funding\s+of\s+\$(\d+(?:\.\d+)?[MBK])',
            r'Series\s+[A-Z]',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(0)
        
        if 'funded' in text.lower() or 'investment' in text.lower():
            return "Funded (details not available)"
        
        return "Not available"
    
    def _extract_competitors(self, results: List[Dict], company_name: str) -> List[str]:
        """Extract competitor names from search results"""
        import re
        
        competitors = []
        text = ' '.join([r.get('content', '') for r in results])
        
        # Look for competitor mentions
        pattern = r'(?:competitor|alternative|similar to|vs)\s+([A-Z][a-z]+(?:[A-Z][a-z]+)?)'
        matches = re.findall(pattern, text)
        
        for match in matches:
            if match.lower() != company_name.lower() and len(match) > 2:
                competitors.append(match)
        
        return list(set(competitors))[:5]
