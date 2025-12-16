# Keyword Research Feedback & Pain Points
## Comprehensive Documentation from Claude AI Chats

**Document Version:** 1.0
**Compiled:** December 2025
**Source:** 50+ past conversations
**Purpose:** Document all keyword research issues for AI workflow optimization

---

## CRITICAL PAIN POINTS

### 1. Skipping Keyword Research Entirely

**The Problem:** Claude frequently jumps to content planning without completing mandatory keyword research first.

**User Quote:** "continue but....you skipped keyword research using ahrefs unless this phase will commence now"

**Required Fix:**
```
MANDATORY WORKFLOW ORDER:
1. Look up URL in site structure CSV
2. Get PRIMARY keyword from CSV (not assumed from URL)
3. Run Ahrefs keyword research (primary + secondary)
4. ONLY THEN proceed to competitor analysis
5. ONLY THEN proceed to content planning

CHECKPOINT: Cannot proceed to Phase 2 until keyword research is complete
```

### 2. Sampling Instead of Full Analysis

**The Problem:** When provided with keyword data files, Claude only samples a few keywords instead of analyzing the complete dataset.

**User Quote:** "Kindly have a broad look at the attached keywords and not sampling just a few"

**Required Fix:**
```
KEYWORD DATA PROCESSING RULES:
1. ALWAYS process 100% of provided keyword data
2. If file too large, summarize into categories:
   - High volume (1000+)
   - Medium volume (100-999)
   - Low volume with low difficulty (quick wins)
   - Question keywords (FAQ opportunities)
3. Report total keywords analyzed: "Analyzed X keywords from provided data"
4. NEVER sample - full analysis or request smaller batches
```

### 3. Manual Keyword Mapping Required

**The Problem:** User expected Claude to automatically extract and implement keywords, but Claude required manual instruction for each placement.

**User Quote:** "I would like the AI to do that from the keyword data that I provided it with"

**Required Fix:**
```
AUTOMATIC KEYWORD EXTRACTION:
When keyword data is provided, AI MUST:
1. PARSE the data automatically
2. IDENTIFY opportunities without being told
3. CATEGORIZE into priority tiers
4. IMPLEMENT strategically in content
5. REPORT which keywords were used and where

NO MANUAL MAPPING REQUIRED FROM USER
```

---

## AHREFS INTEGRATION ISSUES

### Wrong Field Names (CRITICAL)

| WRONG | CORRECT | Used In |
|-------|---------|---------|
| backlinks_links | backlinks | SERP Overview |
| linked_domains | refdomains | SERP Overview |
| referring_domains | refdomains | All functions |
| search_volume | volume | All functions |
| kw_difficulty | difficulty | Keywords Explorer |
| ranking | best_position | Site Explorer |
| traffic | sum_traffic | Organic Keywords |
| query | keyword | All functions |

**Required Protocol:**
```
AHREFS API PROTOCOL:
1. ALWAYS call Ahrefs:doc FIRST for any function
2. Copy EXACT field names from documentation
3. Test with minimal parameters before adding filters
4. If error occurs, re-check documentation
5. Report specific error to user if persistent
```

---

## SECONDARY KEYWORD REQUIREMENTS

### Missing Secondary Keyword Cluster

**Example Cluster:**
```
PRIMARY: "fanduel review" - 500 volume
SECONDARY CLUSTER:
- fanduel sportsbook review - 300
- fanduel app review - 200
- is fanduel legit - 400
- fanduel pros and cons - 150
- fanduel bonus review - 100
- fanduel withdrawal review - 80
- fanduel customer service - 120
- fanduel vs draftkings - 600

TOTAL CLUSTER: 2,450 volume (490% increase)
```

### Keyword-to-Section Mapping

```
KEYWORD TO SECTION MAPPING:
High Volume (200+) -> H2 heading
Medium Volume (100-200) -> H3 subheading
Question Keywords -> FAQ section
Long-tail Variants -> Body content / anchor text
Comparison Keywords -> Dedicated comparison section
```

---

## GSC OPPORTUNITY MINING

### Page 2 Keywords (Quick Wins)

**Position-Based Prioritization:**
```
TIER 1 (QUICK WINS): Position 11-20, Volume 100+
TIER 2 (MEDIUM EFFORT): Position 21-30, Volume 200+
TIER 3 (NEW TARGETS): No position, Volume 500+, KD < 30
TIER 4 (LONG-TERM): Position 30+, Volume 1000+
```

### High Impressions / Low CTR

```
GSC OPPORTUNITY FORMULA:
Score = Impressions x (1 - CTR) x (1 / Position)

HIGH PRIORITY:
- Impressions > 1000
- CTR < 3%
- Position 5-20

ACTION: Title tag optimization, meta description rewrite
```

---

## BRANDED VS NON-BRANDED KEYWORDS

### Critical Distinction

**BRANDED (NO AFFILIATE VALUE):**
- "fanduel kentucky" - User already decided on brand
- "draftkings ohio" - User already decided on brand
- "espn bet promo code" - User already decided on brand

**NON-BRANDED (HIGH CONVERSION VALUE):**
- "best sports betting apps" - User comparing options
- "kansas sports betting sites" - User researching market
- "ohio betting promos" - User looking for best deal

**Required Filtering:**
```
REPORT SEPARATELY:
"Found 90 total ranking keywords:
 - 20 non-branded (conversion value) <- FOCUS HERE
 - 70 branded (brand defense only)"
```

---

## HEADING OPTIMIZATION FROM KEYWORDS

### The Problem: Generic Headers

**BAD (Generic):**
```
H2: About This Calculator
H2: How to Use
H2: Results Explained
```

**GOOD (Keyword-Optimized):**
```
H2: Parlay Calculator - Calculate Your Potential Payout
H2: How to Calculate Parlay Odds (Step-by-Step)
H2: Parlay Payout Chart by Number of Legs
```

### Long-Tail Patterns for Headers

**Pattern 1: [Brand] + [Feature]**
- "fanduel bonus" -> "FanDuel Bonus: Current Welcome Offer"

**Pattern 2: [Brand] + [Question Word]**
- "is fanduel legal" -> "Is FanDuel Legal? State-by-State Availability"

**Pattern 3: [Brand] vs [Competitor]**
- "fanduel vs draftkings" -> "FanDuel vs DraftKings: Which is Better?"

**Pattern 4: Best/Top + [Category]**
- "best nfl betting sites" -> "Best NFL Betting Sites: Top Picks Ranked"

---

## COMPETITOR KEYWORD TRAFFIC ANALYSIS (NEW STEP 2C)

### Purpose
Analyze which keywords are driving traffic to competitor pages using `Ahrefs:site-explorer-organic-keywords`

### Process
```
For each top 3 competitor URL:
1. Call site-explorer-organic-keywords
2. Extract keywords with sum_traffic > 0
3. Map high-traffic keywords to H2/H3/FAQ

API Call:
- target: [competitor URL - exact page]
- mode: "exact"
- select: "keyword,best_position,volume,sum_traffic"
- order_by: "sum_traffic:desc"
- limit: 30
```

### Categorization
| Traffic Level | Keyword Type | Action |
|---------------|--------------|--------|
| 100+ traffic/mo | Primary competitor | Must include as secondary |
| 50-100 traffic/mo | Strong opportunity | Map to H2 title |
| 20-50 traffic/mo | Medium opportunity | Map to H3 title |
| 10-20 traffic/mo | Long-tail | Map to FAQ question |

---

## MANDATORY KEYWORD RESEARCH CHECKLIST

```
[ ] Primary keyword confirmed from site structure CSV
[ ] Ahrefs:doc called before each API function
[ ] Primary keyword metrics retrieved (volume, KD, traffic potential)
[ ] Related terms pulled (minimum 15 keywords)
[ ] Matching terms pulled (minimum 20 keywords)
[ ] SERP overview analyzed (top 10 results)
[ ] Competitor keyword traffic analysis done (Step 2C)
[ ] Secondary keyword cluster identified (8-15 keywords)
[ ] Total cluster volume calculated
[ ] Percentage increase calculated (target: 400-900%)
[ ] Keywords mapped to content sections (H2/H3/FAQ)
[ ] Branded vs non-branded classification complete
[ ] GSC opportunities flagged (if data provided)

CANNOT PROCEED TO PHASE 2 UNTIL ALL BOXES CHECKED
```

---

*Last Updated: December 3, 2024*
