#!/bin/bash
# MCP Tool Wrapper - Calls TopEndSports MCP server directly
# Usage: mcp-topendsports.sh <tool_name> [json_args]
#
# Examples:
#   ./mcp-topendsports.sh get_brand_rules
#   ./mcp-topendsports.sh lookup_site_structure '{"query":"NFL betting"}'
#   ./mcp-topendsports.sh get_template_info '{"template_number":2}'

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
MCP_SERVER="$PROJECT_DIR/mcp-server/dist/index.js"

TOOL_NAME="${1:-}"
ARGS="${2:-"{}"}"

if [ -z "$TOOL_NAME" ]; then
    echo "Usage: $0 <tool_name> [json_args]"
    echo ""
    echo "Available tools:"
    echo "  get_brand_rules        - Get brand positioning rules"
    echo "  lookup_site_structure  - Search site structure (args: {\"query\":\"...\"})"
    echo "  get_page_info          - Get page by URL (args: {\"url\":\"...\"})"
    echo "  list_active_briefs     - List work-in-progress briefs"
    echo "  list_completed_briefs  - List completed briefs"
    echo "  read_phase_data        - Read phase data (args: {\"page_name\":\"...\",\"phase\":1})"
    echo "  get_template_info      - Get template info (args: {\"template_number\":1-4})"
    echo "  submit_feedback        - Submit feedback"
    exit 1
fi

# Build JSON-RPC request
REQUEST="{\"jsonrpc\": \"2.0\", \"method\": \"tools/call\", \"params\": {\"name\": \"$TOOL_NAME\", \"arguments\": $ARGS}, \"id\": 1}"
# Debug: uncomment to see the request
# echo "REQUEST: $REQUEST" >&2

# Call MCP server and parse response
echo "$REQUEST" | timeout 10 node "$MCP_SERVER" 2>/dev/null | grep -E '^\{"' | tail -1 | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'result' in data and 'content' in data['result']:
    for item in data['result']['content']:
        if item.get('type') == 'text':
            print(item['text'])
"
