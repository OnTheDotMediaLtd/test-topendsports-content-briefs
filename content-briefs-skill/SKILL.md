---
name: tes-content-briefs
description: Generate complete SEO content briefs for sports betting affiliate websites. Use this skill when asked to create content briefs, writer briefs, or AI enhancement briefs for betting pages. Triggers include requests like "generate brief for [URL]", "create content brief", "betting content", "writer brief for [page]", or any URL containing /sport/betting/. Supports English (topendsports.com) and Spanish (/es/) content with keyword cluster optimization targeting 400-900% more search volume.
---

# TES Betting Content Brief Generator

Generate complete content briefs for Topendsports.com betting section using a 3-phase workflow.

## Workflow Overview

```
User provides URL → Phase 1 → Phase 2 → Phase 3 → Complete Brief Package
```

**Phase 1: Research & Discovery** (10-15 min)
- Look up URL in site structure CSV
- Research keywords (primary + 8-15 secondary)
- Analyze competitor gaps
- Output: Brief Control Sheet (500-700 words)

**Phase 2: Writer Brief Creation** (5-10 min)
- Create keyword-optimized content outline
- Assign correct writer
- Specify source requirements
- Output: Writer Brief (2-3 pages)

**Phase 3: AI Enhancement** (10-15 min)
- Build HTML components (tables, calculators, T&Cs)
- Add schema markup
- Include compliance sections
- Output: AI Enhancement Brief (5-8 pages with code)

## CRITICAL CONTENT OUTPUT RULES (From Team Feedback - December 2024)

> **These rules are MANDATORY and must be followed at all times:**

- **NEVER shorten, compress, or skip content.** Output ALL content in full.
- **Do NOT include max-width CSS on elements** - site handles maximum content size
- **No placeholders** - deliver complete, working code always
- **Break into multiple artifacts if needed** - but each must be complete
- **ESPN BET is now theScore BET** (rebranded December 1, 2025)
- **Use Gold Standard Templates** (see `references/gold-standard-templates.md`)

## Quick Start

1. Read the URL from user
2. Search site structure: `grep -i "[page-name]" assets/data/site-structure-english.csv`
3. Execute Phase 1 using `references/phase1-research.md` → save to `output/`
4. Execute Phase 2 using `references/phase2-writer.md` → save to `output/`
5. Execute Phase 3 using `references/phase3-technical.md` → save to `output/`
6. Convert to Word: `python scripts/convert_to_docx.py --all`
7. Deliver both `.md` and `.docx` files to user

## Critical Rules

### Mandatory Discovery
- ALWAYS search site structure CSV first
- Use ACTUAL keyword from CSV (not from URL)
- Identify affiliate competitors (actionnetwork.com, covers.com) NOT brand pages

### Writer Assignment
```
/es/ URL? → Gustavo Cantella (always)
Found in CSV? → Use assigned writer
Not found? → Lewis (high priority) or Tom (supporting)
```

### Brand Positioning (Locked)
- Position #1: FanDuel (always)
- Position #2: BetMGM (always)
- Positions #3-7: Research-driven

### Secondary Keywords (Always Required)
- Research 8-15 secondary keywords
- Map to sections: High volume (200+) → H2, Medium (100-200) → H3, Questions → FAQ
- Calculate total cluster volume
- Target: 400-900% increase over primary alone

### Spanish Content (/es/ URLs)
- Target: USA Spanish speakers (NOT Spain)
- Sportsbooks: FanDuel, DraftKings, BetMGM (USA operators)
- Age: 21+ (NOT 18+)
- Language: "ustedes" (NOT "vosotros")

### No Dated Language
- NEVER in titles: "October 2025", "Review 2025"
- USE instead: "Comprehensive Review", "The #1 Rated App"
- Add "Last Updated" badge after H1

## Template Selection

| URL Pattern | Template | Words | T&Cs |
|-------------|----------|-------|------|
| `[brand]-review.htm` | Template 1 (Review) | 3,500-4,000 | Complete (1 brand) |
| `best-[category].htm` | Template 2 (Comparison) | 2,500-3,500 | Complete (ALL brands) |
| `how-to-[action].htm` | Template 3 (How-To) | 1,500-2,500 | Brief only |
| `legal-states/[state].htm` | Template 4 (State) | 2,000-2,800 | Complete (state ops) |

## Document Priority Hierarchy

When guidance overlaps, follow this precedence (highest to lowest):

| Priority | Document | Authority |
|----------|----------|-----------|
| 1 | **SKILL.md Critical Rules** (this file, lines 34-44) | ABSOLUTE - Never override |
| 2 | **gold-standard-templates.md** | HTML/CSS/JS patterns - Use exactly |
| 3 | **compliance-standards.md** | Legal requirements - Mandatory |
| 4 | **Phase-specific docs** (phase1/2/3-*.md) | Workflow instructions |
| 5 | **Validation checklists** | Pre-output verification |
| 6 | **Other reference docs** | Supporting information |

> **Rule:** If a newer document contradicts a higher-priority document, the higher-priority document wins. Higher-priority standards are more professionally vetted.

## Reference Files

Load these as needed during each phase:

- **Phase 1**: `references/phase1-research.md` - Research protocol with keyword clustering
- **Phase 2**: `references/phase2-writer.md` - Writer brief creation with optimization
- **Phase 3**: `references/phase3-technical.md` - HTML templates and schema markup
- **Quick Lookups**: `references/reference-library.md` - Writers, brands, compliance
- **Quality Check**: `references/quality-checklist.md` - Pre-delivery verification
- **Content Templates**: `references/content-templates.md` - 4 template structures
- **Verification**: `references/verification-standards.md` - Bonus verification, T&Cs
- **Lessons**: `references/lessons-learned.md` - Edge cases and anti-patterns
- **Gold Standard Templates**: `references/gold-standard-templates.md` - HTML/CSS/JS patterns for page uniformity
- **State Availability**: `assets/data/state-availability.json` - State-by-state sportsbook availability
- **HTML Validation**: `references/html-validation-checklist.md` - Pre-output HTML structure validation
- **Compliance Standards**: `references/compliance-standards.md` - Banned language, accessibility, AI/LLM schema optimization
- **Ahrefs Workflow**: `references/ahrefs-keyword-workflow.md` - Mandatory keyword research workflow
- **Calculator UX**: `references/calculator-ux-standards.md` - Interactive element standards (add/remove, validation, mobile)

## Data Files

- `assets/data/site-structure-english.csv` - English URL/keyword mappings
- `assets/data/site-structure-spanish.csv` - Spanish URL/keyword mappings

## Output Format

Save three files for each brief:
1. `[page-name]-brief-control-sheet.md` - Phase 1 output
2. `[page-name]-writer-brief.md` - Phase 2 output
3. `[page-name]-ai-enhancement.md` - Phase 3 output

**After all phases complete**, convert to Word format:
```bash
python scripts/convert_to_docx.py --all
```
This creates `.docx` versions for content writers.

## Compliance (Every Page)

- Age: 21+ (most states)
- Hotline: 1-800-522-4700
- Affiliate disclosure (top)
- Responsible gambling section (bottom)
- State availability disclaimer

## Continuous Improvement System

This project learns from feedback over time:

- **Submit feedback**: Copy `feedback/FEEDBACK-TEMPLATE.md` to `feedback/submitted/`
- **System updates**: Validated feedback updates reference docs automatically
- **Track improvements**: See `feedback/FEEDBACK-LOG.md` for metrics and changes

**Process documentation**: `feedback/FEEDBACK-PROCESS.md`

All users (writers, SEO, editors) can submit feedback to improve brief quality.
