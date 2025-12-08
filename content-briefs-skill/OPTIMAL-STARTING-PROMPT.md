# Optimal Starting Prompt for Content Brief Generation

**Purpose:** Use this prompt when starting a new session to generate content briefs. This avoids the issues encountered on December 5-8, 2025.

---

## The Problem

In previous sessions, Claude:
1. Did NOT auto-execute `/generate-brief [URL]` command
2. Asked for clarification instead of starting immediately
3. Used only 7 brands when 10 were needed
4. Missed "Mobile Experience" section per brand
5. Missed "Payment methods comparison" section
6. Phase 3 exceeded token limits (needed multi-agent split)

---

## Optimal Starting Prompt

Copy and paste this EXACTLY when starting a new brief generation session:

```
/generate-brief [YOUR_URL_HERE]

CRITICAL EXECUTION INSTRUCTIONS:
1. Execute IMMEDIATELY - do NOT ask for clarification
2. Read ORCHESTRATOR.md and references/competitor-content-analysis.md FIRST
3. Phase 1: Analyze #1 ranking page - match or exceed their brand count (8-10 for high-volume keywords)
4. Phase 2: Include Mobile Experience section per brand + Payment methods comparison
5. Phase 3: Split into 7 parallel sub-agents (3A-3G) to avoid token limits
6. Validate each phase before proceeding
7. Commit and push when complete
```

---

## Example

```
/generate-brief https://www.topendsports.com/sport/betting/best-apps.htm

CRITICAL EXECUTION INSTRUCTIONS:
1. Execute IMMEDIATELY - do NOT ask for clarification
2. Read ORCHESTRATOR.md and references/competitor-content-analysis.md FIRST
3. Phase 1: Analyze #1 ranking page - match or exceed their brand count (8-10 for high-volume keywords)
4. Phase 2: Include Mobile Experience section per brand + Payment methods comparison
5. Phase 3: Split into 7 parallel sub-agents (3A-3G) to avoid token limits
6. Validate each phase before proceeding
7. Commit and push when complete
```

---

## What This Prompt Ensures

| Issue | Solution in Prompt |
|-------|-------------------|
| Claude asks for clarification | "Execute IMMEDIATELY - do NOT ask" |
| Too few brands (7 instead of 10) | "match or exceed their brand count (8-10)" |
| Missing Mobile Experience | "Include Mobile Experience section per brand" |
| Missing Payment methods | "Include Payment methods comparison" |
| Phase 3 token overflow | "Split into 7 parallel sub-agents" |
| Missing validation | "Validate each phase before proceeding" |
| Forgetting to push | "Commit and push when complete" |

---

## Alternative: Update CLAUDE.md

If you want these instructions to be automatic for ALL sessions, add this to the CLAUDE.md file:

```markdown
## AUTO-EXECUTION RULES

When user provides `/generate-brief [URL]`:
1. Execute IMMEDIATELY without asking for clarification
2. Follow ORCHESTRATOR.md multi-agent workflow
3. Phase 1: Analyze #1 ranking page, use 8-10 brands for high-volume keywords
4. Phase 2: Include Mobile Experience + Payment methods sections
5. Phase 3: Use 7 parallel sub-agents (token limit workaround)
6. Validate, commit, and push automatically
```

---

## Checklist for Brief Generation

Before starting, ensure the system will:

- [ ] NOT ask for clarification on /generate-brief
- [ ] Analyze #1 ranking page content structure
- [ ] Use 8-10 brands (not 5-7) for 10K+/mo keywords
- [ ] Include Mobile Experience section per brand
- [ ] Include Payment methods comparison section
- [ ] Include Calculator tool links
- [ ] Split Phase 3 into 7 sub-agents
- [ ] Use H2 headings in Phase 3 sub-agents (not H1)
- [ ] Validate each phase with scripts/validate-phase.sh
- [ ] Fix markdown lint errors before committing
- [ ] Commit and push all changes

---

## Quick Reference: Brand Count by Volume

| Primary Keyword Volume | Minimum Brands | Target Brands |
|------------------------|----------------|---------------|
| 10,000+/mo | 8 | 10 |
| 5,000-10,000/mo | 7 | 8 |
| 1,000-5,000/mo | 5 | 7 |
| <1,000/mo | 5 | 5 |

---

## Quick Reference: Expanded Brand List

For 10-brand briefs, use:

| Position | Brand | Badge |
|----------|-------|-------|
| #1 | FanDuel | FD |
| #2 | BetMGM | MGM |
| #3 | Bet365 | 365 |
| #4 | DraftKings | DK |
| #5 | theScore BET | SCR |
| #6 | Caesars | CZR |
| #7 | Fanatics | FAN |
| #8 | BetRivers | BRV |
| #9 | Hard Rock Bet | HRB |
| #10 | Borgata | BOR |

---

## Quick Reference: Per-Brand Sections

Each brand MUST have:

1. **Key Features** (150-200 words)
2. **Mobile Experience** (100-150 words) ← Don't forget!
3. **Pros & Cons** (100-150 words)
4. **Current Bonus** (75-100 words)

Total per brand: ~500-600 words
10 brands × 550 words = 5,500 words (just from brand sections)
