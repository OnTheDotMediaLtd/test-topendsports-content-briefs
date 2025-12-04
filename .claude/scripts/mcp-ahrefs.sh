#!/bin/bash
# MCP Tool Wrapper - Calls Ahrefs MCP server directly
# Usage: mcp-ahrefs.sh <tool_name> [json_args]
#
# Examples:
#   ./mcp-ahrefs.sh doc
#   ./mcp-ahrefs.sh keywords-explorer-overview '{"select":"keyword,volume,difficulty","country":"us","keywords":"nfl betting sites"}'

set -euo pipefail

TOOL_NAME="${1:-}"
ARGS="${2:-"{}"}"

# Ahrefs API key
API_KEY="${AHREFS_API_KEY:-DuQE.MbAOsd7LEWgStWIpQOSh6To0ZjkvcDVpRlZ0ZlBvM3RHajQ3a1IrUGxMRUdhcWtHdFd2T1NCYXJNTFlBUVMxRmx3MXExYkhvL2hqNDdvLzdGYXI0cDhnRE5YRFlPVEZhYXIwYkg3TExST3YycmYwR0tDUTRCbkt2clUxSnBPTkJ0OUNjeURNWUs0RlU.opcl}"

if [ -z "$TOOL_NAME" ]; then
    echo "Usage: $0 <tool_name> [json_args]"
    echo ""
    echo "Common tools:"
    echo "  doc                              - Get documentation for any tool"
    echo "  keywords-explorer-overview       - Keyword metrics (needs: select, country, keywords)"
    echo "  keywords-explorer-matching-terms - Keyword ideas"
    echo "  site-explorer-organic-keywords   - Site organic keywords"
    echo "  site-explorer-domain-rating      - Domain rating"
    echo "  serp-overview-serp-overview      - SERP overview"
    echo ""
    echo "Run with 'doc' to see full documentation"
    exit 1
fi

# Build JSON-RPC request
REQUEST="{\"jsonrpc\": \"2.0\", \"method\": \"tools/call\", \"params\": {\"name\": \"$TOOL_NAME\", \"arguments\": $ARGS}, \"id\": 1}"

# Export API key and call Ahrefs MCP server
export API_KEY

# Call MCP server and parse response
echo "$REQUEST" | timeout 60 npx --prefix=/root/.global-node-modules @ahrefs/mcp 2>/dev/null | grep -E '^\{"' | tail -1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'error' in data:
        print('Error:', data['error'].get('message', 'Unknown error'))
    elif 'result' in data and 'content' in data['result']:
        for item in data['result']['content']:
            if item.get('type') == 'text':
                print(item['text'])
except json.JSONDecodeError:
    print('Error: No response from MCP server')
"
