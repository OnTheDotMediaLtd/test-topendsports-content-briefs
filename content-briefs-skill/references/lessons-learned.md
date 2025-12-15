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

🚩 **File count doesn't match expected** → Silent phase failure in batch

🚩 **Phase 3 took >5 min without output** → Likely token limit exceeded

🚩 **File names don't match pattern** → Naming inconsistency breaks automation

---

## Batch Generation Learnings

**Added:** December 15, 2025 (44-brief batch for UK, Ireland, Canada)

### Lesson 1: File Naming Must Be Deterministic

**Problem:** Inconsistent naming between phases breaks automation.

**Root Cause:** Phase 3 used dynamic name construction instead of inheriting from Phase 1.

**Example of Problem:**
```
✗ Phase 1: ireland-wonder-luck-review-phase1.json
✗ Phase 2: ireland-wonder-luck-review-phase2.json
✗ Phase 3: ireland-wonder-luck-sportsbook-review-ai-enhancement.md  ← MISMATCH
```

**Rule:** Establish base name in Phase 1, use EXACT same base across all phases:
```
✓ ireland-wonder-luck-review-phase1.json
✓ ireland-wonder-luck-review-phase2.json
✓ ireland-wonder-luck-review-ai-enhancement.md
```

### Lesson 2: Silent Failures in Batch Processing

**Problem:** UK 22bet Phase 3 was skipped without error notification.

**Impact:** Incomplete deliverables discovered only during manual audit.

**Solution:** After each batch wave, verify expected file count:
```
expected_files=5  # phase1.json, phase2.json, 3x markdown
actual_files=$(ls ${page_name}* | wc -l)
if [ $actual_files -ne $expected_files ]; then HALT fi
```

### Lesson 3: Token Limits in Phase 3

**Problem:** Large briefs (7+ brands, 12+ keywords) can exceed token limits.

**Trigger Conditions:**
- 7+ brands in comparison
- 12+ secondary keywords
- Comprehensive T&Cs for all brands

**Proactive Detection:** If brands ≥ 7 OR (brands ≥ 5 AND keywords ≥ 12) → use Haiku model

### Lesson 4: Writer Briefs Must Not Include Phase 3 Tasks

**Problem:** Some writer briefs asked writers to create "mobile-responsive" or "sortable" tables.

**Rule:** Writer briefs should:
- ✓ Describe WHAT content goes in the table
- ✓ Specify data accuracy requirements
- ✓ Note that "Phase 3 will handle formatting/interactivity"
- ✗ Never mention CSS, responsive design, JavaScript functionality

### Lesson 5: Ahrefs MCP Reliability

**Status:** SOLVED - Python fallback is reliable

**Best Practice:** Try MCP first, immediately fallback to Python script on 403:
```bash
python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview '{...}'
```

### Lesson 6: Keyword Cannibalization Prevention
**Added:** December 15, 2025

**Problem:** Hub pages were targeting keywords that belonged to dedicated pages (e.g., uk-betting-hub targeting "betting apps" when uk-betting-apps page exists).

**Impact:** Multiple pages competing for same keywords hurts SEO rankings for all pages.

**Rule:** Each page type owns specific keyword clusters:
- **Hub pages** → Navigation only, link to dedicated pages, NO keyword targeting
- **Betting Apps page** → "betting apps", "mobile betting", "download app"
- **Betting Offers page** → "betting offers", "welcome bonus", "sign up bonus"
- **Free Bets page** → "free bets", "no deposit", "risk-free bet"
- **Football Betting page** → "football betting", "football betting sites"
- **Horse Racing page** → "horse racing betting", "horse racing sites"
- **New Betting Sites page** → "new betting sites", "new bookmakers"
- **Sports Betting Sites page** → "sports betting", "sportsbook"

**Prevention:** Before adding keywords to a brief:
1. Check if keyword belongs to another dedicated page
2. If yes, DO NOT add it - link to that page instead
3. Hub pages should have minimal keywords, mostly navigation

---

## Batch Generation Validation Checklist

- [ ] Established consistent base name for all files
- [ ] Estimated token usage for Phase 3
- [ ] Selected appropriate model (Sonnet vs Haiku based on size)
- [ ] Verified file count after each wave
- [ ] Writer briefs contain NO Phase 3 technical language
- [ ] Quality gate run after generation (lint + placeholder check)

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
