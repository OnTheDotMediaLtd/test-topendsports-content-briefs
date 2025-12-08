# Brief Generation Prompt Template

**Purpose:** Copy this prompt when starting a new Claude Code chat to generate a content brief.

---

## How to Use

1. Start a new Claude Code session in this repo
2. Copy the prompt below
3. Replace `[URL]` with your target URL
4. Paste and send

---

## The Prompt

```
Generate a complete content brief for: [URL]

CRITICAL EXECUTION INSTRUCTIONS:

1. Execute IMMEDIATELY - do NOT ask for clarification
2. Read ORCHESTRATOR.md and references/competitor-content-analysis.md FIRST
3. Phase 1: Analyze #1 ranking page - match or exceed their brand count (8-10 for high-volume keywords)
4. Phase 2: Include Mobile Experience section per brand + Payment methods comparison + Calculator tool links
5. Phase 3: Split into 7 parallel sub-agents (3A-3G) to avoid token limits
6. Validate each phase before proceeding
7. Commit and push when complete

Expected deliverables:
- output/[page]-brief-control-sheet.md
- output/[page]-writer-brief.md
- output/[page]-ai-enhancement.md
- All converted to .docx
```

---

## Example Usage

```
Generate a complete content brief for: /sport/betting/nba-betting-sites.htm

CRITICAL EXECUTION INSTRUCTIONS:

1. Execute IMMEDIATELY - do NOT ask for clarification
2. Read ORCHESTRATOR.md and references/competitor-content-analysis.md FIRST
3. Phase 1: Analyze #1 ranking page - match or exceed their brand count (8-10 for high-volume keywords)
4. Phase 2: Include Mobile Experience section per brand + Payment methods comparison + Calculator tool links
5. Phase 3: Split into 7 parallel sub-agents (3A-3G) to avoid token limits
6. Validate each phase before proceeding
7. Commit and push when complete

Expected deliverables:
- output/nba-betting-sites-brief-control-sheet.md
- output/nba-betting-sites-writer-brief.md
- output/nba-betting-sites-ai-enhancement.md
- All converted to .docx
```

---

## Alternative: Use Slash Command

If already in a session, you can also use:

```
/generate-brief /sport/betting/[page].htm
```

The slash command contains all the same instructions embedded.

---

## What Claude Will Do

1. **Phase 0:** Extract page name, look up in site structure, test Ahrefs
2. **Phase 1:** Research keywords (8-15), analyze competitors, select brands (8-10)
3. **Phase 2:** Create writer brief with keyword-optimized outline, 7+ FAQs
4. **Phase 3:** Generate complete HTML/CSS/JS code via 7 parallel sub-agents
5. **Convert:** All markdown to DOCX
6. **Commit & Push:** To the feature branch

Total time: ~15-25 minutes

---

## Troubleshooting

### Ahrefs MCP Returns 403
Claude will automatically fall back to Python:
```bash
python3 .claude/scripts/ahrefs-api.py [endpoint] [params]
```

### Phase 3 Token Limit
The 7 sub-agent split (3A-3G) prevents this. If it still happens, Claude will retry with smaller chunks.

### Validation Fails
Claude will fix issues and re-validate before proceeding.

---

## Required Branch Naming

When using Claude Code with GitHub integration, ensure branch follows pattern:
```
claude/[task-description]-[session-id]
```

---

**Last Updated:** December 8, 2025
