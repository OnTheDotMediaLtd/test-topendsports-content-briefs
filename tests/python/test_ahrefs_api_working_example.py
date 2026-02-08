"""
Tests for ahrefs_api_working_example.py

Tests the AhrefsAPI class and helper functions for direct Ahrefs API access.
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import requests

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ahrefs_api_working_example import (
    AhrefsAPI,
    test_domain_rating as _src_test_domain_rating,
    test_metrics as _src_test_metrics,
    test_backlinks_stats as _src_test_backlinks_stats,
    main,
    API_KEY,
    BASE_URL,
    CA_BUNDLE,
)


class TestAhrefsAPIInit:
    """Test AhrefsAPI initialization."""

    def test_init_default_values(self):
        """Test initialization with default CA bundle."""
        api = AhrefsAPI("test_api_key")
        
        assert api.api_key == "test_api_key"
        assert api.base_url == BASE_URL
        assert api.ca_bundle == CA_BUNDLE

    def test_init_custom_ca_bundle(self):
        """Test initialization with custom CA bundle."""
        custom_ca = "/custom/path/ca-bundle.crt"
        api = AhrefsAPI("test_api_key", ca_bundle=custom_ca)
        
        assert api.ca_bundle == custom_ca

    def test_init_session_headers(self):
        """Test that session headers are set correctly."""
        api = AhrefsAPI("test_api_key_123")
        
        assert "Authorization" in api.session.headers
        assert api.session.headers["Authorization"] == "Bearer test_api_key_123"
        assert "User-Agent" in api.session.headers

    def test_init_session_verify(self):
        """Test that session verify is set to CA bundle."""
        api = AhrefsAPI("test_api_key")
        
        assert api.session.verify == CA_BUNDLE


class TestAhrefsAPIGet:
    """Test AhrefsAPI.get() method."""

    @patch('requests.Session.get')
    def test_get_successful_request(self, mock_get):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"domain_rating": 85}
        mock_response.headers = {
            "x-request-id": "req-123",
            "x-api-units-cost-total": "10",
            "x-api-cache": "HIT",
        }
        mock_get.return_value = mock_response

        api = AhrefsAPI("test_key")
        result = api.get("site-explorer/domain-rating", {"target": "example.com"})

        assert result == {"domain_rating": 85}
        mock_get.assert_called_once()

    @patch('requests.Session.get')
    def test_get_constructs_correct_url(self, mock_get):
        """Test that correct URL is constructed."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}
        mock_get.return_value = mock_response

        api = AhrefsAPI("test_key")
        api.get("test-endpoint", {"param1": "value1"})

        call_args = mock_get.call_args
        assert f"{BASE_URL}/test-endpoint" in call_args[0][0] or call_args[1].get('url', call_args[0][0]) == f"{BASE_URL}/test-endpoint"

    @patch('requests.Session.get')
    def test_get_ssl_error(self, mock_get):
        """Test SSL error handling."""
        mock_get.side_effect = requests.exceptions.SSLError("SSL certificate verify failed")

        api = AhrefsAPI("test_key")
        
        with pytest.raises(requests.exceptions.SSLError):
            api.get("site-explorer/domain-rating", {"target": "example.com"})

    @patch('requests.Session.get')
    def test_get_http_403_error(self, mock_get):
        """Test 403 Forbidden error handling."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_get.return_value = mock_response

        api = AhrefsAPI("test_key")
        
        with pytest.raises(requests.exceptions.HTTPError):
            api.get("site-explorer/domain-rating", {"target": "example.com"})

    @patch('requests.Session.get')
    def test_get_http_404_error(self, mock_get):
        """Test 404 Not Found error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_get.return_value = mock_response

        api = AhrefsAPI("test_key")
        
        with pytest.raises(requests.exceptions.HTTPError):
            api.get("invalid/endpoint", {"target": "example.com"})

    @patch('requests.Session.get')
    def test_get_request_exception(self, mock_get):
        """Test generic request exception handling."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

        api = AhrefsAPI("test_key")
        
        with pytest.raises(requests.exceptions.RequestException):
            api.get("site-explorer/domain-rating", {"target": "example.com"})

    @patch('requests.Session.get')
    def test_get_timeout_parameter(self, mock_get):
        """Test that timeout is passed correctly."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}
        mock_get.return_value = mock_response

        api = AhrefsAPI("test_key")
        api.get("test-endpoint")

        call_kwargs = mock_get.call_args[1]
        assert call_kwargs.get("timeout") == 30

    @patch('requests.Session.get')
    def test_get_no_params(self, mock_get):
        """Test request without parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_response.headers = {}
        mock_get.return_value = mock_response

        api = AhrefsAPI("test_key")
        result = api.get("health-check")

        assert result == {"status": "ok"}


class TestDomainRatingHelper:
    """Test test_domain_rating helper function."""

    @patch.object(AhrefsAPI, 'get')
    def test_domain_rating_returns_data(self, mock_get, capsys):
        """Test domain rating returns correct data."""
        mock_data = {"domain_rating": 85, "ahrefs_rank": 1000}
        mock_get.return_value = mock_data

        api = AhrefsAPI("test_key")
        result = _src_test_domain_rating(api, "example.com", "2025-01-01")

        assert result == mock_data
        mock_get.assert_called_once_with('site-explorer/domain-rating', {
            'target': "example.com",
            'date': "2025-01-01"
        })

    @patch.object(AhrefsAPI, 'get')
    def test_domain_rating_prints_output(self, mock_get, capsys):
        """Test domain rating prints formatted output."""
        mock_get.return_value = {"domain_rating": 85}

        api = AhrefsAPI("test_key")
        _src_test_domain_rating(api, "example.com", "2025-01-01")

        captured = capsys.readouterr()
        assert "site-explorer/domain-rating" in captured.out
        assert "example.com" in captured.out


class TestMetricsHelper:
    """Test test_metrics helper function."""

    @patch.object(AhrefsAPI, 'get')
    def test_metrics_returns_data(self, mock_get):
        """Test metrics returns correct data."""
        mock_data = {"organic_traffic": 50000, "organic_keywords": 10000}
        mock_get.return_value = mock_data

        api = AhrefsAPI("test_key")
        result = _src_test_metrics(api, "example.com", "2025-01-01")

        assert result == mock_data
        mock_get.assert_called_once_with('site-explorer/metrics', {
            'target': "example.com",
            'date': "2025-01-01"
        })

    @patch.object(AhrefsAPI, 'get')
    def test_metrics_prints_output(self, mock_get, capsys):
        """Test metrics prints formatted output."""
        mock_get.return_value = {"organic_traffic": 50000}

        api = AhrefsAPI("test_key")
        _src_test_metrics(api, "example.com", "2025-01-01")

        captured = capsys.readouterr()
        assert "site-explorer/metrics" in captured.out


class TestBacklinksStatsHelper:
    """Test test_backlinks_stats helper function."""

    @patch.object(AhrefsAPI, 'get')
    def test_backlinks_stats_returns_data(self, mock_get):
        """Test backlinks stats returns correct data."""
        mock_data = {"live_backlinks": 100000, "referring_domains": 5000}
        mock_get.return_value = mock_data

        api = AhrefsAPI("test_key")
        result = _src_test_backlinks_stats(api, "example.com", "2025-01-01")

        assert result == mock_data
        mock_get.assert_called_once_with('site-explorer/backlinks-stats', {
            'target': "example.com",
            'date': "2025-01-01"
        })

    @patch.object(AhrefsAPI, 'get')
    def test_backlinks_stats_prints_output(self, mock_get, capsys):
        """Test backlinks stats prints formatted output."""
        mock_get.return_value = {"live_backlinks": 100000}

        api = AhrefsAPI("test_key")
        _src_test_backlinks_stats(api, "example.com", "2025-01-01")

        captured = capsys.readouterr()
        assert "site-explorer/backlinks-stats" in captured.out


class TestMainFunction:
    """Test main() function."""

    @patch('ahrefs_api_working_example.test_backlinks_stats')
    @patch('ahrefs_api_working_example.test_metrics')
    @patch('ahrefs_api_working_example.test_domain_rating')
    def test_main_calls_all_test_functions(self, mock_dr, mock_m, mock_bs, capsys):
        """Test that main calls all test helper functions."""
        mock_dr.return_value = {"domain_rating": 85}
        mock_m.return_value = {"organic_traffic": 50000}
        mock_bs.return_value = {"live_backlinks": 100000}

        main()

        assert mock_dr.called
        assert mock_m.called
        assert mock_bs.called

    @patch('ahrefs_api_working_example.test_backlinks_stats')
    @patch('ahrefs_api_working_example.test_metrics')
    @patch('ahrefs_api_working_example.test_domain_rating')
    def test_main_prints_configuration(self, mock_dr, mock_m, mock_bs, capsys):
        """Test that main prints configuration info."""
        mock_dr.return_value = {}
        mock_m.return_value = {}
        mock_bs.return_value = {}

        main()

        captured = capsys.readouterr()
        assert "Configuration" in captured.out
        assert "API Key" in captured.out
        assert "Base URL" in captured.out

    @patch('ahrefs_api_working_example.test_domain_rating')
    def test_main_handles_exception(self, mock_dr, capsys):
        """Test that main handles exceptions and exits with code 1."""
        mock_dr.side_effect = Exception("API Error")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    @patch('ahrefs_api_working_example.test_backlinks_stats')
    @patch('ahrefs_api_working_example.test_metrics')
    @patch('ahrefs_api_working_example.test_domain_rating')
    def test_main_success_message(self, mock_dr, mock_m, mock_bs, capsys):
        """Test success message on completion."""
        mock_dr.return_value = {}
        mock_m.return_value = {}
        mock_bs.return_value = {}

        main()

        captured = capsys.readouterr()
        assert "All tests completed successfully" in captured.out

    @patch('ahrefs_api_working_example.test_backlinks_stats')
    @patch('ahrefs_api_working_example.test_metrics')
    @patch('ahrefs_api_working_example.test_domain_rating')
    def test_main_uses_correct_target(self, mock_dr, mock_m, mock_bs):
        """Test that main uses ahrefs.com as target."""
        mock_dr.return_value = {}
        mock_m.return_value = {}
        mock_bs.return_value = {}

        main()

        # Check the target parameter
        call_args = mock_dr.call_args[0]
        assert call_args[1] == "ahrefs.com"


class TestModuleConstants:
    """Test module-level constants."""

    def test_api_key_is_placeholder(self):
        """Test that API_KEY is a placeholder."""
        assert API_KEY == "YOUR_AHREFS_API_KEY"

    def test_base_url_is_v3(self):
        """Test that BASE_URL points to V3 API."""
        assert "v3" in BASE_URL
        assert BASE_URL == "https://api.ahrefs.com/v3"

    def test_ca_bundle_path(self):
        """Test CA bundle path is system certificates."""
        assert CA_BUNDLE == "/etc/ssl/certs/ca-certificates.crt"
