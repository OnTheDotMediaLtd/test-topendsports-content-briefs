# Phase 1: Research Protocol

**Time:** 10-15 minutes
**Output:** Brief Control Sheet (500-700 words)

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
- ✅ actionnetwork.com, covers.com, thelines.com, sportsbookreview.com
- ❌ NOT brand pages (fanduel.com, draftkings.com)

---

## Step 2: Keyword Research

### A. Primary Keyword
Use web search to gather:
- Search volume estimate
- Difficulty level
- Traffic potential
- Top ranking sites

### B. Secondary Keywords (8-15 Required)

**Must Include:**
1. Comparison: "[brand] vs [competitor]"
2. Features: "[brand] bonus", "[brand] app", "[brand] withdrawal"
3. Questions: "is [brand] legal", "do I need [brand] promo code"
4. Location: "[brand] [state]" for state pages

**Volume Thresholds:**
| Volume | Placement |
|--------|-----------|
| 200+/mo | H2 section title |
| 100-200/mo | H3 subsection |
| 50-100/mo | FAQ or natural |
| <50/mo | Natural mentions |

---

## Step 3: Competitor Gap Analysis

For top 3 affiliate competitors, identify:
1. What H2 sections do ALL 3 have?
2. What features do they lack?
3. Approximate word count
4. Number of brands featured

**Gap → Build Mapping:**
| Gap | Build |
|-----|-------|
| No calculator | Interactive calculator |
| Static table | Sortable/filterable table |
| 3 FAQs | 7 FAQs with schema |
| No tabs | Tabbed interface |

---

## Step 4: Brand Selection

### Locked Positions
- #1: FanDuel (always)
- #2: BetMGM (always)

### Research-Driven (#3-7)
**Required for:** "Best X" comparisons, major brand reviews
**Skip for:** How-to guides (use defaults: FanDuel, BetMGM, DraftKings)

**Process:**
1. Check competitor brand frequency (3+ mentions = include)
2. Reddit search: `site:reddit.com/r/sportsbook [keyword] best`
3. Document rationale for each position

---

## Step 5: Internal Links

Identify 12 internal links from site structure:
- Same sport category
- Related bet types
- State pages (if relevant)
- Calculator tools

---

## Output: Brief Control Sheet

```markdown
# BRIEF CONTROL SHEET: [Page Title]

## ASSIGNMENT
- Target Keyword: [from Site Structure]
- Writer: [Lewis/Tom/Gustavo]
- Opportunity: [HIGH/MEDIUM/LOW]
- Template: [1/2/3/4]

## KEYWORD CLUSTER OPTIMIZATION
**Primary:** "[keyword]" (XXX/mo)

**Secondary Keywords:**
- "[keyword 1]" (XXX/mo) → H2: "[title]"
- "[keyword 2]" (XXX/mo) → H3: "[title]"
- "[keyword 3]" (XXX/mo) → FAQ: "[question]"
[...8-15 total]

**Total Volume:** X,XXX/mo
**Increase:** XXX%

## BRAND SELECTION
[Document positions #1-7 with rationale]

## STRATEGIC DIRECTION
- [Gap 1 to exploit]
- [Gap 2 to exploit]
- [Unique angle]

## TECHNICAL REQUIREMENTS
- [ ] [Element from gap analysis]
- [ ] [Element from gap analysis]

## INTERNAL LINKS
1. "[anchor]" → [url]
[...12 total]

## LOGISTICS
- Word Count Target: [based on competitors + 10%]
- Compliance: Standard USA (21+, 1-800-522-4700)
```

---

## Self-Check

- [ ] Used ACTUAL keyword from Site Structure
- [ ] Identified affiliate competitors (not brands)
- [ ] 8-15 secondary keywords mapped
- [ ] Total search volume calculated
- [ ] Brand selection documented
- [ ] Competitor gaps → build requirements
- [ ] 12 internal links listed
- [ ] Under 700 words
