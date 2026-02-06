# PHASE 1: RESEARCH AGENT

**Purpose:** Research and discovery for betting content briefs
**Time:** 10-15 minutes
**Output:** Brief Control Sheet (500-700 words) + JSON data file

---

## STEP 1: MANDATORY DISCOVERY

### A. Search Site Structure
```bash
# For English URLs
grep -i "[page-name]" data/site-structure-english.csv

# For Spanish /es/ URLs
grep -i "[page-name]" data/site-structure-spanish.csv
```

### B. Extract Critical Info
From the CSV row, extract:
- ✅ Target keyword (from "Target Keywords" column - NOT from URL)
- ✅ Writer assigned (from "Writer" column)
- ✅ Priority level (from "Priority" column)
- ✅ Current status (from "Status" column)
- ✅ Volume (from "Volume" column)

### C. Identify Content Type
Based on URL pattern:
- `/[brand]-review.htm` → Template 1 (Sportsbook Review)
- `/best-[category].htm` → Template 2 (Comparison Page)
- `/how-to-[action].htm` → Template 3 (How-To Guide)
- `/legal-states/[state].htm` → Template 4 (State Page)
- `/es/` prefix → Spanish content (Gustavo assigned)

### D. Identify Competitors
For "best X" keywords, analyze AFFILIATE competitors:
- ✅ Analyze: actionnetwork.com, covers.com, thelines.com, sportsbookreview.com
- ❌ DON'T analyze: Brand pages (fanduel.com, draftkings.com)

---

## STEP 2: KEYWORD RESEARCH

### A. Primary Keyword Analysis
Use web search to gather:
- Search volume estimate
- Keyword difficulty level
- Traffic potential
- SERP landscape (who ranks)

### B. Secondary Keyword Research (CRITICAL - 8-15 keywords)

**Must Include:**
1. **Comparison keywords:** "[brand] vs [competitor]"
2. **Feature keywords:** "[brand] bonus", "[brand] app", "[brand] withdrawal"
3. **Question keywords:** "is [brand] legal", "do I need [brand] promo code"
4. **Location keywords:** "[brand] [state]" (for state pages)

**Volume Thresholds for Mapping:**
- 200+/mo → H2 section title
- 100-200/mo → H3 subsection
- 50-100/mo → FAQ or natural mentions
- <50/mo → Natural mentions only

**Output Format:**
```json
{
  "primary_keyword": "best nfl betting sites",
  "primary_volume": 600,
  "secondary_keywords": [
    {"keyword": "nfl betting apps", "volume": 400, "placement": "H2", "title": "Best NFL Betting Apps"},
    {"keyword": "nfl prop bets sites", "volume": 150, "placement": "H3", "title": "Best Sites for NFL Prop Bets"},
    {"keyword": "is nfl betting legal", "volume": 180, "placement": "FAQ", "question": "Is NFL betting legal in my state?"}
  ],
  "total_volume": 1830,
  "increase_percentage": 205
}
```

---

## STEP 3: COMPETITOR GAP ANALYSIS

### Web Search Competitors
Search: `"best [keyword]" site:actionnetwork.com OR site:covers.com OR site:thelines.com`

### For Each Top 3 Competitor, Note:
1. What H2 sections do ALL 3 have?
2. What features do they lack? (calculators, FAQs, tables)
3. Approximate word count
4. Number of brands featured

### Gap Mapping
For each gap found, specify the build requirement:

| Competitor Gap | Build Requirement |
|----------------|-------------------|
| No calculator | → Build interactive calculator |
| Static table | → Build sortable/filterable table |
| 3 FAQs only | → Build 7 FAQs with schema |
| No tabs | → Build tabbed interface |

---

## STEP 4: BRAND SELECTION (If Comparison/Review Page)

### Locked Positions
- Position #1: FanDuel (always - tracking available)
- Position #2: BetMGM (always - tracking available)

### Research-Driven Positions (#3-7)
**Only required for:**
- "Best X" comparison pages
- Major brand reviews (FanDuel, DraftKings, BetMGM, Caesars, bet365)

**Skip (use defaults) for:**
- How-to guides
- Explainer articles
→ Defaults: FanDuel #1, BetMGM #2, DraftKings #3

### Research Process (When Required)
1. Check which brands top competitors feature (3+ mentions = include)
2. Reddit search: `site:reddit.com/r/sportsbook [keyword] best`
3. Note brands with specific strengths for this topic

### Document Selection
```json
{
  "brand_selection": {
    "locked": [
      {"position": 1, "brand": "FanDuel", "usp": "Best mobile app, user experience"},
      {"position": 2, "brand": "BetMGM", "usp": "Best market variety, MGM Rewards"}
    ],
    "research_driven": [
      {"position": 3, "brand": "DraftKings", "reason": "5/5 competitors feature, strong live betting"},
      {"position": 4, "brand": "Caesars", "reason": "12-leg SGP leader, mentioned in 15 Reddit threads"}
    ],
    "excluded": [
      {"brand": "BetRivers", "reason": "Only 1/5 competitors, no clear advantage for this topic"}
    ]
  }
}
```

---

## STEP 5: BONUS VERIFICATION

### For Each Featured Brand:
1. Search for current bonus on official site
2. Note exact offer text
3. Note key T&Cs (wagering, expiration)
4. Document verification date

**Source Priority:**
- ✅ Official promo page (sportsbook.fanduel.com/promos)
- ❌ Never use affiliate sites for bonus info

---

## STEP 6: INTERNAL LINKS

### Identify 12 Internal Links
Search the site structure CSVs for related pages:
- Same sport category
- Related bet types
- State pages (if relevant)
- Calculator tools

**Format:**
```json
{
  "internal_links": [
    {"anchor": "parlay calculator", "url": "/sport/betting-tools/parlay-calculator.htm"},
    {"anchor": "NFL betting guide", "url": "/sport/betting/nfl-betting-sites.htm"}
  ]
}
```

---

## OUTPUT: BRIEF CONTROL SHEET

Save two files:

### 1. JSON Data File: `active/[page-name]-phase1.json`
```json
{
  "url": "/sport/betting/nfl-betting-sites.htm",
  "page_name": "Best NFL Betting Sites",
  "target_keyword": "best nfl betting sites",
  "writer": "Lewis Humphries",
  "priority": "High",
  "template": "Template 2 - Comparison",
  "keyword_cluster": {
    "primary": {"keyword": "best nfl betting sites", "volume": 600},
    "secondary": [...],
    "total_volume": 1830,
    "increase_percentage": 205
  },
  "brand_selection": {...},
  "competitor_gaps": [...],
  "internal_links": [...],
  "strategic_direction": "...",
  "word_count_target": 2800
}
```

### 2. Markdown Brief: `output/[page-name]-brief-control-sheet.md`

```markdown
# BRIEF CONTROL SHEET: [Page Title]

## ASSIGNMENT
- Target Keyword: [from Site Structure]
- Writer: [Lewis/Tom/Gustavo]
- Opportunity: [HIGH/MEDIUM/LOW]
- Reason: [1 sentence]

---

## KEYWORD CLUSTER OPTIMIZATION

**Primary Keyword:** "[keyword]" (XXX/mo)

**Secondary Keywords (Mapped to Sections):**
- "[keyword 1]" (XXX/mo) → H2: "[Exact title]"
- "[keyword 2]" (XXX/mo) → H3: "[Exact title]"
- "[keyword 3]" (XXX/mo) → FAQ: "[Exact question]"
[...continue for all 8-15 keywords]

**Total Search Volume:** X,XXX/mo
**Increase over primary alone:** XXX%

---

## BRAND SELECTION STRATEGY
[If research done, document rationale]
[If using defaults, state: "Using defaults: FanDuel #1, BetMGM #2, DraftKings #3"]

---

## STRATEGIC DIRECTION FOR WRITER
**Content Focus:**
- [Gap 1 to exploit]
- [Gap 2 to exploit]
- [Gap 3 to exploit]

**Unique Angle:** [1 sentence vs competitors]

**Word Count Target:** [Based on competitor average + 10%]

---

## TECHNICAL REQUIREMENTS FOR AI ENHANCEMENT
**Required Interactive Elements:**
- [ ] [Element 1 based on competitor gap]
- [ ] [Element 2 based on competitor gap]
- [ ] [Element 3 based on competitor gap]

**Schema Opportunities:**
- [ ] FAQ schema (7 questions optimized for keywords)
- [ ] Article schema (always)
- [ ] Breadcrumb schema (always)

---

## LOGISTICS
**Internal Links:** [12 listed with anchors]
**Bonuses Verified:** [YES/NO] - [Date]
**Compliance:** Standard USA (21+, 1-800-522-4700, T&Cs)
```

---

## SELF-CHECK BEFORE COMPLETING

- [ ] Used ACTUAL keyword from Site Structure
- [ ] Identified affiliate competitors (not brands)
- [ ] Identified 8-15 secondary keywords
- [ ] Mapped each keyword to section (H2/H3/FAQ)
- [ ] Calculated total search volume
- [ ] Completed brand selection (or documented defaults)
- [ ] Listed competitor gaps with build requirements
- [ ] Listed 12 internal links
- [ ] Brief Control Sheet under 700 words
- [ ] Saved JSON to `active/`
- [ ] Saved markdown to `output/`

---

## COMPLETION MESSAGE

After saving both files, output:
```
Phase 1 complete. Brief Control Sheet delivered.
- Keyword cluster targeting X,XXX monthly searches (XXX% increase)
- Template: [Template type]
- Writer: [Name]
- JSON saved to: active/[page-name]-phase1.json
- Brief saved to: output/[page-name]-brief-control-sheet.md

Ready for Phase 2.
```
