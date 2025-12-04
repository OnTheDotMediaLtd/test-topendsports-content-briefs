#!/bin/bash
# Fix Ahrefs MCP package to work with proxy

set -e

echo "🔧 Fixing Ahrefs MCP package for proxy support..."

# Function to fix a specific installation
fix_installation() {
  local base_path=$1
  echo "Fixing installation at: $base_path"
  
  if [ ! -d "$base_path" ]; then
    echo "  ⚠️  Path not found, skipping"
    return
  fi
  
  cd "$base_path"
  
  # Install https-proxy-agent
  echo "  📦 Installing https-proxy-agent..."
  npm install https-proxy-agent >/dev/null 2>&1
  
  # Backup original
  if [ ! -f "build/server.js.backup" ]; then
    cp build/server.js build/server.js.backup
  fi
  
  # Apply patch
  cat > build/fix_proxy.cjs << 'PATCH_EOF'
const fs = require('fs');
let content = fs.readFileSync('server.js', 'utf8');
const lines = content.split('\n');
const importLineIndex = lines.findIndex(line => line.includes("import axios from 'axios'"));
if (importLineIndex !== -1) {
  lines.splice(importLineIndex + 1, 0, "import { HttpsProxyAgent } from 'https-proxy-agent';");
}
content = lines.join('\n');
const oldConfig = `axiosInstance = axios.create({
        baseURL: API_BASE_URL, // Axios will use this as the base for requests
        timeout: 30000, // 30 second timeout
    });`;
const newConfig = `axiosInstance = (() => {
        const config = {
            baseURL: API_BASE_URL,
            timeout: 30000,
            proxy: false,
        };
        if (process.env.HTTPS_PROXY || process.env.HTTP_PROXY) {
            const proxyUrl = process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
            config.httpsAgent = new HttpsProxyAgent(proxyUrl);
            console.error('Using https-proxy-agent with proxy:', proxyUrl.replace(/jwt_[^@]+/, 'jwt_***'));
        }
        return axios.create(config);
    })();`;
content = content.replace(oldConfig, newConfig);
fs.writeFileSync('server.js', content, 'utf8');
console.log('✅ Patched');
PATCH_EOF
  
  cd build
  node fix_proxy.cjs
  rm fix_proxy.cjs
  
  echo "  ✅ Fixed successfully"
}

# Fix both installations
fix_installation "/root/.global-node-modules/lib/node_modules/@ahrefs/mcp"
fix_installation "/root/.npm/_npx/65270d372377e4d2/node_modules/@ahrefs/mcp"

echo ""
echo "✅ All fixes applied!"
echo "⚠️  You need to restart your Claude Code session for changes to take effect"
