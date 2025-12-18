# TES Skills Library

**7 Foundational Skills for Autonomous Learning & Optimization**

This skills library provides modular, reusable knowledge components that Claude can reference during page optimization tasks. Each skill is self-contained with validation rules, examples, anti-patterns, and success criteria.

## How to Use Skills

Skills are automatically available to Claude during optimization tasks. Reference them when:
- Starting a new optimization
- Troubleshooting issues
- Validating output quality
- Learning from past mistakes

## The 7 Core Skills

### 1. [Validation HTML Structure](validation-html-structure.md)
**Purpose:** Validate TopEndSports HTML structure to prevent layout-breaking issues

**Use When:**
- Before delivering optimized files
- Creating new page templates
- Debugging layout issues

**Critical Rules:**
- Uses `id="content"` NOT `class="content"`
- Proper container > content + grouping hierarchy
- All 6 library items present in correct order
- All JavaScript in HEAD section

---

### 2. [Content Preservation](content-preservation.md)
**Purpose:** Preserve Rob Wood's expert content while optimizing for SEO

**Use When:**
- Optimizing pages with expert content
- Adding keywords to existing content
- Rewriting headings

**The Golden Rule:**
- ADD to content, don't REPLACE it
- ENHANCE structure, don't REWRITE substance
- OPTIMIZE headings, but PRESERVE paragraphs

---

### 3. [SEO Keyword Integration](seo-keyword-integration.md)
**Purpose:** Integrate keywords naturally without AI patterns or keyword stuffing

**Use When:**
- After completing keyword research
- Optimizing headings and content
- Writing title tags and meta descriptions

**Key Principles:**
- Natural placement > keyword density
- Avoid AI patterns (heavy colons, formulaic headings)
- Primary in H1, first paragraph, conclusion
- Secondary distributed across H2s and body

---

### 4. [Internal Linking Strategy](internal-linking-strategy.md)
**Purpose:** Add high-value internal links using ONLY verified URLs

**Use When:**
- Adding contextual links
- Improving page authority distribution
- Before final delivery

**Critical Rules:**
- VERIFIED URLs ONLY (if not on list, ASK FIRST)
- Maximum 3-4 instances per link
- Vary anchor text
- No clustering (distribute across sections)

---

### 5. [CTA Placement Strategy](cta-placement-strategy.md)
**Purpose:** Place CTAs that convert without harming user experience

**Use When:**
- Adding affiliate links
- Improving conversion rates
- Final layout review

**The Value-First Rule:**
- FIRST CTA after minimum 400 words
- NO CTAs above the fold
- Distribute throughout (not clustered)
- Vary messaging (early vs middle vs late)

---

### 6. [Interactive Elements](interactive-elements.md)
**Purpose:** Add 7 types of interactive elements that enhance engagement

**Use When:**
- Pages over 1,500 words (minimum 3-4 elements)
- Breaking up text-heavy content
- Improving mobile user experience

**7 Element Types:**
1. Decision Tool / Flowchart
2. Interactive Checklist
3. Scenario Cards
4. Stat Callout Boxes
5. Definition Boxes
6. Key Takeaway Boxes
7. Comparison Tables

---

### 7. [Research Workflow](research-workflow.md)
**Purpose:** Complete 4-phase workflow from research to delivery

**Use When:**
- Starting any optimization project
- Coordinating multiple skills
- Ensuring systematic quality

**4 Phases:**
1. Pre-Optimization Research (10-15 min)
2. Optimization Planning (10-15 min)
3. Implementation (30-45 min)
4. Validation & Delivery (10-15 min)

---

## Skill Dependencies

```
research-workflow.md (MASTER SKILL)
    ├── Phase 1: Research
    │   ├── Uses: seo-keyword-integration.md
    │   └── Checks: content-preservation.md
    │
    ├── Phase 2: Planning
    │   ├── Uses: seo-keyword-integration.md
    │   ├── Uses: internal-linking-strategy.md
    │   ├── Uses: cta-placement-strategy.md
    │   └── Uses: interactive-elements.md
    │
    ├── Phase 3: Implementation
    │   ├── Uses: validation-html-structure.md
    │   ├── Uses: content-preservation.md
    │   ├── Uses: seo-keyword-integration.md
    │   ├── Uses: internal-linking-strategy.md
    │   ├── Uses: cta-placement-strategy.md
    │   └── Uses: interactive-elements.md
    │
    └── Phase 4: Validation
        ├── Uses: validation-html-structure.md
        ├── Uses: content-preservation.md
        ├── Uses: seo-keyword-integration.md
        ├── Uses: internal-linking-strategy.md
        └── Uses: cta-placement-strategy.md
```

## Quick Reference

| Need to... | Use This Skill |
|------------|----------------|
| Fix broken layout | validation-html-structure.md |
| Add keywords naturally | seo-keyword-integration.md |
| Preserve expert content | content-preservation.md |
| Add internal links safely | internal-linking-strategy.md |
| Place CTAs effectively | cta-placement-strategy.md |
| Break up text walls | interactive-elements.md |
| Complete full optimization | research-workflow.md |

## Validation Workflow

**For every optimization, validate using:**

1. **Structure** → validation-html-structure.md
2. **Content Integrity** → content-preservation.md
3. **Keyword Quality** → seo-keyword-integration.md
4. **Link Safety** → internal-linking-strategy.md
5. **CTA Placement** → cta-placement-strategy.md
6. **UX Enhancement** → interactive-elements.md

## Success Metrics

Skills are working when:
- [ ] All optimizations pass validation checks
- [ ] No layout-breaking errors
- [ ] Expert content always preserved
- [ ] Keywords integrated naturally
- [ ] No 404 errors from internal links
- [ ] CTAs placed value-first
- [ ] Engaging interactive elements
- [ ] Consistent quality across all pages

## Continuous Improvement

**These skills evolve based on feedback:**
- Feedback submitted via `/submit-feedback`
- Weekly processing updates skill documentation
- Lessons learned incorporated automatically
- Anti-patterns added to prevent future issues

**See:** Each repository's `feedback/` directory for submission guidelines

---

**Last Updated:** December 18, 2025
**Version:** 1.0
**Status:** Foundation deployment across 5 TES repositories
