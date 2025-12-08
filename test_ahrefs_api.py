#!/usr/bin/env python3
"""
Test Ahrefs API with Python requests library
Testing different SSL and configuration settings
"""

import requests
import json
import urllib3
from datetime import datetime

API_KEY = "SjPt1JPhRgqMpi5UN8G7e8P3s57SjW86734J2r1Z"
BASE_URL_V3 = "https://api.ahrefs.com/v3"
BASE_URL_V2 = "https://api.ahrefs.com/v2"

def print_separator(title):
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")

def test_request(method_name, url, headers, verify_ssl=True, timeout=30):
    """Test a single request configuration"""
    print(f"Testing: {method_name}")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"SSL Verify: {verify_ssl}")
    print(f"Timeout: {timeout}s")
    print("-" * 80)

    try:
        response = requests.get(
            url,
            headers=headers,
            verify=verify_ssl,
            timeout=timeout
        )

        print(f"Status Code: {response.status_code}")
        print(f"Status Reason: {response.reason}")
        print("\nResponse Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")

        print("\nResponse Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)

        return True

    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {str(e)}")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {str(e)}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {str(e)}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__}: {str(e)}")
        return False
    finally:
        print("\n")

# Test configurations
tests = []

# V3 API Tests
endpoint_v3 = "/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
url_v3 = BASE_URL_V3 + endpoint_v3

# Test 1: Bearer token with SSL verification
tests.append({
    "name": "V3 API - Bearer token - SSL verify",
    "url": url_v3,
    "headers": {"Authorization": f"Bearer {API_KEY}"},
    "verify_ssl": True
})

# Test 2: Bearer token without SSL verification
tests.append({
    "name": "V3 API - Bearer token - SSL disabled",
    "url": url_v3,
    "headers": {"Authorization": f"Bearer {API_KEY}"},
    "verify_ssl": False
})

# Test 3: Direct API key in header
tests.append({
    "name": "V3 API - Direct API key - SSL verify",
    "url": url_v3,
    "headers": {"Authorization": API_KEY},
    "verify_ssl": True
})

# Test 4: API key with 'Token' prefix
tests.append({
    "name": "V3 API - Token prefix - SSL verify",
    "url": url_v3,
    "headers": {"Authorization": f"Token {API_KEY}"},
    "verify_ssl": True
})

# Test 5: API key in custom header
tests.append({
    "name": "V3 API - X-API-Key header - SSL verify",
    "url": url_v3,
    "headers": {"X-API-Key": API_KEY},
    "verify_ssl": True
})

# Test 6: API key as query parameter
tests.append({
    "name": "V3 API - API key in query string - SSL verify",
    "url": url_v3 + f"&token={API_KEY}",
    "headers": {},
    "verify_ssl": True
})

# V2 API Tests (if they exist)
endpoint_v2 = "/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
url_v2 = BASE_URL_V2 + endpoint_v2

# Test 7: V2 API with Bearer token
tests.append({
    "name": "V2 API - Bearer token - SSL verify",
    "url": url_v2,
    "headers": {"Authorization": f"Bearer {API_KEY}"},
    "verify_ssl": True
})

# Test 8: V2 API with query parameter
tests.append({
    "name": "V2 API - API key in query string - SSL verify",
    "url": url_v2 + f"&token={API_KEY}",
    "headers": {},
    "verify_ssl": True
})

# Test 9: Different endpoint format
tests.append({
    "name": "V3 API - Alternative endpoint format",
    "url": "https://api.ahrefs.com/v3/site-explorer/metrics?target=ahrefs.com&date=2025-12-01",
    "headers": {"Authorization": f"Bearer {API_KEY}"},
    "verify_ssl": True
})

# Test 10: With User-Agent and Accept headers
tests.append({
    "name": "V3 API - With full headers",
    "url": url_v3,
    "headers": {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Python-Requests-Test/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
    "verify_ssl": True
})

# Disable SSL warnings for insecure tests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print_separator("AHREFS API PYTHON TESTING")
print(f"Test started at: {datetime.now()}")
print(f"Total tests: {len(tests)}")

results = {"success": [], "failed": []}

for i, test in enumerate(tests, 1):
    print_separator(f"TEST {i}/{len(tests)}: {test['name']}")
    success = test_request(
        test['name'],
        test['url'],
        test['headers'],
        test.get('verify_ssl', True),
        test.get('timeout', 30)
    )

    if success:
        results["success"].append(test['name'])
    else:
        results["failed"].append(test['name'])

# Summary
print_separator("TEST SUMMARY")
print(f"Successful tests: {len(results['success'])}/{len(tests)}")
for test_name in results['success']:
    print(f"  ✓ {test_name}")

print(f"\nFailed tests: {len(results['failed'])}/{len(tests)}")
for test_name in results['failed']:
    print(f"  ✗ {test_name}")

print(f"\nTest completed at: {datetime.now()}")
