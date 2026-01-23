# REFERENCE LIBRARY v3.0

**Purpose:** Quick lookups during brief generation
**Token Reduction:** 8,000 → 2,500 words (69% reduction)

---

## 🔧 PART 1: AHREFS VERIFIED FIELD NAMES

### Critical Rule
**ALWAYS call `Ahrefs:doc` with `tool="[function-name]"` BEFORE using any Ahrefs function.**

### Common Field Errors

| ❌ WRONG | ✅ CORRECT | Used In |
|----------|-----------|---------|
| backlinks_links | `backlinks` | SERP Overview |
| linked_domains | `refdomains` | SERP Overview |
| referring_domains | `refdomains` | All functions |
| search_volume | `volume` | All functions |
| kw_difficulty | `difficulty` | Keywords Explorer |
| ranking | `best_position` | Site Explorer |
| traffic | `sum_traffic` | Organic Keywords |
| query | `keyword` | All functions |

### Most Common Functions

**keywords-explorer-overview:**
- Required: `country`, `select`, `keywords` (or `keyword_list_id`)
- Common select: `"keyword,volume,difficulty,traffic_potential"`

**serp-overview-serp-overview:**
- Required: `country`, `keyword`, `select`
- Common select: `"position,url,title,traffic,backlinks,refdomains,domain_rating"`
- ⚠️ Use `backlinks` NOT `backlinks_links`

**site-explorer-organic-keywords:**
- Required: `target`, `date`, `select`
- Common select: `"keyword,best_position,best_position_url,volume,sum_traffic"`

---

## 👥 PART 2: WRITER ASSIGNMENTS

### Quick Decision Tree
```
Is it /es/ URL?
├─ YES → Gustavo Cantella (no exceptions)
└─ NO → Check Site Structure
    ├─ Found → Use assigned writer
    └─ Not found → Apply rules:
        ├─ 10K+ searches → Lewis
        ├─ Review/Comparison → Lewis
        ├─ State page → Lewis
        └─ How-to/Supporting → Tom
```

### The Three Writers

**Lewis Humphries** (English - High Priority)
- Reviews, comparisons, state pages
- 10K+ monthly searches
- Conversion-focused

**Tom Goldsmith** (English - Supporting)
- How-to guides, explainers
- <10K monthly searches
- Educational

**Gustavo Cantella** (Spanish - ALL)
- Every /es/ URL
- USA Spanish market
- No exceptions

---

## 🇪🇸 PART 3: SPANISH CONTENT RULES

**Critical: USA Market, NOT Spain**

✅ Correct:
- Target: USA Spanish speakers
- Sportsbooks: FanDuel, DraftKings, BetMGM
- Age: 21+ (NOT 18+)
- Hotline: 1-800-522-4700
- Regulations: USA state-by-state
- Language: "ustedes" (NOT "vosotros")

❌ Wrong:
- Spain market
- Spanish brands
- 18+ age
- Spanish hotlines

---

## 📝 PART 4: INTRO FORMAT

**Mandatory: 100-150 words total (including disclosure)**

**Structure:**
1. Opening (40-50 words)
   - Sentence 1: Direct answer with winners
   - Sentence 2: Authority statement
2. Affiliate disclosure (50-75 words)

**Example:**
```
"The best NFL betting sites are FanDuel, DraftKings, and BetMGM. They offer
the most competitive NFL odds and comprehensive prop markets, verified through
extensive testing.

[Disclosure: We may earn commission...50-75 words...]

We've analyzed 20+ licensed sportsbooks to identify the best options."
```

**Forbidden:**
- ❌ "Welcome to..."
- ❌ "Looking for..."
- ❌ Rhetorical questions
- ❌ Over 150 words

---

## 🏢 PART 5: BRAND INVENTORY (TOP 10)

### Tier 1: Locked Positions

**1. FanDuel** ✅ Tracking available
- Position: Always #1
- URL: [tracking URL from controller]
- Best for: User-friendly, mobile app, overall experience

**2. BetMGM** ✅ Tracking available
- Position: Always #2
- URL: [tracking URL from controller]
- Best for: Market variety, MGM Rewards, parlay builder

### Tier 2: Dynamic Selection (Research-Driven)

**3. DraftKings** ❌ Tracking pending
- Best for: Competitive odds, live betting, props
- Appears in: 90%+ competitor content

**4. Caesars** ❌ Tracking pending
- Best for: Same-game parlays (12-leg leader)
- Use for: Parlay-focused pages

**5. BetRivers** ❌ Tracking pending
- Best for: Tennis, soccer, alternative markets
- Use for: Niche sport pages

**6. bet365** ❌ Tracking pending
- Best for: Live streaming, international sports
- Note: Limited US presence - verify state availability

**7. ESPN BET** ❌ Tracking pending
- Best for: ESPN integration, casual bettors
- Use for: Beginner content

**8. Fanatics** ❌ Tracking pending
- Best for: Rewards, merchandise crossover
- Use for: New markets, younger demographic

**9. PointsBet** ❌ Tracking pending
- Best for: PointsBetting (unique bet type)
- Use for: Innovative betting features

**10. Unibet** ❌ Tracking pending
- Best for: Kambi platform, soccer
- Use for: Soccer/international sports

### Regional Operators (State Pages Only)
- Borgata (NJ), BetParx (PA), SugarHouse (PA/NJ)
- TwinSpires (horse racing), Hard Rock Bet, Golden Nugget

**⚠️ Defunct:** FOX Bet - DO NOT USE

---

## ✅ PART 6: COMPLIANCE CHECKLIST

### Every Page Must Include
- [ ] Age: 21+ mentioned
- [ ] Hotline: 1-800-522-4700
- [ ] Affiliate disclosure (top)
- [ ] State availability disclaimer
- [ ] Risk warnings ("Gambling involves risk")
- [ ] Bonus T&Cs (if applicable)

### Forbidden Language
❌ Never use: "Guaranteed wins", "Can't lose", "Risk-free", "Beat the house", "Sure thing", "Lock"

---

## 📋 PART 7: CONTENT TYPE QUICK REFERENCE

| Type | Writer | Word Count | T&Cs |
|------|--------|------------|------|
| Sportsbook Review | Lewis/Tom | 3,500-4,000 | Complete (1) |
| Comparison ("Best X") | Lewis | 2,500-3,500 | Complete (ALL) |
| State Page | Lewis | 2,000-2,800 | Complete (State) |
| How-To Guide | Tom | 1,500-2,500 | Brief (if any) |

---

## 🎨 PART 8: HTML QUICK TEMPLATES

### Affiliate Link
```html
<a href="[TRACKING_URL]" target="_blank" rel="nofollow noopener">
  Visit [Brand] →
</a>
```

### Compliance Box
```html
<div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem;">
  <p style="margin: 0; font-size: 14px;">
    <strong>[Title]:</strong> [Message]
  </p>
</div>
```

### Quick Answer Box
```html
<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left: 4px solid #2e7d32; padding: 1.5rem; margin: 2rem 0; border-radius: 8px;">
  <h2 style="color: #2e7d32; margin-top: 0;">Quick Answer</h2>
  <p style="font-size: 1.1rem;">[Answer]</p>
</div>
```

---

## 🔍 PART 9: COMMON LOOKUPS

### Age Requirements by State
- **21+:** Most states (AZ, CO, CT, IL, IN, IA, KS, KY, LA, MA, MD, MI, NV, NJ, NY, OH, PA, TN, VA, WV)
- **18+:** MT, NH, RI, WY, DC

### Popular Keywords by Type
- **Review:** "[brand] review", "[brand] sportsbook", "[brand] bonus"
- **Comparison:** "best", "top", "vs", "comparison"
- **State:** "[state] betting", "legal in [state]"
- **How-to:** "how to", "guide", "tutorial", "beginner"

### Internal Link Anchors (Common)
- "parlay calculator", "odds calculator"
- "NFL betting guide", "NBA betting tips"
- "legal sports betting states"
- "best sportsbook bonuses"

---

## 🆘 PART 10: TROUBLESHOOTING

**Ahrefs returns error:**
1. Did you call `Ahrefs:doc` first?
2. Check field names in this reference
3. Try once more with corrected names
4. If still fails → use `web_search` fallback

**URL not in Site Structure:**
→ Proceed with manual writer assignment
→ Use decision tree
→ Document reasoning

**Competitor analysis confusing:**
→ For "best X": Review sites only
→ Ignore brand landing pages
→ Focus on affiliate competitors

**Intro too long:**
→ Count total (including disclosure)
→ Must be 100-150 words max
→ Cut unnecessary details

---

## 📊 PART 11: METRICS USAGE

### Use Internally (Decisions)
- Traffic potential → Determines opportunity level
- Keyword difficulty → Identifies quick wins
- Competitor traffic → Finds gaps

### Don't Output in Briefs
❌ KD scores (45, 38, 52)
❌ Domain Rating (78, 71)
❌ Traffic potential (63K/mo)
❌ Monthly volume (12.4K/mo)

### Instead Say
✅ "HIGH opportunity" (not KD 45)
✅ "Strong competitor" (not DR 78)
✅ "Significant traffic" (not 63K/mo)

---

## 🎯 PART 12: SOURCE HIERARCHY (Quick Reference)

**TIER 1 (Primary):** Real users
- App Store, Google Play, Reddit, Trustpilot

**TIER 2 (Verification):** Official sources
- Brand websites, state gaming commissions

**TIER 3 (Facts):** Industry sources
- Market data, revenue reports

**TIER 4 (Sparingly):** Affiliate sites
- ❌ NEVER cite for pros/cons
- ✅ Only for research gaps

---

## 📅 PART 13: DATING LANGUAGE RULES

### NEVER in Titles/H1s
❌ "October 2025", "Review 2025", "Best Sites 2025"

### USE Instead
✅ "Comprehensive Review", "The #1 Rated App", "Best [X] Sites"

### WHERE Dates OK
✅ "Last Updated" badge (after H1)
✅ Schema `dateModified`
✅ T&Cs verification ("Last Verified: [date]")
✅ Within content ("As of October 2025...")

---

## 📋 PART 14: T&Cs BY TEMPLATE

| Template | Required | Version |
|----------|----------|---------|
| 1 (Review) | ✅ YES | Complete (1 brand) |
| 2 (Comparison) | ✅ YES | Complete (ALL) |
| 3 (How-To) | ⚠️ CONDITIONAL | Brief (if bonuses) |
| 4 (State) | ✅ YES | Complete (State ops) |

**Brief T&Cs:**
`*21+ only. New customers. T&Cs apply. See details below.`

**Complete T&Cs:**
Full HTML template with all legal language (see Verification Standards)

---

## 🔄 CROSS-REFERENCE GUIDE

**During Phase 1:**
- This document: Ahrefs fields, quick lookups
- Phase 1 Protocol: Step-by-step process
- Lessons Learned: Best practices

**During Phase 2:**
- This document: Writers, intro format, brands
- Phase 2 Protocol: Brief structure
- Content Type Templates: Complete structures

**During Phase 3:**
- This document: HTML templates, compliance
- Phase 3 Protocol: Build instructions
- Verification Standards: Complete T&Cs template

---

**END OF REFERENCE LIBRARY v3.0**

*Condensed 69%. All critical data preserved. Removed: Verbose explanations, redundant examples, repeated rules.*
