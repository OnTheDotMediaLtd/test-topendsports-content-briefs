# TES Content Brief Generator - Pain Points & Feedback
## Comprehensive Documentation from Project Conversations

**Last Updated:** December 3, 2024
**Purpose:** Document all friction, pain points, and solutions from TES project usage

---

## 1. TOKEN/RESOURCE EXHAUSTION ISSUES

### Primary Problem
**Issue:** Workflow consistently ran out of resources before completing Phase 2, never reaching Phase 3

**User Quote:** "This project is running out of resources before we complete the 2nd phase"
**User Quote:** "the cycle was completed over 2 chats and not one. Are we playing idiot savant now?"

### Root Causes
1. **Documentation Too Verbose:** Content Type Templates ~15,000 words (~19,500 tokens)
2. **Over-Researching:** Checking 10 competitors instead of 3
3. **Verbose Data Passing:** Complete T&Cs passed through all 3 phases

### Solutions Implemented
- 87% token reduction (190,000 -> 25,000 tokens)
- Hard limits on competitor research (max 3 web_fetch)
- Research depth scaling based on page type

### Rules for Claude Code
```
RESOURCE MANAGEMENT:
1. Set hard limits on tool calls per phase
   - Major brand reviews: 15-20 max
   - Comparison pages: 12-15 max
   - How-to guides: 8-12 max
2. STOP after 3 competitor web_fetch calls
3. Don't load all documents upfront - load as needed
4. Track token usage, warn at 50%, 75%, 90%
5. Create resume points after each phase
```

---

## 2. AHREFS API PROBLEMS

### Ahrefs Being Skipped
**Issue:** Workflow assumed Ahrefs was not available and skipped it entirely
**Root Cause:** Instruction said "If Ahrefs Available" - made it optional

**Fix:** Make Ahrefs MANDATORY, not optional

### Wrong Column Being Read
**User Quote:** "I need to ensure you are conducting research based on the 'target keywords' column M"

**Fix:** Read from Column M (Target Keywords) - NEVER from Page Name column

---

## 3. CANNIBALIZATION NOT CHECKED

**User Quote:** "kindly make sure you take cannibalization into consideration. 'compare betting sites' would have cannibalized with the homepage"

**Fix:** Before recommending any keyword, check if it already exists elsewhere in the site structure file

---

## 4. OUTPUT FORMATTING ISSUES

### CSV Paste Failures
**User Quote:** "I copied and pasted into excel and this is the result... Everything got pasted in cell A1"

**Issue:** Commas in URLs broke CSV format

**Solution Found:**
**User Quote:** "It worked!" (after TSV format provided)

**Rule:** ALWAYS use TSV (tab-separated), NEVER CSV with commas

---

## 5. PAGE OPTIMIZATION ISSUES

### Betting Homepage Problems
**User Quote:** "Hey, we worked on the betting homepage and I am not happy with the results. Rob is being used as a betting expert. this is a cardinal sin."

**Problems Found:**
1. Rob Wood incorrectly positioned as "betting expert" (he's sports science)
2. Affiliate links missing (75% potential revenue lost)
3. Quick Answer Box placed BEFORE intro text (should be AFTER)
4. Links to unpublished pages included
5. Missing library codes (GA, tag managers)

### T&Cs Compliance
**User Quote:** "the comparison table should have had the T&C of the bonuses for compliance"

**Fix:** Complete T&Cs required for ALL brands in comparison pages

---

## 6. WORKFLOW & PHASE MANAGEMENT

### Resume State Required
**User Quote:** "We reached chat limits in the previous chat. You had to implement just the last step"

**Required Resume State:**
```
RESUME STATE FOR NEW CHAT:
- Domain Type: [State Hub: STATE NAME] OR [General USA]
- Last completed: [Phase X]
- Document generated: [which one]
- Keyword research complete: [Yes/No]
- Next step: [Phase Y - specific step]
- Key decisions from Phase 1: [List]
```

---

## 7. CONTENT QUALITY ISSUES

### Source Hierarchy Violations
**Issue:** Citing affiliate competitor sites instead of real user feedback

**Correct Priority:**
1. TIER 1: App Store, Google Play, Reddit, Trustpilot
2. TIER 2: Brand official sites (verification only)
3. TIER 3: Industry/regulatory sources
4. TIER 4 (SPARINGLY): Affiliate sites for research gaps only

**Rule:** NEVER cite affiliate sites for pros/cons or user experience

### Dating Language
**Wrong:** "FanDuel Review October 2025"
**Correct:** "FanDuel Sportsbook Review: The #1 Rated Betting App"

### Secondary Keywords Underutilized
**User Quote:** "We worked on these briefs earlier but they had poor usage of secondary keywords throughout. Fix this"

**Result:** Implementing proper secondary keywords increased potential traffic 400-900%

---

## 8. STATE HUB SYSTEM

### Requirements
- Support for 23 states across 27 domains
- Only feature state-licensed operators
- Integrate local teams (NFL, NBA, MLB, NHL, MLS, NCAAF, NCAAB)
- State-specific age requirements (21+ or 18+)

### Solution Delivered
- ONE Master Structure with {state} and {team} variables
- ONE State Config CSV (23 rows)
- Automatic domain detection
- Automatic operator filtering

---

## VERSION HISTORY

| Version | Changes | Token Impact |
|---------|---------|--------------|
| v1.0 | Initial system | ~190,000 tokens |
| v2.0 | Added templates | Same |
| v3.0 | 87% token reduction | ~25,000 tokens |
| v3.1 | Secondary keywords | ~27,000 tokens |

---

## PRIORITY MATRIX FOR IMPLEMENTATION

### P0 - Critical
1. Token/resource management with hard limits
2. Ahrefs API proper field name handling
3. Phase stopping and resume state
4. TSV output format for Excel

### P1 - High Priority
1. Secondary keyword research automation
2. Keyword cannibalization checking
3. SERP affiliate percentage verification
4. Correct column reading (M not Page Name)

### P2 - Medium Priority
1. Compliance automation (T&Cs, age, hotline)
2. Source hierarchy enforcement
3. Word count calculation from competitors

---

## KEY USER PAIN POINT SUMMARY

1. **Running out of tokens/resources** - Most frequent frustration
2. **Output formatting failures** - CSV not pasting correctly
3. **Wrong column being read** - Page Name vs Target Keywords
4. **Missing compliance elements** - T&Cs, affiliate links
5. **Cross-chat context loss** - Work split across sessions
6. **Ahrefs being skipped** - API calls not being made
7. **Generic content** - Not using secondary keywords

---

*Last Updated: December 3, 2024*
