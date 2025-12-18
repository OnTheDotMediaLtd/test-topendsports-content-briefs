#!/bin/bash
# Claude Code Project Setup Script
# MERGES settings instead of overwriting - safe for multi-project setups

set -e

echo "=================================================="
echo "Claude Code Project Setup"
echo "=================================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$HOME/.claude"

echo "[1/4] Creating Claude config directory..."
mkdir -p "$CLAUDE_DIR"

echo "[2/4] Merging Claude settings..."

# Python script to merge settings (more reliable than jq)
python3 << 'PYTHON_SCRIPT'
import json
import os
from pathlib import Path

claude_dir = Path.home() / ".claude"
settings_file = claude_dir / "settings.json"

# Required settings for all Claude Code projects
required_settings = {
    "enableAllProjectMcpServers": True,
    "permissions": {
        "allow": ["Skill"]
    }
}

# Load existing settings or start fresh
if settings_file.exists():
    with open(settings_file) as f:
        settings = json.load(f)
    print("      Merging with existing settings...")
else:
    settings = {"$schema": "https://json.schemastore.org/claude-code-settings.json"}
    print("      Creating new settings...")

# Merge enableAllProjectMcpServers
settings["enableAllProjectMcpServers"] = True

# Merge permissions (add to existing, don't overwrite)
if "permissions" not in settings:
    settings["permissions"] = {}
if "allow" not in settings["permissions"]:
    settings["permissions"]["allow"] = []
if "Skill" not in settings["permissions"]["allow"]:
    settings["permissions"]["allow"].append("Skill")

# Save merged settings
with open(settings_file, "w") as f:
    json.dump(settings, f, indent=4)

print("      Settings merged successfully")
PYTHON_SCRIPT

echo "[3/4] Installing Python dependencies..."
pip install python-docx markdown lxml --quiet 2>/dev/null || {
    echo "      Warning: pip install failed. Run manually:"
    echo "      pip install python-docx markdown lxml"
}
echo "      Python packages ready"

echo "[4/4] Verifying setup..."
echo ""

ERRORS=0

if [ -f "$CLAUDE_DIR/settings.json" ]; then
    if grep -q "enableAllProjectMcpServers" "$CLAUDE_DIR/settings.json"; then
        echo "  [OK] settings.json configured"
    else
        echo "  [WARN] settings.json missing MCP setting"
    fi
else
    echo "  [FAIL] settings.json not found"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "$PROJECT_DIR/.mcp.json" ]; then
    echo "  [OK] .mcp.json found in project"
else
    echo "  [INFO] No .mcp.json in project (MCP servers optional)"
fi

if python -c "import docx" 2>/dev/null; then
    echo "  [OK] python-docx installed"
else
    echo "  [WARN] python-docx not installed"
fi

echo ""
echo "=================================================="
echo "Setup complete! Restart Claude Code to apply."
echo "=================================================="
echo ""
echo "To switch projects: cd /path/to/project && claude"
echo ""
