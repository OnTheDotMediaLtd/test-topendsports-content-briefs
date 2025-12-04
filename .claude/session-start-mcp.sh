#!/bin/bash
# SessionStart hook to initialize MCP servers for Claude Code Remote
# This addresses the known bug (Issue #3426) where MCP tools are not exposed to new AI sessions

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MCP_JSON="$PROJECT_DIR/.mcp.json"

echo "=== MCP Session Initialization ==="
echo "Project: $PROJECT_DIR"

# Verify .mcp.json exists
if [ -f "$MCP_JSON" ]; then
    echo "✓ MCP configuration found"

    # Ensure TopEndSports MCP server dependencies are installed
    MCP_SERVER_DIR="$PROJECT_DIR/mcp-server"
    if [ -d "$MCP_SERVER_DIR" ]; then
        if [ ! -d "$MCP_SERVER_DIR/node_modules" ]; then
            echo "Installing TopEndSports MCP server dependencies..."
            cd "$MCP_SERVER_DIR" && npm install --silent 2>/dev/null
        fi
        echo "✓ TopEndSports MCP server ready"
    fi

    # Verify Ahrefs MCP is available
    if command -v npx &> /dev/null; then
        if [ ! -d "/root/.global-node-modules/node_modules/@ahrefs" ]; then
            echo "Installing Ahrefs MCP package..."
            npm install --prefix=/root/.global-node-modules @ahrefs/mcp -g --silent 2>/dev/null
        fi
        echo "✓ Ahrefs MCP package ready"
    fi

    echo "=== MCP Initialization Complete ==="
else
    echo "⚠ Warning: No .mcp.json found at $MCP_JSON"
fi
