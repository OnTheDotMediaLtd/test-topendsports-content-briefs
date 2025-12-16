# LESSONS LEARNED - OPTIMIZED v3.0

**Purpose:** Critical insights from failures. Use when edge cases arise.
**Token Reduction:** 10,000 → 3,000 words (70% reduction)

---

## 🎯 CORE PRINCIPLE

Balance: **Accuracy** (research facts) + **Completeness** (cover all bases) + **Utility** (actionable info)

**Common Failure:** Rushing research → missing gaps → underweighted weaknesses

---

## 📋 RESEARCH DEPTH BY PAGE TYPE

| Page Type | Tool Calls | Brand Research | Notes |
|-----------|------------|----------------|-------|
| Major Brand Review | 15-20 | Full Step 1B | FanDuel, DraftKings, BetMGM, Caesars, bet365 only |
| Comparison Page | 12-15 | Simplified 1B | Competitor frequency analysis |
| How-To Guide | 8-12 | Skip (defaults) | FanDuel #1, BetMGM #2, DraftKings #3 |
| State Page | 10-15 | State-specific | Only licensed operators |

**Rule:** More tool calls ≠ better automatically. Match depth to importance.

---

## ❌ CRITICAL MISTAKES TO AVOID

### Mistake 1: Insufficient Research Depth
**Problem:** Made 8 tool calls on major page (FanDuel review)
**Should:** 15-20 tool calls for major brands
**Impact:** Missed current issues (app lag, Face ID failures)

**Fix:**
- Major pages: 15+ tool calls minimum
- Competitor analysis: web_fetch all top 3 (read full content)
- User sentiment: 3-5 Reddit searches (different angles)
- Current issues: Search "[brand] problems 2025"

### Mistake 2: Underweighted Major Competitive Gaps
**Problem:** Listed "no loyalty program" as bullet point
**Should:** Dedicated H2 section (300-400 words) if ALL competitors have it
**Impact:** Missed what users care about most

**Fix:**
```
IF 3/3 competitors emphasize topic extensively
→ Brief must match that emphasis

Example: All competitors dedicate 300-400 words to loyalty programs
→ Your brief specifies dedicated section, not bullet
```

### Mistake 3: Conservative Word Count Targets
**Problem:** Target 2,000 words when competitors average 3,200
**Should:** (Competitor avg) + 10%
**Impact:** Less comprehensive than competition

**Fix:** Calculate competitor average → target 10% higher

### Mistake 4: Not Using web_fetch on Competitors
**Problem:** Only web_search to find URLs, never read full content
**Should:** web_fetch top 3 competitors, analyze H2 structure
**Impact:** Missed what they emphasize, their word counts, their gaps

### Mistake 5: Stopping After First Reddit Search
**Problem:** Tried 1 search, hit quota, moved on
**Should:** Try multiple angles; if quota hit, read competitor mentions
**Impact:** Missed user pain points competitors acknowledge

**Alternative when search quota hit:**
- web_fetch competitor pages → see what issues THEY mention
- Look at competitor FAQ sections → reveals common questions
- Check competitor pros/cons → shows acknowledged weaknesses

### Mistake 6: Missing "What ALL Competitors Cover"
**Problem:** Noted features but didn't identify common patterns
**Should:** Create mental matrix: "What do 3/3 emphasize?"
**Impact:** Missed user expectations

**Fix:** After web_fetch, ask:
- What H2 sections appear in ALL 3?
- What word counts for shared topics?
- What do ALL 3 have that subject lacks?

---

## ✅ RESEARCH QUALITY INDICATORS

**Good research means:**

✅ 15+ tool calls for major pages
✅ Identified what ALL 3 competitors emphasize
✅ Found competitive gaps competitors missed
✅ Verified target keyword from Site Structure
✅ Word count matches competitor landscape
✅ Noted current issues (last 3 months)

**Verification:**
- [ ] Made enough tool calls for page type?
- [ ] Read full content of top 3 competitors?
- [ ] Know what ALL competitors emphasize?
- [ ] Calculated competitor average word count?
- [ ] Found subject's #1 strength AND #1 weakness?

---

## 📊 STRATEGIC DIRECTION FRAMEWORK

### Priority Hierarchy

**1. Address What ALL Competitors Cover (Baseline)**
```
Rule: IF 3/3 competitors dedicate significant space
→ Brief must match or exceed

Example: All 3 have 300-400 words on loyalty programs
→ Specify: "Dedicated H2 section, 350 words, compare to DK Dynasty/MGM Rewards"
```

**2. Identify Competitive Gaps (Differentiators)**
```
Rule: What do 0/3 or 1/3 cover that adds value?

Examples:
- Interactive calculators (0/3 have)
- 2025 innovations not yet updated
- Current user issues not acknowledged
- Honest weakness coverage
```

**3. Major Weaknesses (Content-Type Specific)**
```
IF subject lacks what ALL competitors have
→ Dedicated section required

Example: No loyalty program when DK/MGM/Caesars all have
→ H2 section explaining gap, comparing to competitors
```

---

## 🎯 FANDUEL REVIEW CASE STUDY (What I Learned)

**What I Should Have Done:**

### Research Phase
1. ✅ 15-20 tool calls (not 8)
   - 6 competitor analysis (web_fetch top 3 full pages)
   - 5 user sentiment (multiple Reddit angles)
   - 2 verification (bonus, features)

2. ✅ Multiple Reddit searches:
   - "site:reddit.com/r/sportsbook fanduel problems"
   - "site:reddit.com/r/sportsbook fanduel vs draftkings"
   - "site:reddit.com fanduel app issues 2025"

3. ✅ Identify what ALL 3 competitors emphasize:
   - ALL: 300-400 words on loyalty program gap
   - ALL: 400-500 words on mobile app
   - ALL: 400+ words on Same Game Parlays

4. ✅ Set word count to 3,500+ (not 2,000-2,500)
   - Competitors averaged 3,200 words
   - Should target 3,500+ to match/exceed

### Strategic Direction
1. ✅ Specify dedicated H2 for loyalty gap (350w)
   - "Create H2 comparing to DK Dynasty, MGM Rewards, Caesars Rewards"

2. ✅ Specify dedicated H2 for Same Game Parlays (450w)
   - Match competitor emphasis

3. ✅ Note current issues in brief
   - "Address app lag mentioned in 834 reviews (Sept-Oct 2025)"

4. ✅ Include 3-brand comparison table
   - Even for single-brand review
   - Shows competitive context

**What I Got Right:**
- ✅ 2025 innovations (AI chat, Bet Back Token) - competitors missed
- ✅ Interactive calculators adding utility
- ✅ Tabbed interface for organization
- ✅ Specific data points (withdrawal speeds)

---

## 📋 PRE-FLIGHT CHECKLIST (Use Before Delivering)

### Phase 1: Research Validation
- [ ] Made 15+ tool calls for major pages (10+ for supporting)
- [ ] web_fetch on top 3 competitors
- [ ] Tried 3+ Reddit searches (or documented workaround)
- [ ] Identified what ALL 3 competitors emphasize
- [ ] Checked Site Structure for actual keyword
- [ ] Calculated competitor average word count
- [ ] Set word count based on competitor average (not arbitrary)

### Phase 2: Strategic Direction Validation
- [ ] What ALL competitors emphasize → brief matches emphasis
- [ ] Identified subject's unique strengths → brief highlights
- [ ] Identified major weaknesses → brief addresses appropriately
- [ ] IF 3/3 cover extensively → specified dedicated section
- [ ] IF 0/3 cover valuable topic → added as differentiator
- [ ] Word count target matches/exceeds competitors
- [ ] Content type identified (Review/Comparison/How-To/State)

### Phase 3: Content Structure Validation
- [ ] Comparison table specified (reviews/comparisons)
- [ ] Quick answer box placement
- [ ] Dedicated sections for major topics
- [ ] 7+ FAQs planned
- [ ] For reviews: Major competitive gaps → dedicated sections
- [ ] For comparisons: Brand count matches/exceeds competitors
- [ ] Interactive elements based on gaps (not arbitrary)

### Phase 4: Compliance Validation
- [ ] Affiliate disclosure specified
- [ ] Responsible gambling section
- [ ] Age requirements noted
- [ ] Internal links specified (8-12)
- [ ] Correct writer assigned
- [ ] Correct author attribution (Lewis/Tom/Gustavo)

---

## 🆘 WHEN IN DOUBT

### URL Not in Site Structure
→ Apply manual assignment logic
→ Document decision in Brief Control Sheet

### Ahrefs Unavailable
→ Note "Ahrefs unavailable - using web research"
→ Use web_search for estimates
→ Mark data as estimated

### Writer Assignment Unclear
→ Default to Lewis for high-priority
→ Check Spanish rule first (/es/ = Gustavo)
→ Document reasoning

### Brand Selection Unclear
→ Complete competitor frequency analysis
→ Check Reddit for this topic
→ Apply page type decision matrix
→ Document confidence level

### Competitor Gap Unclear
→ Default: Calculator, 7 FAQs, Comparison table
→ These are always improvements

---

## 🔄 CONTINUOUS IMPROVEMENT

**After Each Brief, Self-Assess:**

1. Made 15+ tool calls for major pages?
2. web_fetch all top 3 competitors?
3. Identified what ALL 3 emphasize?
4. Noted subject's major weaknesses?
5. Checked for 2025 innovations?
6. Set word count from competitor average?
7. Specified comparison table?
8. Noted current issues?

**Red Flags:**

🚩 **Brief feels generic** → Didn't read competitors deeply
🚩 **Word count arbitrary** → Didn't calculate competitor average
🚩 **Missing obvious gaps** → Didn't analyze what ALL have/lack
🚩 **Outdated feel** → Didn't check 2025 updates

---

**END OF LESSONS LEARNED v3.0**

*Updated: Condensed 70%. All critical insights preserved. Removed: Verbose examples, redundant explanations, repeated rules.*
