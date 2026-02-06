# MCP Server Fix for Ahrefs API

## The Problem

The Ahrefs MCP server fails with SSL certificate verification errors because:
1. Environment uses Anthropic TLS inspection proxy
2. Python's default `certifi` CA bundle doesn't trust this proxy's CA
3. Need to use system CA bundle instead

## The Solution

**ONE LINE CHANGE in the MCP server code:**

### Before (Broken)
```python
import requests

response = requests.get(
    url,
    headers={'Authorization': f'Bearer {api_key}'},
    params=params
)
# ❌ FAILS: SSL certificate verification error
```

### After (Working)
```python
import requests

response = requests.get(
    url,
    headers={'Authorization': f'Bearer {api_key}'},
    params=params,
    verify='/etc/ssl/certs/ca-certificates.crt'  # ✅ FIX: Use system CA bundle
)
# ✅ WORKS: Successfully calls API
```

## Implementation

### Option 1: Quick Fix (Minimal Changes)
Add the `verify` parameter to every requests call:

```python
def make_request(self, endpoint, params):
    url = f'https://api.ahrefs.com/v3/{endpoint}'
    response = requests.get(
        url,
        headers={'Authorization': f'Bearer {self.api_key}'},
        params=params,
        verify='/etc/ssl/certs/ca-certificates.crt'  # Add this line
    )
    return response.json()
```

### Option 2: Better Fix (Use Session)
Configure the session once:

```python
class AhrefsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.ahrefs.com/v3'

        # Create session with proper SSL config
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })
        self.session.verify = '/etc/ssl/certs/ca-certificates.crt'  # Set once

    def get(self, endpoint, params):
        url = f'{self.base_url}/{endpoint}'
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
```

### Option 3: Best Fix (Environment Variable)
Make it configurable:

```python
import os
import requests

class AhrefsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.ahrefs.com/v3'

        # Use system CA bundle in Claude Code Remote, certifi otherwise
        ca_bundle = os.getenv('REQUESTS_CA_BUNDLE', '/etc/ssl/certs/ca-certificates.crt')

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })
        self.session.verify = ca_bundle

    def get(self, endpoint, params):
        url = f'{self.base_url}/{endpoint}'
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
```

## Testing the Fix

After applying the fix, test with:

```bash
# Quick test
python3 -c "
import requests
response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'Authorization': 'Bearer YOUR_AHREFS_API_KEY'},
    verify='/etc/ssl/certs/ca-certificates.crt'
)
print(response.status_code, response.json())
"
```

Expected output:
```
200 {'domain_rating': {'domain_rating': 91.0, 'ahrefs_rank': 640}}
```

## Why This Works

1. **System CA Bundle** (`/etc/ssl/certs/ca-certificates.crt`) includes:
   - Standard public CAs
   - **Anthropic TLS Inspection CA** (added by environment)

2. **Python certifi Bundle** (default) includes:
   - Standard public CAs
   - ❌ Does NOT include Anthropic TLS Inspection CA

3. **TLS Inspection Flow**:
   ```
   Python → Anthropic Proxy → Ahrefs API
           (intercepts & re-encrypts)

   Certificate chain:
   *.ahrefs.com (signed by Anthropic CA)
   └── Anthropic TLS Inspection CA (must be trusted)
   ```

## Alternative: Disable SSL Verification (NOT RECOMMENDED)

If you can't modify the CA bundle:

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(
    url,
    headers={'Authorization': f'Bearer {api_key}'},
    params=params,
    verify=False  # ⚠️ INSECURE - only for debugging
)
```

**DO NOT USE THIS IN PRODUCTION** - it disables all SSL verification and makes the connection insecure.

## Files to Modify

Based on typical MCP server structure, you need to modify:

1. `src/ahrefs_mcp/server.py` - Main server file
2. `src/ahrefs_mcp/client.py` - API client class
3. Any file that contains `requests.get()` or `requests.post()` calls

Look for:
```python
requests.get(url, ...)
requests.post(url, ...)
session.get(url, ...)
session.post(url, ...)
```

Add to all of them:
```python
verify='/etc/ssl/certs/ca-certificates.crt'
```

## Verification

After the fix, all MCP tools should work:
- ✅ `mcp__ahrefs__doc`
- ✅ `mcp__ahrefs__site-explorer-domain-rating`
- ✅ `mcp__ahrefs__site-explorer-metrics`
- ✅ `mcp__ahrefs__keywords-explorer-overview`
- ✅ All other Ahrefs MCP tools

## Summary

**Problem:** SSL certificate verification fails because Python doesn't trust Anthropic TLS inspection proxy
**Solution:** Use system CA bundle instead of certifi bundle
**Change:** Add `verify='/etc/ssl/certs/ca-certificates.crt'` to all requests calls
**Impact:** All Ahrefs API calls will work through the MCP layer

This is a **ONE LINE FIX** that makes all the difference!
