# PHASE 2: WRITER BRIEF AGENT

**Purpose:** Create clear writer instructions with keyword optimization
**Input:** `active/[page-name]-phase1.json`
**Output:** Writer Brief (2-3 pages) + JSON data file

---

## STEP 1: LOAD PHASE 1 DATA

Read the JSON file from Phase 1:
```bash
cat active/[page-name]-phase1.json
```

Extract:
- Target keyword and cluster
- Writer assignment
- Template type
- Brand selection
- Strategic direction
- Word count target

---

## STEP 2: IDENTIFY CONTENT TEMPLATE

Based on Phase 1 template assignment:

| Template | Structure | Word Count | T&Cs |
|----------|-----------|------------|------|
| Template 1 (Review) | Single brand deep-dive | 3,500-4,000 | Complete (1) |
| Template 2 (Comparison) | Multiple brand comparison | 2,500-3,500 | Complete (ALL) |
| Template 3 (How-To) | Step-by-step guide | 1,500-2,500 | Brief only |
| Template 4 (State) | State-specific guide | 2,000-2,800 | Complete (state) |

---

## STEP 3: BUILD KEYWORD-OPTIMIZED OUTLINE

### Create Section Structure
Map secondary keywords to content sections:

**For Template 1 (Review):**
```
H1: [Brand] Sportsbook Review: [Timeless Angle]
├── [Last Updated Badge]
├── Introduction (100-150w)
├── Comparison Table (3 brands)
├── Quick Answer Box
├── H2: [Brand] Overview (300-350w)
├── H2: Getting Started (300-350w)
├── H2: [Brand] Bonus: Current Welcome Offer (400-500w) ← "[brand] bonus"
│   ├── H3: Do I Need a [Brand] Promo Code? ← "[brand] promo code"
│   ├── H3: Complete Terms & Conditions
│   └── H3: Is This a Good Bonus?
├── H2: [Brand] App Review: iOS & Android (500-600w) ← "[brand] app review"
│   ├── H3: iOS App Features
│   ├── H3: Android App Features
│   └── H3: [Brand] App Download Guide ← "[brand] app download"
├── H2: [Signature Feature] (400-500w)
├── H2: Live Betting & Streaming (400-450w)
├── H2: Betting Markets (400-450w)
├── H2: Odds Quality (350-400w)
├── H2: Banking: Deposits & Withdrawals (400-450w)
│   └── H3: [Brand] Withdrawal Time ← "[brand] withdrawal time"
├── H2: Customer Support (300-350w)
├── H2: [Brand] vs DraftKings vs BetMGM (400-500w) ← "[brand] vs [competitor]"
├── H2: Is [Brand] Legal & Safe? (300-350w) ← "is [brand] legal"
│   └── H3: Where is [Brand] Available? ← "[brand] states"
├── Pros & Cons Summary
├── FAQs (7 minimum - keyword optimized)
├── Final Verdict (200-250w)
├── References (5-10)
├── Related Pages (3+)
├── Responsible Gambling
└── Legal Disclaimer
```

**For Template 2 (Comparison):**
```
H1: Best [Category] Sites
├── [Last Updated Badge]
├── Introduction (100-150w)
├── Comparison Table (5-7 brands)
├── Quick Answer Box
├── H2: Quick Winner Summaries
├── H2: [Brand #1] Review (500w)
├── H2: [Brand #2] Review (400w)
├── H2: [Brand #3] Review (350w)
├── H2: [Brand #4] Review (300w)
├── H2: [Brand #5] Review (250w)
├── H2: Complete Bonus Terms (ALL brands)
├── H2: How We Test & Rank (400w)
├── H2: Alternative Options (300w)
├── H2: What to Look For (400w)
├── FAQs (5-7 keyword optimized)
├── References (5-10)
├── Related Pages (3+)
├── Responsible Gambling
└── Legal Disclaimer
```

---

## STEP 4: MANDATORY INTRO FORMAT

**Structure (100-150 words total):**

**Opening (40-50 words before disclosure):**
- Sentence 1: Direct answer with winners
- Sentence 2: Authority statement

**Example:**
```
"The best NFL betting sites are FanDuel, DraftKings, and BetMGM. They offer 
the most competitive NFL odds and comprehensive prop markets, verified through 
extensive testing across all major sportsbooks."
```

**Then:** Affiliate disclosure (50-75 words)

**Forbidden:**
- ❌ "Welcome to..."
- ❌ "Looking for..."
- ❌ Rhetorical questions
- ❌ Over 150 words total

---

## STEP 5: SOURCE REQUIREMENTS

### Specify Required Sources

**TIER 1 (Primary) - MUST USE:**
- App Store Reviews: "Cited as '4.9/5 (1.8M reviews) - analyzed [date range]'"
- Google Play Reviews: "Reported in X reviews"
- Reddit r/sportsbook: "Reddit users report [finding] (X threads analyzed)"

**TIER 2 (Verification):**
- Brand official sites for features and licenses only

**TIER 3 (Facts):**
- Industry publications for market data

**TIER 4 (Sparingly):**
- Affiliate sites for research gaps ONLY
- ❌ NEVER cite for pros/cons or user experience

---

## STEP 6: OPTIMIZED FAQ QUESTIONS

Create 7 FAQ questions targeting high-volume keywords:

**Example for FanDuel Review:**
```json
{
  "faqs": [
    {"question": "Is FanDuel legal in my state?", "keyword": "is fanduel legal", "volume": 180},
    {"question": "Do I need a FanDuel promo code for the welcome bonus?", "keyword": "fanduel promo code", "volume": 1200},
    {"question": "How fast are FanDuel withdrawals?", "keyword": "fanduel withdrawal time", "volume": 150},
    {"question": "Is FanDuel better than DraftKings?", "keyword": "fanduel vs draftkings", "volume": 200},
    {"question": "What states is FanDuel available in?", "keyword": "fanduel states", "volume": 220},
    {"question": "How do I download the FanDuel app?", "keyword": "fanduel app download", "volume": 300},
    {"question": "What is the FanDuel welcome bonus?", "keyword": "fanduel bonus", "volume": 800}
  ]
}
```

---

## STEP 7: META KEYWORDS LIST

Compile all primary + secondary keywords for AI to add to meta tag:

```
fanduel review, fanduel bonus, fanduel promo code, fanduel app review, 
fanduel withdrawal time, fanduel vs draftkings, is fanduel legal, 
fanduel states, fanduel sportsbook, fanduel betting app
```

---

## OUTPUT: WRITER BRIEF

Save two files:

### 1. JSON Data File: `active/[page-name]-phase2.json`
```json
{
  "url": "/sport/betting/fanduel-review.htm",
  "writer": "Lewis Humphries",
  "template": "Template 1 - Review",
  "word_count_target": 3800,
  "content_outline": [...],
  "keyword_optimization": {
    "h2_titles": [...],
    "h3_titles": [...],
    "faqs": [...],
    "meta_keywords": "..."
  },
  "source_requirements": {...},
  "compliance": {...}
}
```

### 2. Markdown Brief: `output/[page-name]-writer-brief.md`

```markdown
# WRITER BRIEF: [Page Title]

## ASSIGNED TO: [Lewis/Tom/Gustavo]

---

## PAGE BASICS
- URL: [Full URL]
- Target Keyword: "[keyword]"
- Total Search Volume: X,XXX/mo (keyword cluster)
- Word Count: [Target]
- Content Type: [Review/Comparison/How-To/State]
- Template: [Template 1/2/3/4]
- Priority: [HIGH/MEDIUM/LOW]

---

## 🔑 SECONDARY KEYWORD OPTIMIZATION

**Target Keyword Cluster (X,XXX monthly searches total):**

**Primary:** "[keyword]" (XXX/mo)

**Secondary Keywords - Mapped to Sections:**

| Keyword | Volume | Section | Implementation |
|---------|--------|---------|----------------|
| [keyword 1] | XXX/mo | H2 title | "[Exact optimized H2 title]" |
| [keyword 2] | XXX/mo | H3 title | "[Exact optimized H3 title]" |
| [keyword 3] | XXX/mo | FAQ | FAQ: "[Exact question]" |
[...continue for all keywords]

**Natural Keyword Placement Strategy:**
- Use primary keyword in first sentence of every major section
- Rotate variations: "[brand] sportsbook", "[brand] betting app"
- Include location phrases when discussing availability

**Meta Keywords (for AI):**
[comma-separated list]

---

## MANDATORY INTRO FORMAT (100-150 words)

**Opening (40-50 words):**
Sentence 1: "[Direct answer with winners]"
Sentence 2: "[Authority statement]"

**Then:** Affiliate disclosure (50-75 words)

❌ DON'T: "Welcome to...", rhetorical questions, exceed 150 words
✅ DO: Direct answer, specific winners, keyword in sentence 1

---

## ⚠️ NO DATED LANGUAGE IN TITLE/H1

❌ NEVER: "October 2025", "Review 2025"
✅ USE: "Comprehensive Review", "The #1 Rated App"
✅ "Last Updated" badge immediately after H1

---

## 📝 OPTIMIZED CONTENT OUTLINE

[Full outline with all H2/H3 sections and word counts]

---

## 🔍 SOURCE REQUIREMENTS

**MUST USE Real User Feedback:**
- App Store: Format as "4.9/5 (1.8M reviews) - analyzed [dates]"
- Google Play: Format as "Reported in X reviews"
- Reddit: Format as "Reddit users report X (Y threads)"

**DO NOT use affiliate sites for pros/cons**

---

## 🏢 BRANDS TO FEATURE

**Tier 1 (Locked):**
1. FanDuel - [USP for this topic]
2. BetMGM - [USP for this topic]

**Tier 2 (Research-Driven):**
3. [Brand] - WHY: [rationale from Phase 1]
[...continue]

---

## ❓ OPTIMIZED FAQs (7 minimum)

1. **[Question targeting keyword]** ← "[keyword]" (XXX/mo)
2. **[Question targeting keyword]** ← "[keyword]" (XXX/mo)
[...continue for 7 questions]

---

## ✅ COMPLIANCE REQUIREMENTS

Every article MUST include:
- Age requirement (21+)
- Risk warnings
- Problem gambling: 1-800-522-4700
- Legal disclaimers
- Affiliate disclosure
- Complete T&Cs (if Template 1/2/4)

---

## 📋 QUALITY CHECKLIST
- [ ] Intro 100-150 words
- [ ] Direct answer first sentence
- [ ] No dated language in H1/title
- [ ] Word count meets target
- [ ] All H2/H3 titles optimized with keywords
- [ ] FAQ questions target high-volume searches
- [ ] User feedback cited with numbers
- [ ] 12 internal links placed
- [ ] 7 FAQs (optimized)
- [ ] All compliance met

---

END OF WRITER BRIEF
```

---

## SELF-CHECK BEFORE COMPLETING

- [ ] Correct writer assigned (Spanish = Gustavo)
- [ ] Content type identified (Template 1/2/3/4)
- [ ] Secondary keyword optimization table included
- [ ] All H2/H3 titles optimized with keywords
- [ ] FAQ questions optimized for searches
- [ ] Intro format specified (100-150w)
- [ ] Source requirements specified (TIER 1: real users)
- [ ] Brand selection rationale from Phase 1 included
- [ ] 12 internal links listed
- [ ] Meta keywords list provided
- [ ] NO dated language in H1/title
- [ ] Writer Brief is 2-3 pages
- [ ] Saved JSON to `active/`
- [ ] Saved markdown to `output/`

---

## COMPLETION MESSAGE

After saving both files, output:
```
Phase 2 complete. Writer Brief delivered.
- Writer: [Name]
- Template: [Type]
- Word Count Target: X,XXX
- Keyword cluster: X,XXX monthly searches
- JSON saved to: active/[page-name]-phase2.json
- Brief saved to: output/[page-name]-writer-brief.md

Ready for Phase 3.
```
