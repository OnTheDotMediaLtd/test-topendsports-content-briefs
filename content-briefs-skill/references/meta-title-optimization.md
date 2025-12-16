# Meta Title & Description Optimization

**Added:** December 16, 2025
**Purpose:** SERP-optimized meta tags using Ahrefs data

---

## Critical Rules

| Element | Requirement |
|---------|-------------|
| **Title** | < 60 chars, primary keyword at START, **NO YEAR** |
| **Description** | < 155 chars |

**Why NO YEAR?** Years in titles cause content to appear outdated when the year changes. Use the "Last Updated" badge in page content instead for freshness signals.

---

## Why This Matters

Meta titles and descriptions directly impact:
- **Click-through rate (CTR)** from search results
- **Ranking signals** (Google uses engagement metrics)
- **User expectations** before clicking

Generic titles = Low CTR = Lower rankings over time.

---

## MANDATORY Process: SERP-First Meta Optimization

### Step 1: Analyze Competitor Titles via SERP Overview

```bash
# Get top 10 ranking titles for your target keyword
python3 .claude/scripts/ahrefs-api.py serp-overview/serp-overview \
  '{"select":"position,title,url,traffic","country":"gb","keyword":"YOUR_KEYWORD","top_positions":10}'
```

**What to extract:**
- Title patterns (what words appear in 5+ of top 10?)
- Character lengths that rank well
- Power words used (Best, Top, #1, Guide, etc.)
- How competitors start their titles (keyword placement)
- SERP features present (Featured Snippets, PAA)

### Step 2: Title Formula Based on SERP Analysis

| Page Type | Formula | Example |
|-----------|---------|---------|
| Comparison | `[Primary Keyword] \| [Count] [Modifier]` | "Best Betting Apps UK \| 9 Expert-Tested Sportsbooks" |
| Review | `[Brand] Review: [Key Benefit] + [Bonus Info]` | "Bet442 Review: Fast Payouts + Welcome Bonus" |
| How-To | `How to [Action] in [Location] \| [Benefit]` | "How to Bet on Football in UK \| Complete Guide" |
| Hub/State | `[Primary Keyword]: [Key Info]` | "Sports Betting in Ireland: Laws & Best Sites" |

**Key Rule:** Primary keyword MUST be at the START of the title.

### Step 3: Character Limits

| Element | Limit | Notes |
|---------|-------|-------|
| Title tag | < 60 chars | Primary keyword at start |
| Meta description | < 155 chars | Google truncates around 155 |
| OG title | 60-90 chars | Social media display |

**Check before finalizing:** Count characters, ensure no truncation at key info.

---

## Meta Title Requirements

### Must Include:
1. **Primary keyword** - At the START of the title
2. **Location/Market** - UK, Ireland, Canada (where applicable)
3. **Differentiator** - What makes this page unique (count, modifier)

### Must Avoid:
1. **Year in title** - NO "2025" or any year
2. **Dated language** - Never "December 2025" or "Updated December"
3. **Keyword stuffing** - Natural readability first
4. **Clickbait** - Accuracy over sensationalism
5. **Brand first** - Put keywords before "TopEndSports"

### Power Words That Improve CTR:
- Best, Top, #1, Expert, Tested, Reviewed
- Complete, Ultimate, Definitive, Comprehensive
- Free, Bonus, Exclusive, Official
- [Number] + [Items] (e.g., "9 Best Apps")

---

## Meta Description Requirements

### Formula:
```
[Hook with primary keyword]. [Key benefit/USP]. [Social proof or specifics].
```

### Example (154 chars):
```
Compare the best UK betting apps for iOS and Android. 9 UKGC-licensed sportsbooks tested. Expert ratings, bonuses, and app store scores compared.
```

### Must Include:
1. **Primary keyword** - Early in description
2. **Unique value** - Why click THIS result?
3. **Specifics** - Numbers, facts, not vague claims

### Must Avoid:
1. **"Click here"** - Obvious and wastes characters
2. **Repetition** - Don't repeat title exactly
3. **Empty promises** - Only claim what's delivered
4. **Years** - Same rule as titles - no years

---

## Ahrefs SERP Analysis Commands

### Get Competitor Titles
```bash
python3 .claude/scripts/ahrefs-api.py serp-overview/serp-overview \
  '{"select":"position,title,url,traffic","country":"[COUNTRY_CODE]","keyword":"[KEYWORD]","top_positions":10}'
```

Country codes:
- `us` - United States
- `gb` - United Kingdom
- `ie` - Ireland
- `ca` - Canada

### Analyze Title Patterns
After getting SERP data, document:

```markdown
## SERP Title Analysis: [Keyword]

**Top 10 Title Patterns:**
| Position | Title | Chars | Keyword at Start? |
|----------|-------|-------|-------------------|
| 1 | [title] | [#] | Y/N |
...

**Common Elements:**
- X of 10 start with primary keyword
- X of 10 include numbers
- Average length: XX chars
- Power words: [list]

**Our Differentiation:**
- [What we can add that's missing]
```

---

## Phase Integration

### Phase 1 (Research):
- Run SERP overview for primary keyword
- Document competitor title patterns
- Note gaps/opportunities in competitor titles

### Phase 3 (Technical):
- Apply SERP insights to title creation
- Ensure primary keyword is at START
- Verify character counts (title < 60, description < 155)
- Create meta description using formula

---

## Output Template

Add to AI Enhancement Brief:

```html
<!-- Meta Title (XX chars) - NO YEAR, keyword at start -->
<title>[Primary Keyword] | [Differentiator]</title>

<!-- Meta Description (XXX chars) - under 155 -->
<meta name="description" content="[Description using formula - max 155 chars]">

<!-- SERP Analysis Notes -->
<!--
  Competitor pattern: [what top 10 do]
  Our differentiation: [what we added]
  CTR optimization: [power words used]
-->
```

---

## Quality Checklist

Before finalizing meta tags:

- [ ] Primary keyword at START of title
- [ ] Title under 60 characters
- [ ] **NO YEAR in title**
- [ ] Location/market specified
- [ ] Description under 155 characters
- [ ] Description has unique value prop
- [ ] No dated language anywhere
- [ ] SERP competitor analysis documented
- [ ] Differentiator from competitors clear

---

## Examples by Market

### UK Betting Apps
```html
<title>Best Betting Apps UK | 9 UKGC-Licensed Sportsbooks Tested</title>
<meta name="description" content="Compare the best UK betting apps for iOS and Android. 9 licensed sportsbooks tested with expert ratings, bonuses, and withdrawal speeds.">
```
- Title: 54 chars ✓
- Description: 147 chars ✓
- Keyword "Best Betting Apps UK" at start ✓
- No year ✓

### Ireland Free Bets
```html
<title>Free Bets Ireland | Best Betting Offers Compared</title>
<meta name="description" content="Claim the best free bet offers in Ireland. Compare welcome bonuses from 10 licensed bookmakers with no wagering requirements.">
```
- Title: 49 chars ✓
- Description: 130 chars ✓
- Keyword "Free Bets Ireland" at start ✓
- No year ✓

### Canada Betting Sites
```html
<title>Best Betting Sites Canada | Top 9 Sportsbooks Rated</title>
<meta name="description" content="Find Canada's best online betting sites. 9 licensed sportsbooks reviewed with bonuses, odds quality, and payment options.">
```
- Title: 52 chars ✓
- Description: 127 chars ✓
- Keyword "Best Betting Sites Canada" at start ✓
- No year ✓

---

## Direct Answer Alignment

The first ~50 words after your H1 must directly answer the search query. This content feeds:
- Featured snippets
- AI Overviews
- Voice search results

Your title should align with this immediate answer, creating consistency across SERP features.

---

**Document Version:** 2.0
**Last Updated:** December 2025
