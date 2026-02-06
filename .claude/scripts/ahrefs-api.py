#!/usr/bin/env python3
"""
Direct Ahrefs API wrapper that works in Claude Code Remote.
Bypasses the MCP server's axios SSL issues by using Python requests
with the system CA bundle.

This script now uses the centralized AhrefsClient from tes-shared-infrastructure
when available, falling back to standalone mode if not installed.

IMPROVEMENTS (Production-Grade):
- Environment variable support for API key
- Automatic retry logic for transient errors (503)
- Simple in-memory caching (1-hour TTL)
- Parameter validation before API calls
- Structured logging (to stderr)
- Centralized client with rate limiting when available
"""

import sys
import json
import warnings
import os
import logging
import time
import hashlib

# Configure logging to stderr (stdout reserved for JSON output)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Try to import centralized client
_using_centralized_client = False
_centralized_client = None

try:
    from tes_shared.api_clients import AhrefsClient, default_ahrefs_limiter
    _using_centralized_client = True
    logger.info("Using centralized AhrefsClient from tes-shared-infrastructure")
except ImportError:
    logger.info("tes-shared-infrastructure not installed, using standalone mode")
    import requests
    import urllib3
    # Suppress SSL warnings since we're behind a TLS-inspecting proxy
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# API Configuration - Env var with fallback for backward compatibility
API_KEY = os.getenv("AHREFS_API_KEY", "YOUR_AHREFS_API_KEY")
BASE_URL = "https://api.ahrefs.com/v3"

# Cache configuration (used in standalone mode)
CACHE = {}
CACHE_TTL = 3600  # 1 hour in seconds

# Required parameters by endpoint
REQUIRED_PARAMS = {
    "keywords-explorer/overview": ["select", "country"],
    "keywords-explorer/related-terms": ["select", "country"],
    "keywords-explorer/search-suggestions": ["select", "country"],
    "keywords-explorer/matching-terms": ["select", "country"],
    "site-explorer/domain-rating": ["target", "date"],
    "site-explorer/organic-keywords": ["select", "target", "date"],
    "site-explorer/metrics": ["target", "date"],
    "site-explorer/top-pages": ["select", "target", "date"],
    "site-explorer/backlinks-stats": ["target", "date"],
    "batch-analysis/batch-analysis": ["select", "targets"],
}


def get_cache_key(endpoint, params):
    """Generate cache key from endpoint and params."""
    key_string = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
    return hashlib.md5(key_string.encode()).hexdigest()


def get_cached_response(endpoint, params):
    """Get response from cache if valid."""
    key = get_cache_key(endpoint, params)
    if key in CACHE:
        cached = CACHE[key]
        if time.time() - cached['time'] < CACHE_TTL:
            logger.info(f"Cache HIT for {endpoint}")
            return cached['data']
        else:
            logger.info(f"Cache EXPIRED for {endpoint}")
            del CACHE[key]
    return None


def set_cache(endpoint, params, data):
    """Store response in cache."""
    key = get_cache_key(endpoint, params)
    CACHE[key] = {'data': data, 'time': time.time()}
    logger.info(f"Cached response for {endpoint}")


def validate_params(endpoint, params):
    """Validate required parameters before API call."""
    required = REQUIRED_PARAMS.get(endpoint, [])
    missing = [p for p in required if p not in params]
    if missing:
        return False, f"Missing required parameters: {missing}"
    return True, None


def call_api_standalone(endpoint, params):
    """Call Ahrefs API with SSL verification disabled for proxy compatibility (standalone mode)."""
    import requests
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        logger.info(f"Calling Ahrefs API: {endpoint}")
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=False,  # Required for TLS-inspecting proxies in Claude Code Remote
            timeout=60
        )

        if response.status_code == 200:
            logger.info(f"API call successful: {endpoint}")
            return response.json()
        else:
            logger.error(f"API call failed: HTTP {response.status_code}")
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        logger.error(f"Exception during API call: {str(e)}")
        return {"error": str(e)}


def call_api_with_retry_standalone(endpoint, params, max_retries=3, backoff_factor=2):
    """
    Call API with exponential backoff for transient errors (standalone mode).

    Args:
        endpoint: API endpoint path
        params: Query parameters dict
        max_retries: Maximum number of retry attempts (default 3)
        backoff_factor: Exponential backoff multiplier (default 2)

    Returns:
        API response dict
    """
    result = None
    for attempt in range(max_retries):
        result = call_api_standalone(endpoint, params)

        if isinstance(result, dict) and "error" in result:
            error_str = str(result["error"])
            # Retry on 503 (transient) but not 400/401/403 (client errors)
            if "503" in error_str and attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed with 503, retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                # Non-retryable error or last attempt
                logger.error(f"API call failed: {error_str}")
                return result

        # Success
        return result

    return result


def call_api(endpoint, params):
    """Call Ahrefs API - uses centralized client if available, falls back to standalone."""
    global _centralized_client

    if _using_centralized_client:
        try:
            if _centralized_client is None:
                _centralized_client = AhrefsClient(
                    api_key=API_KEY,
                    rate_limiter=default_ahrefs_limiter,
                    cache_ttl=CACHE_TTL
                )

            # Use the centralized client's generic request method
            result = _centralized_client._request(endpoint, params)
            return result
        except Exception as e:
            logger.error(f"Centralized client error: {e}")
            return {"error": str(e)}
    else:
        return call_api_standalone(endpoint, params)


def call_api_with_retry(endpoint, params, max_retries=3, backoff_factor=2):
    """
    Call API with exponential backoff for transient errors.
    Uses centralized client if available (which has built-in retry).
    """
    if _using_centralized_client:
        # Centralized client has built-in retry logic
        return call_api(endpoint, params)
    else:
        return call_api_with_retry_standalone(endpoint, params, max_retries, backoff_factor)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: ahrefs-api.py <endpoint> [params_json]",
            "using_centralized_client": _using_centralized_client,
            "examples": {
                "domain_rating": "ahrefs-api.py site-explorer/domain-rating '{\"target\":\"example.com\",\"date\":\"2025-12-01\"}'",
                "keywords": "ahrefs-api.py keywords-explorer/overview '{\"select\":\"keyword,volume,difficulty\",\"country\":\"us\",\"keywords\":\"nfl betting\"}'",
                "organic_keywords": "ahrefs-api.py site-explorer/organic-keywords '{\"select\":\"keyword,volume,position\",\"target\":\"example.com\",\"date\":\"2025-12-01\",\"country\":\"us\"}'"
            }
        }, indent=2))
        sys.exit(1)

    endpoint = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    # Validate parameters
    is_valid, error_msg = validate_params(endpoint, params)
    if not is_valid:
        logger.error(f"Parameter validation failed: {error_msg}")
        print(json.dumps({"error": error_msg}, indent=2))
        sys.exit(1)

    # Check cache first (standalone mode only - centralized client has its own cache)
    if not _using_centralized_client:
        cached_result = get_cached_response(endpoint, params)
        if cached_result is not None:
            print(json.dumps(cached_result, indent=2))
            sys.exit(0)

    # Call API with retry logic
    result = call_api_with_retry(endpoint, params)

    # Cache successful responses (standalone mode only)
    if not _using_centralized_client:
        if isinstance(result, dict) and "error" not in result:
            set_cache(endpoint, params, result)

    # Output to stdout (for CLI compatibility)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
