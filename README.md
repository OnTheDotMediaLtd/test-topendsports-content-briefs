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

## Usage

1. Open the project folder in Claude Code
2. Use the appropriate agents/skills for your content brief generation needs
3. Follow the phase-based workflow for consistent results

## Team Collaboration

This repository is set up for team collaboration. All team members can:
- Clone the repository to their local machine
- Access the same configurations and workflows
- Contribute improvements via pull requests
