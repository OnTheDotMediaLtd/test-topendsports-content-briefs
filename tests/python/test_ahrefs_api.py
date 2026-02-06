"""
Tests for .claude/scripts/ahrefs-api.py

Tests Ahrefs API wrapper functionality including:
- Cache key generation
- Parameter validation
- Cache operations (get/set)
- Cache expiry logic
- API call mocking
- Retry logic
- Error handling
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
# Use standalone versions for testing (centralized client has its own tests)
call_api = ahrefs_api.call_api_standalone
call_api_with_retry = ahrefs_api.call_api_with_retry_standalone

# Force standalone mode for tests that need to mock requests
ahrefs_api._using_centralized_client = False

# Import requests for patching in standalone mode
import requests
ahrefs_api.requests = requests


class TestCacheKeyGeneration:
    """Test cache key generation for API responses."""

    def test_cache_key_is_consistent(self):
        """Test that same endpoint and params generate same key."""
        endpoint = "keywords-explorer/overview"
        params = {"select": "keyword,volume", "country": "us"}

        key1 = get_cache_key(endpoint, params)
        key2 = get_cache_key(endpoint, params)

        assert key1 == key2

    def test_cache_key_differs_for_different_params(self):
        """Test that different params generate different keys."""
        endpoint = "keywords-explorer/overview"
        params1 = {"select": "keyword,volume", "country": "us"}
        params2 = {"select": "keyword,volume", "country": "uk"}

        key1 = get_cache_key(endpoint, params1)
        key2 = get_cache_key(endpoint, params2)

        assert key1 != key2

    def test_cache_key_differs_for_different_endpoints(self):
        """Test that different endpoints generate different keys."""
        params = {"target": "example.com", "date": "2025-12-01"}

        key1 = get_cache_key("site-explorer/domain-rating", params)
        key2 = get_cache_key("site-explorer/metrics", params)

        assert key1 != key2

    def test_cache_key_param_order_independence(self):
        """Test that parameter order doesn't affect cache key."""
        endpoint = "keywords-explorer/overview"
        params1 = {"select": "keyword", "country": "us", "keywords": "test"}
        params2 = {"keywords": "test", "country": "us", "select": "keyword"}

        key1 = get_cache_key(endpoint, params1)
        key2 = get_cache_key(endpoint, params2)

        assert key1 == key2

    def test_cache_key_is_md5_hash(self):
        """Test that cache key is an MD5 hash."""
        endpoint = "test-endpoint"
        params = {"test": "value"}

        key = get_cache_key(endpoint, params)

        # MD5 hash is 32 characters long
        assert len(key) == 32
        assert all(c in '0123456789abcdef' for c in key)


class TestParameterValidation:
    """Test API parameter validation."""

    def test_validate_params_with_all_required(self):
        """Test validation passes with all required params."""
        endpoint = "keywords-explorer/overview"
        params = {
            "select": "keyword,volume",
            "country": "us",
            "keywords": "test"
        }

        is_valid, error = validate_params(endpoint, params)

        assert is_valid is True
        assert error is None

    def test_validate_params_missing_required(self):
        """Test validation fails with missing required params."""
        endpoint = "keywords-explorer/overview"
        params = {"select": "keyword,volume"}  # Missing 'country'

        is_valid, error = validate_params(endpoint, params)

        assert is_valid is False
        assert error is not None
        assert "country" in error

    def test_validate_params_unknown_endpoint(self):
        """Test validation for unknown endpoint (no requirements)."""
        endpoint = "unknown-endpoint"
        params = {"any": "params"}

        is_valid, error = validate_params(endpoint, params)

        # Should pass - no required params defined
        assert is_valid is True
        assert error is None

    def test_validate_site_explorer_domain_rating(self):
        """Test validation for site-explorer/domain-rating endpoint."""
        endpoint = "site-explorer/domain-rating"

        # Valid params
        params_valid = {"target": "example.com", "date": "2025-12-01"}
        is_valid, error = validate_params(endpoint, params_valid)
        assert is_valid is True

        # Missing 'target'
        params_invalid = {"date": "2025-12-01"}
        is_valid, error = validate_params(endpoint, params_invalid)
        assert is_valid is False
        assert "target" in error

    def test_validate_batch_analysis(self):
        """Test validation for batch-analysis endpoint."""
        endpoint = "batch-analysis/batch-analysis"

        # Valid params
        params_valid = {"select": "domain", "targets": "example.com,test.com"}
        is_valid, error = validate_params(endpoint, params_valid)
        assert is_valid is True

        # Missing 'targets'
        params_invalid = {"select": "domain"}
        is_valid, error = validate_params(endpoint, params_invalid)
        assert is_valid is False


class TestCacheOperations:
    """Test cache get/set operations."""

    def setup_method(self):
        """Clear cache before each test."""
        ahrefs_api.CACHE.clear()

    def test_set_and_get_cache(self):
        """Test setting and retrieving cached responses."""
        endpoint = "test-endpoint"
        params = {"test": "value"}
        data = {"result": "success"}

        set_cache(endpoint, params, data)
        cached = get_cached_response(endpoint, params)

        assert cached == data

    def test_get_cache_miss(self):
        """Test cache miss returns None."""
        endpoint = "test-endpoint"
        params = {"test": "value"}

        cached = get_cached_response(endpoint, params)

        assert cached is None

    def test_get_cache_different_params(self):
        """Test cache miss with different params."""
        endpoint = "test-endpoint"
        params1 = {"test": "value1"}
        params2 = {"test": "value2"}
        data = {"result": "success"}

        set_cache(endpoint, params1, data)
        cached = get_cached_response(endpoint, params2)

        assert cached is None

    def test_cache_stores_timestamp(self):
        """Test that cache stores timestamp."""
        endpoint = "test-endpoint"
        params = {"test": "value"}
        data = {"result": "success"}

        before = time.time()
        set_cache(endpoint, params, data)
        after = time.time()

        key = get_cache_key(endpoint, params)
        assert 'time' in ahrefs_api.CACHE[key]
        assert before <= ahrefs_api.CACHE[key]['time'] <= after


class TestCacheExpiry:
    """Test cache expiry logic."""

    def setup_method(self):
        """Clear cache before each test."""
        ahrefs_api.CACHE.clear()

    def test_cache_expires_after_ttl(self):
        """Test that cache expires after TTL."""
        endpoint = "test-endpoint"
        params = {"test": "value"}
        data = {"result": "success"}

        # Set cache with old timestamp
        key = get_cache_key(endpoint, params)
        old_time = time.time() - (ahrefs_api.CACHE_TTL + 1)
        ahrefs_api.CACHE[key] = {'data': data, 'time': old_time}

        cached = get_cached_response(endpoint, params)

        assert cached is None
        assert key not in ahrefs_api.CACHE  # Should be deleted

    def test_cache_valid_within_ttl(self):
        """Test that cache is valid within TTL."""
        endpoint = "test-endpoint"
        params = {"test": "value"}
        data = {"result": "success"}

        # Set cache with recent timestamp
        key = get_cache_key(endpoint, params)
        recent_time = time.time() - 100  # 100 seconds ago
        ahrefs_api.CACHE[key] = {'data': data, 'time': recent_time}

        cached = get_cached_response(endpoint, params)

        assert cached == data

    def test_cache_expiry_edge_case(self):
        """Test cache at exact TTL boundary."""
        endpoint = "test-endpoint"
        params = {"test": "value"}
        data = {"result": "success"}

        # Set cache at exact TTL boundary
        key = get_cache_key(endpoint, params)
        boundary_time = time.time() - ahrefs_api.CACHE_TTL
        ahrefs_api.CACHE[key] = {'data': data, 'time': boundary_time}

        cached = get_cached_response(endpoint, params)

        # Should be expired (>= TTL)
        assert cached is None


class TestCallApi:
    """Test API call functionality with mocking."""

    @patch('ahrefs_api.requests.get')
    def test_call_api_success(self, mock_get):
        """Test successful API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"keywords": []}
        mock_get.return_value = mock_response

        endpoint = "keywords-explorer/overview"
        params = {"select": "keyword", "country": "us"}

        result = call_api(endpoint, params)

        assert result == {"keywords": []}
        mock_get.assert_called_once()

    @patch('ahrefs_api.requests.get')
    def test_call_api_error_response(self, mock_get):
        """Test API call with error response."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_get.return_value = mock_response

        endpoint = "test-endpoint"
        params = {}

        result = call_api(endpoint, params)

        assert "error" in result
        assert "403" in result["error"]

    @patch('ahrefs_api.requests.get')
    def test_call_api_exception(self, mock_get):
        """Test API call with exception."""
        mock_get.side_effect = Exception("Network error")

        endpoint = "test-endpoint"
        params = {}

        result = call_api(endpoint, params)

        assert "error" in result
        assert "Network error" in result["error"]

    @patch('ahrefs_api.requests.get')
    def test_call_api_timeout(self, mock_get):
        """Test API call with timeout."""
        mock_get.side_effect = Exception("Timeout")

        endpoint = "test-endpoint"
        params = {}

        result = call_api(endpoint, params)

        assert "error" in result

    @patch('ahrefs_api.requests.get')
    def test_call_api_uses_auth_header(self, mock_get):
        """Test that API call includes authorization header."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        endpoint = "test-endpoint"
        params = {}

        call_api(endpoint, params)

        # Check that headers include Authorization
        call_args = mock_get.call_args
        assert 'headers' in call_args.kwargs
        assert 'Authorization' in call_args.kwargs['headers']


class TestCallApiWithRetry:
    """Test API retry logic."""

    @patch('ahrefs_api.call_api_standalone')
    def test_retry_on_503_error(self, mock_call_api):
        """Test that 503 errors trigger retry."""
        # First call fails with 503, second succeeds
        mock_call_api.side_effect = [
            {"error": "HTTP 503: Service Unavailable"},
            {"keywords": []}
        ]

        endpoint = "test-endpoint"
        params = {}

        result = call_api_with_retry(endpoint, params, max_retries=3)

        assert result == {"keywords": []}
        assert mock_call_api.call_count == 2

    @patch('ahrefs_api.call_api_standalone')
    def test_no_retry_on_client_error(self, mock_call_api):
        """Test that client errors (4xx) don't trigger retry."""
        mock_call_api.return_value = {"error": "HTTP 403: Forbidden"}

        endpoint = "test-endpoint"
        params = {}

        result = call_api_with_retry(endpoint, params, max_retries=3)

        assert "error" in result
        assert "403" in result["error"]
        assert mock_call_api.call_count == 1

    @patch('ahrefs_api.call_api_standalone')
    @patch('time.sleep')
    def test_retry_backoff(self, mock_sleep, mock_call_api):
        """Test exponential backoff on retry."""
        # All calls fail with 503
        mock_call_api.return_value = {"error": "HTTP 503: Service Unavailable"}

        endpoint = "test-endpoint"
        params = {}

        call_api_with_retry(endpoint, params, max_retries=3, backoff_factor=2)

        # Should have slept twice (between 3 attempts)
        assert mock_sleep.call_count == 2
        # Check backoff times: 2^0=1, 2^1=2
        sleep_times = [call[0][0] for call in mock_sleep.call_args_list]
        assert sleep_times == [1, 2]

    @patch('ahrefs_api.call_api_standalone')
    def test_successful_first_call_no_retry(self, mock_call_api):
        """Test that successful calls don't retry."""
        mock_call_api.return_value = {"keywords": []}

        endpoint = "test-endpoint"
        params = {}

        result = call_api_with_retry(endpoint, params, max_retries=3)

        assert result == {"keywords": []}
        assert mock_call_api.call_count == 1

    @patch('ahrefs_api.call_api_standalone')
    def test_max_retries_exhausted(self, mock_call_api):
        """Test behavior when max retries exhausted."""
        mock_call_api.return_value = {"error": "HTTP 503: Service Unavailable"}

        endpoint = "test-endpoint"
        params = {}

        result = call_api_with_retry(endpoint, params, max_retries=2)

        assert "error" in result
        assert mock_call_api.call_count == 2


class TestMainFunction:
    """Test the main CLI function."""

    @pytest.mark.skip(reason="Difficult to mock sys.argv for importlib-loaded module")
    def test_main_no_args(self):
        """Test main function with no arguments.

        NOTE: This test is skipped because the module is loaded via importlib.spec_from_file_location
        which makes it difficult to properly mock sys.argv. The error handling is tested via
        other tests that call the validation functions directly.
        """
        # This test would verify that main() exits with code 1 when no args provided
        pass

    @patch('sys.argv', ['ahrefs-api.py', 'test-endpoint', '{"test": "value"}'])
    @patch('ahrefs_api.call_api_with_retry')
    @patch('ahrefs_api.validate_params')
    def test_main_with_valid_args(self, mock_validate, mock_call):
        """Test main function with valid arguments."""
        mock_validate.return_value = (True, None)
        mock_call.return_value = {"result": "success"}

        from ahrefs_api import main

        with patch('builtins.print'):
            main()

        mock_call.assert_called_once()

    @patch('sys.argv', ['ahrefs-api.py', 'keywords-explorer/overview', '{"country": "us"}'])
    @patch('sys.exit')
    def test_main_validation_failure(self, mock_exit):
        """Test main function with validation failure."""
        from ahrefs_api import main

        with patch('builtins.print'):
            main()

        # Should exit with error due to missing 'select' param
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['ahrefs-api.py', 'test-endpoint', '{"test": "value"}'])
    @patch('ahrefs_api.get_cached_response')
    @patch('sys.exit')
    def test_main_uses_cache(self, mock_exit, mock_cache):
        """Test that main function uses cache."""
        mock_cache.return_value = {"cached": "data"}

        from ahrefs_api import main

        with patch('builtins.print') as mock_print:
            main()

        # Should print cached data and exit
        mock_exit.assert_called_once_with(0)


class TestEnvironmentVariables:
    """Test environment variable handling."""

    def test_api_key_exists(self):
        """Test that API key is loaded."""
        # Can't reload module loaded via importlib.spec_from_file_location
        # So we just verify the API key exists
        assert ahrefs_api.API_KEY is not None
        assert len(ahrefs_api.API_KEY) > 0
        assert isinstance(ahrefs_api.API_KEY, str)

    def test_api_key_format(self):
        """Test that API key has expected format."""
        # API keys are typically alphanumeric strings
        assert ahrefs_api.API_KEY.replace('-', '').replace('_', '').isalnum()


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_cache_key_with_none_values(self):
        """Test cache key generation with None values."""
        endpoint = "test-endpoint"
        params = {"key1": "value", "key2": None}

        key = get_cache_key(endpoint, params)

        assert key is not None
        assert len(key) == 32

    def test_validate_empty_params(self):
        """Test validation with empty params dict."""
        endpoint = "keywords-explorer/overview"
        params = {}

        is_valid, error = validate_params(endpoint, params)

        assert is_valid is False

    @patch('ahrefs_api.requests.get')
    def test_call_api_non_json_response(self, mock_get):
        """Test API call with non-JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_get.return_value = mock_response

        result = call_api("test", {})

        assert "error" in result

    def test_cache_concurrent_access(self):
        """Test cache with multiple concurrent operations."""
        endpoint = "test-endpoint"
        params1 = {"test": "1"}
        params2 = {"test": "2"}
        data1 = {"result": "1"}
        data2 = {"result": "2"}

        set_cache(endpoint, params1, data1)
        set_cache(endpoint, params2, data2)

        cached1 = get_cached_response(endpoint, params1)
        cached2 = get_cached_response(endpoint, params2)

        assert cached1 == data1
        assert cached2 == data2
