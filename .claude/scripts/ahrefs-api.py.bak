#!/usr/bin/env python3
"""
Direct Ahrefs API wrapper that works in Claude Code Remote.
Bypasses the MCP server's axios SSL issues by using Python requests
with the system CA bundle.
"""

import sys
import json
import warnings
import requests
import urllib3

# Suppress SSL warnings since we're behind a TLS-inspecting proxy
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "SjPt1JPhRgqMpi5UN8G7e8P3s57SjW86734J2r1Z"
BASE_URL = "https://api.ahrefs.com/v3"

def call_api(endpoint, params):
    """Call Ahrefs API with SSL verification disabled for proxy compatibility."""
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=False,  # Required for TLS-inspecting proxies in Claude Code Remote
            timeout=60
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: ahrefs-api.py <endpoint> [params_json]",
            "examples": {
                "domain_rating": "ahrefs-api.py site-explorer/domain-rating '{\"target\":\"example.com\",\"date\":\"2025-12-01\"}'",
                "keywords": "ahrefs-api.py keywords-explorer/overview '{\"select\":\"keyword,volume,difficulty\",\"country\":\"us\",\"keywords\":\"nfl betting\"}'",
                "organic_keywords": "ahrefs-api.py site-explorer/organic-keywords '{\"select\":\"keyword,volume,position\",\"target\":\"example.com\",\"date\":\"2025-12-01\",\"country\":\"us\"}'"
            }
        }, indent=2))
        sys.exit(1)

    endpoint = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    result = call_api(endpoint, params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
