# Research Workflow Skill

## Description
Complete 4-phase workflow for page optimization, from initial research through final delivery. Ensures systematic, high-quality optimization that incorporates GSC data, Ahrefs research, content preservation, and validation.

## When to Use This Skill
- Starting any page optimization project
- When user provides HTML to optimize
- For systematic, repeatable optimization process
- When coordinating multiple optimization skills
- To ensure no steps are skipped

## The 4-Phase Workflow

### Phase 1: Pre-Optimization Research (10-15 minutes)

**Purpose:** Gather data before making changes

#### Step 1.1: Search Intent Analysis

**Identify primary search intent:**
- **INFORMATIONAL:** "how to", "what is", "guide", "explained"
- **COMMERCIAL:** "best", "top", "comparison", "vs", "review"
- **TRANSACTIONAL:** "buy", "sign up", "get bonus", "promo code"

**Match content structure to intent:**
- Informational → Deep explanations, expert analysis, educational structure
- Commercial → Comparison tables, pros/cons, rankings, CTAs
- Transactional → Quick info, prominent CTAs, trust signals, urgency

#### Step 1.2: Google Search Console Analysis

**Analyze GSC data for:**

| Signal | Meaning | Action |
|--------|---------|--------|
| High impressions + Low clicks | CTR problem | Optimize title tag & meta description |
| High impressions + Position 10-20 | Almost there | Add keyword to H1, H2s, intro |
| Position 4-10 | Push-up opportunity | Strengthen content for that keyword |
| Position 1-3 + Low CTR | Title not compelling | Rewrite title with power words |
| Queries you don't target | Content gap | Add section addressing that query |

**Priority Keywords:**
1. High impressions + Position 5-15 = BEST opportunities
2. High impressions + 0 clicks = CTR crisis (fix title/meta)
3. Position 11-20 with decent volume = Quick wins

#### Step 1.3: Ahrefs Research

**Run these queries:**

**STEP 1: Current Page Performance**
Tool: `site-explorer-organic-keywords`
- Target: [PAGE URL]
- Select: keyword, position, volume, traffic, serp_features
- Look for: Keywords in position 5-20 (push-up targets)

**STEP 2: Keyword Metrics & Expansion**
Tool: `keywords-explorer-overview`
- Keywords: [PRIMARY TARGET KEYWORD]
- Country: us
- Select: keyword, volume, difficulty, cpc, parent_topic

Tool: `keywords-explorer-matching-terms`
- Keywords: [PRIMARY KEYWORD]
- Country: us
- Select: keyword, volume, difficulty
- Look for: Long-tail variations, question keywords for FAQ

Tool: `keywords-explorer-related-terms`
- Keywords: [PRIMARY KEYWORD]
- Country: us
- View_for: also_rank_for
- Look for: Keywords competitors rank for that we should include

**STEP 3: SERP Analysis**
Tool: `serp-overview-serp-overview`
- Keyword: [PRIMARY KEYWORD]
- Country: us
- Select: position, url, title, domain_rating, backlinks, traffic
- Look for: SERP features present, competitor content characteristics

**STEP 4: Competitor Analysis**
Tool: `site-explorer-organic-competitors`
- Target: [YOUR DOMAIN]
- Country: us
- Look for: Who ranks for similar keywords, content gaps

Tool: `site-explorer-top-pages` (on competitor domains)
- Target: [COMPETITOR DOMAIN]
- Look for: Their best pages on this topic, what makes them rank

**STEP 5: Cross-Reference Data**
- GSC shows what Google SHOWS the page for (actual impressions)
- Ahrefs shows what the page COULD rank for (market potential)
- Overlap = Validate and prioritize these opportunities
- Ahrefs-only = Content gaps to fill with NEW sections
- GSC-only = Quick wins (already indexed, optimize existing content)

#### Step 1.4: SERP Feature Targeting

**Check which SERP features appear for target keywords:**

| Feature | How to Target |
|---------|---------------|
| Featured Snippet | Add definition box, numbered list, or table that directly answers query |
| People Also Ask | Include those EXACT questions in FAQ section |
| Video Carousel | Embed relevant video content |
| Image Pack | Add images with descriptive alt text containing keywords |
| FAQ Rich Result | Implement FAQPage schema |
| How-To Rich Result | Implement HowTo schema with clear steps |

#### Step 1.5: Competitor Gap Analysis

**Check what top 3 ranking competitors include:**
- Topics/subtopics we're missing
- Types of media (videos, infographics, calculators, tools)
- Word count comparison
- Number and quality of internal/external links
- SERP features they're capturing
- Interactive elements they use

**Action:** Add missing elements as NEW sections (don't replace existing content)

#### Step 1.6: Keyword Cannibalization Check

**Before adding internal links, verify:**
- No other page on the site targets the same primary keyword
- If cannibalization exists, decide which page should be primary
- Internal links should use VARIED anchor text (not always exact match)
- The page being optimized is the BEST page for those keywords

#### Phase 1 Deliverables:
- [ ] Primary keyword identified with search intent
- [ ] GSC opportunities prioritized (5-10 keywords)
- [ ] Ahrefs data collected (secondary, long-tail, related terms)
- [ ] SERP features identified for targeting
- [ ] Competitor gaps documented
- [ ] Cannibalization check complete
- [ ] Content gaps list created

---

### Phase 2: Optimization Planning (10-15 minutes)

**Purpose:** Plan changes before executing

#### Step 2.1: Keyword Mapping

**Map keywords to specific locations:**

| Keyword Type | Where to Place |
|--------------|----------------|
| Primary (1) | H1, first paragraph, 2-3 H2s, conclusion, title tag, meta |
| Secondary (8-15) | H2s, body paragraphs, FAQ questions, image alt text |
| Long-tail (20-30) | H3s, FAQ questions, definition boxes, list items |
| Related (15-25) | Natural mentions throughout body content |

#### Step 2.2: Title Tag Optimization

**Create optimized title:**
- Under 60 characters
- Primary keyword near beginning
- Include year (2025) for freshness
- Use power words (Complete, Guide, Explained, Best)
- AVOID heavy colon usage (max 1)

**Formula:** `[Primary Keyword] - [Value Proposition] (Year)`

**Example:** "NBA Betting Strategy Guide - 10 Expert Tips (2025)"

#### Step 2.3: Heading Optimization

**Plan heading rewrites:**
- H1: Include primary keyword, make compelling
- H2s: Include secondary keywords, every 200-300 words
- H3s: Include long-tail keywords, answer specific questions

**Avoid AI patterns:**
- No "Understanding X: A Complete Guide" formulas
- No heavy colon usage
- Keep natural, conversational tone

#### Step 2.4: Internal Link Planning

**Identify 3-5 high-value link opportunities:**
- Use VERIFIED URLs from CLAUDE.md Section 5 only
- Maximum 3-4 instances of same link
- Vary anchor text
- Distribute throughout content (no clustering)

**Priority targets:**
1. Sportsbook reviews (FanDuel, BetMGM, DraftKings)
2. Promo code pages
3. Category pages (best-apps, compare-sportsbooks)
4. Sport-specific guides

#### Step 2.5: CTA Placement Planning

**Plan CTA locations:**
- FIRST CTA: After 400-500 words minimum
- SECOND CTA: After major comparison/analysis
- THIRD CTA: Before FAQ section
- FINAL CTA: After FAQ, before footer

**Plan messaging variation:**
- Early: "Compare Sportsbooks" / "See Bonuses"
- Middle: "Get Started" / "Claim Bonus"
- Late: "Start Betting Today" / "Don't Miss Out"

#### Step 2.6: Interactive Elements Planning

**For 1,500+ words, plan 3-4 elements:**
- Stat callout boxes (highlight key numbers)
- Definition boxes (explain terminology)
- Key takeaway boxes (section summaries)
- Interactive checklists (prep workflows)
- Scenario cards (example situations)
- Comparison tables (side-by-side features)

**Placement:** One element every 400-600 words, alternate types

#### Step 2.7: Content Gaps Planning

**Identify NEW sections to add:**
- Topics competitors have but we don't
- Questions from "People Also Ask"
- Long-tail keywords needing dedicated sections
- FAQ questions (minimum 5-7)

**Remember:** ADD sections, don't REPLACE existing expert content

#### Phase 2 Deliverables:
- [ ] Keyword mapping complete (all keywords assigned locations)
- [ ] Title tag and meta description drafted
- [ ] Heading optimization plan created
- [ ] 3-5 internal link opportunities identified (verified URLs)
- [ ] CTA placement locations marked (4 CTAs minimum)
- [ ] 3-4 interactive elements planned
- [ ] New content sections outlined (gaps to fill)
- [ ] FAQ questions drafted (5-7 minimum)

---

### Phase 3: Implementation (30-45 minutes)

**Purpose:** Execute optimization with preservation

#### Step 3.1: Site Structure Validation

**Ensure correct HTML structure FIRST:**
- Use `id="content"` NOT `class="content"`
- Use `id="container"` as wrapper
- Use `id="grouping"` for sidebar
- All 6 library items present in correct order
- Clearfix div before closing container

**See:** validation-html-structure.md skill

#### Step 3.2: Title Tag & Meta Implementation

**Update HEAD section:**
```html
<title>[Optimized Title under 60 chars]</title>
<meta name="description" content="[Optimized description under 155 chars]">
<link rel="canonical" href="[CANONICAL URL]">
```

#### Step 3.3: Heading Optimization

**Rewrite headings (preserve meaning):**
- H1: Include primary keyword
- H2s: Include secondary keywords
- H3s: Include long-tail keywords

**PRESERVE expert content paragraphs:**
- Only optimize opening sentences if needed
- Don't rewrite scientific explanations
- Keep research citations intact
- Maintain author voice

**See:** content-preservation.md skill

#### Step 3.4: Keyword Integration

**Add keywords naturally:**
- Primary in H1, first paragraph, conclusion
- Secondary in H2s and body
- Long-tail in H3s and FAQs
- Related terms sprinkled throughout

**AVOID:**
- Keyword stuffing
- Unnatural placement
- AI-generated patterns
- Heavy colon usage

**See:** seo-keyword-integration.md skill

#### Step 3.5: Internal Link Implementation

**Add links using verified URLs:**
- Add in transition sentences (not forced into existing text)
- Vary anchor text
- Maximum 3-4 instances per link
- Distribute across sections

**See:** internal-linking-strategy.md skill

#### Step 3.6: CTA Implementation

**Add CTA blocks:**
- First CTA after 400+ words
- Include responsible gambling disclaimer
- Affiliate links with rel="nofollow sponsored"
- Vary CTA messaging

**See:** cta-placement-strategy.md skill

#### Step 3.7: Interactive Elements Implementation

**Add elements:**
- All JavaScript in HEAD section (Dreamweaver compatibility)
- All CSS in HEAD section
- Mobile-optimized (touch-friendly)
- Alternate element types

**See:** interactive-elements.md skill

#### Step 3.8: Schema Markup Implementation

**Add schema types:**
1. **Article Schema** (all pages)
2. **BreadcrumbList Schema** (all pages)
3. **FAQPage Schema** (if FAQ present)
4. **HowTo Schema** (if step-by-step content)
5. **Speakable Schema** (for voice search)

#### Step 3.9: FAQ Section Implementation

**Add FAQ section:**
- Minimum 5-7 questions
- Use exact question phrases from keyword research
- Include FAQPage schema
- Answer concisely (50-150 words per answer)

#### Phase 3 Deliverables:
- [ ] HTML structure validated (id selectors, libraries, clearfix)
- [ ] Title tag and meta description implemented
- [ ] Headings optimized (keywords added, natural tone)
- [ ] Keywords integrated naturally throughout
- [ ] 3-5 internal links added (verified URLs, varied anchors)
- [ ] 4 CTAs placed strategically (value-first approach)
- [ ] 3-4 interactive elements added (HEAD scripts, mobile-friendly)
- [ ] Schema markup added (Article, FAQ, Breadcrumb)
- [ ] FAQ section implemented (5-7 questions minimum)
- [ ] Expert content preserved (no rewrites of scientific explanations)

---

### Phase 4: Validation & Delivery (10-15 minutes)

**Purpose:** Verify quality before delivery

#### Step 4.1: Structure Validation

**Run structure checks:**
- [ ] Uses `id="content"` NOT `class="content"`
- [ ] Uses `id="container"` as wrapper
- [ ] Has `id="grouping"` for sidebar
- [ ] All 6 library items present and correctly placed
- [ ] All JavaScript in HEAD section
- [ ] Has clearfix div before container close
- [ ] Proper nesting: container > content + grouping

#### Step 4.2: Link Validation

**Run link checks:**
- [ ] Every internal link uses VERIFIED URL from Section 5
- [ ] No invented or guessed URLs
- [ ] Maximum 3-4 instances of same internal link
- [ ] Affiliate links have `rel="nofollow sponsored"`
- [ ] No duplicate links within 200 words

#### Step 4.3: SEO Validation

**Run SEO checks:**
- [ ] Title tag under 60 characters
- [ ] Meta description under 155 characters
- [ ] H1 appears only ONCE
- [ ] Target keywords in H1, first paragraph, H2s
- [ ] Schema validates at schema.org/validator

#### Step 4.4: Content Validation

**Run content checks:**
- [ ] NO expert content removed or rewritten
- [ ] All "Athletic edge" paragraphs preserved
- [ ] Author voice maintained (not generic/AI-sounding)
- [ ] Research citations preserved
- [ ] All original sections present

#### Step 4.5: AI Pattern Validation

**Run AI pattern checks:**
- [ ] No heavy colon usage (max 1-2 per section)
- [ ] No repetitive sentence structures
- [ ] No formulaic headings ("Understanding X: A Complete Guide")
- [ ] Varied sentence lengths
- [ ] Natural, conversational tone

#### Step 4.6: UX Validation

**Run UX checks:**
- [ ] Quick Answer box present at top
- [ ] Table of Contents present
- [ ] First CTA not until after 400+ words
- [ ] CTAs distributed throughout (not clustered)
- [ ] Interactive elements present (3-4 minimum for long content)
- [ ] Visual breaks every 400-500 words
- [ ] Responsible gambling disclaimer with affiliate CTAs

#### Step 4.7: Technical Validation

**Run technical checks:**
- [ ] No truncation - file ends with `</body></html>`
- [ ] All library codes preserved exactly
- [ ] HTML validates (no unclosed tags)
- [ ] All interactive elements have JS in HEAD
- [ ] Mobile-friendly (tested on small screens)

#### Step 4.8: Final Quality Review

**Read entire page aloud:**
- Does it sound natural?
- Can you identify the author's voice?
- Are keywords integrated smoothly?
- Does content flow logically?

#### Phase 4 Deliverables:
- [ ] All validation checks passed (structure, links, SEO, content, UX, technical)
- [ ] No expert content removed or altered
- [ ] All keywords integrated naturally
- [ ] No AI-generated patterns detected
- [ ] File complete with no truncation
- [ ] Ready for delivery

---

## Time Estimates

| Phase | Estimated Time | Can Be Shortened By |
|-------|----------------|---------------------|
| Phase 1: Research | 10-15 minutes | Having GSC/Ahrefs data pre-loaded |
| Phase 2: Planning | 10-15 minutes | Using templates for common page types |
| Phase 3: Implementation | 30-45 minutes | Batch operations, code snippets |
| Phase 4: Validation | 10-15 minutes | Automated validation scripts |
| **TOTAL** | **60-90 minutes** | **Experience and tools** |

## When to Skip Phases

**NEVER skip Phase 1 (Research) or Phase 4 (Validation)**

**Can abbreviate Phase 2 (Planning) when:**
- Simple page with clear structure
- Similar to previously optimized pages
- User provides clear requirements

**Can abbreviate Phase 3 (Implementation) when:**
- Minor optimizations only
- No structural changes needed
- Content already high-quality

## Success Criteria

Workflow is successful when:

1. All 4 phases completed in order
2. All deliverables from each phase present
3. All validation checks pass
4. Expert content preserved
5. Keywords integrated naturally
6. Internal links use verified URLs
7. CTAs placed value-first
8. Interactive elements enhance UX
9. No AI-generated patterns
10. File complete and ready to deploy

## Common Mistakes to Avoid

### Mistake 1: Skipping Research Phase
```
WRONG: Start optimizing without GSC/Ahrefs data

RIGHT: Complete Phase 1 research before making any changes
```

### Mistake 2: Not Planning Before Implementing
```
WRONG: Add keywords and links randomly as you go

RIGHT: Map all keywords and links in Phase 2, then execute in Phase 3
```

### Mistake 3: Skipping Validation
```
WRONG: Deliver immediately after implementing changes

RIGHT: Run all validation checks in Phase 4 before delivery
```

### Mistake 4: Rewriting Expert Content
```
WRONG: Rewrite scientific explanations to add keywords

RIGHT: Preserve expert content, only add keywords to headings/transitions
```

## Related Skills

**This workflow coordinates ALL other skills:**
- validation-html-structure.md → Used in Phase 3.1 and Phase 4.1
- content-preservation.md → Used in Phase 3.3 and Phase 4.4
- seo-keyword-integration.md → Used in Phase 2.1, 3.4, and 4.3
- internal-linking-strategy.md → Used in Phase 2.4, 3.5, and 4.2
- cta-placement-strategy.md → Used in Phase 2.5, 3.6, and 4.6
- interactive-elements.md → Used in Phase 2.6, 3.7, and 4.6

**This is the MASTER skill that orchestrates all others.**
