"""
Expanded tests for ahrefs-api.py to increase coverage.
Target: from 48.96% to 70%+
"""

import pytest
import sys
import json
import time
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add scripts directory to path and import ahrefs-api.py
SCRIPT_DIR = Path(__file__).parent.parent.parent / ".claude" / "scripts"
AHREFS_SCRIPT = SCRIPT_DIR / "ahrefs-api.py"

# Import module with hyphen in name using importlib
spec = importlib.util.spec_from_file_location("ahrefs_api", AHREFS_SCRIPT)
ahrefs_api = importlib.util.module_from_spec(spec)
sys.modules["ahrefs_api"] = ahrefs_api
spec.loader.exec_module(ahrefs_api)

# Import functions from the module
get_cache_key = ahrefs_api.get_cache_key
validate_params = ahrefs_api.validate_params
get_cached_response = ahrefs_api.get_cached_response
set_cache = ahrefs_api.set_cache
call_api_standalone = ahrefs_api.call_api_standalone
call_api_with_retry_standalone = ahrefs_api.call_api_with_retry_standalone
call_api = ahrefs_api.call_api
call_api_with_retry = ahrefs_api.call_api_with_retry
main = ahrefs_api.main

# Ensure standalone mode for testing
ahrefs_api._using_centralized_client = False
import requests
ahrefs_api.requests = requests


class TestCacheKeyAdvanced:
    """Advanced tests for cache key generation."""

    def test_cache_key_with_special_characters(self):
        """Test cache key with special characters in params."""
        endpoint = "test"
        params = {
            "query": "test query with spaces",
            "filter": "a&b=c"
        }
        key = get_cache_key(endpoint, params)
        assert len(key) == 32

    def test_cache_key_with_list_values(self):
        """Test cache key with list values in params."""
        endpoint = "test"
        params = {"keywords": ["one", "two", "three"]}
        key = get_cache_key(endpoint, params)
        assert len(key) == 32

    def test_cache_key_with_nested_dict(self):
        """Test cache key with nested dictionary."""
        endpoint = "test"
        params = {"config": {"nested": {"deep": "value"}}}
        key = get_cache_key(endpoint, params)
        assert len(key) == 32

    def test_cache_key_with_empty_params(self):
        """Test cache key with empty params dict."""
        endpoint = "test-endpoint"
        params = {}
        key = get_cache_key(endpoint, params)
        assert len(key) == 32

    def test_cache_key_with_unicode(self):
        """Test cache key with unicode characters."""
        endpoint = "test"
        params = {"keyword": "café résumé naïve"}
        key = get_cache_key(endpoint, params)
        assert len(key) == 32


class TestValidateParamsAdvanced:
    """Advanced tests for parameter validation."""

    def test_validate_keywords_explorer_related_terms(self):
        """Test validation for keywords-explorer/related-terms."""
        endpoint = "keywords-explorer/related-terms"

        # Valid params
        params = {"select": "keyword,volume", "country": "us", "keyword": "test"}
        is_valid, error = validate_params(endpoint, params)
        assert is_valid is True

        # Missing country
        params_invalid = {"select": "keyword,volume"}
        is_valid, error = validate_params(endpoint, params_invalid)
        assert is_valid is False
        assert "country" in error

    def test_validate_keywords_explorer_matching_terms(self):
        """Test validation for keywords-explorer/matching-terms."""
        endpoint = "keywords-explorer/matching-terms"

        params = {"select": "keyword", "country": "uk"}
        is_valid, error = validate_params(endpoint, params)
        assert is_valid is True

    def test_validate_site_explorer_organic_keywords(self):
        """Test validation for site-explorer/organic-keywords."""
        endpoint = "site-explorer/organic-keywords"

        # Valid
        params = {"select": "keyword", "target": "example.com", "date": "2025-01-01", "country": "us"}
        is_valid, error = validate_params(endpoint, params)
        assert is_valid is True

        # Missing select
        params_invalid = {"target": "example.com", "date": "2025-01-01", "country": "us"}
        is_valid, error = validate_params(endpoint, params_invalid)
        assert is_valid is False

    def test_validate_site_explorer_metrics(self):
        """Test validation for site-explorer/metrics."""
        endpoint = "site-explorer/metrics"

        params = {"target": "example.com", "date": "2025-01-01"}
        is_valid, error = validate_params(endpoint, params)
        assert is_valid is True

        # Missing target
        params_invalid = {"date": "2025-01-01"}
        is_valid, error = validate_params(endpoint, params_invalid)
        assert is_valid is False

    def test_validate_site_explorer_top_pages(self):
        """Test validation for site-explorer/top-pages."""
        endpoint = "site-explorer/top-pages"

        params = {"select": "url", "target": "example.com", "date": "2025-01-01"}
        is_valid, error = validate_params(endpoint, params)
        assert is_valid is True

    def test_validate_site_explorer_backlinks_stats(self):
        """Test validation for site-explorer/backlinks-stats."""
        endpoint = "site-explorer/backlinks-stats"

        params = {"target": "example.com", "date": "2025-01-01"}
        is_valid, error = validate_params(endpoint, params)
        assert is_valid is True


class TestCacheOperationsAdvanced:
    """Advanced tests for cache operations."""

    def setup_method(self):
        """Clear cache before each test."""
        ahrefs_api.CACHE.clear()

    def test_cache_overwrite(self):
        """Test that cache can be overwritten."""
        endpoint = "test"
        params = {"key": "value"}
        data1 = {"result": "first"}
        data2 = {"result": "second"}

        set_cache(endpoint, params, data1)
        set_cache(endpoint, params, data2)

        cached = get_cached_response(endpoint, params)
        assert cached == data2

    def test_cache_multiple_endpoints(self):
        """Test caching multiple endpoints."""
        params = {"key": "value"}

        set_cache("endpoint1", params, {"data": 1})
        set_cache("endpoint2", params, {"data": 2})
        set_cache("endpoint3", params, {"data": 3})

        assert get_cached_response("endpoint1", params)["data"] == 1
        assert get_cached_response("endpoint2", params)["data"] == 2
        assert get_cached_response("endpoint3", params)["data"] == 3

    def test_cache_size_grows(self):
        """Test that cache size grows with entries."""
        for i in range(10):
            set_cache(f"endpoint{i}", {"i": i}, {"result": i})

        assert len(ahrefs_api.CACHE) == 10


class TestCallApiAdvanced:
    """Advanced tests for API calling."""

    @patch('ahrefs_api.requests.get')
    def test_call_api_builds_correct_url(self, mock_get):
        """Test that API call builds correct URL."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        endpoint = "keywords-explorer/overview"
        params = {"country": "us"}

        call_api_standalone(endpoint, params)

        # Verify URL construction
        call_args = mock_get.call_args
        url = call_args[0][0] if call_args[0] else call_args.kwargs.get('url')
        assert "keywords-explorer/overview" in url

    @patch('ahrefs_api.requests.get')
    def test_call_api_passes_params(self, mock_get):
        """Test that API call passes params correctly."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        params = {"country": "us", "select": "keyword,volume"}
        call_api_standalone("test", params)

        call_args = mock_get.call_args
        assert call_args.kwargs.get('params') == params

    @patch('ahrefs_api.requests.get')
    def test_call_api_500_error(self, mock_get):
        """Test handling of 500 server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        result = call_api_standalone("test", {})

        assert "error" in result
        assert "500" in result["error"]

    @patch('ahrefs_api.requests.get')
    def test_call_api_429_rate_limit(self, mock_get):
        """Test handling of 429 rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Too Many Requests"
        mock_get.return_value = mock_response

        result = call_api_standalone("test", {})

        assert "error" in result
        assert "429" in result["error"]

    @patch('ahrefs_api.requests.get')
    def test_call_api_connection_error(self, mock_get):
        """Test handling of connection error."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        result = call_api_standalone("test", {})

        assert "error" in result

    @patch('ahrefs_api.requests.get')
    def test_call_api_timeout_error(self, mock_get):
        """Test handling of timeout error."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        result = call_api_standalone("test", {})

        assert "error" in result


class TestCallApiWithRetryAdvanced:
    """Advanced tests for retry logic."""

    @patch('ahrefs_api.call_api_standalone')
    @patch('time.sleep')
    def test_retry_503_three_times(self, mock_sleep, mock_call_api):
        """Test that 503 errors retry up to max."""
        mock_call_api.return_value = {"error": "HTTP 503: Service Unavailable"}

        result = call_api_with_retry_standalone("test", {}, max_retries=3)

        assert mock_call_api.call_count == 3
        assert "error" in result

    @patch('ahrefs_api.call_api_standalone')
    def test_retry_success_on_second_attempt(self, mock_call_api):
        """Test successful retry on second attempt."""
        mock_call_api.side_effect = [
            {"error": "HTTP 503: Service Unavailable"},
            {"keywords": ["test"]}
        ]

        result = call_api_with_retry_standalone("test", {}, max_retries=3)

        assert mock_call_api.call_count == 2
        assert result == {"keywords": ["test"]}

    @patch('ahrefs_api.call_api_standalone')
    def test_no_retry_on_401(self, mock_call_api):
        """Test no retry on 401 unauthorized."""
        mock_call_api.return_value = {"error": "HTTP 401: Unauthorized"}

        result = call_api_with_retry_standalone("test", {}, max_retries=3)

        assert mock_call_api.call_count == 1

    @patch('ahrefs_api.call_api_standalone')
    def test_no_retry_on_400(self, mock_call_api):
        """Test no retry on 400 bad request."""
        mock_call_api.return_value = {"error": "HTTP 400: Bad Request"}

        result = call_api_with_retry_standalone("test", {}, max_retries=3)

        assert mock_call_api.call_count == 1

    @patch('ahrefs_api.call_api_standalone')
    @patch('time.sleep')
    def test_retry_with_custom_backoff(self, mock_sleep, mock_call_api):
        """Test retry with custom backoff factor."""
        mock_call_api.return_value = {"error": "HTTP 503: Service Unavailable"}

        call_api_with_retry_standalone("test", {}, max_retries=3, backoff_factor=3)

        # Check backoff times: 3^0=1, 3^1=3
        sleep_times = [call[0][0] for call in mock_sleep.call_args_list]
        assert sleep_times == [1, 3]


class TestCallApiCentralized:
    """Tests for centralized client integration."""

    def test_call_api_uses_standalone_when_centralized_unavailable(self):
        """Test fallback to standalone when centralized not available."""
        ahrefs_api._using_centralized_client = False

        with patch('ahrefs_api.call_api_standalone') as mock_standalone:
            mock_standalone.return_value = {"test": "data"}

            result = call_api("test-endpoint", {})

            mock_standalone.assert_called_once()

    def test_call_api_with_retry_uses_standalone(self):
        """Test retry function uses standalone when centralized unavailable."""
        ahrefs_api._using_centralized_client = False

        with patch('ahrefs_api.call_api_with_retry_standalone') as mock_retry:
            mock_retry.return_value = {"test": "data"}

            result = call_api_with_retry("test-endpoint", {})

            mock_retry.assert_called_once()


class TestMainFunction:
    """Tests for the main CLI function."""

    def test_main_no_args_shows_usage(self, capsys):
        """Test main with no arguments shows usage."""
        with patch('sys.argv', ['ahrefs-api.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "error" in output
        assert "examples" in output

    def test_main_with_valid_endpoint(self, capsys):
        """Test main with valid endpoint and params."""
        with patch('sys.argv', ['ahrefs-api.py', 'test-endpoint', '{"test": "value"}']):
            with patch('ahrefs_api.call_api_with_retry') as mock_api:
                mock_api.return_value = {"result": "success"}

                main()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output == {"result": "success"}

    def test_main_validation_failure(self, capsys):
        """Test main with invalid params for known endpoint."""
        with patch('sys.argv', [
            'ahrefs-api.py',
            'keywords-explorer/overview',
            '{"country": "us"}'  # Missing 'select'
        ]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "error" in output
        assert "select" in output["error"]

    def test_main_uses_cache(self, capsys):
        """Test main uses cache for repeated requests."""
        ahrefs_api._using_centralized_client = False
        ahrefs_api.CACHE.clear()

        endpoint = "test-endpoint"
        params = '{"test": "value"}'

        # Set up cache
        set_cache(endpoint, {"test": "value"}, {"cached": "response"})

        with patch('sys.argv', ['ahrefs-api.py', endpoint, params]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output == {"cached": "response"}

    def test_main_caches_successful_response(self):
        """Test main caches successful API responses."""
        ahrefs_api._using_centralized_client = False
        ahrefs_api.CACHE.clear()

        endpoint = "test-endpoint"
        params = {"test": "value"}

        with patch('sys.argv', ['ahrefs-api.py', endpoint, json.dumps(params)]):
            with patch('ahrefs_api.call_api_with_retry') as mock_api:
                mock_api.return_value = {"result": "success"}

                main()

        # Check that response was cached
        cached = get_cached_response(endpoint, params)
        assert cached == {"result": "success"}

    def test_main_does_not_cache_errors(self):
        """Test main does not cache error responses."""
        ahrefs_api._using_centralized_client = False
        ahrefs_api.CACHE.clear()

        endpoint = "test-endpoint"
        params = {"test": "value"}

        with patch('sys.argv', ['ahrefs-api.py', endpoint, json.dumps(params)]):
            with patch('ahrefs_api.call_api_with_retry') as mock_api:
                mock_api.return_value = {"error": "API Error"}

                main()

        # Check that error was not cached
        cached = get_cached_response(endpoint, params)
        assert cached is None


class TestEnvironmentVariables:
    """Tests for environment variable handling."""

    def test_api_key_from_env(self):
        """Test API key is loaded from environment."""
        assert ahrefs_api.API_KEY is not None

    def test_base_url_configured(self):
        """Test base URL is properly configured."""
        assert ahrefs_api.BASE_URL == "https://api.ahrefs.com/v3"

    def test_cache_ttl_configured(self):
        """Test cache TTL is properly configured."""
        assert ahrefs_api.CACHE_TTL == 3600


class TestRequiredParams:
    """Tests for REQUIRED_PARAMS configuration."""

    def test_all_endpoints_have_required_params(self):
        """Test all configured endpoints have required params."""
        for endpoint, required in ahrefs_api.REQUIRED_PARAMS.items():
            assert isinstance(required, list)
            assert len(required) > 0

    def test_keywords_explorer_endpoints(self):
        """Test keywords-explorer endpoints are configured."""
        assert "keywords-explorer/overview" in ahrefs_api.REQUIRED_PARAMS
        assert "keywords-explorer/related-terms" in ahrefs_api.REQUIRED_PARAMS

    def test_site_explorer_endpoints(self):
        """Test site-explorer endpoints are configured."""
        assert "site-explorer/domain-rating" in ahrefs_api.REQUIRED_PARAMS
        assert "site-explorer/organic-keywords" in ahrefs_api.REQUIRED_PARAMS
        assert "site-explorer/metrics" in ahrefs_api.REQUIRED_PARAMS


class TestEdgeCases:
    """Edge case tests."""

    def test_cache_key_with_very_long_params(self):
        """Test cache key with very long parameters."""
        endpoint = "test"
        params = {"long_key": "x" * 10000}
        key = get_cache_key(endpoint, params)
        assert len(key) == 32  # MD5 hash is always 32 chars

    @patch('ahrefs_api.requests.get')
    def test_call_api_empty_json_response(self, mock_get):
        """Test handling empty JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = call_api_standalone("test", {})
        assert result == {}

    @patch('ahrefs_api.requests.get')
    def test_call_api_large_response(self, mock_get):
        """Test handling large response."""
        mock_response = Mock()
        mock_response.status_code = 200
        large_data = {"keywords": [{"kw": f"keyword_{i}"} for i in range(1000)]}
        mock_response.json.return_value = large_data
        mock_get.return_value = mock_response

        result = call_api_standalone("test", {})
        assert len(result["keywords"]) == 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
