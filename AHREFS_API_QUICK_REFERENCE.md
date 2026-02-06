# Ahrefs API Quick Reference - Direct Access

## TL;DR - What Works

### curl (SIMPLEST)
```bash
curl -H "Authorization: Bearer YOUR_AHREFS_API_KEY" \
  "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
```

### Python (RECOMMENDED)
```python
import requests

response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'Authorization': 'Bearer YOUR_AHREFS_API_KEY'},
    verify='/etc/ssl/certs/ca-certificates.crt'  # CRITICAL!
)
```

### wget
```bash
wget --header="Authorization: Bearer YOUR_AHREFS_API_KEY" \
  -O - "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
```

---

## Key Requirements

1. **Use V3 API only** - V2 doesn't exist (404)
2. **Authorization format** - MUST be `Authorization: Bearer <API_KEY>` (no other format works)
3. **SSL CA bundle** - Python must use `/etc/ssl/certs/ca-certificates.crt` (not certifi default)
4. **No query auth** - Query parameter `?token=` doesn't work (403)
5. **No alternative headers** - `X-API-Key` doesn't work (403)

---

## Why MCP Failed

The environment uses **Anthropic TLS inspection proxy** that intercepts HTTPS:
- Certificate issuer: `O=Anthropic; CN=sandbox-egress-production TLS Inspection CA`
- This CA is in system bundle: `/etc/ssl/certs/ca-certificates.crt`
- Python's certifi bundle doesn't include it
- **Solution:** Point Python to system CA bundle

---

## Common Errors

### 503 Service Unavailable + Certificate Error
```
TLS_error:|268435581:SSL routines:OPENSSL_internal:CERTIFICATE_VERIFY_FAILED
```
**Fix:** Use system CA bundle in Python: `verify='/etc/ssl/certs/ca-certificates.crt'`

### 403 Forbidden
```json
["Error","Forbidden"]
```
**Fix:** Use `Authorization: Bearer <API_KEY>` header format

### 404 Not Found
```json
["Error", ["NotFound", "this route does not exist /v2/..."]]
```
**Fix:** Use V3 API endpoints only

---

## Available Endpoints (V3)

All endpoints work with the correct configuration:

- `site-explorer/domain-rating` - Domain authority metrics
- `site-explorer/metrics` - Organic/paid search metrics
- `site-explorer/backlinks-stats` - Backlink statistics
- `site-explorer/organic-keywords` - Keyword rankings
- `site-explorer/top-pages` - Top performing pages
- `keywords-explorer/overview` - Keyword research
- `serp-overview/serp-overview` - SERP analysis
- And many more...

---

## Working Example Script

Run the provided example:
```bash
python3 ahrefs_api_working_example.py
```

This demonstrates:
- Correct SSL configuration
- Proper authentication
- Multiple endpoint calls
- Error handling

---

## Test Results Summary

**Tested Methods:**
- ✅ curl with Bearer token (22/25 tests passed)
- ✅ wget with Bearer token (4/5 tests passed)
- ✅ Python with system CA bundle (works perfectly)
- ✅ Python with verify=False (works but not secure)
- ❌ Node.js (all methods failed - DNS issues)
- ❌ Python with default certifi (certificate error)

**Full test results:** See `AHREFS_API_TEST_RESULTS.md`

---

## For MCP Integration

Update the MCP server to use:

```python
import requests

class AhrefsAPI:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })
        self.session.verify = '/etc/ssl/certs/ca-certificates.crt'  # KEY FIX

    def get(self, endpoint, params):
        return self.session.get(
            f'https://api.ahrefs.com/v3/{endpoint}',
            params=params
        ).json()
```

This single change fixes the MCP integration.
