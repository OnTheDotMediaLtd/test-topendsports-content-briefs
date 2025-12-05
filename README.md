# TopEndSports Content Briefs Generation System

This project contains the content brief generation system for topendsports.com, built with Claude Code.

## Project Structure

### content-briefs-v1/
The original content briefs system containing:
- Agent definitions (research, technical, writer)
- Data files (site structure CSV)
- Templates and reference library
- Scripts for document conversion
- Output documents

### content-briefs-skill/
Claude Code Skill version of the content briefs system with:
- Organized references and templates
- Quality checklists and verification standards
- Orchestrator configuration
- Phase-based workflow documentation

### mcp-server/
MCP (Model Context Protocol) server providing programmatic access to:
- Site structure lookup and search
- Brand positioning rules and compliance requirements
- Brief management (active/completed briefs)
- Document conversion (markdown to docx)
- Feedback submission system
- Template information

See [mcp-server/README.md](mcp-server/README.md) for installation and usage.

## Requirements

- Claude Code CLI
- Python 3.x (for document conversion scripts)
- Ahrefs API access (for SEO data)

## Environment Setup

### Claude Code on Web (Recommended)
The `.mcp.json` is pre-configured for the web environment. The `session-start.sh` hook automatically installs dependencies including the Ahrefs MCP package.

### Local Desktop Setup
The default `.mcp.json` uses a web-environment-specific path for the Ahrefs MCP server (`/root/.global-node-modules/...`). For local desktop usage:

1. Copy `.claude/settings.local.json.example` to `.claude/settings.local.json`
2. Either:
   - Install `@ahrefs/mcp` globally and update the path in `.mcp.json`, OR
   - Use `npx @ahrefs/mcp` by modifying the ahrefs config to:
     ```json
     "ahrefs": {
       "command": "npx",
       "args": ["@ahrefs/mcp"],
       "env": { "API_KEY": "your-api-key" }
     }
     ```

**Note:** The web environment uses direct node execution for 3x faster MCP startup compared to npx.

## Usage

1. Open the project folder in Claude Code
2. Use the appropriate agents/skills for your content brief generation needs
3. Follow the phase-based workflow for consistent results

## Quick Access

### For Writers & Team Members
- **[Download Completed Briefs](content-briefs-skill/output/)** - All finished briefs (.docx and .md)
- **[Team Guide](docs/TEAM-GUIDE.md)** - How to use GitHub and find briefs (for beginners)
- **[Quick Start Guide](QUICKSTART.md)** - How to generate new briefs

### For Project Managers
- **[GitHub Projects Setup](docs/GITHUB-PROJECTS-SETUP.md)** - Set up project tracking board
- **[Feedback System](content-briefs-skill/feedback/)** - Review submitted feedback

## Team Collaboration

This repository is set up for team collaboration. All team members can:
- Clone the repository to their local machine
- Access the same configurations and workflows
- Contribute improvements via pull requests

### New to GitHub?
Read the **[Team Guide](docs/TEAM-GUIDE.md)** for simple explanations of:
- How to download briefs
- What "pull", "push", and "branch" mean
- How to submit feedback
