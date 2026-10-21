import asyncio
import time
import os
import logging
from typing import Optional
from datetime import datetime

from app.models.company import Company, CompanyProfile
from app.models.signals import Signals, HiringSignal, NewsSignal
from app.models.scoring import IntentScore, ScoreBreakdown
from app.models.gaps import Gap, GapAnalysis
from app.models.outreach import OutreachMessage
from app.models.research import ResearchResult, ResearchMetadata, Source
from app.scrapers.web_scraper import WebScraper
from app.scrapers.tavily_search import TavilySearcher
from app.utils.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class ResearchAgent:
    """Main agent orchestrating company research"""
    
    def __init__(self):
        self.scraper = WebScraper()
        self.searcher = TavilySearcher()
        
        # Try Google Gemini first (free), fallback to OpenAI
        gemini_key = os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if gemini_key and gemini_key != "your_google_api_key_here":
            # Use Google Gemini (FREE!)
            self.client = GeminiClient(api_key=gemini_key)
            self.llm_type = "gemini"
            logger.info("✓ Using Google Gemini for research (FREE)")
        elif openai_key and openai_key != "your_openai_api_key_here":
            # Fallback to OpenAI
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                api_key=openai_key
            )
            self.llm_type = "openai"
            logger.info("✓ Using OpenAI GPT-4 for research")
        else:
            raise ValueError("No AI API key configured. Add GOOGLE_API_KEY or OPENAI_API_KEY to .env")
    
    async def research_company(
        self,
        company_url: str,
        company_name: Optional[str] = None,
        research_depth: str = "standard"
    ) -> ResearchResult:
        """Execute full research pipeline"""
        start_time = time.time()
        research_id = f"res_{int(time.time())}"
        
        logger.info(f"Starting research for {company_url}")
        
        try:
            # Step 1: Scrape company website
            website_data = await self.scraper.scrape_company_website(company_url)
            
            # Extract company name if not provided
            if not company_name:
                company_name = self._extract_company_name(company_url, website_data)
            
            # Step 2: Search for additional intelligence
            news_results = await self.searcher.search_company_news(company_name, limit=5)
            company_info = await self.searcher.search_company_info(company_name, company_url)
            
            # Step 3: Scrape careers page if available
            careers_url = website_data.get('links', {}).get('careers')
            jobs = await self.scraper.scrape_careers_page(careers_url)
            
            # Fallback: If no jobs found from careers page, search for hiring data
            if len(jobs) == 0:
                logger.info(f"No jobs from careers page, searching for hiring signals")
                hiring_results = await self.searcher.search(
                    f'"{company_name}" hiring jobs openings positions',
                    limit=3
                )
                
                # Extract job titles from search results
                for result in hiring_results:
                    content = result.get('content', '')
                    title = result.get('title', '')
                    
                    # Look for job title patterns in content
                    import re
                    job_patterns = [
                        r'hiring (?:for |a )?([A-Z][a-z]+(?: [A-Z][a-z]+){0,4})',
                        r'looking for (?:an? )?([A-Z][a-z]+(?: [A-Z][a-z]+){0,4})',
                        r'open positions?: ([A-Z][a-z]+(?: [A-Z][a-z]+){0,4})',
                    ]
                    
                    for pattern in job_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches[:3]:  # Max 3 per result
                            job_title = match if isinstance(match, str) else ' '.join(match)
                            if 5 < len(job_title) < 100:
                                dept = self.scraper._extract_department(job_title)
                                jobs.append({
                                    'title': job_title,
                                    'department': dept,
                                })
                
                logger.info(f"Found {len(jobs)} jobs from search fallback")
            
            # Step 4: Build company profile
            company = self._build_company_profile(
                company_url,
                company_name,
                website_data,
                company_info,
                research_id
            )
            
            # Step 5: Extract signals
            signals = self._extract_signals(website_data, news_results, jobs)
            
            # Step 6: Calculate intent score
            intent_score = self._calculate_intent_score(signals, company)
            
            # Step 7: AI-powered gap analysis
            gaps = await self._analyze_gaps(company, signals, website_data)
            
            # Step 8: Generate personalized messages
            messages = await self._generate_outreach_messages(company, gaps, signals)
            
            # Step 9: Compile sources
            sources = self._compile_sources(company_url, careers_url, news_results)
            
            # Calculate metrics
            elapsed_time = time.time() - start_time
            metadata = ResearchMetadata(
                research_time_seconds=round(elapsed_time, 2),
                tokens_used=5000,  # Approximate
                cost_usd=0.02,
                research_depth=research_depth
            )
            
            return ResearchResult(
                id=research_id,
                status="completed",
                company=company,
                signals=signals,
                intent_score=intent_score,
                gaps=gaps,
                outreach_messages=messages,
                sources=sources,
                metadata=metadata
            )
        
        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            elapsed_time = time.time() - start_time
            
            return ResearchResult(
                id=research_id,
                status="failed",
                company=Company(
                    id=research_id,
                    name=company_name or "Unknown",
                    url=company_url
                ),
                signals=Signals(),
                intent_score=IntentScore(overall=0, breakdown={}, recommendation="ERROR"),
                gaps=GapAnalysis(
                    primary=Gap(title="Research Failed", description=str(e), severity="HIGH")
                ),
                outreach_messages=[],
                sources=[],
                metadata=ResearchMetadata(research_time_seconds=elapsed_time),
                error=str(e)
            )
    
    def _extract_company_name(self, url: str, website_data: dict) -> str:
        """Extract company name from URL or website data"""
        # Try from title first
        title = website_data.get('title', '')
        if title:
            # Clean up title
            name = title.split('|')[0].split('-')[0].strip()
            if name:
                return name
        
        # Fallback: extract from domain
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace('www.', '')
        name = domain.split('.')[0].capitalize()
        return name
    
    def _build_company_profile(
        self,
        url: str,
        name: str,
        website_data: dict,
        search_info: dict,
        company_id: str
    ) -> Company:
        """Build company profile from collected data"""
        return Company(
            id=company_id,
            name=name,
            url=url,
            industry=search_info.get('industry') or self._detect_industry(website_data),
            location=website_data.get('meta_info', {}).get('location') or search_info.get('location'),
            size=search_info.get('size'),
            description=website_data.get('description') or self._generate_description(website_data),
            founded=website_data.get('meta_info', {}).get('founded'),
            funding=search_info.get('funding'),
            tech_stack=website_data.get('tech_stack', []),
            competitors=[]
        )
    
    def _detect_industry(self, website_data: dict) -> str:
        """Detect industry from website content"""
        text = (website_data.get('about', '') + ' ' + 
                website_data.get('description', '')).lower()
        
        if any(kw in text for kw in ['saas', 'software', 'platform', 'cloud']):
            return 'SaaS / Software'
        elif any(kw in text for kw in ['ai', 'artificial intelligence', 'machine learning']):
            return 'AI / ML'
        elif any(kw in text for kw in ['ecommerce', 'e-commerce', 'retail', 'shop']):
            return 'E-commerce'
        elif any(kw in text for kw in ['fintech', 'finance', 'payment', 'banking']):
            return 'Fintech'
        else:
            return 'Technology'
    
    def _generate_description(self, website_data: dict) -> str:
        """Generate one-line description"""
        desc = website_data.get('description', '')
        if desc:
            return desc[:200]
        
        about = website_data.get('about', '')
        if about:
            return about[:200]
        
        return "Technology company"
    
    def _extract_signals(
        self,
        website_data: dict,
        news_results: list,
        jobs: list
    ) -> Signals:
        """Extract buying signals"""
        hiring_signals = []
        for job in jobs:
            hiring_signals.append(HiringSignal(
                title=job['title'],
                department=job['department'],
                signal=self._interpret_hiring_signal(job['title'], job['department'])
            ))
        
        news_signals = []
        for news in news_results:
            news_signals.append(NewsSignal(
                title=news['title'],
                date=datetime.utcnow().strftime('%Y-%m-%d'),
                url=news['url'],
                relevance=self._assess_news_relevance(news['title'], news['content'])
            ))
        
        return Signals(
            hiring=hiring_signals,
            news=news_signals,
            tech_stack=website_data.get('tech_stack', []),
            competitors_detected=[],
            recent_activities=[]
        )
    
    def _interpret_hiring_signal(self, title: str, department: str) -> str:
        """Interpret what a hiring signal means"""
        title_lower = title.lower()
        
        if department == 'Sales':
            return "Scaling outbound sales motion"
        elif department == 'Engineering':
            if 'senior' in title_lower or 'lead' in title_lower:
                return "Building technical leadership"
            return "Expanding engineering team"
        elif department == 'Marketing':
            return "Investing in growth initiatives"
        elif department == 'Product':
            return "Expanding product capabilities"
        else:
            return f"Growing {department} function"
    
    def _assess_news_relevance(self, title: str, content: str) -> str:
        """Assess relevance of news"""
        text = (title + ' ' + content).lower()
        
        if 'funding' in text or 'raised' in text:
            return "Funding event - likely have budget"
        elif 'launch' in text or 'released' in text:
            return "Product launch - in growth phase"
        elif 'partnership' in text or 'partner' in text:
            return "Partnership - expanding ecosystem"
        else:
            return "General news"
    
    def _calculate_intent_score(self, signals: Signals, company: Company) -> IntentScore:
        """Calculate buying intent score"""
        breakdown = {}
        
        # Hiring signals (0-25)
        hiring_score = min(len(signals.hiring) * 5, 25)
        hiring_evidence = [f"{h.title} - {h.signal}" for h in signals.hiring[:3]]
        breakdown['hiring_signals'] = ScoreBreakdown(
            category="Hiring Signals",
            score=hiring_score,
            max_score=25,
            evidence=hiring_evidence,
            reasoning="Active hiring indicates growth and new initiatives"
        )
        
        # Funding & growth (0-20)
        funding_score = 15 if company.funding else 0
        breakdown['funding_growth'] = ScoreBreakdown(
            category="Funding & Growth",
            score=funding_score,
            max_score=20,
            evidence=[company.funding] if company.funding else [],
            reasoning="Recent funding means available budget"
        )
        
        # News signals (0-20)
        news_score = min(len(signals.news) * 5, 20)
        news_evidence = [n.title for n in signals.news[:3]]
        breakdown['news_activity'] = ScoreBreakdown(
            category="News & Activity",
            score=news_score,
            max_score=20,
            evidence=news_evidence,
            reasoning="Recent news indicates active company"
        )
        
        # Tech stack (0-15)
        tech_score = min(len(signals.tech_stack) * 3, 15)
        breakdown['tech_presence'] = ScoreBreakdown(
            category="Tech Presence",
            score=tech_score,
            max_score=15,
            evidence=signals.tech_stack,
            reasoning="Tech stack visibility indicates maturity"
        )
        
        # Timing (0-20)
        timing_score = 10  # Default baseline
        breakdown['timing'] = ScoreBreakdown(
            category="Timing",
            score=timing_score,
            max_score=20,
            evidence=["Company actively operating"],
            reasoning="Current market conditions"
        )
        
        overall = sum(b.score for b in breakdown.values())
        
        if overall >= 70:
            recommendation = "HIGH PRIORITY"
        elif overall >= 40:
            recommendation = "MEDIUM PRIORITY"
        else:
            recommendation = "LOW PRIORITY"
        
        return IntentScore(
            overall=overall,
            breakdown=breakdown,
            recommendation=recommendation,
            summary=f"Score {overall}/100 based on {len(breakdown)} factors"
        )
    
    async def _call_llm(self, prompt: str) -> str:
        """Helper method to call either Gemini or OpenAI"""
        if self.llm_type == "gemini":
            return self.client.generate_content(prompt)
        else:
            from langchain_core.prompts import ChatPromptTemplate
            prompt_template = ChatPromptTemplate.from_template(prompt)
            response = await self.llm.ainvoke(prompt_template.format_messages())
            return response.content
    
    async def _analyze_gaps(
        self,
        company: Company,
        signals: Signals,
        website_data: dict
    ) -> GapAnalysis:
        """Use AI to identify strategic gaps"""
        hiring_summary = "; ".join([f"{h.title} ({h.department})" for h in signals.hiring[:5]])
        website_excerpt = website_data.get('about', '')[:500]
        
        prompt = f"""Analyze {company.name} and identify their #1 business gap or challenge.

Company: {company.name}
Industry: {company.industry or 'Unknown'}
Description: {company.description or 'No description'}
Hiring: {hiring_summary or 'No hiring data'}
Recent Funding: {company.funding or 'None detected'}
Size: {company.size or 'Unknown'}
Tech Stack: {", ".join(signals.tech_stack) or 'Unknown'}

RULES:
1. Keep title under 6 words
2. Description must be 1-2 sentences max
3. Be specific to THIS company, not generic
4. Use evidence from the data above
5. Make it actionable - what should they do?

Format:
PRIMARY GAP:
Title: [4-6 words, no jargon]
Description: [1-2 specific sentences about their actual challenge]
Evidence: [2-3 bullet points from data above]
Severity: HIGH

SECONDARY GAPS (2 only):
1. Title: [One specific challenge]
2. Title: [One specific challenge]"""
        
        try:
            content = await self._call_llm(prompt)
            logger.info(f"Gap analysis AI response received ({len(content)} chars)")
            logger.debug(f"Raw response: {content[:500]}")  # Log first 500 chars
            gaps = self._parse_gap_response(content)
            logger.info(f"✓ Gap analysis completed for {company.name}: {gaps.primary.title}")
            return gaps
        
        except Exception as e:
            logger.error(f"Gap analysis failed for {company.name}: {str(e)}")
            
            # Generate rule-based fallback gap analysis
            fallback_gap = self._generate_fallback_gap(company, signals, hiring_summary)
            logger.info(f"Using fallback gap analysis for {company.name}")
            return fallback_gap
    
    def _generate_fallback_gap(
        self,
        company: Company,
        signals: Signals,
        hiring_summary: str
    ) -> GapAnalysis:
        """Generate rule-based gap analysis when AI is unavailable"""
        
        # Determine primary gap based on available data
        if signals.hiring and len(signals.hiring) >= 3:
            # Active hiring suggests scaling challenges
            primary = Gap(
                title="Scaling Team Quickly",
                description=f"Hiring {len(signals.hiring)} roles across {len(set(h.department for h in signals.hiring))} departments. Fast growth often creates coordination and onboarding challenges.",
                evidence=[
                    f"{len(signals.hiring)} open positions",
                    f"Departments: {', '.join(set(h.department for h in signals.hiring[:3]))}",
                    "Rapid team expansion phase"
                ],
                severity="HIGH",
                actionable_insight="Fast-growing teams need tools for coordination, onboarding, and maintaining productivity"
            )
            secondary = [
                Gap(
                    title="New Hire Onboarding",
                    description="Getting new team members productive quickly",
                    evidence=[f"{len(signals.hiring)} positions to fill"],
                    severity="MEDIUM"
                ),
                Gap(
                    title="Team Communication",
                    description="Maintaining alignment as team grows",
                    evidence=["Growing headcount"],
                    severity="MEDIUM"
                )
            ]
        
        elif company.funding:
            # Recent funding suggests capital deployment
            primary = Gap(
                title="Deploying Capital Efficiently",
                description=f"Recently raised {company.funding}. Need to deploy capital strategically across hiring, product, and go-to-market to hit growth milestones.",
                evidence=[
                    f"Funding: {company.funding}",
                    "Post-funding execution phase",
                    "Growth capital available"
                ],
                severity="HIGH",
                actionable_insight="Post-funding companies need efficiency tools to maximize runway and hit key metrics"
            )
            secondary = [
                Gap(
                    title="Resource Prioritization",
                    description="Deciding where to invest for maximum impact",
                    evidence=["Recent capital raise"],
                    severity="MEDIUM"
                ),
                Gap(
                    title="Growth Tracking",
                    description="Measuring ROI on capital deployment",
                    evidence=["Active investment phase"],
                    severity="MEDIUM"
                )
            ]
        
        elif signals.news and len(signals.news) >= 2:
            # Recent news suggests momentum
            primary = Gap(
                title="Capitalizing on Momentum",
                description=f"Recent visibility ({len(signals.news)} mentions) creates opportunity. Need to convert attention into pipeline before market moves on.",
                evidence=[n.title for n in signals.news[:2]] + ["Active media presence"],
                severity="MEDIUM",
                actionable_insight="Companies with momentum need to move fast - right tools enable speed"
            )
            secondary = [
                Gap(
                    title="Lead Conversion Speed",
                    description="Converting inbound interest quickly",
                    evidence=["Recent visibility"],
                    severity="MEDIUM"
                )
            ]
        
        else:
            # Limited data - focus on market visibility
            primary = Gap(
                title="Market Visibility",
                description=f"Limited public presence detected. {company.industry or 'Technology'} companies need visibility to attract customers and talent.",
                evidence=[
                    "Minimal hiring signals",
                    "Few news mentions",
                    "Limited online footprint"
                ],
                severity="MEDIUM",
                actionable_insight="Direct outreach recommended - limited public data suggests stealth mode or early stage"
            )
            secondary = [
                Gap(
                    title="Brand Awareness",
                    description="Building market presence",
                    evidence=["Limited visibility"],
                    severity="LOW"
                )
            ]
        
        return GapAnalysis(primary=primary, secondary=secondary)
    
    def _parse_gap_response(self, content: str) -> GapAnalysis:
        """Parse AI gap analysis response"""
        try:
            # Initialize defaults
            primary_title = None
            primary_desc = None
            primary_evidence = []
            primary_severity = "MEDIUM"
            secondary_gaps = []
            
            # Split by lines and clean
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Strategy 1: Look for clear section markers
            in_primary = False
            in_secondary = False
            current_field = None
            
            for i, line in enumerate(lines):
                line_upper = line.upper()
                
                # Detect sections
                if 'PRIMARY' in line_upper and 'GAP' in line_upper:
                    in_primary = True
                    in_secondary = False
                    continue
                elif 'SECONDARY' in line_upper and 'GAP' in line_upper:
                    in_secondary = True
                    in_primary = False
                    continue
                
                # Extract primary gap fields
                if in_primary:
                    if line.startswith('Title:'):
                        primary_title = line.split(':', 1)[1].strip()
                        current_field = 'title'
                    elif line.startswith('Description:'):
                        primary_desc = line.split(':', 1)[1].strip()
                        current_field = 'desc'
                    elif line.startswith('Evidence:'):
                        current_field = 'evidence'
                        # Check if evidence is on same line
                        if len(line.split(':', 1)) > 1:
                            evidence_text = line.split(':', 1)[1].strip()
                            if evidence_text:
                                primary_evidence.append(evidence_text)
                    elif line.startswith('Severity:'):
                        severity_text = line.split(':', 1)[1].strip().upper()
                        if 'HIGH' in severity_text:
                            primary_severity = 'HIGH'
                        elif 'LOW' in severity_text:
                            primary_severity = 'LOW'
                        current_field = None
                    elif current_field == 'desc' and not line.startswith(('Evidence:', 'Severity:', 'Title:')):
                        # Continue description
                        primary_desc += ' ' + line
                    elif current_field == 'evidence' and line.startswith(('-', '•', '*', '1.', '2.', '3.')):
                        # Evidence bullet point
                        primary_evidence.append(line.lstrip('-•*123. '))
                
                # Extract secondary gaps
                if in_secondary:
                    if line.startswith(('1.', '2.', '-', '•', '*')):
                        gap_text = line.lstrip('12.-•* ')
                        # Extract title (before colon if present)
                        if ':' in gap_text:
                            title = gap_text.split(':')[0].strip()
                        else:
                            title = gap_text[:80]  # First part
                        
                        if title:
                            secondary_gaps.append(Gap(
                                title=title,
                                description="Additional opportunity identified",
                                evidence=["AI analysis"],
                                severity="LOW"
                            ))
            
            # Strategy 2: If no clear structure, extract from unstructured text
            if not primary_title:
                # Look for first meaningful sentence as title
                for line in lines[:10]:  # Check first 10 lines
                    if len(line) > 10 and len(line) < 100 and not ':' in line:
                        primary_title = line
                        break
                
                # If still nothing, use first short line after "gap" mention
                if not primary_title:
                    for i, line in enumerate(lines):
                        if 'gap' in line.lower() and i + 1 < len(lines):
                            next_line = lines[i + 1]
                            if 10 < len(next_line) < 100:
                                primary_title = next_line
                                break
            
            # Extract description from middle paragraphs
            if not primary_desc:
                # Find longer text blocks
                for line in lines:
                    if len(line) > 50 and not line.startswith(('Title:', 'Description:', 'Evidence:', 'Severity:', 'PRIMARY', 'SECONDARY')):
                        primary_desc = line[:500]
                        break
            
            # Clean up and finalize
            primary_title = primary_title[:100] if primary_title else "Strategic Gap"
            primary_desc = primary_desc[:500] if primary_desc else "Review analysis for detailed insights"
            primary_evidence = primary_evidence[:5] if primary_evidence else ["AI analysis completed"]
            
            logger.info(f"Parsed gap - Title: '{primary_title}', Evidence count: {len(primary_evidence)}")
            
            primary = Gap(
                title=primary_title,
                description=primary_desc,
                evidence=primary_evidence,
                severity=primary_severity,
                actionable_insight="Focus outreach on this specific challenge"
            )
            
            return GapAnalysis(primary=primary, secondary=secondary_gaps[:2])
            
        except Exception as e:
            logger.error(f"Error parsing gap response: {str(e)}")
            logger.debug(f"Failed content: {content[:200]}")
            # Return minimal gap with actual content
            return GapAnalysis(
                primary=Gap(
                    title="Growth Opportunity",
                    description=content[:300] if content else "Analysis complete",
                    evidence=["AI analysis"],
                    severity="MEDIUM"
                ),
                secondary=[]
            )
    
    async def _generate_outreach_messages(
        self,
        company: Company,
        gaps: GapAnalysis,
        signals: Signals
    ) -> list[OutreachMessage]:
        """Generate personalized outreach messages"""
        hiring_summary = signals.hiring[0].title if signals.hiring else "None detected"
        
        prompt = f"""You are writing a cold outreach message to {company.name}.

Company Context:
- Industry: {company.industry or 'Unknown'}
- Description: {company.description or 'Technology company'}
- Primary Gap: {gaps.primary.title} - {gaps.primary.description}
- Hiring: {hiring_summary}

Write a personalized outreach message that:
1. Leads with THEIR problem, not your product
2. References specific, researched details
3. Is under 120 words
4. Ends with a low-friction question (not a meeting request)
5. Sounds conversational, not corporate

Write 3 variants:
1. GAP-BASED: Lead with the identified gap
2. CURIOSITY-BASED: Lead with an interesting observation/question
3. TIMING-BASED: Lead with a recent event or trend

Format each as:
[TYPE]
Subject: [subject line]
Message: [body]
---
"""
        
        try:
            content = await self._call_llm(prompt)
            messages = self._parse_message_response(content)
            logger.info(f"✓ Generated {len(messages)} outreach messages for {company.name}")
            return messages
        
        except Exception as e:
            logger.error(f"Message generation failed for {company.name}: {str(e)}")
            
            # Generate rule-based fallback messages
            fallback_messages = self._generate_fallback_messages(company, gaps, signals)
            logger.info(f"Using fallback message generation for {company.name}")
            return fallback_messages
    
    def _generate_fallback_messages(
        self,
        company: Company,
        gaps: GapAnalysis,
        signals: Signals
    ) -> list[OutreachMessage]:
        """Generate rule-based outreach messages when AI is unavailable"""
        
        messages = []
        
        # Message 1: Gap-based
        gap_msg = f"""Hey [Name],

I was researching {company.name} and noticed {gaps.primary.title.lower()}.

{gaps.primary.description[:150]}...

Has this come up in your planning discussions? Would love to hear your perspective.

Best,
[Your name]"""
        
        messages.append(OutreachMessage(
            type="gap-based",
            subject=f"Question about {company.name}'s {gaps.primary.title.lower()}",
            message=gap_msg,
            word_count=len(gap_msg.split()),
            references=[gaps.primary.title]
        ))
        
        # Message 2: Hiring-based (if hiring data available)
        if signals.hiring and len(signals.hiring) > 0:
            hiring_msg = f"""Hey [Name],

Saw you're hiring for {signals.hiring[0].title} at {company.name}. That's usually a sign of {signals.hiring[0].signal.lower()}.

I work with companies in similar growth phases - curious what's driving the expansion?

Worth a quick chat?

Best,
[Your name]"""
            
            messages.append(OutreachMessage(
                type="curiosity-based",
                subject=f"Noticed the {signals.hiring[0].title} role",
                message=hiring_msg,
                word_count=len(hiring_msg.split()),
                references=[signals.hiring[0].title]
            ))
        else:
            # Curiosity-based without hiring
            curiosity_msg = f"""Hey [Name],

Been following {company.name}'s work in {company.industry or 'your space'}.

{company.description[:100] if company.description else 'Interesting approach to the market'}.

What's the biggest operational challenge you're tackling right now?

Best,
[Your name]"""
            
            messages.append(OutreachMessage(
                type="curiosity-based",
                subject=f"Quick question about {company.name}",
                message=curiosity_msg,
                word_count=len(curiosity_msg.split()),
                references=[]
            ))
        
        # Message 3: Timing-based
        if company.funding:
            timing_msg = f"""Hey [Name],

Congrats on {company.funding}. That's exciting momentum.

Post-funding execution is always interesting - how are you thinking about deploying capital across team, product, and go-to-market?

Would love to exchange notes if you have 15 mins.

Best,
[Your name]"""
            
            messages.append(OutreachMessage(
                type="timing-based",
                subject=f"Congrats on the funding",
                message=timing_msg,
                word_count=len(timing_msg.split()),
                references=[company.funding]
            ))
        
        elif signals.news and len(signals.news) > 0:
            timing_msg = f"""Hey [Name],

Saw the recent news about {company.name}: "{signals.news[0].title[:60]}..."

{signals.news[0].relevance} - what's the story behind it?

Happy to share what we're seeing in the market if useful.

Best,
[Your name]"""
            
            messages.append(OutreachMessage(
                type="timing-based",
                subject=f"Saw the news about {company.name}",
                message=timing_msg,
                word_count=len(timing_msg.split()),
                references=[signals.news[0].title]
            ))
        else:
            # Generic timing message
            timing_msg = f"""Hey [Name],

Been seeing a lot of momentum in {company.industry or 'your industry'} lately.

How is {company.name} thinking about the next 6-12 months? Any major initiatives kicking off?

Would be great to connect briefly.

Best,
[Your name]"""
            
            messages.append(OutreachMessage(
                type="timing-based",
                subject=f"Market trends in {company.industry or 'your space'}",
                message=timing_msg,
                word_count=len(timing_msg.split()),
                references=[]
            ))
        
        return messages
    
    def _parse_message_response(self, content: str) -> list[OutreachMessage]:
        """Parse AI message generation response"""
        messages = []
        
        # Simple split by --- (production would be more robust)
        variants = content.split('---')
        
        for i, variant in enumerate(variants[:3]):
            if not variant.strip():
                continue
            
            # Extract subject and message (simplified)
            lines = variant.strip().split('\n')
            
            msg_type = "gap-based" if i == 0 else "curiosity-based" if i == 1 else "timing-based"
            subject = "Quick question"
            message_body = variant.strip()
            
            # Try to extract subject
            for line in lines:
                if line.lower().startswith('subject:'):
                    subject = line.split(':', 1)[1].strip()
                    break
            
            messages.append(OutreachMessage(
                type=msg_type,
                subject=subject,
                message=message_body,
                word_count=len(message_body.split()),
                references=[]
            ))
        
        return messages if messages else [
            OutreachMessage(
                type="gap-based",
                subject="Quick question",
                message="[Message generation in progress]",
                word_count=0,
                references=[]
            )
        ]
    
    def _compile_sources(
        self,
        company_url: str,
        careers_url: Optional[str],
        news_results: list
    ) -> list[Source]:
        """Compile all data sources"""
        sources = [
            Source(
                url=company_url,
                scraped_at=datetime.utcnow(),
                type="website",
                status="success"
            )
        ]
        
        if careers_url:
            sources.append(Source(
                url=careers_url,
                scraped_at=datetime.utcnow(),
                type="jobs",
                status="success"
            ))
        
        for news in news_results[:3]:
            sources.append(Source(
                url=news['url'],
                scraped_at=datetime.utcnow(),
                type="news",
                status="success"
            ))
        
        return sources
