#!/bin/bash
set -euo pipefail

# Only run in remote environments (Claude Code on the web)
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "=== TopEndSports Content Briefs - Session Initialization ==="

# Use CLAUDE_PROJECT_DIR if set, otherwise detect from script location
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

echo "Project directory: $PROJECT_DIR"

# 1. Install MCP server dependencies
MCP_SERVER_DIR="$PROJECT_DIR/mcp-server"
if [ -d "$MCP_SERVER_DIR" ]; then
    echo "Installing MCP server dependencies..."
    cd "$MCP_SERVER_DIR"
    npm install --prefer-offline --no-audit --no-fund 2>/dev/null || npm install
    echo "✓ MCP server dependencies installed"
fi

# 2. Install Ahrefs MCP package globally
echo "Checking Ahrefs MCP package..."
if ! npm list -g @ahrefs/mcp --prefix=/root/.global-node-modules &>/dev/null; then
    echo "Installing Ahrefs MCP package..."
    npm install --prefix=/root/.global-node-modules @ahrefs/mcp -g --no-audit --no-fund 2>/dev/null || true
fi
echo "✓ Ahrefs MCP package ready"

# 3. Install Python dependencies for document conversion
echo "Checking Python dependencies..."
if ! python3 -c "import docx" 2>/dev/null; then
    echo "Installing python-docx..."
    pip3 install python-docx --quiet 2>/dev/null || pip3 install python-docx
fi
echo "✓ Python dependencies ready"

# 4. Verify MCP configuration exists
if [ -f "$PROJECT_DIR/.mcp.json" ]; then
    echo "✓ MCP configuration found"
else
    echo "⚠ Warning: .mcp.json not found"
fi

echo "=== Session Initialization Complete ==="
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  🚨 GUARDRAILS REMINDER - READ CLAUDE.md BEFORE ANY BRIEF 🚨     ║"
echo "╠══════════════════════════════════════════════════════════════════╣"
echo "║  When generating briefs, you MUST:                               ║"
echo "║    1. Execute ALL 3 PHASES (Research → Writer → AI Enhancement)  ║"
echo "║    2. Use REAL Ahrefs data (MCP or Python fallback)              ║"
echo "║    3. Create ALL 6 output files (JSON + MD + DOCX)               ║"
echo "║    4. NEVER skip keyword research or use estimated data          ║"
echo "║                                                                  ║"
echo "║  If Ahrefs MCP fails with 403:                                   ║"
echo "║    python3 .claude/scripts/ahrefs-api.py [endpoint] [params]     ║"
echo "║                                                                  ║"
echo "║  Quick start: Read CLAUDE.md and ORCHESTRATOR.md first           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
