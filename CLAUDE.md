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

## 📁 REQUIRED OUTPUT FILES (6 Total)

For any brief (e.g., `best-sports-betting-apps`):

```
content-briefs-skill/
├── active/
│   ├── best-sports-betting-apps-phase1.json  ← Phase 1 data
│   └── best-sports-betting-apps-phase2.json  ← Phase 2 data
└── output/
    ├── best-sports-betting-apps-brief-control-sheet.md   ← Phase 1 output
    ├── best-sports-betting-apps-brief-control-sheet.docx
    ├── best-sports-betting-apps-writer-brief.md          ← Phase 2 output
    ├── best-sports-betting-apps-writer-brief.docx
    ├── best-sports-betting-apps-ai-enhancement.md        ← Phase 3 output
    └── best-sports-betting-apps-ai-enhancement.docx
```

---

## 📚 REFERENCE DOCUMENTS

Before generating any brief, read:

1. **Orchestration:** `content-briefs-skill/ORCHESTRATOR.md`
2. **Guardrails:** `content-briefs-skill/GUARDRAILS.md`
3. **Phase 1:** `content-briefs-skill/references/phase1-research.md`
4. **Phase 2:** `content-briefs-skill/references/phase2-writer.md`
5. **Phase 3:** `content-briefs-skill/references/phase3-technical.md`

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
