# TopEndSports Content Briefs MCP Server

MCP (Model Context Protocol) server for the TopEndSports content briefs generation system. This server provides tools for managing content briefs, looking up site structure data, and integrating with the brief generation workflow.

## Installation

```bash
cd mcp-server
npm install
npm run build
```

## Configuration

Add to your Claude Code MCP settings (`~/.claude/settings.json` or project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "topendsports-briefs": {
      "command": "node",
      "args": ["/path/to/topendsports-content-briefs/mcp-server/dist/index.js"]
    }
  }
}
```

Or for development:

```json
{
  "mcpServers": {
    "topendsports-briefs": {
      "command": "npx",
      "args": ["ts-node", "--esm", "/path/to/topendsports-content-briefs/mcp-server/src/index.ts"]
    }
  }
}
```

## Available Tools

### lookup_site_structure

Search the site structure CSV to find page information, target keywords, writer assignments, and priorities.

**Parameters:**
- `query` (required): Search query - can be page name, keyword, or partial URL
- `language` (optional): "english" or "spanish" (default: "english")

**Example:**
```
lookup_site_structure(query="NFL betting")
```

### get_page_info

Get complete page information by exact URL.

**Parameters:**
- `url` (required): The full URL of the page

**Example:**
```
get_page_info(url="https://www.topendsports.com/sport/betting/nfl/index.htm")
```

### get_brand_rules

Get brand positioning rules, locked positions, tier information, and compliance requirements.

**Parameters:**
- `section` (optional): "all", "locked_positions", "tiers", "guidelines", "compliance", or "writers"

**Example:**
```
get_brand_rules(section="locked_positions")
```

### list_active_briefs

List all work-in-progress brief JSON files in the active directory.

**Example:**
```
list_active_briefs()
```

### list_completed_briefs

List all completed briefs (markdown and docx) in the output directory.

**Example:**
```
list_completed_briefs()
```

### read_phase_data

Read the JSON data for a specific phase of a brief.

**Parameters:**
- `page_name` (required): The page name slug (e.g., "nfl-betting-sites")
- `phase` (required): Phase number (1 or 2)

**Example:**
```
read_phase_data(page_name="nfl-betting-sites", phase=1)
```

### convert_to_docx

Convert markdown brief files to Word documents (.docx).

**Parameters:**
- `files` (required): List of markdown file paths to convert. Use ["--all"] to convert all markdown files in output folder.

**Example:**
```
convert_to_docx(files=["--all"])
```

### submit_feedback

Submit feedback for a content brief to the continuous improvement system.

**Parameters:**
- `page_name` (required): Name of the page the feedback is about
- `rating` (required): Rating from 1-5
- `submitter` (required): Name of person submitting feedback
- `issues` (optional): List of issues found
- `improvements` (optional): Suggested improvements

**Example:**
```
submit_feedback(
  page_name="Best NFL Betting Sites",
  rating=4,
  submitter="Lewis Humphries",
  issues=["Missing DraftKings promo details"],
  improvements=["Add comparison table for mobile apps"]
)
```

### get_template_info

Get information about content templates.

**Parameters:**
- `template_number` (optional): 1=Review, 2=Comparison, 3=How-To, 4=State Page

**Example:**
```
get_template_info(template_number=2)
```

## Available Resources

The server also exposes the following resources:

- `briefs://site-structure/english` - Complete English site structure data
- `briefs://site-structure/spanish` - Complete Spanish site structure data
- `briefs://brand-rules` - Complete brand positioning and compliance rules

## Brand Rules Summary

### Locked Positions
- **Position 1**: FanDuel (LOCKED - Active commercial deal)
- **Position 2**: BetMGM (LOCKED - Active commercial deal)

### Brand Tiers
- **Tier 1**: FanDuel, BetMGM, DraftKings, Caesars, bet365
- **Tier 2**: Fanatics, ESPN BET, BetRivers, Bally Bet, BetParx
- **Tier 3**: Golden Nugget, Unibet, Borgata, Betfred, WynnBet, SI Sportsbook

### Compliance Rules
- Default age requirement: 21+
- Gambling hotline: 1-800-522-4700
- Affiliate disclosure required at top of page
- Responsible gambling section required at bottom

## Development

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Run in development mode
npm run dev
```

## File Structure

```
mcp-server/
├── src/
│   └── index.ts      # Main MCP server implementation
├── dist/             # Compiled JavaScript (after build)
├── package.json
├── tsconfig.json
└── README.md
```
