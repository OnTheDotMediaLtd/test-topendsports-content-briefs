"""
Demo Mode - Load cached API responses for testing without live APIs.

This module allows running the content brief generator and keyword research
without requiring active API keys (Ahrefs, etc). It loads pre-cached
responses from data/demo-cache/*.json files.

Usage:
    from src.demo_mode import get_demo_keyword_data, is_demo_available
    
    # Check if demo data exists for a URL
    if is_demo_available(url):
        data = get_demo_keyword_data(url)
        print(f"Primary keyword: {data['primary_keyword']['keyword']}")

The demo cache files simulate Ahrefs API responses with realistic
keyword research, competitor analysis, and FAQ questions for
TopEndSports.com betting pages.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


# Map URLs to cache file names
URL_TO_CACHE_MAP = {
    "https://www.topendsports.com/sport/betting/index.htm": "best-sports-betting-sites.json",
    "https://www.topendsports.com/sport/betting/best-apps.htm": "best-betting-apps.json",
    "https://www.topendsports.com/sport/betting/fanduel-review.htm": "fanduel-review.json",
}


@dataclass
class KeywordData:
    """Represents keyword research data."""
    keyword: str
    volume: int
    difficulty: int = 0
    placement: str = "content"
    is_question: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyword": self.keyword,
            "volume": self.volume,
            "difficulty": self.difficulty,
            "placement": self.placement,
            "is_question": self.is_question
        }


@dataclass
class CompetitorData:
    """Represents competitor analysis data."""
    domain: str
    url: str
    position: int = 0
    traffic: int = 0
    top_keyword: str = ""
    keywords_in_common: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "url": self.url,
            "position": self.position,
            "traffic": self.traffic,
            "top_keyword": self.top_keyword,
            "keywords_in_common": self.keywords_in_common
        }


@dataclass
class DemoResearchResult:
    """Complete research result from demo cache."""
    primary_keyword: KeywordData
    secondary_keywords: List[KeywordData] = field(default_factory=list)
    content_gap_keywords: List[KeywordData] = field(default_factory=list)
    faq_questions: List[str] = field(default_factory=list)
    competitors: List[CompetitorData] = field(default_factory=list)
    total_cluster_volume: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_keyword": self.primary_keyword.to_dict(),
            "secondary_keywords": [kw.to_dict() for kw in self.secondary_keywords],
            "content_gap_keywords": [kw.to_dict() for kw in self.content_gap_keywords],
            "faq_questions": self.faq_questions,
            "competitors": [c.to_dict() for c in self.competitors],
            "total_cluster_volume": self.total_cluster_volume
        }


def get_demo_cache_dir() -> Path:
    """Get the demo cache directory path."""
    return Path(__file__).parent.parent / "data" / "demo-cache"


def list_available_demo_pages() -> List[str]:
    """List URLs that have demo cache available."""
    return list(URL_TO_CACHE_MAP.keys())


def is_demo_available(url: str) -> bool:
    """Check if demo data exists for the given URL."""
    if url not in URL_TO_CACHE_MAP:
        return False
    
    cache_file = get_demo_cache_dir() / URL_TO_CACHE_MAP[url]
    return cache_file.exists()


def load_demo_cache(url: str) -> Optional[Dict[str, Any]]:
    """
    Load cached demo data for a URL.
    
    Args:
        url: The URL to load demo data for
        
    Returns:
        Cached data dict or None if not available
    """
    if url not in URL_TO_CACHE_MAP:
        return None
    
    cache_file = get_demo_cache_dir() / URL_TO_CACHE_MAP[url]
    
    if not cache_file.exists():
        return None
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_demo_keyword_data(url: str) -> Optional[Dict[str, Any]]:
    """
    Get keyword research data from demo cache.
    
    Returns the raw cache data in a format similar to Ahrefs API responses.
    
    Args:
        url: The URL to get keyword data for
        
    Returns:
        Dictionary with keyword research data or None if not available
    """
    return load_demo_cache(url)


def get_demo_research_result(url: str) -> Optional[DemoResearchResult]:
    """
    Get a complete DemoResearchResult from demo cache.
    
    This parses the cached JSON into structured dataclass objects.
    
    Args:
        url: The URL to research
        
    Returns:
        DemoResearchResult object or None if no cache available
    """
    cache = load_demo_cache(url)
    if not cache:
        return None
    
    # Parse primary keyword
    pk_data = cache.get('primary_keyword', {})
    primary_keyword = KeywordData(
        keyword=pk_data.get('keyword', ''),
        volume=pk_data.get('volume', 0),
        difficulty=pk_data.get('difficulty', 0),
        placement="H1"
    )
    
    # Parse secondary keywords
    secondary_keywords = []
    for kw in cache.get('secondary_keywords', []):
        secondary_keywords.append(KeywordData(
            keyword=kw.get('keyword', ''),
            volume=kw.get('volume', 0),
            difficulty=kw.get('difficulty', 0),
            placement=kw.get('placement', determine_placement(kw.get('volume', 0))),
            is_question=is_question_keyword(kw.get('keyword', ''))
        ))
    
    # Parse content gap keywords
    content_gap_keywords = []
    for kw in cache.get('content_gap_keywords', []):
        content_gap_keywords.append(KeywordData(
            keyword=kw.get('keyword', ''),
            volume=kw.get('volume', 0),
            difficulty=kw.get('difficulty', 0),
            placement=determine_placement(kw.get('volume', 0))
        ))
    
    # Parse FAQ questions
    faq_questions = cache.get('faq_questions', [])
    
    # Parse competitors
    competitors = []
    for comp in cache.get('competitors', []):
        competitors.append(CompetitorData(
            domain=comp.get('domain', ''),
            url=comp.get('url', ''),
            position=comp.get('position', 0),
            traffic=comp.get('traffic', 0),
            top_keyword=comp.get('top_keyword', ''),
            keywords_in_common=comp.get('keywords_in_common', 0)
        ))
    
    # Calculate total volume
    total_volume = primary_keyword.volume + sum(kw.volume for kw in secondary_keywords)
    
    return DemoResearchResult(
        primary_keyword=primary_keyword,
        secondary_keywords=secondary_keywords,
        content_gap_keywords=content_gap_keywords,
        faq_questions=faq_questions,
        competitors=competitors,
        total_cluster_volume=total_volume
    )


def determine_placement(volume: int) -> str:
    """
    Determine keyword placement based on search volume.
    
    Based on the Ahrefs Keyword Workflow guidelines.
    """
    if volume >= 1000:
        return "H2"
    elif volume >= 500:
        return "H2"
    elif volume >= 200:
        return "H3"
    elif volume >= 100:
        return "content"
    else:
        return "FAQ"


def is_question_keyword(keyword: str) -> bool:
    """Check if a keyword is a question format."""
    question_starters = ['what', 'how', 'why', 'when', 'where', 'which', 'is', 'are', 'can', 'do', 'does']
    keyword_lower = keyword.lower().strip()
    return any(keyword_lower.startswith(q + ' ') for q in question_starters) or keyword_lower.endswith('?')


def print_demo_mode_banner():
    """Print a banner indicating demo mode is active."""
    print()
    print("=" * 60)
    print("  🎭 DEMO MODE ACTIVE")
    print("  Using cached sample data - no live API calls")
    print("=" * 60)
    print()


def print_available_demo_pages():
    """Print list of URLs with available demo data."""
    print("\n📋 Available demo pages:")
    for url in list_available_demo_pages():
        cache_exists = "✅" if is_demo_available(url) else "❌"
        print(f"  {cache_exists} {url}")
    print()


def format_keyword_table(keywords: List[KeywordData]) -> str:
    """Format keywords as a markdown table for briefs."""
    if not keywords:
        return "No keywords available"
    
    lines = ["| Keyword | Volume | KD | Placement |",
             "|---------|--------|----|-----------|"]
    
    for kw in keywords:
        lines.append(f"| {kw.keyword} | {kw.volume:,} | {kw.difficulty} | {kw.placement} |")
    
    return "\n".join(lines)


def generate_demo_brief_section(url: str) -> Optional[str]:
    """
    Generate a complete keyword research section for a content brief using demo data.
    
    Args:
        url: The URL to generate the section for
        
    Returns:
        Markdown formatted keyword research section or None if not available
    """
    result = get_demo_research_result(url)
    if not result:
        return None
    
    section = f"""## Keyword Research Summary

### Primary Keyword
- **Keyword:** {result.primary_keyword.keyword}
- **Search Volume:** {result.primary_keyword.volume:,}/month
- **Keyword Difficulty:** {result.primary_keyword.difficulty}

### Secondary Keywords ({len(result.secondary_keywords)} identified)
{format_keyword_table(result.secondary_keywords)}

### Content Gap Keywords
{format_keyword_table(result.content_gap_keywords) if result.content_gap_keywords else "No content gaps identified"}

### FAQ Target Questions
"""
    
    for q in result.faq_questions:
        section += f"- {q}\n"
    
    section += f"""
### Competitor Analysis
| Domain | Traffic | Top Keyword | Position |
|--------|---------|-------------|----------|
"""
    
    for comp in result.competitors:
        section += f"| {comp.domain} | {comp.traffic:,} | {comp.top_keyword} | {comp.position} |\n"
    
    section += f"""
### Total Keyword Cluster Volume
- Primary: {result.primary_keyword.volume:,} searches/month
- Secondary total: {sum(kw.volume for kw in result.secondary_keywords):,} searches/month
- **Combined opportunity:** {result.total_cluster_volume:,} searches/month
"""
    
    return section
