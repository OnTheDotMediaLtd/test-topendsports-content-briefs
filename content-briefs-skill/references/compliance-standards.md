# Compliance Standards

**Purpose:** Ensure all content meets legal, accessibility, and quality standards
**Source:** Team feedback compilation (December 2024)
**Priority:** CRITICAL - Violations can have legal consequences

---

## 1. Gambling Language Compliance

### BANNED PHRASES (Never Use)

| ❌ BANNED | ✅ USE INSTEAD |
|-----------|----------------|
| guaranteed profit | potential opportunity |
| guaranteed win | potential win |
| risk-free | optimized |
| sure thing | strong option |
| 100% win | high probability |
| always win | may win |
| you will win | you could win |
| can't lose | reduced risk |
| certain outcome | possible outcome |
| definite return | estimated return |
| Elite Performance! | Strong Performance |
| maximize profits | aims to balance |
| exact payouts | potential payouts |

### Pre-Output Compliance Check
- [ ] No "guaranteed" language
- [ ] No "risk-free" claims
- [ ] No absolute certainty language
- [ ] No fabricated statistics
- [ ] Disclaimer present on betting content

### Required Disclaimers
```
Gambling involves risk. Please gamble responsibly.
Problem Gambling? Call 1-800-522-4700
21+ (18+ in some states). Terms apply.
```

---

## 2. No Fabricated Data Policy

### PROHIBITED (Zero Tolerance)
- ❌ Fabricated reader counts ("🔥 2,847 readers today")
- ❌ Invented aggregate ratings in schema
- ❌ Fake "trending now" indicators
- ❌ Made-up member numbers ("Join 15,000+ members")
- ❌ Artificial social proof
- ❌ Fake review counts

### Schema Markup Rules
- Do NOT include AggregateRating unless data is REAL
- Remove ratingValue/reviewCount if not verified
- Only use statistics from verified sources

---

## 3. Accessibility Standards (WCAG AA)

### Color Contrast Requirements

**TES Accessible Color Palette:**
```css
/* Primary - Use These */
--primary-green: #2e7d32;      /* Passes AA */
--primary-green-dark: #1b5e20; /* Passes AA */
--text-primary: #333333;       /* Passes AA */
--text-secondary: #495057;     /* Passes AA */

/* DO NOT USE */
/* #6c757d - Fails contrast on white background */
/* #28a745 - May fail on some backgrounds */
```

### Typography Requirements
- Minimum 16px base font on mobile
- Line height minimum 1.5
- Sufficient color contrast (4.5:1 for normal text)

### Touch Target Requirements
- Minimum 44px × 44px for all interactive elements
- Adequate spacing between touch targets

### ARIA Requirements
- ARIA labels on all interactive elements
- Proper heading hierarchy (H1 → H2 → H3)
- Alt text on all images

---

## 4. External Link Standards

### All External Links Must Have:
```html
<a href="[URL]" target="_blank" rel="noopener">Link Text</a>
```

### Affiliate Links Must Have:
```html
<a href="[URL]" target="_blank" rel="nofollow noopener">Link Text</a>
```

### Internal Links Format:
```html
<!-- Always use complete paths with index.htm -->
<a href="/sport/betting/index.htm">Link Text</a>

<!-- NOT -->
<a href="/sport/betting/">Link Text</a>
```

---

## 5. Schema Markup Standards

### Required Schema Types by Page

| Page Type | Required Schema |
|-----------|----------------|
| Article/Content | Article, BreadcrumbList |
| FAQ present | FAQPage |
| Event pages | SportsEvent |
| Review pages | Review (NO fake ratings) |

### AI/LLM Optimization for Schema

To ensure content is properly understood by AI systems and LLMs:

1. **Structured Data Completeness**
   - Include all relevant schema properties
   - Use specific types (e.g., `SportsOrganization` not just `Organization`)
   - Include `mainEntity` relationships

2. **Content Signals for AI**
   ```json
   {
     "@type": "Article",
     "headline": "[Clear, descriptive headline]",
     "description": "[Comprehensive summary]",
     "about": {
       "@type": "Thing",
       "name": "[Primary topic]"
     },
     "mentions": [
       {"@type": "SportsOrganization", "name": "FanDuel"},
       {"@type": "SportsOrganization", "name": "DraftKings"}
     ],
     "keywords": "[comma-separated keywords]"
   }
   ```

3. **Entity Recognition Helpers**
   - Use `@type` for all entities (brands, people, places)
   - Include `sameAs` links to official sources
   - Provide `description` for key entities

4. **FAQ Schema for AI Understanding**
   ```json
   {
     "@type": "FAQPage",
     "mainEntity": [
       {
         "@type": "Question",
         "name": "[Question text]",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "[Complete answer with key facts]"
         }
       }
     ]
   }
   ```

5. **Semantic Relationships**
   - Link related content with `relatedLink`
   - Use `isPartOf` for series/collections
   - Include `author` with credentials for E-E-A-T

### Schema Validation
- [ ] Correct schema type for page type
- [ ] All required fields present
- [ ] NO fabricated data (ratings, reviews, stats)
- [ ] Validates against Schema.org
- [ ] JSON-LD properly formatted
- [ ] Entity types specified for AI/LLM understanding

---

## 6. Content Preservation Policy

### CRITICAL RULES
- **DO NOT modify H1 and H2 headings** unless explicitly requested
- **DO NOT correct typos, formatting, spacing, structure** unless explicitly requested
- **DO NOT auto-correct** anything without user permission
- Preserve ALL original content
- Only make changes that are specifically requested

### When Fixing Technical Issues
- Fix ONLY the technical issue (sidebar, CSS, etc.)
- Preserve ALL content exactly as-is
- Document any necessary content changes before making them

---

## Pre-Output Compliance Checklist

Before outputting any code:

- [ ] No banned gambling language
- [ ] No fabricated statistics or ratings
- [ ] Color contrast meets WCAG AA
- [ ] Touch targets minimum 44px
- [ ] External links have proper attributes
- [ ] Schema markup validated
- [ ] AI/LLM schema optimization applied
- [ ] Original content preserved
- [ ] Required disclaimers present

---

**Document Version:** 1.0
**Last Updated:** December 2024
