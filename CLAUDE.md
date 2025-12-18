# TopEndSports Content Briefs - AI Instructions

**Last Updated:** December 16, 2025

## MANDATORY: READ BEFORE ANY BRIEF GENERATION

**This file is automatically loaded at session start. Follow these instructions exactly.**

---

## 🚨 CRITICAL RULE: 3-PHASE BRIEF GENERATION

When asked to "generate a brief" for ANY URL, you MUST:

### Phase 1: Research & Discovery
**Input:** URL
**Output:**
- `content-briefs-skill/active/[page-name]-phase1.json`
- `content-briefs-skill/output/[page-name]-brief-control-sheet.md`

**Requirements:**
- Real keyword data from Ahrefs (MCP or Python fallback)
- 8-15 secondary keywords with volume data
- Competitor analysis (affiliate sites, not brands)
- Brand selection with rationale

### Phase 2: Writer Brief
**Input:** Phase 1 JSON
**Output:**
- `content-briefs-skill/active/[page-name]-phase2.json`
- `content-briefs-skill/output/[page-name]-writer-brief.md`

**Requirements:**
- All keywords mapped to H2/H3/FAQ sections
- 7+ FAQs targeting keywords
- Complete source requirements
- Brand sections with word counts
- Mobile Experience section per brand (100-150 words)
- Payment methods comparison section
- Calculator tool links

### Phase 3: AI Enhancement
**Input:** Phase 1 + Phase 2 JSON
**Output:**
- `content-briefs-skill/output/[page-name]-ai-enhancement.md`

**Requirements:**
- Complete HTML/CSS/JS code
- Interactive comparison table
- Schema markup (Article, FAQ, Breadcrumb)
- Complete T&Cs for ALL brands

### Final: Convert to DOCX
```bash
# Use MCP tool: mcp__topendsports-briefs__convert_to_docx
```

---

## 🛑 ANTI-PATTERNS - NEVER DO THESE

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| Create only writer-brief.md | Missing Phase 1 research & Phase 3 technical |
| Skip Ahrefs when MCP fails | Python workaround exists and WORKS |
| Use estimated keyword data | Real data available via Python API |
| Skip Phase 3 AI Enhancement | Dev team needs HTML/code implementation |
| Create 1 file instead of 6 | Brief is incomplete without all outputs |

---

## 🔧 AHREFS FALLBACK PROTOCOL

**When MCP returns 403/error:**

```bash
# Use Python workaround - THIS WORKS
python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview \
  '{"select":"keyword,volume,difficulty,traffic_potential","country":"us","keywords":"YOUR_KEYWORDS"}'
```

**NEVER skip keyword research. The Python fallback is always available.**

---

## 📁 OUTPUT FILES

### 3 Main Deliverables (in `output/`)
| File | Phase | Description |
|------|-------|-------------|
| `[page]-brief-control-sheet.md` | Phase 1 | Research findings, keyword cluster, brand selection |
| `[page]-writer-brief.md` | Phase 2 | Content outline, H2/H3 optimization, FAQs |
| `[page]-ai-enhancement.md` | Phase 3 | Complete HTML/CSS/JS code, schema markup |

### 2 Intermediate Files (in `active/`)
| File | Purpose |
|------|---------|
| `[page]-phase1.json` | Structured data passed to Phase 2 |
| `[page]-phase2.json` | Structured data passed to Phase 3 |

These JSON files are working files for data exchange between phases.

### Optional: DOCX Conversion
Run `mcp__topendsports-briefs__convert_to_docx` to create Word versions for writers.

---

## 📚 REFERENCE DOCUMENTS

### MUST Read Before Starting
| Document | Path | Purpose |
|----------|------|---------|
| **Orchestrator** | `content-briefs-skill/ORCHESTRATOR.md` | Multi-agent workflow |
| **Ahrefs Workflow** | `content-briefs-skill/references/ahrefs-keyword-workflow.md` | **CRITICAL** - Keyword research steps |
| **Guardrails** | `content-briefs-skill/GUARDRAILS.md` | Anti-patterns to avoid |
| **Competitor Analysis** | `references/competitor-content-analysis.md` | Match #1 ranking page structure |

### Phase-Specific Instructions
| Phase | Document |
|-------|----------|
| Phase 1 | `references/phase1-research.md` |
| Phase 2 | `references/phase2-writer.md` |
| Phase 3 | `references/phase3-technical.md` |
| Meta Tags | `references/meta-title-optimization.md` |

### Supporting References (consult as needed)
| Document | Purpose |
|----------|---------|
| `gold-standard-templates.md` | HTML/CSS/JS patterns for tables, cards |
| `reference-library.md` | Quick lookups (bonuses, states, contacts) |
| `lessons-learned.md` | Past mistakes to avoid |
| `content-templates.md` | Outline structures by template type |
| `verification-standards.md` | T&Cs verification requirements |
| `quality-checklist.md` | Pre-delivery quality checks |
| `html-validation-checklist.md` | HTML validation rules |
| `compliance-standards.md` | Legal/gambling compliance |
| `calculator-ux-standards.md` | Interactive calculator patterns |

---

## ✅ PRE-FLIGHT CHECKLIST

Before starting ANY brief:

- [ ] Read ORCHESTRATOR.md for workflow
- [ ] Test Ahrefs connectivity (MCP or Python)
- [ ] Identify page in site structure
- [ ] Confirm 3-phase output requirement
- [ ] Plan to create ALL 6 output files

---

## 🎯 BRAND POSITIONING (LOCKED)

| Position | Brand | Status |
|----------|-------|--------|
| #1 | FanDuel | LOCKED (commercial deal) |
| #2 | BetMGM | LOCKED (commercial deal) |
| #3-7 | Research-driven | Based on competitor analysis |

**theScore BET** (formerly ESPN BET) - rebranded December 2025

---

## 🔢 KEYWORD TARGETS

- Primary keyword: From site structure CSV
- Secondary keywords: 8-15 with real volume data
- Total cluster volume: 400-900% increase over primary
- All keywords mapped to specific sections

---

## ⚠️ COMPLIANCE (ALWAYS INCLUDE)

- Age: 21+ (18+ in MT, NH, RI, WY, DC)
- Hotline: 1-800-522-4700
- Responsible gambling section at bottom
- NO dated language in H1 (use Last Updated badge)
- **NO affiliate disclosure in content** (it's in website sidebar)

---

## 🚀 QUICK START

When user says "generate brief for [URL]":

1. **Read** ORCHESTRATOR.md
2. **Execute** Phase 1 with real Ahrefs data
3. **Execute** Phase 2 using Phase 1 JSON
4. **Execute** Phase 3 using Phase 1 + Phase 2 JSON
5. **Convert** all outputs to DOCX
6. **Verify** all 6 files exist
7. **Ask for feedback** (see Feedback section below)

**INCOMPLETE = Any phase skipped or any file missing**

---

## 🔒 VALIDATION GATES

**Run after each phase:**
```bash
bash content-briefs-skill/scripts/validate-phase.sh [phase] [page-name]
```

**DO NOT proceed to next phase until validation PASSES.**

---

## 📋 MINIMUM REQUIREMENTS

### Phase 1 Minimums
- [ ] Primary keyword with REAL volume from Ahrefs
- [ ] 8+ secondary keywords with REAL volume
- [ ] 3 competitor analyses (actionnetwork, covers, thelines)
- [ ] 5-7 brands with rationale
- [ ] Content gaps identified

### Phase 2 Minimums
- [ ] Every secondary keyword mapped to H2/H3/FAQ
- [ ] 7+ FAQs targeting keywords
- [ ] Source requirements (TIER 1: App Store, Reddit)
- [ ] Word count targets per section
- [ ] 12 internal links
- [ ] Mobile Experience section per brand
- [ ] Payment methods comparison included
- [ ] Calculator tool links

### Phase 3 Minimums
- [ ] **SERP-optimized meta tags** (see `references/meta-title-optimization.md`)
  - Title: Under 60 chars, primary keyword at START, **NO YEAR**
  - Description: Under 155 chars, unique value proposition
  - SERP competitor analysis documented
- [ ] Last Updated badge HTML
- [ ] Comparison table with ALL brands
- [ ] T&Cs for ALL brands (not just top 3)
- [ ] Schema markup (Article + FAQ + Breadcrumb)
- [ ] Interactive element with working code
- [ ] Responsible gambling section (NO affiliate disclosure - it's in sidebar)
- [ ] **ZERO placeholders** (no "...", no "[Insert]")

---

## 💀 FAILURE CONDITIONS

You have **FAILED** the task if ANY of these are true:

1. Created fewer than 3 deliverable files
2. Skipped Ahrefs research (MCP error is NOT an excuse - use Python)
3. Used estimated/guessed keyword volumes instead of real data
4. Fewer than 8 secondary keywords
5. Fewer than 7 FAQs
6. AI Enhancement contains "..." or "[Insert]" placeholders
7. Missing T&Cs for some brands
8. Missing schema markup
9. Skipped any validation step

---

## 🏁 USE THE SLASH COMMAND

For brief generation, use: `/generate-brief [URL]`

This command contains ALL steps embedded directly - follow it exactly.

---

## 📝 FEEDBACK & CONTINUOUS IMPROVEMENT

### After EVERY Task Completion

When you complete a brief or significant task, prompt the user:

> **Task Complete!** Help us improve:
> - `/submit-feedback` - Report issues, edge cases, or suggestions
> - Quick rating: Was this brief generation smooth? (1-5)

### Submit Feedback Command

Use `/submit-feedback [category]` where category is:

| Category | Use When |
|----------|----------|
| `keyword` | Missing keywords, cannibalization issues |
| `writer` | Unclear instructions, missing info |
| `technical` | HTML/code bugs, schema errors |
| `template` | Outline structure problems |
| `workflow` | Process bottlenecks, timing issues |
| `edge-case` | Unusual scenarios not covered |

### Feedback Routing

Feedback automatically routes to the right documentation:

| Issue Type | Updates |
|------------|---------|
| Keyword problems | `references/phase1-research.md` |
| Writer confusion | `references/phase2-writer.md` |
| Technical bugs | `references/phase3-technical.md` |
| Recurring mistakes | `references/lessons-learned.md` |
| Quality failures | `references/quality-checklist.md` |

### How Feedback Improves the System

```
[User submits feedback]
    ↓
[Weekly validation review]
    ↓
[Extract lessons learned]
    ↓
[Update reference docs]
    ↓
[Next brief uses improved instructions]
```

### Run Feedback Ingestion

To apply validated feedback to documentation:
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons
```

### Feedback Files Location

| Folder | Purpose |
|--------|---------|
| `feedback/submitted/` | New feedback awaiting review |
| `feedback/validated/` | Reviewed and confirmed feedback |
| `feedback/applied/` | Feedback that updated docs |
| `feedback/FEEDBACK-LOG.md` | Changelog of all feedback |

---

## 📚 Skills Library

This project includes **7 foundational skills** for autonomous learning and optimization:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **validation-html-structure** | Validate TopEndSports HTML structure | Before delivery, debugging layout |
| **content-preservation** | Preserve Rob Wood's expert content | Optimizing existing content |
| **seo-keyword-integration** | Natural keyword placement | After keyword research |
| **internal-linking-strategy** | Safe internal links (verified URLs only) | Adding contextual links |
| **cta-placement-strategy** | Value-first CTA placement | Improving conversion |
| **interactive-elements** | 7 engagement element types | Pages over 1,500 words |
| **research-workflow** | Complete 4-phase optimization | Starting any project |

### Accessing Skills

Skills are located in `.claude/skills/` directory:
- **Quick reference:** `.claude/skills/index.md`
- **Individual skills:** `.claude/skills/[skill-name].md`

### Skills Are Self-Learning

Skills improve automatically through feedback:
1. Submit feedback via `/submit-feedback [category]`
2. Weekly processing updates skill documentation
3. Lessons learned prevent future issues

**See:** `.claude/skills/index.md` for complete documentation

