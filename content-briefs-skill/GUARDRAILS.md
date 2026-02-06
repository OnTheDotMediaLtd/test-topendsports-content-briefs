# GUARDRAILS - MANDATORY BRIEF GENERATION CHECKLIST

**Purpose:** Prevent incomplete or incorrect brief generation. This document MUST be consulted at the START of every brief generation task.

**Status:** MANDATORY - Not following these guardrails will result in incomplete or incorrect briefs.

---

## ⚠️ STOP - Read This First

Before generating ANY brief, you must:

1. ✅ Read `content-briefs-skill/ORCHESTRATOR.md`
2. ✅ Verify you understand the 3-phase requirement
3. ✅ Check Ahrefs connectivity (MCP or Python fallback ready)
4. ✅ Confirm you have the correct page URL

**If you skip ANY phase or ANY output file, the brief is INCOMPLETE.**

---

## 🚦 PRE-FLIGHT CHECKLIST

Execute these checks BEFORE starting Phase 1:

### 1. Document Review
```bash
# Read the orchestration architecture
cat content-briefs-skill/ORCHESTRATOR.md

# Verify phase instructions exist
ls -la content-briefs-skill/references/phase*.md
```

**Expected files:**
- `content-briefs-skill/references/phase1-research.md`
- `content-briefs-skill/references/phase2-writer.md`
- `content-briefs-skill/references/phase3-technical.md`

### 2. Ahrefs Connectivity Test

**Option A: Try MCP First**
```bash
# Test if Ahrefs MCP is available
# Use mcp__ahrefs__doc to check connectivity
```

**Option B: Python Fallback (REQUIRED if MCP fails)**
```bash
# Test Python workaround
python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview '{"select":"keyword,volume","country":"us","keywords":"test"}'
```

**CRITICAL:** If MCP returns 403, errors, or is unavailable, you MUST use the Python fallback. Never proceed without keyword data.

### 3. Output Directory Verification
```bash
# Ensure directories exist
ls -la content-briefs-skill/active/
ls -la content-briefs-skill/output/
```

### 4. Page Name Extraction
```python
# Given URL: /sport/betting/nfl-betting-sites.htm
url = "/sport/betting/nfl-betting-sites.htm"
page_name = url.split('/')[-1].replace('.htm', '')
# Result: "nfl-betting-sites"
```

**Verify page exists in site structure:**
```bash
grep -i "nfl-betting-sites" content-briefs-skill/assets/data/site-structure-english.csv
```

---

## 🔒 PHASE VALIDATION GATES

Each phase MUST produce specific outputs. **DO NOT proceed to the next phase until current phase outputs exist.**

### Phase 1: Research & Discovery (10-15 minutes)

**Instructions file:** `content-briefs-skill/references/phase1-research.md`

**REQUIRED OUTPUTS:**
1. ✅ `content-briefs-skill/active/[page-name]-phase1.json`
2. ✅ `content-briefs-skill/output/[page-name]-brief-control-sheet.md`

**Validation Command:**
```bash
# Replace [page-name] with actual page name
PAGE_NAME="nfl-betting-sites"
test -f "content-briefs-skill/active/${PAGE_NAME}-phase1.json" && \
test -f "content-briefs-skill/output/${PAGE_NAME}-brief-control-sheet.md" && \
echo "✅ Phase 1 outputs verified" || echo "❌ Phase 1 INCOMPLETE"
```

**Minimum Content Requirements:**
- Primary keyword with search volume
- 8-15 secondary keywords with real Ahrefs volume data
- Top 3 competitor analysis (actionnetwork.com, covers.com, thelines.com)
- Brand selection with rationale (FanDuel #1, BetMGM #2, research-driven #3-7)
- Content gaps identified from competitor analysis

**Quality Check:**
```bash
# Verify phase1.json has required keys
PAGE_NAME="nfl-betting-sites"
python3 -c "import json; data=json.load(open('content-briefs-skill/active/${PAGE_NAME}-phase1.json')); assert 'primaryKeyword' in data; assert len(data.get('secondaryKeywords', [])) >= 8; print('✅ Phase 1 JSON valid')"
```

### Phase 2: Writer Brief Creation (5-10 minutes)

**Instructions file:** `content-briefs-skill/references/phase2-writer.md`

**PREREQUISITE:** Phase 1 outputs MUST exist (validated above)

**REQUIRED OUTPUTS:**
1. ✅ `content-briefs-skill/active/[page-name]-phase2.json`
2. ✅ `content-briefs-skill/output/[page-name]-writer-brief.md`

**Validation Command:**
```bash
PAGE_NAME="nfl-betting-sites"
test -f "content-briefs-skill/active/${PAGE_NAME}-phase2.json" && \
test -f "content-briefs-skill/output/${PAGE_NAME}-writer-brief.md" && \
echo "✅ Phase 2 outputs verified" || echo "❌ Phase 2 INCOMPLETE"
```

**Minimum Content Requirements:**
- Content outline with keyword mapping (secondary keywords → H2/H3 sections)
- 7 FAQ questions targeting high-volume keywords
- Source requirements (TIER 1: App Store, Reddit, state .gov sites)
- Word count targets per section
- Internal linking strategy

**Quality Check:**
```bash
# Verify writer brief contains required sections
PAGE_NAME="nfl-betting-sites"
grep -q "FAQ Questions" "content-briefs-skill/output/${PAGE_NAME}-writer-brief.md" && \
grep -q "Source Requirements" "content-briefs-skill/output/${PAGE_NAME}-writer-brief.md" && \
echo "✅ Phase 2 content valid" || echo "❌ Phase 2 missing required sections"
```

### Phase 3: Technical Implementation (10-15 minutes)

**Instructions file:** `content-briefs-skill/references/phase3-technical.md`

**PREREQUISITE:** Phase 1 AND Phase 2 outputs MUST exist

**REQUIRED OUTPUTS:**
1. ✅ `content-briefs-skill/output/[page-name]-ai-enhancement.md`

**Validation Command:**
```bash
PAGE_NAME="nfl-betting-sites"
test -f "content-briefs-skill/output/${PAGE_NAME}-ai-enhancement.md" && \
echo "✅ Phase 3 output verified" || echo "❌ Phase 3 INCOMPLETE"
```

**Minimum Content Requirements:**
- Complete meta tags (title, description, Open Graph, Twitter Card)
- Full HTML comparison table using Gold Standard Templates
- Interactive elements (calculators, filters, etc.)
- Complete T&Cs sections for ALL featured brands
- Schema markup (Article, FAQ, Breadcrumb)
- Compliance sections (affiliate disclosure, responsible gambling)
- All code complete and ready to implement (no placeholders)

**Quality Check:**
```bash
# Verify AI enhancement has required elements
PAGE_NAME="nfl-betting-sites"
grep -q "schema.org" "content-briefs-skill/output/${PAGE_NAME}-ai-enhancement.md" && \
grep -q "comparison-table" "content-briefs-skill/output/${PAGE_NAME}-ai-enhancement.md" && \
echo "✅ Phase 3 content valid" || echo "❌ Phase 3 missing required elements"
```

---

## 🛡️ AHREFS FALLBACK PROTOCOL

**When MCP Fails (403, timeout, or error):**

### Step 1: Identify the Failure
```
MCP Error Indicators:
- HTTP 403 Forbidden
- Connection timeout
- "unauthorized" or "authentication failed" messages
- Empty or null results from mcp__ahrefs__* tools
```

### Step 2: Switch to Python Workaround IMMEDIATELY

**Location:** `.claude/scripts/ahrefs-api.py`

**Usage Pattern:**
```bash
python3 .claude/scripts/ahrefs-api.py <endpoint> '<params_json>'
```

### Step 3: Common Research Commands

**Keyword Research (Primary & Secondary Keywords):**
```bash
# Get keyword overview with volume and difficulty
python3 .claude/scripts/ahrefs-api.py \
  keywords-explorer/overview \
  '{"select":"keyword,volume,difficulty,cpc,traffic_potential","country":"us","keywords":"nfl betting sites"}'

# Get related keywords
python3 .claude/scripts/ahrefs-api.py \
  keywords-explorer/related-terms \
  '{"select":"keyword,volume,difficulty","country":"us","keywords":"nfl betting sites","limit":20}'

# Get search suggestions
python3 .claude/scripts/ahrefs-api.py \
  keywords-explorer/search-suggestions \
  '{"select":"keyword,volume,difficulty","country":"us","keywords":"nfl betting","limit":15}'
```

**Competitor Analysis:**
```bash
# Analyze competitor's organic keywords
python3 .claude/scripts/ahrefs-api.py \
  site-explorer/organic-keywords \
  '{"select":"keyword,volume,position,traffic","target":"actionnetwork.com","date":"2025-12-01","country":"us","limit":50}'

# Get competitor's top pages
python3 .claude/scripts/ahrefs-api.py \
  site-explorer/top-pages \
  '{"select":"url,traffic,keywords_count","target":"covers.com","date":"2025-12-01","country":"us","limit":20}'

# Domain rating
python3 .claude/scripts/ahrefs-api.py \
  site-explorer/domain-rating \
  '{"target":"thelines.com","date":"2025-12-01"}'
```

**SERP Analysis:**
```bash
# Check top 10 search results for keyword
python3 .claude/scripts/ahrefs-api.py \
  serp-overview/serp-overview \
  '{"select":"url,position,traffic,domain_rating","country":"us","keyword":"best nfl betting sites","top_positions":10}'
```

### Step 4: Document the Fallback

When using Python workaround, note it in the Brief Control Sheet:
```markdown
## Research Methodology

**Ahrefs Access:** Python API workaround (MCP unavailable)
**Date:** 2025-12-05
**Keywords Researched:** [list commands used]
```

---

## ✅ QUALITY GATES - Minimum Requirements

Before marking ANY phase as complete, verify these minimums:

### Phase 1 Requirements

| Requirement | Minimum | How to Verify |
|------------|---------|---------------|
| Primary keyword | 1 with volume data | Check phase1.json `primaryKeyword.volume` |
| Secondary keywords | 8-15 with volume | Check phase1.json `secondaryKeywords` array length |
| Competitor sites analyzed | 3 (actionnetwork, covers, thelines) | Check phase1.json `competitors` array |
| Brands selected | 7 total (FD #1, MGM #2, 5 others) | Check phase1.json `brands` array |
| Content gaps identified | At least 3 | Check phase1.json `contentGaps` |
| Data source | Real Ahrefs data (not estimated) | All volumes should be integers > 0 |

### Phase 2 Requirements

| Requirement | Minimum | How to Verify |
|------------|---------|---------------|
| Content outline | H2 sections mapped to keywords | Check writer-brief.md outline |
| FAQ questions | 7 questions | Count FAQs in phase2.json |
| Source requirements | TIER 1 sources listed | Check "Source Requirements" section |
| Keyword distribution | Every secondary keyword used | Match outline to phase1 keywords |
| Word count targets | Specified per section | Check "Word Count" in writer brief |

### Phase 3 Requirements

| Requirement | Minimum | How to Verify |
|------------|---------|---------------|
| Meta tags | Title, description, OG, Twitter | Search for `<meta` tags |
| Comparison table | Gold Standard Template used | Search for "comparison-table" class |
| Schema markup | Article + FAQ + Breadcrumb | Search for `schema.org` |
| T&Cs sections | All 7 featured brands | Count T&C sections in output |
| Interactive elements | At least 1 (calculator/filter) | Check for `<script>` or interactive HTML |
| Compliance | Disclosure + responsible gambling | Search for "affiliate disclosure" |
| Complete code | No "..." or "[Insert]" placeholders | grep for placeholders |

---

## 🚫 ANTI-PATTERN WARNINGS

**These actions should NEVER happen. If you find yourself doing any of these, STOP immediately:**

### ❌ NEVER: Skip Phase 1 Research

**Wrong:**
```
User: Generate a brief for nfl-betting-sites
Assistant: [Creates writer-brief.md directly]
```

**Why it's wrong:**
- No keyword research = no SEO optimization
- No competitor analysis = missing content opportunities
- No data-driven brand selection = arbitrary choices

**Right:**
```
User: Generate a brief for nfl-betting-sites
Assistant: Starting Phase 1 research...
[Performs Ahrefs keyword research]
[Analyzes competitors]
[Creates phase1.json + brief-control-sheet.md]
Now proceeding to Phase 2...
```

### ❌ NEVER: Skip Ahrefs Research When MCP Fails

**Wrong:**
```
Assistant: Ahrefs MCP returned 403, so I'll use estimated search volumes...
```

**Why it's wrong:**
- Estimated data is unreliable for SEO
- Python workaround is available and required
- Skipping research undermines entire brief quality

**Right:**
```
Assistant: Ahrefs MCP returned 403, switching to Python workaround...
[Executes: python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview ...]
[Gets real data]
Research complete with actual search volumes.
```

### ❌ NEVER: Generate Only 1 of 3 Required Files

**Wrong:**
```
Assistant: Brief complete! Generated:
- output/nfl-betting-sites-writer-brief.md
```

**Why it's wrong:**
- Missing Phase 1 control sheet (research findings)
- Missing Phase 3 AI enhancement (technical implementation)
- Incomplete brief package

**Right:**
```
Assistant: Brief package complete! Generated:
- output/nfl-betting-sites-brief-control-sheet.md (Phase 1)
- output/nfl-betting-sites-writer-brief.md (Phase 2)
- output/nfl-betting-sites-ai-enhancement.md (Phase 3)
All phases validated and exported to Word format.
```

### ❌ NEVER: Skip Phase 3 Technical Implementation

**Wrong:**
```
Assistant: Writer brief is done, so the brief is complete!
```

**Why it's wrong:**
- Missing HTML/code implementation
- Missing schema markup
- Missing T&Cs sections
- Technical team has nothing to implement

**Right:**
```
Assistant: Writer brief complete (Phase 2). Now proceeding to Phase 3 technical implementation...
[Reads phase1.json and phase2.json]
[Generates complete HTML, schema, T&Cs]
Phase 3 complete with full technical specifications.
```

### ❌ NEVER: Use Placeholders or Shortened Content

**Wrong:**
```html
<!-- Comparison table with all 7 brands -->
<table>
  <tr><td>FanDuel</td></tr>
  <!-- ... remaining brands ... -->
</table>
```

**Why it's wrong:**
- Placeholders require manual completion
- Team feedback: "NEVER shorten or skip content"
- Incomplete deliverable

**Right:**
```html
<!-- Comparison table with all 7 brands -->
<table class="comparison-table">
  <tr><td>FanDuel</td><td>$150 bonus</td><td>4.8★</td></tr>
  <tr><td>BetMGM</td><td>$1500 bonus</td><td>4.7★</td></tr>
  <tr><td>DraftKings</td><td>$1000 bonus</td><td>4.7★</td></tr>
  <!-- ... all 7 brands with complete data ... -->
</table>
```

### ❌ NEVER: Proceed Without Validating Previous Phase

**Wrong:**
```
Assistant: Phase 1 agent completed. Starting Phase 2...
[Phase 2 starts but phase1.json doesn't exist]
Error: Cannot read phase1.json
```

**Why it's wrong:**
- Phases are dependent on previous outputs
- Wastes time and causes errors
- Breaks the orchestration flow

**Right:**
```
Assistant: Phase 1 agent completed. Validating outputs...
✅ Verified: active/nfl-betting-sites-phase1.json (14KB)
✅ Verified: output/nfl-betting-sites-brief-control-sheet.md (8KB)
✅ Verified: 12 secondary keywords with volume data
Validation passed. Starting Phase 2...
```

---

## Keyword Cannibalization Prevention

### Before Adding Keywords to Any Brief:

| Check | Action |
|-------|--------|
| Is this a hub page? | Hub pages should NOT target keywords - only link to dedicated pages |
| Does another page own this keyword? | Check dedicated pages first |
| Is keyword in wrong cluster? | Move to correct page's brief |

### Keyword Ownership by Page Type:

| Page Type | Owns These Keywords |
|-----------|---------------------|
| Hub | NONE (navigation only) |
| Betting Apps | betting apps, mobile betting, app download |
| Betting Offers | betting offers, welcome bonus, sign up bonus |
| Free Bets | free bets, no deposit, risk-free |
| Football Betting | football betting, football sites |
| Horse Racing | horse racing betting, horse racing sites |
| New Betting Sites | new betting sites, new bookmakers |

### Red Flags:
- ❌ Hub page with 10+ secondary keywords
- ❌ Hub page with H2 sections matching dedicated page titles
- ❌ Two pages targeting same "best X" keyword
- ❌ Comparison page with review-style sections

---

## 📋 QUICK CHECKLIST FOR BRIEF GENERATION

Copy this checklist for every brief:

```
[ ] Pre-Flight
    [ ] Read ORCHESTRATOR.md
    [ ] Test Ahrefs connectivity (MCP or Python)
    [ ] Extract page name from URL
    [ ] Verify page exists in site structure

[ ] Phase 1: Research & Discovery
    [ ] Read references/phase1-research.md
    [ ] Execute Ahrefs keyword research (8-15 secondary keywords)
    [ ] Analyze top 3 competitors (actionnetwork, covers, thelines)
    [ ] Select 7 brands (FD #1, MGM #2, 5 research-driven)
    [ ] Create active/[page-name]-phase1.json
    [ ] Create output/[page-name]-brief-control-sheet.md
    [ ] Validate: JSON contains all required keys
    [ ] Validate: All keywords have real volume data

[ ] Phase 2: Writer Brief Creation
    [ ] Read references/phase2-writer.md
    [ ] Load active/[page-name]-phase1.json
    [ ] Map secondary keywords to H2/H3 sections
    [ ] Create 7 FAQ questions from high-volume keywords
    [ ] Specify TIER 1 source requirements
    [ ] Create active/[page-name]-phase2.json
    [ ] Create output/[page-name]-writer-brief.md
    [ ] Validate: All secondary keywords used in outline
    [ ] Validate: 7 FAQs present

[ ] Phase 3: Technical Implementation
    [ ] Read references/phase3-technical.md
    [ ] Load active/[page-name]-phase1.json
    [ ] Load active/[page-name]-phase2.json
    [ ] Create complete meta tags
    [ ] Build comparison table (Gold Standard Template)
    [ ] Generate schema markup (Article + FAQ + Breadcrumb)
    [ ] Write T&Cs for all 7 brands
    [ ] Add interactive elements
    [ ] Include compliance sections
    [ ] Create output/[page-name]-ai-enhancement.md
    [ ] Validate: No placeholders or "..." in code
    [ ] Validate: Schema markup present

[ ] Final Steps
    [ ] Convert to Word: python scripts/convert_to_docx.py --all
    [ ] Verify 3 output files exist (.md and .docx)
    [ ] Report completion with file list
```

---

## 🔧 TROUBLESHOOTING

### Issue: "MCP returned 403"
**Solution:** Use Python workaround immediately
```bash
python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview '{"select":"keyword,volume","country":"us","keywords":"your keyword"}'
```

### Issue: "phase1.json not found"
**Solution:** You skipped Phase 1. Go back and complete it.
```bash
# Check if file exists
ls -la content-briefs-skill/active/
# If missing, restart Phase 1
```

### Issue: "Only 5 secondary keywords found"
**Solution:** Minimum is 8. Use related-terms or search-suggestions endpoints
```bash
python3 .claude/scripts/ahrefs-api.py \
  keywords-explorer/related-terms \
  '{"select":"keyword,volume","country":"us","keywords":"your primary keyword","limit":20}'
```

### Issue: "Brief has placeholders like '...'"
**Solution:** This violates team feedback rule #1. Output ALL content in full.
- Never use "..." or "[Insert X here]"
- Generate complete code always
- Reference: ORCHESTRATOR.md line 11

---

## 📚 REFERENCE DOCUMENTS

**Must Read Before Each Phase:**

| Phase | Document Path | Purpose |
|-------|--------------|---------|
| Phase 1 | `content-briefs-skill/references/phase1-research.md` | Research instructions |
| Phase 2 | `content-briefs-skill/references/phase2-writer.md` | Writer brief instructions |
| Phase 3 | `content-briefs-skill/references/phase3-technical.md` | Technical implementation |

**Supporting References:**

- `content-briefs-skill/references/gold-standard-templates.md` - HTML/CSS/JS patterns (MANDATORY for Phase 3)
- `content-briefs-skill/references/reference-library.md` - Quick lookups
- `content-briefs-skill/references/lessons-learned.md` - Common mistakes to avoid
- `content-briefs-skill/references/ahrefs-keyword-workflow.md` - Keyword research process

---

## 🎯 SUCCESS CRITERIA

A brief is COMPLETE when:

✅ **All 3 phases executed** (Research → Writer → Technical)
✅ **All output files exist** (control sheet, writer brief, AI enhancement)
✅ **Real data used** (Ahrefs keyword volumes, not estimated)
✅ **All quality gates passed** (8-15 keywords, 7 FAQs, complete code)
✅ **No anti-patterns present** (no placeholders, no skipped phases)
✅ **Word documents generated** (all .md files converted to .docx)

**Time estimate:** 25-40 minutes for complete brief package

**If you cannot meet these criteria, the brief is INCOMPLETE and must be revised.**

---

## 📞 WHEN IN DOUBT

If you're unsure whether to skip a step or take a shortcut:

1. **Check this document** - If it's in the Anti-Patterns section, don't do it
2. **Check ORCHESTRATOR.md** - Follow the architecture
3. **Check team feedback** - Lines 7-16 in ORCHESTRATOR.md are rules from real usage
4. **Default to completeness** - Better to over-deliver than under-deliver

**Remember:** This is a 3-phase process. Shortcuts break the system.

---

**Document Version:** 1.0
**Last Updated:** 2025-12-05
**Status:** MANDATORY FOR ALL BRIEF GENERATION
