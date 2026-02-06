"""
Tests for demo mode functionality.

These tests verify that demo mode can load cached API responses
and provide keyword research data without live API calls.
"""

import json
import pytest
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from demo_mode import (
    get_demo_cache_dir,
    list_available_demo_pages,
    is_demo_available,
    load_demo_cache,
    get_demo_keyword_data,
    get_demo_research_result,
    determine_placement,
    is_question_keyword,
    format_keyword_table,
    generate_demo_brief_section,
    KeywordData,
    CompetitorData,
    DemoResearchResult,
    URL_TO_CACHE_MAP,
)


class TestDemoCacheDirectory:
    """Tests for demo cache directory functionality."""
    
    def test_get_demo_cache_dir_returns_path(self):
        """Demo cache dir should return a Path object."""
        cache_dir = get_demo_cache_dir()
        assert isinstance(cache_dir, Path)
    
    def test_demo_cache_dir_exists(self):
        """Demo cache directory should exist."""
        cache_dir = get_demo_cache_dir()
        assert cache_dir.exists(), f"Demo cache directory not found: {cache_dir}"
    
    def test_demo_cache_dir_is_directory(self):
        """Demo cache path should be a directory."""
        cache_dir = get_demo_cache_dir()
        assert cache_dir.is_dir()


class TestURLMapping:
    """Tests for URL to cache file mapping."""
    
    def test_url_map_not_empty(self):
        """URL to cache map should have entries."""
        assert len(URL_TO_CACHE_MAP) > 0
    
    def test_list_available_demo_pages(self):
        """Should return list of demo page URLs."""
        pages = list_available_demo_pages()
        assert isinstance(pages, list)
        assert len(pages) > 0
        # All should be valid URLs
        for url in pages:
            assert url.startswith("https://")
            assert "topendsports.com" in url
    
    def test_mapped_urls_are_topendsports(self):
        """All mapped URLs should be TopEndSports.com pages."""
        for url in URL_TO_CACHE_MAP.keys():
            assert "topendsports.com" in url


class TestDemoAvailability:
    """Tests for checking demo data availability."""
    
    def test_is_demo_available_for_mapped_url(self):
        """Demo should be available for URLs with cache files."""
        # Get a URL that should have demo data
        test_url = list(URL_TO_CACHE_MAP.keys())[0]
        
        # Check if cache file exists
        cache_dir = get_demo_cache_dir()
        cache_file = cache_dir / URL_TO_CACHE_MAP[test_url]
        
        if cache_file.exists():
            assert is_demo_available(test_url) is True
    
    def test_is_demo_available_returns_false_for_unknown_url(self):
        """Demo should not be available for unmapped URLs."""
        unknown_url = "https://www.example.com/unknown-page"
        assert is_demo_available(unknown_url) is False
    
    def test_is_demo_available_returns_false_for_missing_file(self):
        """Demo should return False if cache file is missing."""
        # Test with a URL that might be mapped but file doesn't exist
        fake_url = "https://www.topendsports.com/sport/betting/nonexistent.htm"
        assert is_demo_available(fake_url) is False


class TestLoadDemoCache:
    """Tests for loading demo cache data."""
    
    def test_load_demo_cache_returns_dict(self):
        """Should return dict for valid cached URL."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            data = load_demo_cache(test_url)
            assert isinstance(data, dict)
    
    def test_load_demo_cache_returns_none_for_unknown(self):
        """Should return None for unknown URL."""
        data = load_demo_cache("https://example.com/unknown")
        assert data is None
    
    def test_load_demo_cache_has_required_fields(self):
        """Cached data should have required keyword research fields."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            data = load_demo_cache(test_url)
            assert "primary_keyword" in data
            assert "secondary_keywords" in data
            assert "faq_questions" in data
            assert "competitors" in data


class TestGetDemoKeywordData:
    """Tests for getting keyword data from demo cache."""
    
    def test_get_demo_keyword_data_returns_dict(self):
        """Should return keyword data dict."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            data = get_demo_keyword_data(test_url)
            assert isinstance(data, dict)
            assert "primary_keyword" in data


class TestGetDemoResearchResult:
    """Tests for getting structured research result."""
    
    def test_get_demo_research_result_returns_object(self):
        """Should return DemoResearchResult for valid URL."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            result = get_demo_research_result(test_url)
            assert isinstance(result, DemoResearchResult)
    
    def test_demo_research_result_has_primary_keyword(self):
        """Result should have primary keyword data."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            result = get_demo_research_result(test_url)
            assert result.primary_keyword is not None
            assert isinstance(result.primary_keyword, KeywordData)
            assert result.primary_keyword.keyword != ""
    
    def test_demo_research_result_has_secondary_keywords(self):
        """Result should have secondary keywords list."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            result = get_demo_research_result(test_url)
            assert isinstance(result.secondary_keywords, list)
            assert len(result.secondary_keywords) > 0
    
    def test_demo_research_result_calculates_total_volume(self):
        """Result should calculate total cluster volume."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            result = get_demo_research_result(test_url)
            expected_total = result.primary_keyword.volume + sum(
                kw.volume for kw in result.secondary_keywords
            )
            assert result.total_cluster_volume == expected_total
    
    def test_demo_research_result_to_dict(self):
        """Should be able to convert result to dict."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            result = get_demo_research_result(test_url)
            data = result.to_dict()
            assert isinstance(data, dict)
            assert "primary_keyword" in data
            assert "total_cluster_volume" in data


class TestHelperFunctions:
    """Tests for helper functions."""
    
    def test_determine_placement_h2_high_volume(self):
        """High volume keywords should be H2."""
        assert determine_placement(1500) == "H2"
        assert determine_placement(1000) == "H2"
        assert determine_placement(500) == "H2"
    
    def test_determine_placement_h3_medium_volume(self):
        """Medium volume keywords should be H3."""
        assert determine_placement(350) == "H3"
        assert determine_placement(200) == "H3"
    
    def test_determine_placement_content_low_volume(self):
        """Low volume keywords should be in content."""
        assert determine_placement(150) == "content"
        assert determine_placement(100) == "content"
    
    def test_determine_placement_faq_very_low(self):
        """Very low volume should be FAQ."""
        assert determine_placement(50) == "FAQ"
        assert determine_placement(10) == "FAQ"
    
    def test_is_question_keyword_true(self):
        """Should detect question keywords."""
        assert is_question_keyword("what is sports betting") is True
        assert is_question_keyword("how to bet on sports") is True
        assert is_question_keyword("is online betting legal?") is True
        assert is_question_keyword("Which sportsbook is best") is True
    
    def test_is_question_keyword_false(self):
        """Should not flag non-question keywords."""
        assert is_question_keyword("best sports betting sites") is False
        assert is_question_keyword("fanduel promo code") is False
        assert is_question_keyword("legal sportsbooks") is False


class TestDataClasses:
    """Tests for data classes."""
    
    def test_keyword_data_creation(self):
        """KeywordData should be creatable with required fields."""
        kw = KeywordData(keyword="test keyword", volume=1000)
        assert kw.keyword == "test keyword"
        assert kw.volume == 1000
        assert kw.difficulty == 0  # default
    
    def test_keyword_data_to_dict(self):
        """KeywordData should convert to dict."""
        kw = KeywordData(keyword="test", volume=500, difficulty=45, placement="H2")
        data = kw.to_dict()
        assert data["keyword"] == "test"
        assert data["volume"] == 500
        assert data["difficulty"] == 45
        assert data["placement"] == "H2"
    
    def test_competitor_data_creation(self):
        """CompetitorData should be creatable."""
        comp = CompetitorData(domain="example.com", url="https://example.com/page")
        assert comp.domain == "example.com"
        assert comp.url == "https://example.com/page"
    
    def test_competitor_data_to_dict(self):
        """CompetitorData should convert to dict."""
        comp = CompetitorData(
            domain="example.com",
            url="https://example.com/page",
            position=5,
            traffic=10000
        )
        data = comp.to_dict()
        assert data["domain"] == "example.com"
        assert data["position"] == 5
        assert data["traffic"] == 10000


class TestFormatting:
    """Tests for formatting functions."""
    
    def test_format_keyword_table(self):
        """Should format keywords as markdown table."""
        keywords = [
            KeywordData(keyword="test keyword", volume=1000, difficulty=50, placement="H2"),
            KeywordData(keyword="another keyword", volume=500, difficulty=30, placement="H3"),
        ]
        table = format_keyword_table(keywords)
        
        assert "| Keyword | Volume | KD | Placement |" in table
        assert "test keyword" in table
        assert "another keyword" in table
        assert "1,000" in table  # formatted with comma
        assert "H2" in table
    
    def test_format_keyword_table_empty(self):
        """Should handle empty keyword list."""
        table = format_keyword_table([])
        assert "No keywords available" in table


class TestGenerateDemoBriefSection:
    """Tests for generating brief sections from demo data."""
    
    def test_generate_demo_brief_section(self):
        """Should generate markdown brief section."""
        test_url = "https://www.topendsports.com/sport/betting/index.htm"
        if is_demo_available(test_url):
            section = generate_demo_brief_section(test_url)
            assert section is not None
            assert "## Keyword Research Summary" in section
            assert "### Primary Keyword" in section
            assert "### Secondary Keywords" in section
            assert "### FAQ Target Questions" in section
            assert "### Total Keyword Cluster Volume" in section
    
    def test_generate_demo_brief_section_unknown_url(self):
        """Should return None for unknown URL."""
        section = generate_demo_brief_section("https://example.com/unknown")
        assert section is None


class TestIntegration:
    """Integration tests for demo mode."""
    
    def test_full_workflow_betting_index(self):
        """Test full demo workflow for betting index page."""
        url = "https://www.topendsports.com/sport/betting/index.htm"
        
        # 1. Check availability
        if not is_demo_available(url):
            pytest.skip("Demo cache not available for test URL")
        
        # 2. Load raw cache
        cache = load_demo_cache(url)
        assert cache is not None
        
        # 3. Get structured result
        result = get_demo_research_result(url)
        assert result is not None
        assert result.primary_keyword.keyword == "best sports betting sites"
        
        # 4. Generate brief section
        section = generate_demo_brief_section(url)
        assert "best sports betting sites" in section
        assert "14,800" in section  # primary volume
    
    def test_full_workflow_fanduel_review(self):
        """Test full demo workflow for FanDuel review page."""
        url = "https://www.topendsports.com/sport/betting/fanduel-review.htm"
        
        if not is_demo_available(url):
            pytest.skip("Demo cache not available for test URL")
        
        result = get_demo_research_result(url)
        assert result is not None
        assert "fanduel" in result.primary_keyword.keyword.lower()
        
        # Should have competitors
        assert len(result.competitors) > 0
        
        # Should have FAQ questions
        assert len(result.faq_questions) > 0
