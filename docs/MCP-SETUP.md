# MCP Server Setup Guide

This guide explains how to use the MCP (Model Context Protocol) tools in this project.

---

## Quick Status Check

When starting a new Claude Code session, the MCP tools should be automatically available. To verify:

1. **TopEndSports MCP** - Try: "lookup NFL betting in site structure"
2. **Ahrefs MCP** - Try: "get ahrefs doc for keywords-explorer-overview"

---

## What's Configured

### TopEndSports MCP Server (Local)

Provides tools for content brief generation:

| Tool | Description |
|------|-------------|
| `lookup_site_structure` | Search site structure CSV |
| `get_page_info` | Get page details by URL |
| `get_brand_rules` | Get brand positioning rules |
| `list_active_briefs` | Show work-in-progress briefs |
| `list_completed_briefs` | Show completed briefs |
| `read_phase_data` | Read phase JSON data |
| `convert_to_docx` | Convert markdown to Word |
| `submit_feedback` | Submit brief feedback |
| `get_template_info` | Get template information |

### Ahrefs MCP Server (External API)

Provides SEO research tools:

| Tool | Description |
|------|-------------|
| `keywords-explorer-overview` | Keyword metrics |
| `site-explorer-domain-rating` | Domain authority |
| `site-explorer-organic-keywords` | Organic keywords |
| `serp-overview-serp-overview` | SERP analysis |
| And 35+ more tools | See `doc` tool for full list |

---

## For New Team Members

### Step 1: Clone the Repository

```bash
git clone https://github.com/OnTheDotMediaLtd/topendsports-content-briefs.git
cd topendsports-content-briefs
```

### Step 2: Open in Claude Code

The MCP configuration is automatically loaded from:
- `.mcp.json` - Server definitions
- `.claude/settings.json` - Permissions and hooks

### Step 3: Verify MCP Tools

In Claude Code, try these commands:
```
# Test TopEndSports MCP
lookup site structure for "NFL betting"

# Test Ahrefs MCP (documentation)
get ahrefs doc for keywords-explorer-overview
```

---

## Configuration Files

### `.mcp.json` (Project Root)

Defines the MCP servers:

```json
{
  "mcpServers": {
    "topendsports-briefs": {
      "command": "node",
      "args": ["mcp-server/dist/index.js"]
    },
    "ahrefs": {
      "command": "npx",
      "args": ["@ahrefs/mcp"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### `.claude/settings.json`

Enables MCP servers and sets permissions:

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["topendsports-briefs", "ahrefs"],
  "permissions": {
    "allow": [
      "mcp__topendsports-briefs__*",
      "mcp__ahrefs__*"
    ]
  }
}
```

### `.claude/hooks/session-start.sh`

Automatically installs dependencies when running in Claude Code Remote (web):
- Installs MCP server npm dependencies
- Installs Ahrefs MCP package
- Installs Python docx converter

---

## Troubleshooting

### MCP Tools Not Available

1. **Restart Claude Code** - MCP changes require restart
2. **Check dependencies installed**:
   ```bash
   cd mcp-server && npm install
   ```
3. **Verify configuration**:
   ```bash
   cat .mcp.json
   cat .claude/settings.json
   ```

### Ahrefs API Returns 403

The Ahrefs API requires a valid API key with appropriate permissions:

1. Log into your Ahrefs account
2. Go to API settings
3. Generate a new API key (not MCP key)
4. Update `.mcp.json` with the new key

**Note:** The API key must have access to the specific endpoints you're using. Different Ahrefs plans have different API access levels.

### TopEndSports MCP Not Working

1. Rebuild the MCP server:
   ```bash
   cd mcp-server
   npm install
   npm run build
   ```
2. Check the server exists:
   ```bash
   ls mcp-server/dist/index.js
   ```

---

## Using Wrapper Scripts (Fallback)

If MCP tools aren't available, use the wrapper scripts directly:

```bash
# TopEndSports
.claude/scripts/mcp-topendsports.sh get_brand_rules '{"section":"tiers"}'

# Ahrefs
.claude/scripts/mcp-ahrefs.sh doc '{"tool":"keywords-explorer-overview"}'
```

See `.claude/scripts/mcp-functions.sh` for helper functions.

---

## Desktop vs Web (Claude Code Remote)

| Feature | Desktop | Web (Remote) |
|---------|---------|--------------|
| MCP Config Location | Local files | Copied to container |
| SessionStart Hook | Skipped | Runs automatically |
| Dependencies | Pre-installed | Installed on session start |
| Performance | Faster | Initial delay for install |

The SessionStart hook only runs in web environments (detected via `CLAUDE_CODE_REMOTE=true`).

---

## Support

- **GitHub Issues**: Report problems at the repository
- **Documentation**: See `QUICKSTART.md` for general usage
- **MCP Server README**: See `mcp-server/README.md` for tool details

---

*Last updated: December 2025*
