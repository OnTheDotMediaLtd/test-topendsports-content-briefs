#!/usr/bin/env python3
"""
Working Example: Ahrefs API Direct Access
==========================================

This script demonstrates the correct way to call the Ahrefs API directly,
bypassing the MCP layer, in the Claude Code Remote environment.

Key Points:
1. Uses system CA bundle (/etc/ssl/certs/ca-certificates.crt) instead of certifi
2. Uses "Bearer" prefix in Authorization header
3. Only uses V3 API endpoints
"""

import requests
import json
import sys

# Configuration
API_KEY = "SjPt1JPhRgqMpi5UN8G7e8P3s57SjW86734J2r1Z"
BASE_URL = "https://api.ahrefs.com/v3"
CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"  # CRITICAL: Use system CA bundle


class AhrefsAPI:
    """
    Simple wrapper for Ahrefs API V3

    This class handles authentication and SSL configuration correctly
    for the Claude Code Remote environment with TLS inspection.
    """

    def __init__(self, api_key, ca_bundle=CA_BUNDLE):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.ca_bundle = ca_bundle

        # Create a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',  # Must use "Bearer" prefix
            'User-Agent': 'Ahrefs-API-Direct-Client/1.0'
        })
        self.session.verify = ca_bundle  # Use system CA bundle

    def get(self, endpoint, params=None):
        """
        Make a GET request to the Ahrefs API

        Args:
            endpoint: API endpoint (e.g., 'site-explorer/domain-rating')
            params: Query parameters as a dictionary

        Returns:
            JSON response as a dictionary

        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        url = f'{self.base_url}/{endpoint}'

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            # Log useful headers
            print(f"Request ID: {response.headers.get('x-request-id')}", file=sys.stderr)
            print(f"API Units Cost: {response.headers.get('x-api-units-cost-total')}", file=sys.stderr)
            print(f"API Cache Status: {response.headers.get('x-api-cache')}", file=sys.stderr)

            return response.json()

        except requests.exceptions.SSLError as e:
            print(f"SSL Error: {e}", file=sys.stderr)
            print("This usually means the CA bundle doesn't include the TLS inspection CA.", file=sys.stderr)
            raise
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}", file=sys.stderr)
            if e.response.status_code == 403:
                print("403 Forbidden - Check your API key and authorization header format.", file=sys.stderr)
            elif e.response.status_code == 404:
                print("404 Not Found - Check the endpoint path (V3 API only).", file=sys.stderr)
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}", file=sys.stderr)
            raise


def test_domain_rating(api, target, date):
    """Test the domain-rating endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: site-explorer/domain-rating")
    print(f"Target: {target}")
    print(f"Date: {date}")
    print('='*60)

    data = api.get('site-explorer/domain-rating', {
        'target': target,
        'date': date
    })

    print("\nResult:")
    print(json.dumps(data, indent=2))
    return data


def test_metrics(api, target, date):
    """Test the metrics endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: site-explorer/metrics")
    print(f"Target: {target}")
    print(f"Date: {date}")
    print('='*60)

    data = api.get('site-explorer/metrics', {
        'target': target,
        'date': date
    })

    print("\nResult:")
    print(json.dumps(data, indent=2))
    return data


def test_backlinks_stats(api, target, date):
    """Test the backlinks-stats endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: site-explorer/backlinks-stats")
    print(f"Target: {target}")
    print(f"Date: {date}")
    print('='*60)

    data = api.get('site-explorer/backlinks-stats', {
        'target': target,
        'date': date
    })

    print("\nResult:")
    print(json.dumps(data, indent=2))
    return data


def main():
    """Run example tests"""
    print("="*60)
    print("Ahrefs API Direct Access - Working Example")
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  API Key: {API_KEY[:20]}...")
    print(f"  Base URL: {BASE_URL}")
    print(f"  CA Bundle: {CA_BUNDLE}")

    # Initialize API client
    api = AhrefsAPI(API_KEY)

    # Test with ahrefs.com
    target = "ahrefs.com"
    date = "2025-12-01"

    try:
        # Test 1: Domain Rating
        test_domain_rating(api, target, date)

        # Test 2: Metrics
        test_metrics(api, target, date)

        # Test 3: Backlinks Stats
        test_backlinks_stats(api, target, date)

        print("\n" + "="*60)
        print("All tests completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR: {e}")
        print('='*60)
        sys.exit(1)


if __name__ == "__main__":
    main()
