"""Shared pytest fixtures for topendsports-content-briefs."""

import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir() -> Path:
    """Return path to test data directory."""
    return Path(__file__).parent.parent / "test_data"


@pytest.fixture
def sample_html() -> str:
    """Return sample HTML for testing."""
    return "<html><body><h1>Test Content Brief</h1><p>Content here.</p></body></html>"


@pytest.fixture
def tmp_output_dir(tmp_path: Path) -> Path:
    """Create and return a temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_brief_config() -> dict:
    """Return sample brief configuration for testing."""
    return {
        "keyword": "test keyword",
        "target_word_count": 2000,
        "competitor_count": 5,
        "include_serp_analysis": True,
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "requires_api: Tests needing API credentials")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add integration marker to tests in integration/ folder
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
