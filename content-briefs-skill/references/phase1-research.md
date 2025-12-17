# Phase 1: Research Protocol

**Time:** 15-20 minutes
**Output:** Brief Control Sheet (600-800 words)

---

## Step 1: Mandatory Discovery

### A. Search Site Structure
```bash
# English URLs
grep -i "[page-name]" assets/data/site-structure-english.csv

# Spanish /es/ URLs
grep -i "[page-name]" assets/data/site-structure-spanish.csv
```

### B. Extract From CSV
- Target keyword (from "Target Keywords" column - NOT from URL)
- Writer assigned
- Priority level
- Volume estimate

### C. Identify Content Type
- `/[brand]-review.htm` → Template 1 (Review)
- `/best-[category].htm` → Template 2 (Comparison)
- `/how-to-[action].htm` → Template 3 (How-To)
- `/legal-states/[state].htm` → Template 4 (State)

### D. Identify Competitors
For "best X" keywords, analyze AFFILIATE sites:
- ✅ actionnetwork.com, covers.com, thelines.com, sportsbookreview.com, sportshandle.com
- ❌ NOT brand pages (fanduel.com, draftkings.com)

---

## Step 1.5: Page Type Identification (CRITICAL)

**Reference:** `references/hub-page-strategy.md`

Before keyword research, identify the page type:

| Page Type | URL Pattern | Keyword Strategy |
|-----------|-------------|------------------|
| **Hub Page** | `/[market]/index.htm` | Broad market keywords, legal info, how-to. See hub-page-strategy.md |
| **Comparison Page** | `/best-[category].htm`, `/[category]-apps.htm` | Specific category keywords, full depth |
| **Review Page** | `/[brand]-review.htm` | Brand-specific keywords only |
| **How-To Page** | `/how-to-[action].htm` | Action-oriented keywords |

### If Hub Page Identified:
1. Reference `references/hub-page-strategy.md` for keyword rules
2. Identify dedicated pages that own specific keyword clusters
3. EXCLUDE keywords belonging to dedicated pages
4. Target word count: ~7,500 (not 9,000+)
5. Ensure dedicated page links in first 500 words

### Dedicated Pages by Market:
| Market | Dedicated Pages |
|--------|-----------------|
| Canada | `/betting-apps.htm`, `/sports-betting-sites.htm`, `/new-betting-sites.htm` |
| UK | `/betting-apps.htm`, `/new-betting-sites.htm`, `/free-bets.htm`, `/betting-offers.htm` |
| Ireland | `/betting-apps.htm`, `/free-bets.htm` |

---

## Step 2: Competitor Content Analysis (NEW - CRITICAL)

**Reference:** `references/competitor-content-analysis.md`

### A. Analyze #1 Ranking Page Structure

For the #1 ranking affiliate page, identify:

1. **Number of brands covered** — You MUST match or exceed this
2. **Sections per brand** — Typically 2-3 (Key Features, Mobile Experience, Pros/Cons)
3. **Word count estimate** — Approximate total words
4. **H2/H3 patterns** — Common content sections
5. **Interactive elements** — Tables, calculators, maps

### B. Calculate Competitive Word Count

```
DON'T GUESS — Calculate based on #1 ranking page:

Example (sports betting apps SERP):
- sportshandle.com (#1): ~8,000-9,000 words, 10 brands
- legalsportsreport.com: ~9,000+ words
- foxsports.com: ~7,000+ words

YOUR TARGET: Match or exceed #1 ranking page
```

### C. Brand Count Requirements

| Primary Keyword Volume | Minimum Brands | Target Brands |
|------------------------|----------------|---------------|
| 10,000+/mo | 8 | 10 |
| 5,000-10,000/mo | 7 | 8 |
| 1,000-5,000/mo | 5 | 7 |
| <1,000/mo | 5 | 5 |

---

## Step 3: Keyword Research

### A. Primary Keyword
Use Ahrefs (MCP or Python) to get:
- Search volume (REAL data, not estimates)
- Difficulty level
- Traffic potential
- Top ranking sites

### B. Secondary Keywords (8-15 Required)

**Must Include:**
1. Comparison: "[brand] vs [competitor]"
2. Features: "[brand] bonus", "[brand] app", "[brand] withdrawal"
3. Questions: "is [brand] legal", "do I need [brand] promo code"
4. Location: "[brand] [state]" for state pages
5. **Branded app keywords:** "[brand] sportsbook app" (high volume)

**Volume Thresholds:**
| Volume | Placement |
|--------|-----------|
| 500+/mo | H2 section title |
| 200-500/mo | H2 or H3 |
| 100-200/mo | H3 subsection |
| 50-100/mo | FAQ or natural |
| <50/mo | Natural mentions |

### C. Branded Keywords (NEW)

For comparison pages, MUST include high-volume branded keywords:

| Keyword Pattern | Example | Typical Volume |
|-----------------|---------|----------------|
| [brand] app | bet365 app | 59,000/mo |
| [brand] sportsbook app | fanduel sportsbook app | 2,600/mo |

Each brand section should target its branded keyword.

---

## Step 4: Competitor Gap Analysis

For top 3 affiliate competitors, identify:
1. What H2 sections do ALL 3 have?
2. What features do they lack?
3. Approximate word count
4. Number of brands featured
5. **Per-brand section depth** (how many sections per brand?)

**Gap → Build Mapping:**
| Gap | Build |
|-----|-------|
| No calculator | Interactive calculator + links to existing calculators |
| Static table | Sortable/filterable table |
| 3 FAQs | 10 FAQs with schema |
| No tabs | Tabbed interface |
| No payment methods | Payment methods comparison section |
| 5 brands | 10 brands with deeper analysis |

---

## Step 5: Brand Selection

### Locked Positions
- #1: FanDuel (always)
- #2: BetMGM (always)

### Research-Driven (#3-10)

**For high-volume keywords (10K+/mo):**
Select 8-10 brands total. Consider:

| Brand | Badge | Notes |
|-------|-------|-------|
| Bet365 | 365 | Massive app search volume |
| DraftKings | DK | Top 3 operator |
| theScore BET | SCR | Formerly ESPN BET |
| Caesars | CZR | Strong rewards program |
| Fanatics | FAN | Fastest-growing new entrant |
| BetRivers | BRV | RSI operator, growing |
| Hard Rock Bet | HRB | Expanding presence |
| Borgata | BOR | Strong in NJ/PA |

**Process:**
1. Count brands on #1 ranking page — match or exceed
2. Check competitor brand frequency (3+ mentions = include)
3. Reddit search: `site:reddit.com/r/sportsbook [keyword] best`
4. Document rationale for each position

---

## Step 6: Content Sections Checklist

### Mandatory for Comparison Pages

- [ ] Introduction with top 3 picks
- [ ] Comparison table (ALL brands)
- [ ] Individual brand reviews with:
  - [ ] Key Features (150-200 words)
  - [ ] **Mobile Experience** (100-150 words) ← NEW
  - [ ] Pros & Cons with citations (100-150 words)
  - [ ] Current Bonus (75-100 words)
- [ ] FAQs (8-10)
- [ ] Responsible gambling
- [ ] **Payment methods comparison** ← NEW
- [ ] **Calculator tool links** ← NEW

### Sport-Specific (if relevant)
- [ ] NFL app rankings
- [ ] NBA app rankings
- [ ] College sports coverage

---

## Step 7: Internal Links

Identify 12 internal links from site structure:
- Same sport category
- Related bet types
- State pages (if relevant)
- **Calculator tools** (parlay, odds, etc.)
- Individual brand review pages

---

## Output: Brief Control Sheet

```markdown
# BRIEF CONTROL SHEET: [Page Title]

## ASSIGNMENT
- Target Keyword: [from Site Structure]
- Writer: [Lewis/Tom/Gustavo]
- Opportunity: [HIGH/MEDIUM/LOW]
- Template: [1/2/3/4]

## COMPETITOR ANALYSIS (NEW)
**#1 Ranking Page:** [domain.com]
- Brands covered: [X]
- Estimated word count: [X,XXX]
- Key sections: [list]

**Our Target:**
- Brands: [match or exceed #1]
- Word count: [match or exceed #1]

## KEYWORD CLUSTER OPTIMIZATION
**Primary:** "[keyword]" (XXX/mo)

**Secondary Keywords:**
- "[keyword 1]" (XXX/mo) → H2: "[title]"
- "[keyword 2]" (XXX/mo) → H3: "[title]"
- "[keyword 3]" (XXX/mo) → FAQ: "[question]"
[...8-15 total]

**Branded Keywords:**
- "[brand] app" (XXX/mo) → [Brand] section
[...per brand]

**Total Volume:** X,XXX/mo
**Increase:** XXX%

## BRAND SELECTION
| Position | Brand | Rationale |
|----------|-------|-----------|
| #1 | FanDuel | Commercial deal (locked) |
| #2 | BetMGM | Commercial deal (locked) |
| #3 | [Brand] | [Why] |
[...8-10 total for high-volume keywords]

## CONTENT SECTIONS
- [ ] Key Features per brand
- [ ] Mobile Experience per brand
- [ ] Pros/Cons per brand
- [ ] Payment methods comparison
- [ ] Calculator links

## STRATEGIC DIRECTION
- [Gap 1 to exploit]
- [Gap 2 to exploit]
- [Unique angle vs competitors]

## TECHNICAL REQUIREMENTS
- [ ] [Element from gap analysis]
- [ ] [Element from gap analysis]

## INTERNAL LINKS
1. "[anchor]" → [url]
[...12 total, including calculator links]

## LOGISTICS
- Word Count Target: [based on #1 competitor]
- Compliance: Standard USA (21+, 1-800-522-4700)
```

---

## Self-Check

- [ ] Analyzed #1 ranking page structure
- [ ] Brand count matches or exceeds #1 page
- [ ] Used ACTUAL keyword from Site Structure
- [ ] Identified affiliate competitors (not brands)
- [ ] 8-15 secondary keywords mapped
- [ ] Branded keywords included per brand
- [ ] Total search volume calculated
- [ ] Brand selection documented (8-10 for high-volume)
- [ ] Competitor gaps → build requirements
- [ ] Mobile Experience section planned per brand
- [ ] Payment methods section planned
- [ ] Calculator links planned
- [ ] 12 internal links listed
- [ ] Word count target based on competitor analysis
