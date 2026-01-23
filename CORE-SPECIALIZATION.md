# CORE-SPECIALIZATION.md
## TopEndSports Content Briefs Generation System

**Last Updated:** 2025-12-12
**Status:** PROTECTED - Core features that define this project's unique identity

---

## PURPOSE

This document protects the specialized features that make the **Content Briefs Generation System** uniquely different from other TopEndSports projects. These features MUST NOT be altered without explicit approval.

**Key Distinction:** This project CREATES new content plans, not optimizes existing content.

---

## PROJECT IDENTITY

### What This System Does
- **Generates comprehensive content briefs** for writers (NOT implements final pages)
- **Creates strategic content plans** based on real keyword research
- **Provides technical specifications** for developers to implement
- **Produces 3 distinct deliverables** per page request (research, writer brief, technical specs)

### What This System Is NOT
- ❌ NOT a page optimization tool (see: betting-pages-agent for that)
- ❌ NOT a state hub generator (see: state-hubs-agent for that)
- ❌ NOT an article formatter (this is the PLANNING phase)
- ❌ NOT a content writer (produces briefs FOR writers, not final content)

---

## PROTECTED FEATURE 1: 3-PHASE WORKFLOW ARCHITECTURE

### The Sacred Workflow

```
PHASE 1: Research & Discovery (15-20 min)
├── Real Ahrefs keyword data (MCP or Python fallback)
├── Competitor SERP analysis (affiliate sites only)
├── Brand positioning with rationale
└── OUTPUTS: phase1.json + brief-control-sheet.md

PHASE 2: Writer Brief Creation (5-10 min)
├── Keyword mapping to H2/H3/FAQ sections
├── Content structure with word counts
├── Source requirements (TIER 1: App Store, Reddit)
└── OUTPUTS: phase2.json + writer-brief.md

PHASE 3: AI Enhancement (10-15 min - PARALLEL EXECUTION)
├── 7 Sub-Agents running simultaneously
├── Complete HTML/CSS/JS code
├── Schema markup (Article, FAQ, Breadcrumb)
└── OUTPUT: ai-enhancement.md (concatenated from 7 parts)
```

**CRITICAL RULES:**
- All 3 phases MUST execute in order
- Each phase validated before next begins
- Phase 3 MUST split into 7 parallel sub-agents (token limit management)
- Total of 6 files produced (2 per phase: 1 JSON + 1 Markdown)

### Why This Cannot Be Simplified

**Attempt to merge phases = SYSTEM FAILURE**

| What Happens | Why It Breaks |
|--------------|---------------|
| Skip Phase 1 | No keyword research → Generic brief → Poor SEO |
| Skip Phase 2 | Writers lack structure → Inconsistent content |
| Skip Phase 3 | Devs have no implementation guide → Can't build page |
| Single agent Phase 3 | 32K token limit exceeded → Truncated output |

---

## PROTECTED FEATURE 2: BRAND POSITIONING SYSTEM

### The Locked Hierarchy

```
#1: FanDuel   → LOCKED (commercial partnership)
#2: BetMGM    → LOCKED (commercial partnership)
#3-10: Research-driven (based on Ahrefs + competitor analysis)
```

**CRITICAL:** Positions 1 and 2 are NOT negotiable. They are contractual obligations.

### Research-Driven Brand Selection (Positions 3-10)

**Eligible Brands:**
- Bet365 (365)
- DraftKings (DK)
- theScore BET (SCR) ← Formerly ESPN BET (rebranded Dec 2025)
- Caesars (CZR)
- Fanatics (FAN)
- BetRivers (BRV)
- Hard Rock Bet (HRB)
- Borgata (BOR)

**Selection Criteria:**
1. Keyword volume analysis (brand-specific keywords)
2. Competitor inclusion (what #1 ranking page covers)
3. State availability (for state-specific pages)
4. Recent market activity (bonuses, features)

### Brand Count by Keyword Volume

| Primary Keyword Volume | Minimum Brands | Target Brands |
|------------------------|----------------|---------------|
| 10,000+/mo | 8 | 10 |
| 5,000-10,000/mo | 7 | 8 |
| 1,000-5,000/mo | 5 | 7 |
| <1,000/mo | 5 | 5 |

**WHY:** This mirrors #1 ranking competitor strategy to match depth.

---

## PROTECTED FEATURE 3: BETINIRELAND.IE STYLE STANDARDS

### Intro Format (MANDATORY)

**Total:** 100-150 words
**Structure:**
1. **Opening (40-60 words)**
   - Sentence 1: Direct answer with winners (immediate value)
   - Sentence 2: Authority statement (why trust this)
2. **Disclosure (50-75 words)**
   - Affiliate relationship explanation
   - Editorial independence statement

**Forbidden Patterns:**
- ❌ "Welcome to..."
- ❌ "Looking for..."
- ❌ Rhetorical questions
- ❌ "In this article, we will..."

**Example Structure:**
```
[GOOD]
"FanDuel and BetMGM lead our NFL betting sites rankings for 2025,
offering superior odds, live betting, and prop markets. Our testing
team evaluated 15 sportsbooks across 20+ criteria.

[Affiliate disclosure: We earn commissions from qualifying sign-ups
through links on this page. Our rankings remain independent and based
on testing methodology detailed below.]"

[BAD]
"Welcome to our guide! Are you looking for the best NFL betting sites?
In this comprehensive article, we will explore the top options..."
```

---

## PROTECTED FEATURE 4: WRITER ASSIGNMENT LOGIC

### Pre-Assigned Writers (From Site Structure CSV)

**Phase 1 Research** extracts writer assignment from site structure:

```bash
grep -i "[page-name]" assets/data/site-structure-english.csv
# Column: "Writer Assigned"
```

**Current Writer Pool:**
- **Lewis** → NFL, NBA content
- **Tom** → MLB, soccer content
- **Gustavo** → App reviews, state pages

**Assignment Logic:**
1. Check CSV first (pre-assigned takes priority)
2. If blank, assign based on topic category
3. If ambiguous, default to Lewis (primary writer)

**WHY PROTECTED:** Writers have specialized knowledge. Incorrect assignment = rewrites.

---

## PROTECTED FEATURE 5: AHREFS RESEARCH WITH FALLBACK

### The Two-Path System

```
PRIMARY PATH: Ahrefs MCP
├── Fast execution (3x faster than npx)
├── Direct node execution
└── If successful → Use MCP data

FALLBACK PATH: Python API Workaround
├── Triggered on MCP 403/error
├── Uses: .claude/scripts/ahrefs-api.py
└── MANDATORY when MCP fails
```

**CRITICAL RULE:** Never proceed without real keyword data.

### Python Fallback Commands

```bash
# Keyword overview
python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview \
  '{"select":"keyword,volume,difficulty,traffic_potential","country":"us","keywords":"nfl betting sites"}'

# Related keywords
python3 .claude/scripts/ahrefs-api.py keywords-explorer/related-terms \
  '{"select":"keyword,volume,difficulty","country":"us","keywords":"nfl betting sites","limit":20}'

# Competitor analysis
python3 .claude/scripts/ahrefs-api.py site-explorer/organic-keywords \
  '{"select":"keyword,volume,position,traffic","target":"actionnetwork.com","date":"2025-12-01","country":"us","limit":50}'
```

**ANTI-PATTERN:** Using estimated volumes when fallback is available = FAILURE.

---

## PROTECTED FEATURE 6: FAQ GENERATION FROM PAA

### People Also Ask (PAA) Mining

**Minimum:** 7 FAQ questions per brief
**Sources:**
1. Ahrefs PAA data (keywords-explorer queries)
2. Competitor FAQ sections (web_fetch)
3. Reddit question patterns
4. State-specific variations

**Keyword Mapping:**
```
Secondary Keyword Volume → FAQ Placement
├── 500+/mo → Dedicated H2 section
├── 200-500/mo → H2 or H3 section
├── 100-200/mo → H3 subsection
└── 50-100/mo → FAQ or natural content
```

**FAQ Quality Requirements:**
- Questions must target real search queries
- Answers must be 75-150 words (not one-liners)
- Include keyword variations naturally
- Link to related internal pages

**Example FAQ Structure:**
```markdown
### Is FanDuel legal in my state?

FanDuel Sportsbook operates legally in 21+ states including [list].
Legal status depends on your location's gambling regulations. The app
uses geolocation to verify you're within a legal jurisdiction before
allowing betting. [150 words total with state list and requirements]
```

---

## PROTECTED FEATURE 7: PHASE 3 PARALLEL SUB-AGENT SYSTEM

### Why 7 Sub-Agents?

**Problem:** Single agent Phase 3 = 40K+ tokens → Exceeds 32K limit → Truncated output

**Solution:** Split into 7 parallel agents using Haiku model

```
Phase 3 Orchestrator
    ↓
    ├─→ [3A] Meta + Badges + Disclosure (Haiku)
    ├─→ [3B] Comparison Table (Haiku)
    ├─→ [3C] Brand Cards (Haiku)
    ├─→ [3D] T&Cs Brands 1-5 (Haiku)
    ├─→ [3E] T&Cs Brands 6-10 (Haiku)
    ├─→ [3F] Schema Markup (Haiku)
    └─→ [3G] Interactive Elements + Responsible Gambling (Haiku)

    ↓ All complete (parallel execution)

    Concatenate → output/[page]-ai-enhancement.md
```

**CRITICAL RULES:**
1. All 7 sub-agents spawned in SINGLE message (parallel execution)
2. Each uses H2 headings (## not #) to prevent markdown lint errors
3. Concatenation order: 3A → 3B → 3C → 3D → 3E → 3F → 3G
4. Cleanup temp files after concatenation
5. Fix heading levels in final file

**Token Distribution:**
- 3A: ~2,500 tokens
- 3B: ~4,000 tokens (comparison table)
- 3C: ~6,000 tokens (brand cards)
- 3D: ~5,000 tokens (T&Cs 1-5)
- 3E: ~5,000 tokens (T&Cs 6-10)
- 3F: ~3,000 tokens (schema)
- 3G: ~4,000 tokens (interactive)
- **Total: ~29,500 tokens** (fits within limits when split)

---

## PROTECTED FEATURE 8: LETTER BADGE SYSTEM (NO IMAGES)

### Why No Logo Images?

**Problems with image logos:**
- 404 errors when paths change
- Slow loading times
- Accessibility issues
- Dreamweaver path conflicts

**Solution:** Text-based letter badges

```css
.letter-badge {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 16px;
    color: white;
    flex-shrink: 0;
}

/* Brand Colors */
.badge-fd { background: #1493FF; }  /* FanDuel - Blue */
.badge-mgm { background: #C4A137; } /* BetMGM - Gold */
.badge-365 { background: #027B5B; } /* Bet365 - Green */
.badge-dk { background: #53D337; }  /* DraftKings - Green */
.badge-scr { background: #6B2D5B; } /* theScore BET - Purple */
.badge-czr { background: #0A2240; } /* Caesars - Navy */
.badge-fan { background: #004C91; } /* Fanatics - Blue */
.badge-brv { background: #1E5AA8; } /* BetRivers - Blue */
.badge-hrb { background: #000000; } /* Hard Rock - Black */
.badge-bor { background: #8B0000; } /* Borgata - Red */
```

**HTML Usage:**
```html
<div class="letter-badge badge-fd">FD</div>
<div class="letter-badge badge-mgm">MGM</div>
```

---

## PROTECTED FEATURE 9: GOLD STANDARD TEMPLATES

### Mandatory HTML Patterns

**CRITICAL:** All Phase 3 output MUST use these exact patterns.

#### 1. Comparison Table
```html
<div class="wc-comparison">
    <div class="table-header">
        <h2>Top [N] [Topic] Betting Sites</h2>
    </div>
    <div class="mobile-scroll-hint">
        ⟵ Swipe left to see full details ⟶
    </div>
    <table class="comparison-table">
        <!-- Complete table with ALL brands -->
    </table>
</div>
```

#### 2. Brand Cards (Expandable)
```html
<div class="brand-cards-container">
    <div class="brand-card">
        <div class="brand-header">
            <div class="letter-badge badge-fd">FD</div>
            <h3>FanDuel Sportsbook</h3>
            <span class="rating">4.8★</span>
        </div>
        <div class="brand-features">
            <!-- Complete features list -->
        </div>
        <div class="pros-cons">
            <!-- Complete pros/cons -->
        </div>
        <div class="mobile-experience">
            <!-- 100-150 words on mobile app -->
        </div>
    </div>
</div>
```

#### 3. JavaScript Placement
```html
<head>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        console.log('✅ Interactive elements initialized');

        // ALL JavaScript in ONE block
        initComparisonTable();
        initBrandCards();
        initStateFilter();
        initFAQAccordion();
    });
    </script>
</head>
```

**FORBIDDEN:**
- ❌ Inline JavaScript in body
- ❌ Multiple script tags
- ❌ localStorage/sessionStorage usage
- ❌ max-width CSS on elements

**WHY:** Dreamweaver compatibility + team feedback.

---

## PROTECTED FEATURE 10: MANDATORY CONTENT SECTIONS

### Every Brief Must Include

#### Per-Brand Sections (3 Required)
1. **Key Features** (150-200 words)
   - Unique selling points
   - Feature comparison to competitors
   - User experience highlights

2. **Mobile Experience** (100-150 words)
   - App Store ratings
   - iOS vs Android features
   - Mobile-exclusive features
   - App performance notes

3. **Pros/Cons** (100-150 words)
   - Minimum 3 pros, 3 cons each
   - Citation sources (Reddit, App Store)
   - Balanced perspective

#### Page-Wide Sections (Mandatory)
1. **Payment Methods Comparison**
   - Table format
   - All brands side-by-side
   - Withdrawal times
   - Fees (if any)

2. **Calculator Tool Links**
   - Odds calculator
   - Parlay calculator
   - Bonus calculator
   - Links to site tools

3. **Compliance Footer**
   - Age requirements (21+ or 18+)
   - 1-800-522-4700 hotline
   - Affiliate disclosure
   - Responsible gambling section

**WHY PROTECTED:** Missing sections = incomplete brief = writer confusion.

---

## PROTECTED FEATURE 11: COMPETITOR ANALYSIS PROTOCOL

### Who to Analyze (Affiliate Sites Only)

**✅ Analyze These:**
- actionnetwork.com
- covers.com
- thelines.com
- sportsbookreview.com
- sportshandle.com
- legalsportsreport.com

**❌ NEVER Analyze These:**
- fanduel.com (brand site, not affiliate)
- draftkings.com (brand site)
- betmgm.com (brand site)

**WHY:** Brand sites optimize for conversion. Affiliate sites optimize for SEO. We need SEO patterns.

### Analysis Checklist

**For #1 Ranking Page:**
```
[ ] Number of brands covered
[ ] Word count estimate
[ ] H2/H3 structure pattern
[ ] Sections per brand
[ ] Interactive elements used
[ ] FAQ count
[ ] Internal linking strategy
[ ] Schema markup present
```

**Match or Exceed #1:**
- Brand count: Match or +1-2
- Word count: +10% over competitor average
- Sections: Match all common H2s
- FAQs: Match or exceed count

---

## PROTECTED FEATURE 12: VALIDATION GATES

### Phase 1 Minimums

```bash
# Validation command
bash scripts/validate-phase.sh 1 [page-name]
```

**Requirements:**
- [ ] Primary keyword with REAL volume (not estimated)
- [ ] 8-15 secondary keywords with volume data
- [ ] 3 competitor analyses complete
- [ ] 5-7 brands selected with rationale
- [ ] Content gaps identified
- [ ] phase1.json contains all required keys
- [ ] brief-control-sheet.md is 600-800 words

### Phase 2 Minimums

```bash
# Validation command
bash scripts/validate-phase.sh 2 [page-name]
```

**Requirements:**
- [ ] All secondary keywords mapped to sections
- [ ] 7+ FAQ questions with keyword targets
- [ ] TIER 1 source requirements specified
- [ ] Word count targets per section
- [ ] 12+ internal links planned
- [ ] Mobile Experience section per brand
- [ ] Payment methods section planned
- [ ] Calculator tool links included

### Phase 3 Minimums

```bash
# Validation command
bash scripts/validate-phase.sh 3 [page-name]
```

**Requirements:**
- [ ] Complete meta tags (title, description, OG, Twitter)
- [ ] Last Updated badge HTML
- [ ] Comparison table (Gold Standard Template)
- [ ] T&Cs for ALL brands (not just top 3)
- [ ] Schema markup (Article + FAQ + Breadcrumb)
- [ ] Interactive element with working code
- [ ] Compliance sections (disclosure + responsible gambling)
- [ ] ZERO placeholders ("..." or "[Insert]")

**ANTI-PATTERN:** Proceeding to next phase without validation = cascading failures.

---

## PROTECTED FEATURE 13: FEEDBACK INGESTION SYSTEM

### Continuous Improvement Loop

```
[User submits feedback]
    ↓
[Stored in: feedback/submitted/]
    ↓
[Weekly validation review]
    ↓
[Moved to: feedback/validated/]
    ↓
[Run: python3 scripts/ingest-feedback.py --update-lessons]
    ↓
[Updates: references/lessons-learned.md]
    ↓
[Next brief uses improved instructions]
```

### Feedback Categories

| Category | Routes To | Purpose |
|----------|-----------|---------|
| `keyword` | phase1-research.md | Missing keywords, cannibalization |
| `writer` | phase2-writer.md | Unclear instructions, gaps |
| `technical` | phase3-technical.md | HTML bugs, schema errors |
| `template` | content-templates.md | Outline structure issues |
| `workflow` | ORCHESTRATOR.md | Process bottlenecks |
| `edge-case` | lessons-learned.md | Unusual scenarios |

### Slash Command Integration

```
/submit-feedback [category]
```

**After EVERY brief completion, prompt:**
```
Task Complete! Help us improve:
- /submit-feedback - Report issues or suggestions
- Quick rating: Was this brief generation smooth? (1-5)
```

**WHY PROTECTED:** This is the ONLY project with automated feedback ingestion.

---

## PROTECTED FEATURE 14: DREAMWEAVER COMPATIBILITY

### Technical Constraints

**CRITICAL:** Dev team uses Dreamweaver. Modern JS patterns break their workflow.

#### JavaScript Rules
```html
<head>
    <script>
    // ✅ CORRECT - All in head, DOMContentLoaded wrapper
    document.addEventListener('DOMContentLoaded', function() {
        // All interactive code here
    });
    </script>
</head>

<body>
    <!-- ❌ WRONG - No inline scripts -->
    <script>
        function someFunction() { }
    </script>
</body>
```

#### CSS Rules
```css
/* ❌ FORBIDDEN */
.some-element {
    max-width: 1200px;  /* Breaks site layout */
}

/* ✅ REQUIRED */
.some-element {
    width: 100%;  /* Let site handle max-width */
}
```

#### HTML Rules
```html
<!-- ❌ FORBIDDEN - Dreamweaver path issues -->
<img src="../../images/logo.png">

<!-- ✅ REQUIRED - Letter badges instead -->
<div class="letter-badge badge-fd">FD</div>
```

---

## PROTECTED FEATURE 15: ESPN BET → theScore BET REBRAND

### Critical Brand Change (December 2025)

**OLD:** ESPN BET (shut down December 1, 2025)
**NEW:** theScore BET

**Update Requirements:**
- Letter badge: SCR (not ESPN)
- Color: #6B2D5B (purple)
- Full name: "theScore BET" (not "TheScore Bet")
- All historical references updated

**Legacy Content:**
```markdown
❌ "ESPN BET offers..."
✅ "theScore BET (formerly ESPN BET) offers..."
```

**NEW Content:**
```markdown
✅ "theScore BET offers..."
(No mention of ESPN BET needed)
```

---

## ANTI-PATTERNS (NEVER DO THESE)

### 🚫 Pattern 1: Single-Phase Brief
```
User: Generate brief for nfl-betting-sites
Agent: [Creates only writer-brief.md]
```
**WHY WRONG:** Missing research data + missing technical specs = incomplete.

### 🚫 Pattern 2: Skipping Ahrefs on MCP Fail
```
Agent: "Ahrefs MCP returned 403, using estimated volumes..."
```
**WHY WRONG:** Python fallback exists and MUST be used.

### 🚫 Pattern 3: Placeholders in Phase 3
```html
<table>
    <tr><td>FanDuel</td></tr>
    <!-- ... remaining brands ... -->
</table>
```
**WHY WRONG:** Team feedback rule #1 - NEVER shorten or skip content.

### 🚫 Pattern 4: Generic Brand Selection
```
"Selected top 7 brands: FanDuel, BetMGM, DraftKings, Bet365,
Caesars, Fanatics, BetRivers (because they're popular)"
```
**WHY WRONG:** Must have data-driven rationale with Ahrefs keyword volumes.

### 🚫 Pattern 5: Single Agent Phase 3
```
Agent: "Generating complete Phase 3 output..."
[32K token limit exceeded → truncated]
```
**WHY WRONG:** Must split into 7 sub-agents.

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-08 | Initial orchestrator with 3-phase workflow |
| 1.1 | 2025-12-09 | Added Phase 3 parallel sub-agents |
| 1.2 | 2025-12-10 | ESPN BET → theScore BET rebrand |
| 1.3 | 2025-12-11 | Mobile Experience + Payment sections mandatory |
| 1.4 | 2025-12-12 | Core specialization documentation created |

---

## MODIFICATION POLICY

**⚠️ PROTECTED FEATURES CANNOT BE MODIFIED WITHOUT:**

1. Team consensus (Lewis, Tom, Gustavo, Daniel)
2. Impact analysis document
3. Rollback plan
4. Testing on 3 sample briefs
5. Approval from project owner

**Unauthorized modifications will break:**
- Writer workflows (Phase 2 dependencies)
- Developer implementation (Phase 3 specs)
- SEO performance (keyword research)
- Token limits (Phase 3 splitting)

---

## CROSS-PROJECT DIFFERENCES

### Content Briefs vs Betting Pages Agent

| Feature | Content Briefs | Betting Pages |
|---------|----------------|---------------|
| **Input** | URL from site structure | Existing HTML file |
| **Output** | 3 brief documents | Optimized HTML file |
| **Phase Count** | 3 phases (research → writer → technical) | 1 phase (optimize) |
| **Ahrefs Use** | Extensive (15+ queries) | Minimal (verify only) |
| **Target User** | Writers + Developers | SEO team |
| **Preserves Content** | N/A (creates new) | YES (critical rule) |
| **HTML Structure** | Specs only | Must preserve exact template |

### Content Briefs vs State Hubs Agent

| Feature | Content Briefs | State Hubs |
|---------|----------------|------------|
| **Scope** | Any betting page | State-specific only |
| **Brand Count** | 5-10 (research-driven) | State-available only |
| **Legal Section** | Brief mention | Extensive legal analysis |
| **Calculator Tools** | Links only | State-specific calculators |
| **Compliance** | Federal + General | State-specific laws |

---

## QUICK REFERENCE

### When User Says: "/generate-brief [URL]"

**Execute Immediately (DO NOT ask for clarification):**

1. ✅ Extract page name from URL
2. ✅ Read ORCHESTRATOR.md
3. ✅ Spawn Phase 1 agent (research)
4. ✅ Validate Phase 1 outputs
5. ✅ Spawn Phase 2 agent (writer brief)
6. ✅ Validate Phase 2 outputs
7. ✅ Spawn 7 Phase 3 sub-agents (parallel)
8. ✅ Concatenate Phase 3 outputs
9. ✅ Validate Phase 3 output
10. ✅ Convert all to DOCX
11. ✅ Report completion

**Total Time:** 25-40 minutes
**Total Outputs:** 6 files (3 .md + 3 .docx)

---

## MAINTENANCE SCHEDULE

**Weekly:**
- [ ] Review feedback submissions
- [ ] Update lessons-learned.md
- [ ] Validate Ahrefs connectivity

**Monthly:**
- [ ] Review brand positioning (any new brands?)
- [ ] Update bonus data in reference-library.md
- [ ] Check for ESPN→theScore references

**Quarterly:**
- [ ] Competitor analysis refresh
- [ ] Template pattern updates
- [ ] Workflow optimization review

---

## CONCLUSION

**This document protects 15 core features that make this project unique.**

**If you modify ANY protected feature without approval:**
- Writers will be confused (broken Phase 2)
- Developers can't implement (broken Phase 3)
- SEO will suffer (broken Phase 1)
- Token limits will break (broken Phase 3 splitting)
- Feedback loop will break (broken ingestion)

**When in doubt, ask before changing protected features.**

---

**Document Custodian:** Andre Borg
**Review Frequency:** Quarterly
**Next Review:** 2025-03-12
