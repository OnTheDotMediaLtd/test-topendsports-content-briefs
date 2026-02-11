# CONTENT BRIEF GENERATION - MANDATORY 3-PHASE WORKFLOW

**Target URL:** $ARGUMENTS

---

## STOP - READ EVERY WORD BELOW

You are about to generate a content brief. **You MUST follow EVERY step below.** Skipping ANY step makes the brief INCOMPLETE and UNACCEPTABLE.

**This command produces 3 deliverables:**
1. `output/[page]-brief-control-sheet.md` (Phase 1)
2. `output/[page]-writer-brief.md` (Phase 2)
3. `output/[page]-ai-enhancement.md` (Phase 3)

**If you create fewer than 3 deliverables, you have FAILED.**

---

## MULTI-AGENT EXECUTION (RECOMMENDED)

Use the Task tool to spawn separate agents for each phase. This ensures fresh context and prevents shortcuts.

```
ORCHESTRATOR (you)
    │
    ├──► Task: "Phase 1 Research for [page-name]"
    │    subagent_type: "general-purpose"
    │    prompt: [Include Phase 1 instructions below + page URL]
    │    → WAIT for completion
    │    → VALIDATE: bash scripts/validate-phase.sh 1 [page-name]
    │
    ├──► Task: "Phase 2 Writer Brief for [page-name]"
    │    subagent_type: "general-purpose"
    │    prompt: [Include Phase 2 instructions + "Read active/[page]-phase1.json first"]
    │    → WAIT for completion
    │    → VALIDATE: bash scripts/validate-phase.sh 2 [page-name]
    │
    └──► Task: "Phase 3 Technical for [page-name]"
         subagent_type: "general-purpose"
         prompt: [Include Phase 3 instructions + "Read both phase1.json and phase2.json first"]
         → WAIT for completion
         → VALIDATE: bash scripts/validate-phase.sh 3 [page-name]
```

**CRITICAL:** Each agent MUST read and follow the phase instructions below. Copy the relevant phase section into each agent's prompt.

---

## PHASE 0: PRE-FLIGHT (DO THIS FIRST)

### Step 0.1: Extract Page Name
```python
# From URL like /sport/betting/best-apps.htm
page_name = url.split('/')[-1].replace('.htm', '')
# Result: "best-apps"
```

### Step 0.2: Look Up Page in Site Structure
```bash
# Run this MCP tool NOW:
mcp__topendsports-briefs__get_page_info with url="$ARGUMENTS"
```

### Step 0.3: Ahrefs Connectivity

**Desktop NEVER calls Ahrefs MCP tools directly** — they return 403 due to auth environment mismatch.
Use WebSearch (FREE) first for SERP composition, then the Python script for keyword data:

```bash
python3 .claude/scripts/ahrefs-api.py \
  keywords-explorer/overview \
  '{"select":"keyword,volume,difficulty","country":"us","keywords":"YOUR_PRIMARY_KEYWORD"}'
```

**NEVER proceed without working Ahrefs access. NEVER use estimated data.**

---

## PHASE 1: RESEARCH & DISCOVERY (10-15 minutes)

### Step 1.1: Primary Keyword Research
Get volume and difficulty for the primary keyword from site structure.

### Step 1.2: Secondary Keywords (MINIMUM 8, target 15)
**You MUST find 8-15 secondary keywords with REAL volume data.**

Run these Ahrefs queries:

**Related terms:**
```bash
python3 .claude/scripts/ahrefs-api.py keywords-explorer/related-terms \
  '{"select":"keyword,volume,difficulty","country":"us","keywords":"[primary]","limit":20}'
```

**Search suggestions:**
```bash
python3 .claude/scripts/ahrefs-api.py keywords-explorer/search-suggestions \
  '{"select":"keyword,volume,difficulty","country":"us","keywords":"[primary]","limit":15}'
```

**Matching terms:**
```bash
python3 .claude/scripts/ahrefs-api.py keywords-explorer/matching-terms \
  '{"select":"keyword,volume,difficulty","country":"us","terms":"[primary]","limit":20}'
```

### Step 1.2b: SERP Composition Check (FREE — WebSearch)

For the top 3 keyword candidates by volume, run a web search to check who ranks on page 1:
- Classify each result: **affiliate** (gambling.com, casino.org, etc. or title matches "best casino", "top 10", "review"), **brand** (URL has /deposit/, /sign-up/), **editorial** (Wikipedia, Forbes), **government** (.gov), or **other**
- Calculate `affiliate_ratio = affiliate_count / total_results`
- If `affiliate_ratio < 0.3`: keyword is brand-dominated, try a longer-tail variant
- Save results to `serp_composition` in phase1-research.json

### Step 1.2c: Competitor Page Keywords (Ahrefs — MODERATE)

From the SERP check, take the top 3 **affiliate** pages. Get their organic keywords:
```
mcp__claude_ai_Ahrefs__site-explorer-organic-keywords
  target: "{competitor_page_url}"
  country: "{country_code}"
  date: "2026-02-01"
  select: "keyword,volume,position,traffic"
  limit: 20
  mode: "prefix"
```
Save results to `competitor_pages` in phase1-research.json. These keywords will be injected as secondary keywords in the brief.

### Step 1.3: Competitor Analysis (MANDATORY)
Analyze these 3 affiliate sites (NOT brand sites):
1. actionnetwork.com
2. covers.com
3. thelines.com

For each, run:
```bash
python3 .claude/scripts/ahrefs-api.py site-explorer/organic-keywords \
  '{"select":"keyword,volume,position,traffic","target":"[competitor.com]","date":"2025-12-01","country":"us","where":"keyword_contains_[primary]","limit":30}'
```

### Step 1.4: Identify Content Gaps
From competitor analysis, list:
- Keywords they rank for that TopEndSports doesn't
- H2 sections all 3 competitors have
- Features competitors lack (calculator? filter? tabs?)

### Step 1.5: Brand Selection
- Position #1: FanDuel (LOCKED - commercial deal)
- Position #2: BetMGM (LOCKED - commercial deal)
- Positions #3-7: Research-driven based on:
  - Competitor mentions (3+ = include)
  - Reddit sentiment
  - Document rationale for EACH

### Step 1.6: Create Phase 1 Outputs

**File 1: `active/[page-name]-phase1.json`**
```json
{
  "pageName": "[page-name]",
  "url": "[full url]",
  "primaryKeyword": {
    "keyword": "[keyword]",
    "volume": [number],
    "difficulty": [number]
  },
  "secondaryKeywords": [
    {"keyword": "[kw1]", "volume": [num], "difficulty": [num], "placement": "H2"},
    {"keyword": "[kw2]", "volume": [num], "difficulty": [num], "placement": "H3"},
    // MINIMUM 8 keywords with REAL volume data
  ],
  "competitors": [
    {"domain": "actionnetwork.com", "topKeywords": [...], "gaps": [...]},
    {"domain": "covers.com", "topKeywords": [...], "gaps": [...]},
    {"domain": "thelines.com", "topKeywords": [...], "gaps": [...]}
  ],
  "contentGaps": ["[gap1]", "[gap2]", "[gap3]"],
  "brands": [
    {"position": 1, "name": "FanDuel", "rationale": "Commercial deal - locked"},
    {"position": 2, "name": "BetMGM", "rationale": "Commercial deal - locked"},
    {"position": 3, "name": "[Brand]", "rationale": "[why]"},
    // ... 5-7 total brands
  ],
  "totalVolume": [sum of all keyword volumes]
}
```

**File 2: `output/[page-name]-brief-control-sheet.md`**
Must include:
- Assignment info (writer, priority)
- Primary keyword with volume
- Secondary keyword table (keyword, volume, placement)
- Competitor analysis summary
- Brand selection with rationale
- Content gaps to exploit
- Technical requirements

### Step 1.7: VALIDATE PHASE 1
```bash
bash content-briefs-skill/scripts/validate-phase.sh 1 [page-name]
```

**DO NOT proceed to Phase 2 until validation PASSES.**

---

## PHASE 2: WRITER BRIEF (5-10 minutes)

### Step 2.1: Load Phase 1 Data
Read `active/[page-name]-phase1.json`

### Step 2.2: Build Keyword-Optimized Outline
Map EVERY secondary keyword to a specific section:

| Volume | Placement |
|--------|-----------|
| 500+/mo | H2 section title |
| 200-500/mo | H2 or H3 |
| 100-200/mo | H3 subsection |
| 50-100/mo | FAQ or natural |
| Question format | FAQ |

### Step 2.3: Create FAQs (MINIMUM 7)
Each FAQ must target a keyword:
1. "Is [brand] legal in my state?" ← "[brand] legal"
2. "Do I need a [brand] promo code?" ← "[brand] promo code"
3. "How fast are [brand] withdrawals?" ← "[brand] withdrawal"
4. "Is [brand] better than [competitor]?" ← "[brand] vs [competitor]"
5. "What states is [brand] available in?" ← "[brand] states"
6. "How do I download the [brand] app?" ← "[brand] app download"
7. "What is the [brand] welcome bonus?" ← "[brand] bonus"

### Step 2.4: Source Requirements
**TIER 1 (MUST USE):**
- App Store reviews and ratings
- Google Play reviews
- Reddit (r/sportsbook, r/sportsbetting)
- State .gov gambling commission sites

**TIER 2 (Verification only):**
- Brand official sites for features

**NEVER cite affiliate sites for pros/cons**

### Step 2.5: Intro Format Requirements
- Total: 100-150 words MAX
- Sentence 1: Direct answer with top picks
- Sentence 2: Authority statement
- Then: Affiliate disclosure (50-75 words)
- FORBIDDEN: "Welcome to...", "Looking for...", rhetorical questions

### Step 2.6: Create Phase 2 Outputs

**File 1: `active/[page-name]-phase2.json`**
```json
{
  "outline": [
    {"type": "H2", "title": "[title]", "keyword": "[kw]", "wordCount": 400},
    {"type": "H3", "title": "[title]", "keyword": "[kw]", "wordCount": 200},
    // Full outline
  ],
  "faqs": [
    {"question": "[q1]", "keyword": "[kw]", "volume": [num]},
    // MINIMUM 7 FAQs
  ],
  "sourceRequirements": {
    "tier1": ["App Store", "Google Play", "Reddit"],
    "tier2": ["Brand official sites"]
  },
  "wordCountTarget": [number],
  "internalLinks": ["[url1]", "[url2]", ...12 total]
}
```

**File 2: `output/[page-name]-writer-brief.md`**
Must include:
- Page basics (URL, keyword, volume, word count)
- Secondary keyword optimization table
- Mandatory intro format instructions
- Full content outline with H2/H3 and word counts
- Source requirements by tier
- Brands to feature with rationale
- Optimized FAQs (7+)
- Compliance requirements
- Internal links (12)

### Step 2.7: VALIDATE PHASE 2
```bash
bash content-briefs-skill/scripts/validate-phase.sh 2 [page-name]
```

**DO NOT proceed to Phase 3 until validation PASSES.**

---

## PHASE 3: TECHNICAL IMPLEMENTATION (10-15 minutes)

### Step 3.1: Load Phase 1 + Phase 2 Data
Read both JSON files.

### Step 3.2: Meta Tags (Complete HTML)
```html
<meta name="title" content="[Title - NO dates]">
<meta name="description" content="[160 chars with primary keyword]">
<meta name="keywords" content="[ALL keywords from Phase 1]">
<meta name="author" content="[Writer name]">
```

### Step 3.3: Last Updated Badge (ALWAYS FIRST)
```html
<div style="background: #e8f5e9; padding: 0.75rem 1.25rem; border-left: 4px solid #2e7d32; margin-bottom: 1.5rem; border-radius: 4px;">
  <p style="margin: 0; font-size: 14px; color: #2e7d32;">
    <strong>✓ Last Updated:</strong> December 5, 2025
  </p>
</div>
```

### Step 3.4: Comparison Table (Complete HTML)
Use brands from Phase 1. Include ALL brands, not just top 3.
Table must have: Sportsbook, Best For, Current Bonus, Rating.
**NO placeholders like "..."**

### Step 3.5: Complete T&Cs for ALL Brands
For EACH brand in Phase 1, create complete T&Cs section:
- Exact bonus text
- Eligibility requirements
- How to qualify steps
- Bonus terms
- Eligible states list
- Key distinctions
- Last verified date

**You MUST have T&Cs for ALL 5-7 brands, not just top 3.**

### Step 3.6: Schema Markup (3 required)

**Article Schema:**
```json
{"@context": "https://schema.org", "@type": "Article", ...}
```

**FAQ Schema (use FAQs from Phase 2):**
```json
{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [...]}
```

**Breadcrumb Schema:**
```json
{"@context": "https://schema.org", "@type": "BreadcrumbList", ...}
```

### Step 3.7: Interactive Elements
Based on content gaps from Phase 1, build at least ONE:
- Bonus calculator with working JavaScript
- Sortable/filterable table
- Tabbed interface
- State availability checker

### Step 3.8: Compliance Sections
**Affiliate Disclosure (top):**
```html
<div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem;">
  <p><strong>Disclosure:</strong> We may earn commission... Must be 21+.
  Gambling problem? Call 1-800-522-4700.</p>
</div>
```

**Responsible Gambling (bottom):**
- National Hotline: 1-800-522-4700
- Chat: ncpgambling.org/chat
- Age requirement: 21+ (18+ in MT, NH, RI, WY, DC)

### Step 3.9: Create Phase 3 Output

**File: `output/[page-name]-ai-enhancement.md`**
Must include COMPLETE HTML/CSS/JS for:
- Meta tags
- Last Updated badge
- Comparison table (all brands)
- Quick Answer box
- T&Cs for ALL brands
- Interactive elements with working code
- Schema markup (Article + FAQ + Breadcrumb)
- Compliance sections

**CRITICAL: NO PLACEHOLDERS. Every piece of code must be complete.**

### Step 3.10: VALIDATE PHASE 3
```bash
bash content-briefs-skill/scripts/validate-phase.sh 3 [page-name]
```

---

## FINAL: CONVERT TO DOCX

```bash
# Use MCP tool:
mcp__topendsports-briefs__convert_to_docx with files=["--all"]
```

---

## COMPLETION CHECKLIST

Before reporting completion, verify ALL exist:

- [ ] `active/[page-name]-phase1.json` - Has 8+ keywords with real volume
- [ ] `active/[page-name]-phase2.json` - Has 7+ FAQs
- [ ] `output/[page-name]-brief-control-sheet.md`
- [ ] `output/[page-name]-writer-brief.md`
- [ ] `output/[page-name]-ai-enhancement.md` - No placeholders

**Run final validation:**
```bash
bash content-briefs-skill/scripts/validate-phase.sh all [page-name]
```

---

## WHAT FAILURE LOOKS LIKE

You have FAILED if:
- You created only 1 or 2 files instead of 3
- You skipped Ahrefs research when MCP failed
- You used estimated/guessed keyword volumes
- You have fewer than 8 secondary keywords
- You have fewer than 7 FAQs
- Your AI Enhancement has "..." or "[Insert]" placeholders
- You skipped T&Cs for some brands
- You skipped schema markup
- You didn't run validation scripts

---

## NOW EXECUTE

Start with Phase 0 (pre-flight). Execute EVERY step above in order. Report completion only after ALL validations pass.
