# Claude Code Team Setup

This folder contains configuration files for setting up Claude Code on team member machines.

## Quick Setup (Copy & Paste)

**For team members: Copy and paste this entire command block into Claude Code:**

```
I need you to set up Claude Code for the TopEndSports content briefs project. Run these commands:

1. First, make the setup script executable and run it:
bash ~/.claude-setup/setup.sh || bash .claude-setup/setup.sh

2. If that doesn't work, run these commands manually:
mkdir -p ~/.claude && cp .claude-setup/settings.json ~/.claude/settings.json && cp .claude-setup/stop-hook-git-check.sh ~/.claude/stop-hook-git-check.sh && chmod +x ~/.claude/stop-hook-git-check.sh && pip install python-docx markdown lxml

3. After setup, restart Claude Code to load the Ahrefs MCP server.
```

## Manual Setup Instructions

If the automatic setup doesn't work, follow these steps:

### Step 1: Clone the Repository
```bash
git clone https://github.com/OnTheDotMediaLtd/topendsports-content-briefs.git
cd topendsports-content-briefs
```

### Step 2: Run Setup Script
```bash
chmod +x .claude-setup/setup.sh
./.claude-setup/setup.sh
```

### Step 3: Restart Claude Code
Close and reopen Claude Code to load the Ahrefs MCP server.

### Step 4: Verify Setup
In Claude Code, ask:
```
verify my claude code setup is working
```

## What Gets Installed

| File | Location | Purpose |
|------|----------|---------|
| `settings.json` | `~/.claude/settings.json` | Claude Code settings with hooks and MCP enabled |
| `stop-hook-git-check.sh` | `~/.claude/stop-hook-git-check.sh` | Git commit enforcement hook |
| `.mcp.json` | Project root | Ahrefs MCP server configuration |

## Python Dependencies

The setup installs these Python packages:
- `python-docx` - Word document generation
- `markdown` - Markdown processing
- `lxml` - XML processing for docx

## Troubleshooting

### MCP Server Not Loading
- Restart Claude Code after setup
- Verify `.mcp.json` exists in project root
- Check `enableAllProjectMcpServers: true` in settings.json

### Python Packages Missing
```bash
pip install python-docx markdown lxml
```

### Permission Denied on Setup Script
```bash
chmod +x .claude-setup/setup.sh
```

### Settings Not Applied
Check if settings.json was copied correctly:
```bash
cat ~/.claude/settings.json
```

## Configuration Files

### settings.json
Enables:
- Project MCP servers (for Ahrefs)
- Git commit hook (ensures all changes are committed/pushed)
- Skill permissions

### .mcp.json (in project root)
Configures the Ahrefs MCP server for keyword research.

**Note:** The Ahrefs API key is shared across the team via this file.

## After Setup

You can start using the content brief system:
```
generate brief for /sport/betting/nfl/index.htm
```

Or test with a random URL:
```
generate brief for /sport/betting/ufc/index.htm
```
