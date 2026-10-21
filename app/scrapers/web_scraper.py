import asyncio
import re
from typing import Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)


class WebScraper:
    """Scrapes company websites for intelligence"""
    
    def __init__(self):
        self.timeout = 30
        
    def extract_domain(self, url: str) -> str:
        """Extract clean domain from URL"""
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        return domain.replace('www.', '')
    
    async def scrape_company_website(self, url: str) -> dict:
        """Scrape company website for key information"""
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}: {response.status}")
                        return self._empty_result(url)
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    return {
                        'url': url,
                        'title': self._extract_title(soup),
                        'description': self._extract_description(soup),
                        'about': self._extract_about_text(soup),
                        'products': self._extract_products(soup),
                        'value_props': self._extract_value_props(soup),
                        'meta_info': self._extract_meta_info(soup),
                        'links': self._extract_important_links(soup, url),
                        'tech_stack': self._detect_tech_stack(html, soup),
                    }
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return self._empty_result(url)
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        if soup.title:
            return soup.title.string.strip()
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # Try og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()
        
        return ""
    
    def _extract_about_text(self, soup: BeautifulSoup) -> str:
        """Extract about/company text"""
        # Look for about sections
        about_keywords = ['about', 'company', 'who-we-are', 'our-story']
        
        for keyword in about_keywords:
            section = soup.find(['section', 'div'], class_=re.compile(keyword, re.I))
            if section:
                text = section.get_text(separator=' ', strip=True)
                if len(text) > 100:
                    return text[:1000]  # Limit to 1000 chars
        
        # Fallback: first few paragraphs
        paragraphs = soup.find_all('p', limit=5)
        text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        return text[:1000] if text else ""
    
    def _extract_products(self, soup: BeautifulSoup) -> list[str]:
        """Extract product/service mentions"""
        products = []
        
        # Look for product sections
        product_keywords = ['product', 'service', 'solution', 'feature']
        for keyword in product_keywords:
            sections = soup.find_all(['section', 'div'], class_=re.compile(keyword, re.I), limit=3)
            for section in sections:
                headings = section.find_all(['h1', 'h2', 'h3', 'h4'])
                for h in headings:
                    text = h.get_text(strip=True)
                    if text and len(text) < 100:
                        products.append(text)
        
        return list(set(products))[:10]  # Unique, max 10
    
    def _extract_value_props(self, soup: BeautifulSoup) -> list[str]:
        """Extract value propositions"""
        props = []
        
        # Hero section usually has main value prop
        hero = soup.find(['section', 'div'], class_=re.compile('hero|banner|jumbotron', re.I))
        if hero:
            h1 = hero.find('h1')
            if h1:
                props.append(h1.get_text(strip=True))
            
            subtitle = hero.find(['h2', 'p'], class_=re.compile('subtitle|tagline|description', re.I))
            if subtitle:
                props.append(subtitle.get_text(strip=True))
        
        return props[:5]
    
    def _extract_meta_info(self, soup: BeautifulSoup) -> dict:
        """Extract meta information"""
        info = {}
        
        # Look for location/address
        address = soup.find(['address', 'div'], class_=re.compile('address|location', re.I))
        if address:
            info['location'] = address.get_text(strip=True)
        
        # Look for founded year
        text = soup.get_text()
        founded_match = re.search(r'(?:founded|established|since)\s+(\d{4})', text, re.I)
        if founded_match:
            info['founded'] = founded_match.group(1)
        
        return info
    
    def _extract_important_links(self, soup: BeautifulSoup, base_url: str) -> dict:
        """Extract important page links"""
        links = {
            'about': None,
            'careers': None,
            'blog': None,
            'contact': None,
        }
        
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            text = a.get_text(strip=True).lower()
            
            if 'about' in href or 'about' in text:
                links['about'] = urljoin(base_url, a['href'])
            elif 'career' in href or 'job' in href or 'career' in text:
                links['careers'] = urljoin(base_url, a['href'])
            elif 'blog' in href or 'blog' in text:
                links['blog'] = urljoin(base_url, a['href'])
            elif 'contact' in href or 'contact' in text:
                links['contact'] = urljoin(base_url, a['href'])
        
        return links
    
    def _detect_tech_stack(self, html: str, soup: BeautifulSoup) -> list[str]:
        """Detect technologies used"""
        tech = []
        
        # Check for common frameworks/libraries
        tech_patterns = {
            'React': r'react',
            'Vue.js': r'vue',
            'Angular': r'angular',
            'WordPress': r'wp-content|wordpress',
            'Shopify': r'shopify',
            'Google Analytics': r'google-analytics|gtag',
            'Stripe': r'stripe',
            'Intercom': r'intercom',
            'HubSpot': r'hubspot',
        }
        
        html_lower = html.lower()
        for tech_name, pattern in tech_patterns.items():
            if re.search(pattern, html_lower):
                tech.append(tech_name)
        
        return tech
    
    def _empty_result(self, url: str) -> dict:
        """Return empty result structure"""
        return {
            'url': url,
            'title': '',
            'description': '',
            'about': '',
            'products': [],
            'value_props': [],
            'meta_info': {},
            'links': {},
            'tech_stack': [],
        }
    
    async def scrape_careers_page(self, careers_url: Optional[str]) -> list[dict]:
        """Scrape careers page for job postings"""
        if not careers_url:
            logger.info("No careers URL provided")
            return []
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(careers_url, timeout=self.timeout, allow_redirects=True) as response:
                    if response.status != 200:
                        logger.warning(f"Careers page returned {response.status}")
                        return []
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    jobs = []
                    
                    # Strategy 1: Look for common job posting class patterns
                    job_elements = soup.find_all(['div', 'li', 'article', 'tr'], 
                                                class_=re.compile('job|position|role|opening|listing|posting', re.I),
                                                limit=25)
                    
                    for elem in job_elements:
                        title_elem = elem.find(['h1', 'h2', 'h3', 'h4', 'a', 'span'])
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            if title and 10 < len(title) < 150:  # Reasonable title length
                                # Skip navigation/footer links
                                if not any(skip in title.lower() for skip in ['view all', 'see all', 'apply now', 'learn more', 'read more']):
                                    dept = self._extract_department(title)
                                    jobs.append({
                                        'title': title,
                                        'department': dept,
                                    })
                    
                    # Strategy 2: If no jobs found, look for table rows
                    if len(jobs) == 0:
                        table_rows = soup.find_all('tr')
                        for row in table_rows:
                            cells = row.find_all(['td', 'th'])
                            if len(cells) >= 2:
                                # First cell usually has title
                                title = cells[0].get_text(strip=True)
                                if title and 10 < len(title) < 150:
                                    dept = self._extract_department(title)
                                    jobs.append({
                                        'title': title,
                                        'department': dept,
                                    })
                    
                    # Strategy 3: Look for any links that look like job titles
                    if len(jobs) == 0:
                        all_links = soup.find_all('a', href=True)
                        for link in all_links:
                            text = link.get_text(strip=True)
                            href = link.get('href', '')
                            # Job titles usually have job/position in URL or have specific length
                            if (('job' in href.lower() or 'position' in href.lower() or 'career' in href.lower()) 
                                and 10 < len(text) < 150):
                                dept = self._extract_department(text)
                                jobs.append({
                                    'title': text,
                                    'department': dept,
                                })
                    
                    # Remove duplicates
                    seen = set()
                    unique_jobs = []
                    for job in jobs:
                        if job['title'] not in seen:
                            seen.add(job['title'])
                            unique_jobs.append(job)
                    
                    logger.info(f"Found {len(unique_jobs)} job postings from careers page")
                    return unique_jobs[:20]  # Max 20 jobs
        except Exception as e:
            logger.error(f"Error scraping careers page {careers_url}: {str(e)}")
            return []
    
    def _extract_department(self, job_title: str) -> str:
        """Extract department from job title"""
        title_lower = job_title.lower()
        
        dept_keywords = {
            'Engineering': ['engineer', 'developer', 'backend', 'frontend', 'fullstack', 'devops', 'sre'],
            'Sales': ['sales', 'account executive', 'business development', 'bdr', 'sdr'],
            'Marketing': ['marketing', 'content', 'seo', 'growth'],
            'Product': ['product manager', 'product owner'],
            'Design': ['designer', 'ux', 'ui'],
            'Data': ['data scientist', 'data analyst', 'data engineer'],
            'Operations': ['operations', 'ops'],
            'HR': ['hr', 'human resources', 'people'],
            'Finance': ['finance', 'accounting'],
            'Customer Success': ['customer success', 'support', 'customer service'],
        }
        
        for dept, keywords in dept_keywords.items():
            if any(kw in title_lower for kw in keywords):
                return dept
        
        return 'Other'
