# TopEndSports Content Briefs - AI Instructions

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
- 8-10 FAQs targeting keywords
- Complete source requirements
- Brand sections with word counts

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

### Phase-Specific Instructions
| Phase | Document |
|-------|----------|
| Phase 1 | `references/phase1-research.md` |
| Phase 2 | `references/phase2-writer.md` |
| Phase 3 | `references/phase3-technical.md` |

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
- Affiliate disclosure in intro
- Responsible gambling section at bottom
- NO dated language in H1 (use Last Updated badge)

---

## 🚀 QUICK START

When user says "generate brief for [URL]":

1. **Read** ORCHESTRATOR.md
2. **Execute** Phase 1 with real Ahrefs data
3. **Execute** Phase 2 using Phase 1 JSON
4. **Execute** Phase 3 using Phase 1 + Phase 2 JSON
5. **Convert** all outputs to DOCX
6. **Verify** all 6 files exist

**INCOMPLETE = Any phase skipped or any file missing**
