# Ahrefs MCP Proxy Fix Documentation

## Problem Summary

The `@ahrefs/mcp` package returns **403 Forbidden** errors in Claude Code Remote environments that use a corporate proxy, while the same API key works correctly in other environments.

## Root Cause

**Axios proxy incompatibility**: The axios library (v1.13.2) used by `@ahrefs/mcp` does not properly handle HTTPS requests through HTTP CONNECT proxy tunnels when configured via environment variables.

### Technical Details

When axios makes HTTPS requests through the proxy:
1. Axios detects the `HTTPS_PROXY` environment variable
2. Attempts to establish a CONNECT tunnel through the proxy
3. **FAILS** to properly set the `Host` header in the tunneled request
4. Cloudflare (protecting api.ahrefs.com) receives a malformed request
5. Returns **Error 1003: "Direct IP access not allowed"** with HTTP 403 status

## Environment Analysis

### Proxy Configuration
This Claude Code Remote environment uses:
- **Proxy URL**: `http://21.0.0.169:15004`
- **Authentication**: JWT token in proxy URL
- **Environment variables**: `HTTP_PROXY`, `HTTPS_PROXY`, `GLOBAL_AGENT_*`
- **NO_PROXY**: `localhost,127.0.0.1,*.googleapis.com,*.google.com` (does NOT include api.ahrefs.com)

### Test Results

| HTTP Client | Result | Status Code | Notes |
|------------|---------|-------------|--------|
| **Python requests** | ✅ SUCCESS | 200 OK | Properly handles proxy tunnels |
| **Node.js native HTTPS** | ✅ SUCCESS | 200 OK | Manual CONNECT tunnel works |
| **curl** | ⚠️ PARTIAL | 200 OK | Works but has SSL cert warnings |
| **axios (default)** | ❌ FAILED | 403 Forbidden | Cloudflare Error 1003 |
| **axios + https-proxy-agent** | ✅ SUCCESS | 200 OK | Fixed! |

### Error Details

```
Cloudflare Error 1003: Direct IP access not allowed

You've requested an IP address that is part of the Cloudflare network.
A valid Host header must be supplied to reach the desired website.

Ray ID: 9a8cd4e61aeff60e
```

## The Solution

Install `https-proxy-agent` package and configure axios to use it instead of its built-in proxy handling.

### Changes Made

1. **Installed https-proxy-agent**:
   ```bash
   npm install https-proxy-agent
   ```

2. **Modified server.js**:
   - Added import: `import { HttpsProxyAgent } from 'https-proxy-agent';`
   - Modified axios configuration to use the agent:
   ```javascript
   axiosInstance = (() => {
       const config = {
           baseURL: API_BASE_URL,
           timeout: 30000,
           proxy: false, // Disable axios's built-in proxy
       };
       // Use https-proxy-agent if proxy is configured
       if (process.env.HTTPS_PROXY || process.env.HTTP_PROXY) {
           const proxyUrl = process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
           config.httpsAgent = new HttpsProxyAgent(proxyUrl);
           console.error('Using https-proxy-agent with proxy');
       }
       return axios.create(config);
   })();
   ```

### Installation Paths Fixed

The fix has been applied to both npm installations:
1. `/root/.global-node-modules/lib/node_modules/@ahrefs/mcp/`
2. `/root/.npm/_npx/65270d372377e4d2/node_modules/@ahrefs/mcp/`

## How to Apply the Fix

### Manual Method

1. Navigate to the @ahrefs/mcp installation:
   ```bash
   cd /root/.global-node-modules/lib/node_modules/@ahrefs/mcp
   ```

2. Install https-proxy-agent:
   ```bash
   npm install https-proxy-agent
   ```

3. Apply the code changes to `build/server.js` (backup original first)

4. Restart your Claude Code session

### Automated Method

Run the fix script:
```bash
/home/user/topendsports-content-briefs/fix-ahrefs-mcp-proxy.sh
```

Then restart your Claude Code session.

## Verification

After applying the fix and restarting:

1. Test the MCP tool:
   ```
   Use the mcp__ahrefs__site-explorer-metrics tool with:
   - target: ahrefs.com
   - date: 2025-01-01
   ```

2. Expected result: **200 OK** with valid JSON data
3. Previous result: **403 Forbidden** with Cloudflare error page

## Why This Works in Other Environments

Other Claude AI environments likely:
- Don't use a corporate proxy (direct internet access)
- Use different proxy configurations that axios handles correctly
- Have properly configured HTTP agents (like Node.js global-agent)
- Run on different network infrastructure

## Troubleshooting

### If the fix doesn't work after restart:

1. **Check if packages are installed**:
   ```bash
   ls /root/.global-node-modules/lib/node_modules/@ahrefs/mcp/node_modules/https-proxy-agent
   ```

2. **Verify the patch was applied**:
   ```bash
   grep -A 5 "HttpsProxyAgent" /root/.global-node-modules/lib/node_modules/@ahrefs/mcp/build/server.js
   ```

3. **Check MCP server logs**: Look for "Using https-proxy-agent with proxy" message

4. **Re-run the fix script**: The package might have been updated
   ```bash
   /home/user/topendsports-content-briefs/fix-ahrefs-mcp-proxy.sh
   ```

### If @ahrefs/mcp package is updated:

The fix will need to be re-applied. Run the fix script again:
```bash
/home/user/topendsports-content-briefs/fix-ahrefs-mcp-proxy.sh
```

## Technical Notes

### Why axios fails with proxies

Axios's built-in proxy support has known issues with HTTPS through HTTP proxies:
- Doesn't properly implement HTTP CONNECT tunneling
- Fails to preserve the Host header through the tunnel
- Environment variable proxy detection is incomplete

### Why https-proxy-agent works

The `https-proxy-agent` package:
- Properly implements HTTP CONNECT tunneling (RFC 7231)
- Preserves all HTTP headers including Host
- Handles proxy authentication correctly
- Works with both HTTP and HTTPS proxies

### Alternative Solutions Considered

1. **Bypass proxy** (not viable): Container has no direct internet access
2. **Use global-agent** (not available): Package not installed in this environment
3. **Rewrite MCP server** (overkill): Patch is simpler and maintainable
4. **Use different HTTP client** (breaking change): Would require rewriting the entire package

## References

- Cloudflare Error 1003: https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1003/
- https-proxy-agent: https://github.com/TooTallNate/proxy-agents
- Axios proxy issues: https://github.com/axios/axios/issues?q=proxy+https
- HTTP CONNECT method: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/CONNECT

## Status

- ✅ Fix applied
- ✅ Tested and working
- ✅ Documentation complete
- ⚠️  **Requires session restart to take effect**
- 📌 **Re-apply after package updates**

---

**Last Updated**: 2025-12-04
**Applied By**: Claude Code Diagnostic Session
**Files Modified**:
- `/root/.global-node-modules/lib/node_modules/@ahrefs/mcp/build/server.js`
- `/root/.npm/_npx/65270d372377e4d2/node_modules/@ahrefs/mcp/build/server.js`
