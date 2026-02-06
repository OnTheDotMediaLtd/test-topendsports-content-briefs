# TES BETTING CONTENT BRIEF GENERATOR

## Project Overview

This project generates complete content briefs for Topendsports.com's betting section using a 3-phase workflow. Each phase runs independently with focused context to avoid token overflow.

**What This Produces:**
1. **Brief Control Sheet** (Phase 1) - Research findings, keyword cluster, strategic direction
2. **Writer Brief** (Phase 2) - Clear instructions for human writer with keyword optimization
3. **AI Enhancement Brief** (Phase 3) - Complete technical implementation with HTML/code

## Quick Start

When user provides a URL like `/sport/betting/nfl-betting-sites.htm`:

```
generate brief for /sport/betting/nfl-betting-sites.htm
```

The system will:
1. Look up the URL in site structure CSVs
2. Execute Phase 1 → output Brief Control Sheet
3. Execute Phase 2 → output Writer Brief
4. Execute Phase 3 → output AI Enhancement Brief
5. Save all outputs to `output/` folder
6. **Convert all markdown files to Word (.docx) format for writers**

## Project Structure

```
tes-content-briefs/
├── CLAUDE.md                 ← You are here (master instructions)
├── agents/
│   ├── research-agent.md     ← Phase 1 instructions
│   ├── writer-agent.md       ← Phase 2 instructions
│   └── technical-agent.md    ← Phase 3 instructions
├── data/
│   ├── site-structure-english.csv
│   └── site-structure-spanish.csv
├── templates/
│   ├── content-templates.md
│   ├── verification-standards.md
│   └── reference-library.md
├── scripts/
│   └── convert_to_docx.py    ← Markdown to Word converter
├── output/                   ← Final briefs go here (.md + .docx)
└── active/                   ← Work-in-progress files
```

## Workflow Rules

### Phase Execution Order
Always work sequentially: Phase 1 → Phase 2 → Phase 3

### Context Management
- Each phase reads ONLY its agent instructions + relevant data
- Pass data between phases via JSON files in `active/`
- This prevents token overflow

### Phase 1: Research Agent
**Read:** `agents/research-agent.md`
**Input:** URL from user
**Output:** `active/[page-name]-phase1.json` + `output/[page-name]-brief-control-sheet.md`

### Phase 2: Writer Agent
**Read:** `agents/writer-agent.md`
**Input:** `active/[page-name]-phase1.json`
**Output:** `active/[page-name]-phase2.json` + `output/[page-name]-writer-brief.md`

### Phase 3: Technical Agent
**Read:** `agents/technical-agent.md`
**Input:** `active/[page-name]-phase1.json` + `active/[page-name]-phase2.json`
**Output:** `output/[page-name]-ai-enhancement.md`

### Final Step: Convert to Word
**After all 3 phases complete**, automatically run:
```bash
python scripts/convert_to_docx.py --all
```
This converts all `.md` files in `output/` to `.docx` format for content writers.

## Critical Rules

### Mandatory Discovery (Phase 1)
1. Search site structure CSV FIRST
2. Use ACTUAL keyword from structure (not from URL)
3. Identify affiliate competitors (not brand landing pages)
4. Complete secondary keyword research (8-15 keywords)
5. Map keywords to sections (H2/H3/FAQ)

### Writer Assignment
- Spanish `/es/` URLs = ALWAYS Gustavo Cantella
- Check site structure first for assigned writer
- High-priority = Lewis Humphries
- Supporting = Tom Goldsmith

### Brand Positioning (Locked)
- Position #1: FanDuel (always)
- Position #2: BetMGM (always)
- Positions #3-7: Research-driven

### Spanish Content Rules
- Target: USA Spanish speakers (NOT Spain)
- Sportsbooks: FanDuel, DraftKings, BetMGM (USA operators)
- Age: 21+ (NOT 18+)
- Hotline: 1-800-522-4700 (USA)
- Language: "ustedes" (NOT "vosotros")

### Compliance (Always Include)
- Age requirement (21+ most states)
- Affiliate disclosure
- Problem gambling: 1-800-522-4700
- State availability disclaimer
- Responsible gambling section

## Template Types

| Template | Use For | Word Count | T&Cs Required |
|----------|---------|------------|---------------|
| Template 1 | Sportsbook Review | 3,500-4,000 | Complete (1 brand) |
| Template 2 | Comparison Page | 2,500-3,500 | Complete (ALL brands) |
| Template 3 | How-To Guide | 1,500-2,500 | Brief only |
| Template 4 | State Page | 2,000-2,800 | Complete (state ops) |

## Secondary Keyword Optimization

Every brief MUST include:
- 8-15 secondary keywords identified
- Each keyword mapped to section (H2/H3/FAQ)
- Total search volume calculated
- High-volume (200+/mo) → H2 titles
- Medium-volume (100-200/mo) → H3 titles
- Question keywords → FAQs

**Expected Result:** 400-900% increase in target search volume

## Dating Language Rules

**NEVER use in titles/H1:**
- "October 2025", "Review 2025", "Best Sites 2025"

**USE instead:**
- "Comprehensive Review", "The #1 Rated App"
- Add "Last Updated" badge after H1

## Source Requirements

**TIER 1 (Primary):** Real users
- App Store, Google Play, Reddit, Trustpilot

**TIER 2 (Verification):** Official sources
- Brand websites, gaming commissions

**TIER 3 (Facts):** Industry sources
- Market data, revenue reports

**TIER 4 (Sparingly):** Affiliate sites
- NEVER cite for pros/cons

## Commands

### Generate Full Brief
```
generate brief for [URL]
```

### Generate Single Phase
```
run phase 1 for [URL]
run phase 2 for [page-name]
run phase 3 for [page-name]
```

### Check Status
```
show active briefs
show completed briefs
```

## Error Handling

**If URL not in site structure:**
→ Proceed with manual assignment
→ Document reasoning in brief

**If Ahrefs unavailable:**
→ Use web search for keyword estimates
→ Note "estimated" in output

**If token limit approaching:**
→ Save current state to `active/`
→ Resume from saved state
