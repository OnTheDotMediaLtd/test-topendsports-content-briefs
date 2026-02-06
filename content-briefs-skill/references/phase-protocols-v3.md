# PHASE PROTOCOLS v3.1 (ALL PHASES WITH SECONDARY KEYWORDS)

**Token Reduction:** 18,000 → 6,500 words (includes secondary keyword workflow)
**Structure:** All 3 phases consolidated with secondary keyword optimization

---

# PHASE 1: RESEARCH PROTOCOL

**Time:** 10-15 minutes (includes secondary keyword research)
**Output:** Brief Control Sheet (500-700 words max)

---

## 🔍 STEP 1: MANDATORY DISCOVERY

### A. Search Site Structure
```
Search project knowledge: "Betting Site Structure"
Find exact URL: /sport/betting/[page].htm
```

### B. Extract Critical Info
- ✅ Target keyword (NOT from URL - from structure!)
- ✅ Writer assigned
- ✅ Priority level
- ✅ Current status

### C. Identify Competitors
**For "best X" keywords:**
- ✅ Analyze: Review sites (actionnetwork.com, covers.com, thelines.com)
- ❌ DON'T analyze: Brand pages (fanduel.com, draftkings.com)

**Why:** Users want reviews, not brand landing pages.

---

## 🔎 STEP 2: AHREFS RESEARCH

### Critical Rule: Call Ahrefs:doc First
```
BEFORE every Ahrefs function:
1. Call Ahrefs:doc with tool="[function-name]"
2. Review schema response
3. Copy EXACT field names
4. Make actual call
```

### Verified Field Names
✅ Use: `backlinks` (NOT backlinks_links)
✅ Use: `refdomains` (NOT linked_domains)
✅ Use: `volume` (NOT search_volume)
✅ Use: `difficulty` (NOT kw_difficulty)

### What to Gather
- Primary keyword: Volume + difficulty + traffic potential
- Secondary keywords: 8-15 supporting (see Step 2B)
- Competitor insights: Top 3 affiliate names + gaps
- Internal links: 8-12 existing pages

---

## 🔎 STEP 2B: SECONDARY KEYWORD RESEARCH (3-5 min) [NEW]

**When Required:** ALWAYS (for all content types)

### Research Process

**1. Related Keywords (Ahrefs)**
```
Call: keywords-explorer-related-terms
Input: Primary keyword
Filter: KD <30, Volume >50/mo
Identify: 8-15 supporting keywords
```

**2. Map Keywords to Sections**
For each secondary keyword, determine optimal placement:
- High volume (200+/mo) → H2 section title
- Medium volume (100-200/mo) → H3 subsection title
- Lower volume (50-100/mo) → FAQ or natural mentions
- Question keywords ("is X legal", "do I need X") → FAQs

**3. Calculate Total Search Volume**
Sum primary + all secondary keywords to show true opportunity size.

### Output Format

**In Brief Control Sheet, add:**

```markdown
## KEYWORD CLUSTER OPTIMIZATION

**Primary Keyword:** "[keyword]" (XXX/mo)

**Secondary Keywords (Mapped to Sections):**
- "[keyword 1]" (XXX/mo) → H2: [suggested section title]
- "[keyword 2]" (XXX/mo) → H3: [suggested subsection title]
- "[keyword 3]" (XXX/mo) → FAQ + internal link
- "[keyword 4]" (XXX/mo) → Natural mentions throughout
- "[keyword 5]" (XXX/mo) → H2: [suggested section title]
- "[keyword 6]" (XXX/mo) → FAQ: [exact question]
- "[keyword 7]" (XXX/mo) → H3: [suggested subsection title]
- "[keyword 8]" (XXX/mo) → Natural variation

**Total Search Volume:** X,XXX/mo across keyword cluster
**Increase over primary alone:** XXX%
```

### Keyword Types to Prioritize

**Must Include:**
- Comparison keywords: "[brand] vs [competitor]"
- Feature keywords: "[brand] [feature]" (bonus, withdrawal time, app)
- Question keywords: "is [brand] legal", "do I need [brand] promo code"
- Location keywords: "[brand] [state]" (for state pages)

**Examples:**
- Primary: "fanduel review" (500/mo)
- Secondary: "fanduel bonus" (800/mo), "fanduel promo code" (1.2K/mo), "fanduel vs draftkings" (200/mo)
- Total: 2,700/mo cluster (440% increase)

**Self-Check:**
- [ ] Identified 8-15 secondary keywords
- [ ] Each keyword mapped to specific section (H2/H3/FAQ)
- [ ] Total search volume calculated
- [ ] High-volume keywords prioritized for H2/H3 titles

---

## 💼 STEP 1B: BRAND SELECTION RESEARCH (5-7 min)

**When Required:**
- ✅ "Best X" comparison pages
- ✅ Major brand reviews (FanDuel, DraftKings, BetMGM, Caesars, bet365 only)

**When Skip (Use Defaults):**
- ✅ How-to guides
- ✅ Explainer articles
- Defaults: FanDuel #1, BetMGM #2, DraftKings #3

### Critical Rule: Positions #1 & #2 LOCKED
1. **FanDuel** - Always #1 (tracking available)
2. **BetMGM** - Always #2 (tracking available)

**Positions #3-7 are RESEARCH-DRIVEN.**

### Research Process

**1. Competitor Brand Frequency**
- web_fetch top 5 affiliate pages
- Track which brands each features
- Document frequency:
  - 5/5 competitors = Must include
  - 3-4/5 = Strong candidate
  - 1-2/5 = Consider if niche strength
  - 0/5 = Exclude

**2. Reddit User Sentiment**
- Search: `site:reddit.com/r/sportsbook [keyword]`
- Track: Brands recommended, upvotes (20+ = significant)
- Note: Specific features praised for THIS topic

**3. Page Type Decision Matrix**
| Page Type | Auto-Includes | Rationale |
|-----------|---------------|-----------|
| Best [Sport] Sites | FanDuel, BetMGM, DraftKings | Universal leaders |
| Best Parlay Sites | +Caesars | 12-leg SGP leader |
| Best Live Betting | +DraftKings priority | Superior live interface |
| State Pages | Only state-licensed | Legal requirement |
| How-To Guides | Limit to 3 | Keep simple |

**4. Document Selection**
```markdown
## BRAND SELECTION STRATEGY

**Positions #1-2 (LOCKED):**
1. FanDuel - [USP for this keyword]
2. BetMGM - [USP for this keyword]

**Positions #3-7 (Research-Driven):**
3. [Brand] - WHY: [Competitor presence + User sentiment + Evidence]
4. [Brand] - WHY: [Rationale]

**Excluded:**
- [Brand X]: [Reason - e.g., "Only 1/5 competitors, no clear advantage"]
```

---

## 📊 STEP 3: COMPETITOR GAP ANALYSIS

**For each top 3 competitors, identify ONE major gap:**

| Competitor | Gap | Build Opportunity |
|-----------|-----|-------------------|
| ActionNetwork | No calculator | → Build interactive calculator |
| Covers | Static table | → Build filterable table |
| TheLines | 3 FAQs | → Build 7 FAQs with schema |

**This feeds into AI Enhancement requirements.**

---

## 📋 STEP 4: OUTPUT - BRIEF CONTROL SHEET

**Format (500-700 words):**

```markdown
# BRIEF CONTROL SHEET: [Page Title]

## ASSIGNMENT
- Target Keyword: [from Site Structure]
- Writer: [Lewis/Tom/Gustavo]
- Opportunity: [HIGH/MEDIUM/LOW]
- Reason: [1 sentence]

---

## KEYWORD CLUSTER OPTIMIZATION [NEW SECTION]

**Primary Keyword:** "[keyword]" (XXX/mo)

**Secondary Keywords (Mapped to Sections):**
- "[keyword 1]" (XXX/mo) → H2: "[Exact optimized H2 title]"
- "[keyword 2]" (XXX/mo) → H3: "[Exact optimized H3 title]"
- "[keyword 3]" (XXX/mo) → FAQ: "[Exact question]"
- "[keyword 4]" (XXX/mo) → Natural mentions in [section]
[...continue for all 8-15 keywords]

**Total Search Volume:** X,XXX/mo across keyword cluster
**Increase over primary alone:** XXX%

---

## BRAND SELECTION STRATEGY
[Complete if Step 1B done, OR "Using defaults: FanDuel #1, BetMGM #2, DraftKings #3"]

---

## STRATEGIC DIRECTION FOR WRITER
**Content Focus:**
- [Gap 1 to exploit]
- [Gap 2 to exploit]
- [Gap 3 to exploit]

**Unique Angle:** [1 sentence vs competitors]

**Key Points:**
- [Supporting keyword theme 1]
- [Supporting keyword theme 2]
- [Supporting keyword theme 3]

---

## TECHNICAL REQUIREMENTS FOR AI ENHANCEMENT
**Required Interactive Elements:**
- [ ] [Element 1 based on competitor gap]
- [ ] [Element 2 based on competitor gap]
- [ ] [Element 3 based on competitor gap]

**Schema Opportunities:**
- [ ] FAQ schema (7 questions optimized for keywords)
- [ ] HowTo schema (if applicable)
- [ ] Article schema (always)

---

## LOGISTICS
**Internal Links:** [12 max]
1. "[anchor]" → /sport/betting/[page].htm
[...continue to 12]

**Bonuses Verified:** [YES/NO] - [Date]
**Compliance:** Standard USA (21+, 1-800-522-4700, T&Cs)
```

---

## ✅ SELF-CHECK BEFORE STOPPING

- [ ] Used ACTUAL keyword from Site Structure
- [ ] Identified affiliate competitors (not brands)
- [ ] Called Ahrefs:doc before each function
- [ ] **NEW: Identified 8-15 secondary keywords**
- [ ] **NEW: Mapped each keyword to section (H2/H3/FAQ)**
- [ ] **NEW: Calculated total search volume**
- [ ] Step 1B completed if required (or defaults documented)
- [ ] Listed competitor GAPS not just analysis
- [ ] Mapped gaps to AI Enhancement requirements
- [ ] Brief Control Sheet under 700 words

---

## 🛑 STOP HERE

Say: "Phase 1 complete. Brief Control Sheet delivered with keyword cluster targeting [X,XXX] monthly searches. Reply 'continue' for Phase 2."

**DO NOT proceed to Phase 2 automatically.**

---
---

# PHASE 2: WRITER BRIEF PROTOCOL

**Input:** Brief Control Sheet from Phase 1
**Output:** Writer Brief (2-3 pages with keyword optimization)

---

## 🎯 WRITER BRIEF STRUCTURE

```markdown
# WRITER BRIEF: [Page Title]

## ASSIGNED TO: [Lewis/Tom/Gustavo]

---

## PAGE BASICS
- URL: /sport/betting/[page].htm
- Target Keyword: "[keyword]"
- **Total Search Volume:** X,XXX/mo (keyword cluster)
- Word Count: [Based on template and competitors]
- Content Type: [Review/Comparison/How-To/State]
- Template: [Template 1/2/3/4]
- Priority: [HIGH/MEDIUM/LOW]

---

## 🔑 SECONDARY KEYWORD OPTIMIZATION [NEW SECTION]

**Target Keyword Cluster (X,XXX monthly searches total):**

**Primary:** "[keyword]" (XXX/mo)

**Secondary Keywords - Mapped to Sections:**

| Keyword | Volume | Section Placement | Implementation |
|---------|--------|-------------------|----------------|
| [keyword 1] | XXX/mo | H2 title | "[Exact optimized H2 title]" |
| [keyword 2] | XXX/mo | H3 title | "[Exact optimized H3 title]" |
| [keyword 3] | XXX/mo | FAQ | FAQ: "[Exact question using keyword]" |
| [keyword 4] | XXX/mo | Natural mentions | Use throughout [section name] |
| [keyword 5] | XXX/mo | H2 title | "[Exact optimized H2 title]" |
| [keyword 6] | XXX/mo | FAQ | FAQ: "[Exact question]" |
| [keyword 7] | XXX/mo | H3 title | "[Exact optimized H3 title]" |
| [keyword 8] | XXX/mo | Natural variation | Rotate throughout content |

**Natural Keyword Placement Strategy:**
- Use primary keyword in first sentence of every major section
- Rotate variations: "[brand] sportsbook", "[brand] betting app", "[brand] platform"
- Include location phrases: "[brand] in [state]" when discussing availability
- Use comparison keywords in transition sentences between sections

**Meta Keywords (for AI to add):**
[comma-separated list of all primary + secondary keywords]

---

## MANDATORY INTRO FORMAT (100-150 words total)

**Opening (40-50 words before disclosure):**
Sentence 1: "The best [category] is [Winner], followed by [Runner-up] and [Third]."
Sentence 2: "[Authority statement]"

**Then:** Affiliate disclosure (50-75 words)

**Total:** 100-150 words max

❌ DON'T: "Welcome to...", rhetorical questions, exceed 150 words
✅ DO: Direct answer, specific winners, keyword in sentence 1

---

## ⚠️ CRITICAL: NO DATED LANGUAGE IN TITLE/H1

❌ NEVER: "October 2025", "Review 2025", "Best Sites 2025"
✅ USE: "Comprehensive Review", "The #1 Rated App", "Best [X] Sites"
✅ "LAST UPDATED" BADGE: Place immediately after H1

---

## 📖 CONTENT TEMPLATE TO FOLLOW

Template: [Template 1/2/3/4]
See: Content Type Templates for complete structure
Word Count Target: [From template]

---

## 📝 OPTIMIZED CONTENT OUTLINE [UPDATED WITH KEYWORDS]

[Example for Template 1 - Review:]

1. Introduction (100-150w)
2. Comparison Table (3 brands)
3. Quick Answer Box
4. [Brand] Overview & Background (300-350w)
5. Getting Started: Sign-Up Process (300-350w)
6. **[Brand] Bonus: Current Welcome Offer** (400-500w) ← "[brand] bonus"
   - H3: **Do I Need a [Brand] Promo Code?** ← "[brand] promo code"
   - H3: Complete Terms & Conditions
   - H3: Is This a Good Bonus?
7. **[Brand] App Review: iOS & Android** (500-600w) ← "[brand] app review"
   - H3: iOS App Features
   - H3: Android App Features
   - H3: **[Brand] App Download Guide** ← "[brand] app download"
8. [Signature Feature] (400-500w)
9. Live Betting & Streaming (400-450w)
10. Betting Markets & Sports Coverage (400-450w)
11. Odds Quality (350-400w)
12. Banking: Deposits & Withdrawals (400-450w)
    - H3: **[Brand] Withdrawal Time: How Fast?** ← "[brand] withdrawal time"
13. Customer Support (300-350w)
14. Loyalty Program or Gap (300-400w)
15. **[Brand] vs DraftKings vs BetMGM** (400-500w) ← "[brand] vs [competitor]"
16. **Is [Brand] Legal & Safe?** (300-350w) ← "is [brand] legal"
    - H3: **Where is [Brand] Available?** ← "[brand] states"
17. Pros & Cons Summary
18. FAQs (7 minimum - optimized)
19. Final Verdict (200-250w)
20. References (5-10 sources)
21. Related Pages (3+)
22. Responsible Gambling Section
23. Legal Disclaimer

---

## 🔍 SOURCE REQUIREMENTS (CRITICAL)

**For Reviews/Comparisons - Use REAL USER FEEDBACK:**

✅ REQUIRED SOURCES:
1. **App Store Reviews (iOS)**
   - Citation: "4.9/5 (1.8M reviews) - analyzed Oct 1-14, 2025"
   - Example: "Mentioned in 847 App Store reviews as 'best app interface'"

2. **Google Play Reviews (Android)**
   - Citation: "4.7/5 (371.9K reviews) - analyzed Sept-Oct 2025"
   - Example: "Reported in 402 Google Play reviews"

3. **Reddit r/sportsbook**
   - Citation: "Reddit users report 24-48 hour payouts (15 threads analyzed)"
   - Consensus opinions, upvoted posts (20+)

❌ DO NOT USE AS PRIMARY:
- Affiliate competitor sites (for pros/cons)
- Generic marketing claims
- Unattributed statements

✅ USE BRAND SITES FOR:
- Feature verification only
- Bonus offers (verified separately)
- Legal licensing

---

## 💰 BONUS INFORMATION & T&Cs

**Bonuses verified as of [Date]:**

[Brand 1]
- Current Offer: [Exact text from official site]
- Source: [Official promo page URL]
- Complete T&Cs: [Full legal language from Phase 1]
- Last Verified: [Date]
- Critical Distinction: [Key point users must understand]

[Repeat for all featured brands]

**Where to place:**
- Brief in comparison table: "*21+, T&Cs apply. See details below."
- Brief in Quick Answer Box (if bonuses)
- COMPLETE in dedicated section (AI will format with HTML template)

---

## 📊 USER FEEDBACK RESEARCH

[Brand] User Feedback Summary:
- **App Store:** [Rating], [Count], analyzed [dates]
  - Top Praise: "[Item]" - [X] mentions
  - Top Complaint: "[Item]" - [X] mentions
- **Google Play:** [Rating], [Count], recent issues
- **Reddit:** [X] threads, consensus: [Summary]

**Use in content:** Cite these specific numbers. Don't make generic claims.

---

## 🎯 STRATEGIC CONTENT FOCUS
[From Brief Control Sheet]

Emphasize:
- [Point 1]
- [Point 2]
- [Point 3]

Unique Angle: [What we'll do differently]

---

## 🔗 INTERNAL LINKS (12 required)
[From Brief Control Sheet]

---

## 🏢 BRANDS TO FEATURE
[From Phase 1 brand selection]

**Tier 1:**
1. FanDuel - USP: [specific], Tracking: ✅
2. BetMGM - USP: [specific], Tracking: ✅

**Tier 2:**
3. [Brand] - WHY: [rationale], Tracking: ❌

---

## ❓ OPTIMIZED FAQs [UPDATED WITH KEYWORDS]

**7 Minimum - Targeting High-Volume Keywords:**

1. **Is [Brand] legal in my state?** ← "is [brand] legal"
2. **Do I need a [Brand] promo code for the welcome bonus?** ← "[brand] promo code"
3. **How fast are [Brand] withdrawals?** ← "[brand] withdrawal time"
4. **Is [Brand] better than DraftKings?** ← "[brand] vs draftkings"
5. **What states is [Brand] available in?** ← "[brand] states"
6. **How do I download the [Brand] app?** ← "[brand] app download"
7. **What is the [Brand] welcome bonus?** ← "[brand] bonus"

---

## ✅ COMPLIANCE REQUIREMENTS

**Every article MUST include:**
- Age requirement (21+)
- Risk warnings
- Problem gambling: 1-800-522-4700
- Legal disclaimers
- Affiliate disclosure
- Complete T&Cs (if applicable)

❌ FORBIDDEN:
"Guaranteed wins", "Can't lose", "Risk-free", "Beat the house"

---

## 📋 QUALITY CHECKLIST
- [ ] Intro 100-150 words
- [ ] Direct answer first sentence
- [ ] No dated language in H1/title
- [ ] Word count meets target
- [ ] **NEW: All H2/H3 titles optimized with keywords**
- [ ] **NEW: FAQ questions target high-volume searches**
- [ ] User feedback cited with numbers
- [ ] 12 internal links placed
- [ ] 7 FAQs (optimized)
- [ ] All compliance met
- [ ] T&Cs complete and placed correctly
- [ ] **NEW: Meta keywords list provided**

---

END OF WRITER BRIEF
```

---

## 🛑 STOP HERE

Say: "Phase 2 complete. Writer Brief delivered with secondary keyword optimization targeting [X,XXX] monthly searches. Reply 'continue' for Phase 3."

**DO NOT proceed to Phase 3 automatically.**

---
---

# PHASE 3: AI ENHANCEMENT PROTOCOL

**Input:** Writer Brief + Brief Control Sheet
**Output:** AI Enhancement Brief (5-8 pages with HTML and keyword optimization)

---

## 🔍 STEP 1: REVIEW REQUIREMENTS

From Brief Control Sheet:
```
TECHNICAL REQUIREMENTS:
- [ ] [Element 1]
- [ ] [Element 2]
- [ ] [Element 3]

Template Type: [1/2/3/4]
T&Cs Required: [YES/NO]
```

From Writer Brief:
```
SECONDARY KEYWORD OPTIMIZATION:
- Meta keywords list: [all keywords]
- Optimized H2/H3 titles: [list]
- Optimized FAQ questions: [list]
```

---

## 📋 STEP 2: TEMPLATE-SPECIFIC REQUIREMENTS

### Template Checklist
- **Template 1 (Review):** Comparison table (3 brands), Complete T&Cs (1 brand)
- **Template 2 (Comparison):** Comparison table (5-7 brands), Complete T&Cs (ALL brands)
- **Template 3 (How-To):** Quick Answer Box, Brief T&Cs only (if bonuses)
- **Template 4 (State):** Comparison table (state-licensed), Complete T&Cs (state ops)

---

## 🏗️ STEP 3: BUILD REQUIRED ELEMENTS

### A. META TAGS WITH SECONDARY KEYWORDS [UPDATED]

```html
<meta name="title" content="[Page Title - NO dates]">
<meta name="description" content="[160 character description with primary keyword]">
<meta name="keywords" content="[ALL primary + secondary keywords from Phase 2, comma-separated]">
<meta name="author" content="[Lewis Humphries/Tom Goldsmith/Gustavo Cantella]">
<link rel="canonical" href="https://[domain]/sport/betting/[page].htm">
```

**Example:**
```html
<meta name="keywords" content="fanduel review, fanduel bonus, fanduel promo code, fanduel app review, fanduel withdrawal time, fanduel vs draftkings, is fanduel legal, fanduel states, fanduel sportsbook, fanduel betting app">
```

---

### B. "Last Updated" Badge (ALWAYS FIRST)

```html
<div style="background: #e8f5e9; padding: 0.75rem 1.25rem; border-left: 4px solid #2e7d32; margin-bottom: 1.5rem; border-radius: 4px;">
  <p style="margin: 0; font-size: 14px; color: #2e7d32;">
    <strong>✓ Last Updated:</strong> [Current Date]
  </p>
</div>
```

**Placement:** Immediately after H1, before intro

---

### C. Comparison Table (Reviews/Comparisons/State Pages)

```html
<div style="overflow-x: auto; margin: 2rem 0;">
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr style="background: #2e7d32;">
        <th style="color: white; padding: 1rem;">Sportsbook</th>
        <th style="color: white; padding: 1rem;">Best For</th>
        <th style="color: white; padding: 1rem;">Current Bonus</th>
        <th style="color: white; padding: 1rem;">Rating</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 1rem;"><strong>FanDuel</strong></td>
        <td style="padding: 1rem;">[USP from research]</td>
        <td style="padding: 1rem;">[Bonus]*</td>
        <td style="padding: 1rem;">⭐⭐⭐⭐⭐</td>
      </tr>
    </tbody>
  </table>
  <p style="font-size: 12px; color: #666;">
    *21+ only. T&Cs apply. See complete terms below.
  </p>
</div>
```

**Specs:**
- Mobile-responsive
- FanDuel/BetMGM tracking links
- Brief T&Cs inline: "*21+, T&Cs apply"
- Placement: After intro, before main content

---

### D. Quick Answer Box (ALWAYS REQUIRED)

```html
<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left: 4px solid #2e7d32; padding: 1.5rem; margin: 2rem 0; border-radius: 8px;">
  <h2 style="color: #2e7d32; margin-top: 0;">Quick Answer</h2>
  <p style="font-size: 1.1rem;">[Direct 2-3 sentence answer]</p>
  <ul style="line-height: 1.8;">
    <li><strong>[Key fact]</strong></li>
    <li><strong>[Key metric]</strong></li>
  </ul>
</div>
```

**Placement:** After comparison table

---

### E. COMPLETE T&Cs SECTION (Mandatory for Templates 1, 2, 4)

**When Required:**
- ✅ Template 1 (Review): 1 brand
- ✅ Template 2 (Comparison): ALL brands
- ⚠️ Template 3 (How-To): Only if bonuses
- ✅ Template 4 (State): State-licensed operators

**Where to Place:**
- Reviews: Under "Current Welcome Bonus" H2
- Comparisons: After individual reviews
- State Pages: After "Licensed Operators"

**HTML Template:**
```html
<div style="background: #f8f9fa; padding: 2rem; margin: 2rem 0; border-radius: 8px; border: 2px solid #2e7d32;">

  <h3 style="margin-top: 0; color: #2e7d32;">Complete Bonus Terms & Conditions</h3>

  <h4 style="color: #333; border-bottom: 2px solid #2e7d32; padding-bottom: 0.5rem;">
    [Brand Name]
  </h4>

  <div style="background: #e8f5e9; padding: 1.25rem; border-radius: 6px; margin: 1rem 0;">
    <p style="margin: 0; font-weight: 600; color: #2e7d32; font-size: 16px;">
      [EXACT BONUS TEXT FROM PHASE 1]
    </p>
  </div>

  <h5 style="color: #333; margin-top: 1.5rem;">Eligibility Requirements:</h5>
  <ul style="line-height: 1.8; color: #333;">
    <li>Must be 21+ years old</li>
    <li>New [Brand] customers only</li>
    <li>Physically located in eligible state</li>
  </ul>

  <h5 style="color: #333; margin-top: 1.5rem;">How to Qualify:</h5>
  <ul style="line-height: 1.8; color: #333;">
    <li>Opt-in during registration</li>
    <li>First deposit $[X]+ </li>
    <li><strong>[KEY CONDITION]</strong></li>
  </ul>

  <h5 style="color: #333; margin-top: 1.5rem;">Bonus Terms:</h5>
  <ul style="line-height: 1.8; color: #333;">
    <li>$[X] in bonus bets within [timeframe]</li>
    <li>Non-withdrawable</li>
    <li>Expires [X] days</li>
  </ul>

  <h5 style="color: #333; margin-top: 1.5rem;">Eligible States:</h5>
  <p style="color: #333;">[COMPLETE LIST]</p>

  <div style="background: #fff3cd; padding: 1rem; border-radius: 6px; margin: 1.5rem 0; border-left: 4px solid #ffc107;">
    <p style="margin: 0; font-size: 14px; color: #856404;">
      <strong>⚠️ Critical:</strong> [KEY DISTINCTION FROM PHASE 1]
    </p>
  </div>

  <p style="font-size: 13px; color: #666; padding: 1rem; background: white; border-radius: 4px;">
    <strong>Complete Legal Terms:</strong><br><br>
    [PASTE COMPLETE LEGAL LANGUAGE FROM PHASE 1]
  </p>

  <p style="font-size: 13px; color: #666; margin-top: 1rem;">
    <strong>Official Terms:</strong> <a href="[URL]" target="_blank">[brand].com/terms</a>
  </p>

  <p style="font-size: 13px; color: #666; margin-top: 1rem;">
    <strong>Problem Gambling:</strong> Call 1-800-GAMBLER
  </p>

  <p style="font-size: 13px; color: #666; margin-top: 1rem; font-weight: 600;">
    <strong>Last Verified:</strong> [Date from Phase 1]
  </p>

</div>

<!-- For multiple brands: Add <hr> and repeat -->
```

---

### F. Interactive Elements (Based on Gaps)

**If gap = "No calculator":**
Build working calculator with HTML/JS

**If gap = "Static table":**
Build sortable/filterable table

**If gap = "3 FAQs":**
Build 7 FAQs with collapsible format + schema

---

### G. Schema Markup WITH OPTIMIZED FAQs [UPDATED]

**Article Schema:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Page Title]",
  "author": {"@type": "Person", "name": "[Lewis/Tom/Gustavo]"},
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[Current Date]",
  "publisher": {
    "@type": "Organization",
    "name": "Topend Sports"
  }
}
</script>
```

**FAQ Schema WITH OPTIMIZED QUESTIONS [UPDATED]:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is [Brand] legal in my state?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer targeting 'is [brand] legal' keyword]"
      }
    },
    {
      "@type": "Question",
      "name": "Do I need a [Brand] promo code for the welcome bonus?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer targeting '[brand] promo code' keyword]"
      }
    },
    {
      "@type": "Question",
      "name": "How fast are [Brand] withdrawals?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer targeting '[brand] withdrawal time' keyword]"
      }
    },
    {
      "@type": "Question",
      "name": "Is [Brand] better than DraftKings?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer targeting '[brand] vs draftkings' keyword]"
      }
    },
    {
      "@type": "Question",
      "name": "What states is [Brand] available in?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer targeting '[brand] states' keyword]"
      }
    },
    {
      "@type": "Question",
      "name": "How do I download the [Brand] app?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer targeting '[brand] app download' keyword]"
      }
    },
    {
      "@type": "Question",
      "name": "What is the [Brand] welcome bonus?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer targeting '[brand] bonus' keyword]"
      }
    }
  ]
}
</script>
```

**Critical:** FAQ questions MUST match the optimized questions from Phase 2

---

### H. Compliance Sections (ALWAYS)

**Affiliate Disclosure (Top):**
```html
<div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; margin: 1.5rem 0;">
  <p style="margin: 0; font-size: 14px;">
    <strong>Disclosure:</strong> We may earn commission when you sign up through our links.
  </p>
</div>
```

**Responsible Gambling (Bottom):**
```html
<div style="background: #fff3cd; padding: 1.5rem; margin: 2rem 0; border-radius: 8px;">
  <h3 style="margin-top: 0;">Gamble Responsibly</h3>
  <ul>
    <li>National Hotline: <strong>1-800-522-4700</strong></li>
    <li>Visit: ncpgambling.org</li>
    <li>Must be 21+ to bet</li>
  </ul>
</div>
```

---

## 📋 STEP 4: COMPLETE CHECKLIST

### Technical Elements
- [ ] **NEW: Meta keywords tag includes ALL secondary keywords**
- [ ] "Last Updated" badge (after H1)
- [ ] Comparison table (if applicable)
- [ ] Quick Answer Box (always)
- [ ] Interactive elements (based on gaps)
- [ ] Affiliate links: rel="nofollow noopener"

### T&Cs Requirements
- [ ] Complete T&Cs sections (if Template 1/2/4)
- [ ] Used complete template (not abbreviated)
- [ ] Included ALL bonus details from Phase 1
- [ ] Verification dates
- [ ] Brief T&Cs in tables/boxes

### Schema & SEO
- [ ] Article schema
- [ ] **NEW: FAQ schema with optimized questions**
- [ ] **NEW: H2/H3 IDs reflect keyword-optimized titles**
- [ ] NO dated language in meta title

### Compliance
- [ ] Affiliate disclosure (top)
- [ ] Responsible gambling (bottom)
- [ ] 1-800-522-4700 hotline
- [ ] Age requirement (21+)

---

## 🛑 FINAL OUTPUT

**Deliver:** AI Enhancement Brief (5-8 pages)

**Say:** "Phase 3 complete. AI Enhancement Brief delivered with [X] interactive elements, comprehensive meta keywords, and optimized FAQ schema. Complete T&Cs sections included. All 3 artifacts complete."

---

**END OF PHASE PROTOCOLS v3.1**

*Condensed 64% with secondary keyword optimization integrated. Targets 400-900% more search volume.*
