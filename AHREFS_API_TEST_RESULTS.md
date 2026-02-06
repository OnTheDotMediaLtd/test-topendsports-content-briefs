# Ahrefs API Direct Access Test Results

**Test Date:** 2025-12-04
**API Key:** YOUR_AHREFS_API_KEY
**Test Endpoint:** https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01

## Executive Summary

**WORKING SOLUTIONS:**
1. **curl with Bearer token** - ✅ WORKS PERFECTLY
2. **wget with Bearer token** - ✅ WORKS PERFECTLY
3. **Python requests with system CA bundle** - ✅ WORKS PERFECTLY
4. **Python requests with SSL disabled** - ✅ WORKS (not recommended)

**FAILED APPROACHES:**
- Node.js (all methods) - DNS resolution failures
- Python with default SSL settings - Certificate verification failures
- Authorization without "Bearer" prefix - 403 Forbidden
- Query parameter authentication - 403 Forbidden
- V2 API endpoints - 404 Not Found (V2 doesn't exist)

---

## Root Cause Analysis

### TLS Inspection Proxy

The environment uses an **Anthropic TLS inspection proxy** for egress traffic:

- **Proxy:** http://21.0.0.169:15004
- **Certificate Issuer:** O=Anthropic; CN=sandbox-egress-production TLS Inspection CA
- **Certificate Subject:** CN=*.ahrefs.com

This is a man-in-the-middle proxy that intercepts and re-encrypts HTTPS traffic. The proxy's CA certificate is installed in the system CA bundle at `/etc/ssl/certs/ca-certificates.crt`, which is why curl and wget work by default.

### Python SSL Issue

Python's `requests` library by default uses its own bundled CA certificates (from the `certifi` package) which does NOT include the Anthropic TLS inspection CA. This causes certificate verification failures:

```
TLS_error:|268435581:SSL routines:OPENSSL_internal:CERTIFICATE_VERIFY_FAILED
```

**Solution:** Point Python to the system CA bundle instead of using the default.

### Node.js DNS Issue

Node.js completely fails with DNS resolution errors:
```
Error: getaddrinfo EAI_AGAIN api.ahrefs.com
```

This suggests Node.js DNS resolution is not properly configured in the container environment, or there's a DNS caching issue.

---

## Detailed Test Results

### 1. curl Tests (25 tests total: 22 succeeded, 3 failed)

#### ✅ WORKING curl Commands:

```bash
# Standard Bearer token (RECOMMENDED)
curl -H "Authorization: Bearer YOUR_AHREFS_API_KEY" \
  "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"

# Response:
# { "domain_rating": { "domain_rating": 91.0, "ahrefs_rank": 640 } }
```

**All successful curl variations:**
- Bearer token with default SSL ✅
- Bearer token with TLS 1.2 ✅
- Bearer token with TLS 1.3 ✅
- Bearer token with IPv4 ✅
- Bearer token with IPv6 ✅
- Bearer token with compression ✅
- Bearer token with custom User-Agent ✅
- Bearer token with all headers ✅
- Bearer token with cert status ✅
- Bearer token with connection timeout ✅

#### ❌ FAILED curl Commands:

```bash
# Direct API key without "Bearer" prefix
curl -H "Authorization: YOUR_AHREFS_API_KEY" \
  "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
# Result: 403 Forbidden - ["Error","Forbidden"]

# Token prefix instead of Bearer
curl -H "Authorization: Token YOUR_AHREFS_API_KEY" \
  "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
# Result: 503 Service Unavailable - Certificate verification error

# Query parameter authentication
curl "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01&token=YOUR_AHREFS_API_KEY"
# Result: 403 Forbidden - ["Error","Forbidden"]

# X-API-Key header
curl -H "X-API-Key: YOUR_AHREFS_API_KEY" \
  "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
# Result: 403 Forbidden - ["Error","Forbidden"]
```

**Note:** The `--insecure` flag actually makes things WORSE, causing the upstream API to reject the connection with certificate errors. Always use proper SSL verification.

---

### 2. wget Tests (5 tests total: 4 succeeded, 1 failed)

#### ✅ WORKING wget Commands:

```bash
# Standard Bearer token (RECOMMENDED)
wget --header="Authorization: Bearer YOUR_AHREFS_API_KEY" \
  -O - "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"

# Response:
# { "domain_rating": { "domain_rating": 91.0, "ahrefs_rank": 640 } }
```

**All successful wget variations:**
- Bearer token with default settings ✅
- Bearer token with no SSL check ✅
- Bearer token with debug output ✅
- Bearer token with custom User-Agent ✅

#### ❌ FAILED wget Commands:

```bash
# Query parameter authentication
wget -O - "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01&token=YOUR_AHREFS_API_KEY"
# Result: 403 Forbidden
```

---

### 3. Python requests Tests (10 tests total: 10 completed)

#### ✅ WORKING Python Methods:

**Method 1: Using System CA Bundle (RECOMMENDED)**
```python
import requests

response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'Authorization': 'Bearer YOUR_AHREFS_API_KEY'},
    verify='/etc/ssl/certs/ca-certificates.crt'  # Use system CA bundle
)
# Status: 200 OK
# Response: {"domain_rating": {"domain_rating": 91.0, "ahrefs_rank": 640}}
```

**Method 2: Disabling SSL Verification (NOT RECOMMENDED)**
```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'Authorization': 'Bearer YOUR_AHREFS_API_KEY'},
    verify=False  # Disable SSL verification
)
# Status: 200 OK
# Response: {"domain_rating": {"domain_rating": 91.0, "ahrefs_rank": 640}}
```

#### ❌ FAILED Python Methods:

```python
# Default SSL verification (uses certifi CA bundle)
response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'Authorization': 'Bearer YOUR_AHREFS_API_KEY'},
    verify=True  # Default - uses certifi bundle
)
# Result: 503 Service Unavailable
# Error: CERTIFICATE_VERIFY_FAILED

# Direct API key without Bearer prefix
response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'Authorization': 'YOUR_AHREFS_API_KEY'},
    verify='/etc/ssl/certs/ca-certificates.crt'
)
# Result: 403 Forbidden - ["Error","Forbidden"]

# Token prefix
response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'Authorization': 'Token YOUR_AHREFS_API_KEY'},
    verify='/etc/ssl/certs/ca-certificates.crt'
)
# Result: Certificate verification error

# X-API-Key header
response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    headers={'X-API-Key': 'YOUR_AHREFS_API_KEY'},
    verify='/etc/ssl/certs/ca-certificates.crt'
)
# Result: 403 Forbidden

# Query parameter authentication
response = requests.get(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating?token=YOUR_AHREFS_API_KEY',
    params={'target': 'ahrefs.com', 'date': '2025-12-01'},
    verify='/etc/ssl/certs/ca-certificates.crt'
)
# Result: 403 Forbidden
```

---

### 4. Node.js Tests (10 tests total: 0 succeeded, 8 failed, 2 skipped)

#### ❌ ALL Node.js Methods FAILED:

**fetch() API:**
```javascript
const response = await fetch(
    'https://api.ahrefs.com/v3/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01',
    {
        headers: {
            'Authorization': 'Bearer YOUR_AHREFS_API_KEY'
        }
    }
);
// Error: fetch failed
// TypeError: fetch failed
```

**https module:**
```javascript
const https = require('https');
// Result: Error: getaddrinfo EAI_AGAIN api.ahrefs.com
// DNS resolution completely fails
```

**https module with SSL disabled:**
```javascript
const https = require('https');
const options = {
    rejectUnauthorized: false
};
// Result: Error: getaddrinfo EAI_AGAIN api.ahrefs.com
// Still fails at DNS level
```

**axios (not installed):**
Axios tests were skipped because the package is not installed.

---

## API Version Tests

### V3 API (Current)
- **Base URL:** https://api.ahrefs.com/v3
- **Status:** ✅ WORKING
- **Endpoints Tested:**
  - `/site-explorer/domain-rating` ✅
  - `/site-explorer/metrics` ✅

### V2 API (Legacy)
- **Base URL:** https://api.ahrefs.com/v2
- **Status:** ❌ DOES NOT EXIST
- **Error:** 404 Not Found
- **Message:** "this route does not exist /v2/site-explorer/domain-rating"

**Conclusion:** Only V3 API is available. Do not attempt to use V2 endpoints.

---

## Authentication Method Tests

### ✅ WORKING: Bearer Token
```
Authorization: Bearer YOUR_AHREFS_API_KEY
```
**Result:** 200 OK - Returns data successfully

### ❌ FAILED: Direct API Key
```
Authorization: YOUR_AHREFS_API_KEY
```
**Result:** 403 Forbidden

### ❌ FAILED: Token Prefix
```
Authorization: Token YOUR_AHREFS_API_KEY
```
**Result:** 503 Service Unavailable (causes cert errors)

### ❌ FAILED: X-API-Key Header
```
X-API-Key: YOUR_AHREFS_API_KEY
```
**Result:** 403 Forbidden

### ❌ FAILED: Query Parameter
```
?token=YOUR_AHREFS_API_KEY
```
**Result:** 403 Forbidden

**Conclusion:** ONLY "Authorization: Bearer <API_KEY>" works. No other authentication method is accepted.

---

## SSL/TLS Configuration Tests

### TLS Versions Tested:
- **TLS 1.2** ✅ Works
- **TLS 1.3** ✅ Works (default)

### SSL Certificate Details:
- **Subject:** CN=*.ahrefs.com
- **Issuer:** O=Anthropic; CN=sandbox-egress-production TLS Inspection CA
- **Valid From:** Dec 4 16:09:53 2025 GMT
- **Valid Until:** Dec 5 19:27:58 2025 GMT (short-lived certificate)
- **Signature Algorithm:** sha256WithRSAEncryption
- **Public Key:** EC/prime256v1 (256 bits)

### SSL Verification:
- **curl with verify:** ✅ Works (uses system CA bundle)
- **wget with verify:** ✅ Works (uses system CA bundle)
- **Python with system CA bundle:** ✅ Works
- **Python with certifi bundle:** ❌ Fails (doesn't trust Anthropic CA)
- **Python with verify=False:** ✅ Works (not recommended)
- **--insecure flag:** ❌ Makes things worse (causes upstream cert errors)

---

## Response Headers Analysis

### Successful Response Headers:
```
HTTP/2 200
date: Thu, 04 Dec 2025 16:53:59 GMT
content-type: application/json
server: cloudflare
cf-ray: 9a8cd2b4bda261d5-ORD
cf-cache-status: DYNAMIC
strict-transport-security: max-age=31536000; includeSubDomains; preload
x-api-cache: no_cache
x-api-rows: 1
x-api-units-cost-row: 2
x-api-units-cost-total: 50
x-api-units-cost-total-actual: 0
x-request-id: 011ddf19b0826e81c5a3b4f066d61074
x-trace-id: c4c348fb741f40e43ce2c6879ac887a2
```

### Key Response Headers:
- **x-api-rows:** Number of rows returned (1 in this case)
- **x-api-units-cost-row:** Cost per row (2 units)
- **x-api-units-cost-total:** Total cost with minimum (50 units)
- **x-api-units-cost-total-actual:** Actual cost before minimum applied (0 in this case)
- **x-api-cache:** Cache status (no_cache means fresh data)
- **x-request-id:** Unique request identifier
- **x-trace-id:** Trace identifier for debugging

---

## Recommendations

### For Production Use:

1. **Use curl for simple requests:**
   ```bash
   curl -H "Authorization: Bearer ${AHREFS_API_KEY}" \
     "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=example.com&date=2025-12-01"
   ```

2. **Use Python with system CA bundle for complex workflows:**
   ```python
   import requests

   def call_ahrefs_api(endpoint, params):
       response = requests.get(
           f'https://api.ahrefs.com/v3/{endpoint}',
           params=params,
           headers={'Authorization': f'Bearer {api_key}'},
           verify='/etc/ssl/certs/ca-certificates.crt'
       )
       response.raise_for_status()
       return response.json()
   ```

3. **Create a wrapper class:**
   ```python
   import requests

   class AhrefsAPI:
       def __init__(self, api_key):
           self.api_key = api_key
           self.base_url = 'https://api.ahrefs.com/v3'
           self.session = requests.Session()
           self.session.headers.update({
               'Authorization': f'Bearer {api_key}'
           })
           self.session.verify = '/etc/ssl/certs/ca-certificates.crt'

       def get(self, endpoint, params=None):
           url = f'{self.base_url}/{endpoint}'
           response = self.session.get(url, params=params)
           response.raise_for_status()
           return response.json()

   # Usage:
   api = AhrefsAPI('YOUR_AHREFS_API_KEY')
   data = api.get('site-explorer/domain-rating', {
       'target': 'ahrefs.com',
       'date': '2025-12-01'
   })
   ```

### For MCP Integration:

The MCP wrapper should:
1. Use Python requests with `verify='/etc/ssl/certs/ca-certificates.crt'`
2. Always use "Bearer" prefix for Authorization header
3. Only use V3 API endpoints
4. Include error handling for certificate issues
5. Log the x-request-id and x-trace-id for debugging

---

## Error Messages Reference

### 403 Forbidden
```json
["Error","Forbidden"]
```
**Cause:** Invalid authentication format (missing "Bearer" prefix, wrong header name, or query parameter auth)
**Solution:** Use `Authorization: Bearer <API_KEY>` header

### 503 Service Unavailable
```
upstream connect error or disconnect/reset before headers.
reset reason: remote connection failure,
transport failure reason: TLS_error:|268435581:SSL routines:OPENSSL_internal:CERTIFICATE_VERIFY_FAILED:TLS_error_end
```
**Cause:** SSL certificate verification failure (client doesn't trust Anthropic TLS inspection CA)
**Solution:** Use system CA bundle (`/etc/ssl/certs/ca-certificates.crt`)

### 404 Not Found
```json
["Error", ["NotFound", "this route does not exist /v2/site-explorer/domain-rating"]]
```
**Cause:** Using V2 API endpoints which don't exist
**Solution:** Use V3 API endpoints only

---

## Test Scripts

All test scripts are located in the project root:

- **test_ahrefs_api.py** - Python requests library tests (10 test cases)
- **test_ahrefs_api.js** - Node.js fetch/https/axios tests (10 test cases)
- **test_ahrefs_api.sh** - curl and wget tests (25 test cases)

Run them with:
```bash
python3 test_ahrefs_api.py
node test_ahrefs_api.js
bash test_ahrefs_api.sh
```

---

## Conclusion

The Ahrefs API is fully accessible from this environment using curl, wget, or Python requests with the proper configuration. The key requirements are:

1. **Use V3 API endpoints** (V2 doesn't exist)
2. **Use "Authorization: Bearer <API_KEY>" header** (only this format works)
3. **Use system CA bundle for SSL verification** (includes Anthropic TLS inspection CA)
4. **Don't use query parameter or alternative header authentication** (always fails)

The MCP integration issues were likely caused by Python requests using the certifi CA bundle instead of the system CA bundle, which doesn't include the required Anthropic TLS inspection CA certificate.
