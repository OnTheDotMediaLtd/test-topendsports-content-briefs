# Meta Title & Description Optimization

**Added:** December 16, 2025
**Purpose:** SERP-optimized meta tags using Ahrefs data

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
- Year usage (2025 vs no year)
- Brand mentions

### Step 2: Title Formula Based on SERP Analysis

| Page Type | Formula | Example |
|-----------|---------|---------|
| Comparison | `Best [Topic] [Location] [Year] \| [Count] [Modifier]` | "Best Betting Apps UK 2025 \| 9 Expert-Tested" |
| Review | `[Brand] Review [Year]: [Key Benefit] + [Bonus]` | "Bet442 Review 2025: Fast Payouts + Free Bets" |
| How-To | `How to [Action] in [Location] ([Year] Guide)` | "How to Bet on Football in UK (2025 Guide)" |
| State/Region | `[Topic] in [Location]: [Key Info] [Year]` | "Sports Betting in Ireland: Legal Status & Apps 2025" |

### Step 3: Character Limits

| Element | Limit | Notes |
|---------|-------|-------|
| Title tag | 50-60 chars | Google truncates at ~60 |
| Meta description | 150-160 chars | Google truncates at ~160 |
| OG title | 60-90 chars | Social media display |

**Check before finalizing:** Count characters, ensure no truncation at key info.

---

## Meta Title Requirements

### Must Include:
1. **Primary keyword** - Within first 40 characters
2. **Location/Market** - UK, Ireland, Canada (where applicable)
3. **Year** - 2025 (signals freshness)
4. **Differentiator** - What makes this page unique

### Must Avoid:
1. **Dated language** - Never "December 2025" or "Updated December"
2. **Keyword stuffing** - Natural readability first
3. **Clickbait** - Accuracy over sensationalism
4. **Brand first** - Put keywords before "TopEndSports"

### Power Words That Improve CTR:
- Best, Top, #1, Expert, Tested, Reviewed
- Complete, Ultimate, Definitive, Comprehensive
- Free, Bonus, Exclusive, Official
- [Number] + [Items] (e.g., "9 Best Apps")

---

## Meta Description Requirements

### Formula:
```
[Hook with primary keyword]. [Key benefit/USP]. [Social proof or specifics]. [Soft CTA].
```

### Example:
```
Compare the best UK betting apps for iOS and Android. 9 UKGC-licensed sportsbooks tested with real money. Expert ratings, bonuses, and app store scores.
```

### Must Include:
1. **Primary keyword** - Early in description
2. **Unique value** - Why click THIS result?
3. **Specifics** - Numbers, facts, not vague claims
4. **Implicit CTA** - "Compare", "Find", "Discover"

### Must Avoid:
1. **"Click here"** - Obvious and wastes characters
2. **Repetition** - Don't repeat title exactly
3. **Empty promises** - Only claim what's delivered
4. **Passive voice** - Active verbs perform better

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
| Position | Title | Chars | Year? | Number? |
|----------|-------|-------|-------|---------|
| 1 | [title] | [#] | Y/N | Y/N |
...

**Common Elements:**
- X of 10 include year
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
- Use formula matching page type
- Verify character counts
- Create meta description using formula

---

## Output Template

Add to AI Enhancement Brief:

```html
<!-- Meta Title (XX chars) -->
<title>[Optimized title based on SERP analysis]</title>

<!-- Meta Description (XXX chars) -->
<meta name="description" content="[Description using formula]">

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

- [ ] Primary keyword in title (first 40 chars)
- [ ] Title under 60 characters
- [ ] Year included (2025)
- [ ] Location/market specified
- [ ] Description under 160 characters
- [ ] Description has unique value prop
- [ ] No dated language ("Updated December")
- [ ] SERP competitor analysis documented
- [ ] Differentiator from competitors clear

---

## Examples by Market

### UK Betting Apps
```html
<title>Best Betting Apps UK 2025 | 9 UKGC-Licensed Sportsbooks</title>
<meta name="description" content="Compare top UK betting apps with expert reviews. 9 licensed sportsbooks tested on iOS and Android. App ratings, bonuses, and withdrawal speeds.">
```

### Ireland Free Bets
```html
<title>Free Bets Ireland 2025 | Best Betting Offers Compared</title>
<meta name="description" content="Claim the best free bet offers in Ireland. Compare welcome bonuses from 10 licensed bookmakers. Updated weekly with new promotions.">
```

### Canada Betting Sites
```html
<title>Best Betting Sites Canada 2025 | Top 9 Sportsbooks Rated</title>
<meta name="description" content="Find Canada's best online betting sites. 9 licensed sportsbooks reviewed with bonuses, odds quality, and payment options compared.">
```

---

**Document Version:** 1.0
**Last Updated:** December 2025
