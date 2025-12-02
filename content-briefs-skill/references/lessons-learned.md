# Lessons Learned

Critical insights from failures. Reference when edge cases arise.

---

## Feedback System Integration

**This document is continuously updated based on user feedback.**

When users submit feedback via `feedback/FEEDBACK-TEMPLATE.md`, validated issues are added here to prevent future mistakes.

**See**: `feedback/FEEDBACK-PROCESS.md` for how feedback flows into this document

**Recent updates**: Check each entry's date to see what's new

---

## Core Principle

Balance: **Accuracy** + **Completeness** + **Utility**

**Common Failure:** Rushing research → missing gaps → underweighted weaknesses

---

## Research Depth by Page Type

| Page Type | Tool Calls | Brand Research |
|-----------|------------|----------------|
| Major Brand Review | 15-20 | Full Step 1B |
| Comparison Page | 12-15 | Simplified 1B |
| How-To Guide | 8-12 | Skip (defaults) |
| State Page | 10-15 | State-specific |

Major brands requiring deep research: FanDuel, DraftKings, BetMGM, Caesars, bet365

---

## Critical Mistakes to Avoid

### Mistake 1: Insufficient Research Depth
**Problem:** 8 tool calls on major page
**Should:** 15-20 tool calls for major brands
**Impact:** Missed current issues

**Fix:**
- Major pages: 15+ tool calls minimum
- web_fetch all top 3 competitors (read full content)
- 3-5 Reddit searches (different angles)
- Search "[brand] problems 2025"

### Mistake 2: Underweighted Competitive Gaps
**Problem:** Listed "no loyalty program" as bullet point
**Should:** Dedicated H2 section if ALL competitors have it
**Impact:** Missed what users care about

**Fix:**
```
IF 3/3 competitors emphasize topic extensively
→ Brief must match that emphasis
```

### Mistake 3: Conservative Word Counts
**Problem:** Target 2,000 words when competitors average 3,200
**Should:** (Competitor avg) + 10%
**Impact:** Less comprehensive than competition

### Mistake 4: Not Using web_fetch
**Problem:** Only web_search to find URLs, never read content
**Should:** web_fetch top 3 competitors, analyze H2 structure
**Impact:** Missed what they emphasize

### Mistake 5: Single Reddit Search
**Problem:** Tried 1 search, hit quota, moved on
**Should:** Try multiple angles; check competitor mentions

**Alternative when quota hit:**
- web_fetch competitor pages → see issues THEY mention
- Check competitor FAQ sections
- Check competitor pros/cons

### Mistake 6: Missing "What ALL Competitors Cover"
**Problem:** Noted features but not common patterns
**Should:** Create matrix: "What do 3/3 emphasize?"

**After web_fetch, ask:**
- What H2 sections appear in ALL 3?
- What word counts for shared topics?
- What do ALL 3 have that subject lacks?

---

## Research Quality Indicators

Good research means:
- ✅ 15+ tool calls for major pages
- ✅ Identified what ALL 3 competitors emphasize
- ✅ Found gaps competitors missed
- ✅ Verified keyword from Site Structure
- ✅ Word count matches competitor landscape
- ✅ Noted current issues (last 3 months)

---

## Strategic Direction Framework

### Priority Hierarchy

**1. Address What ALL Competitors Cover (Baseline)**
```
IF 3/3 competitors dedicate significant space
→ Brief must match or exceed

Example: All 3 have 300-400 words on loyalty programs
→ Specify dedicated H2 section, 350 words
```

**2. Identify Competitive Gaps (Differentiators)**
```
What do 0/3 or 1/3 cover that adds value?

Examples:
- Interactive calculators (0/3 have)
- 2025 innovations not yet updated
- Current user issues not acknowledged
```

**3. Major Weaknesses (Content-Type Specific)**
```
IF subject lacks what ALL competitors have
→ Dedicated section required

Example: No loyalty program when competitors all have
→ H2 explaining gap, comparing to competitors
```

---

## Pre-Flight Checklist

### Research Validation
- [ ] 15+ tool calls for major pages
- [ ] web_fetch on top 3 competitors
- [ ] 3+ Reddit searches (or workaround)
- [ ] Identified what ALL 3 emphasize
- [ ] Checked Site Structure for keyword
- [ ] Calculated competitor average word count

### Strategic Direction Validation
- [ ] What ALL competitors emphasize → brief matches
- [ ] Unique strengths → brief highlights
- [ ] Major weaknesses → brief addresses
- [ ] IF 3/3 cover extensively → dedicated section
- [ ] IF 0/3 cover valuable topic → added as differentiator

### Content Structure Validation
- [ ] Comparison table specified
- [ ] Quick answer box placement
- [ ] 7+ FAQs planned
- [ ] Interactive elements based on gaps

---

## Red Flags

🚩 **Brief feels generic** → Didn't read competitors deeply

🚩 **Word count arbitrary** → Didn't calculate competitor average

🚩 **Missing obvious gaps** → Didn't analyze what ALL have/lack

🚩 **Outdated feel** → Didn't check 2025 updates

---

## When in Doubt

**URL Not in Site Structure**
→ Apply manual assignment logic
→ Document decision

**Ahrefs Unavailable**
→ Note "using web research"
→ Mark data as estimated

**Writer Assignment Unclear**
→ Default to Lewis for high-priority
→ Check Spanish rule first

**Brand Selection Unclear**
→ Complete competitor frequency analysis
→ Check Reddit for topic
→ Document confidence level

**Competitor Gap Unclear**
→ Default: Calculator, 7 FAQs, Comparison table
→ These are always improvements
