#!/bin/bash
# MCP Helper Functions - Source this file to get easy-to-use functions
# Usage: source .claude/scripts/mcp-functions.sh
#
# Then use:
#   mcp_brand_rules
#   mcp_search "NFL betting"
#   mcp_keywords "nfl betting sites"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# TopEndSports MCP Functions
mcp_brand_rules() {
    "$SCRIPT_DIR/mcp-topendsports.sh" get_brand_rules
}

mcp_search() {
    local query="$1"
    local lang="${2:-english}"
    "$SCRIPT_DIR/mcp-topendsports.sh" lookup_site_structure "{\"query\":\"$query\",\"language\":\"$lang\"}"
}

mcp_page_info() {
    local url="$1"
    "$SCRIPT_DIR/mcp-topendsports.sh" get_page_info "{\"url\":\"$url\"}"
}

mcp_active_briefs() {
    "$SCRIPT_DIR/mcp-topendsports.sh" list_active_briefs
}

mcp_completed_briefs() {
    "$SCRIPT_DIR/mcp-topendsports.sh" list_completed_briefs
}

mcp_template() {
    local num="${1:-}"
    if [ -n "$num" ]; then
        "$SCRIPT_DIR/mcp-topendsports.sh" get_template_info "{\"template_number\":$num}"
    else
        "$SCRIPT_DIR/mcp-topendsports.sh" get_template_info
    fi
}

# Ahrefs MCP Functions
mcp_keywords() {
    local keywords="$1"
    local country="${2:-us}"
    "$SCRIPT_DIR/mcp-ahrefs.sh" keywords-explorer-overview "{\"select\":\"keyword,volume,difficulty,cpc,traffic_potential\",\"country\":\"$country\",\"keywords\":\"$keywords\"}"
}

mcp_keyword_ideas() {
    local terms="$1"
    local country="${2:-us}"
    "$SCRIPT_DIR/mcp-ahrefs.sh" keywords-explorer-matching-terms "{\"select\":\"keyword,volume,difficulty\",\"country\":\"$country\",\"terms\":\"$terms\",\"limit\":20}"
}

mcp_domain_rating() {
    local domain="$1"
    local date="${2:-$(date +%Y-%m-%d)}"
    "$SCRIPT_DIR/mcp-ahrefs.sh" site-explorer-domain-rating "{\"target\":\"$domain\",\"date\":\"$date\"}"
}

mcp_serp() {
    local keyword="$1"
    local country="${2:-us}"
    "$SCRIPT_DIR/mcp-ahrefs.sh" serp-overview-serp-overview "{\"select\":\"position,url,title,traffic\",\"country\":\"$country\",\"keyword\":\"$keyword\"}"
}

mcp_organic_keywords() {
    local domain="$1"
    local country="${2:-us}"
    local date="${3:-$(date +%Y-%m-%d)}"
    "$SCRIPT_DIR/mcp-ahrefs.sh" site-explorer-organic-keywords "{\"select\":\"keyword,position,volume,traffic\",\"target\":\"$domain\",\"country\":\"$country\",\"date\":\"$date\",\"limit\":50}"
}

echo "MCP Helper Functions loaded!"
echo ""
echo "TopEndSports functions:"
echo "  mcp_brand_rules              - Get brand positioning rules"
echo "  mcp_search \"query\"           - Search site structure"
echo "  mcp_page_info \"url\"          - Get page info by URL"
echo "  mcp_active_briefs            - List active briefs"
echo "  mcp_completed_briefs         - List completed briefs"
echo "  mcp_template [1-4]           - Get template info"
echo ""
echo "Ahrefs functions:"
echo "  mcp_keywords \"keywords\"      - Get keyword overview"
echo "  mcp_keyword_ideas \"terms\"    - Get keyword ideas"
echo "  mcp_domain_rating \"domain\"   - Get domain rating"
echo "  mcp_serp \"keyword\"           - Get SERP overview"
echo "  mcp_organic_keywords \"domain\" - Get organic keywords"
