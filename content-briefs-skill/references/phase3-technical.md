# Phase 3: Technical Protocol

**Input:** Brief Control Sheet + Writer Brief
**Output:** AI Enhancement Brief (5-8 pages with HTML)

---

## Step 1: Meta Tags (SERP-Optimized)

**Reference:** `references/meta-title-optimization.md`

### Critical Rules:
| Element | Requirement |
|---------|-------------|
| **Title** | < 60 chars, primary keyword at START, **NO YEAR** |
| **Description** | < 155 chars |

### Process:
1. Run SERP analysis for primary keyword (see meta-title-optimization.md)
2. Analyze top 10 competitor titles for patterns
3. Apply title formula based on page type
4. Verify character limits (title < 60, description < 155)

### Title Formula by Page Type:
| Page Type | Formula |
|-----------|---------|
| Comparison | `[Primary Keyword] \| [Count] [Modifier]` |
| Review | `[Brand] Review: [Key Benefit] + [Bonus Info]` |
| How-To | `How to [Action] in [Location] \| [Benefit]` |
| Hub/State | `[Primary Keyword]: [Key Info]` |

**Key Rule:** Primary keyword MUST be at the START of the title. NO YEAR.

### Output:
```html
<!-- Meta Title (XX chars) - keyword at start, NO YEAR -->
<title>[Primary Keyword] | [Differentiator]</title>

<!-- Meta Description (XXX chars) - under 155 -->
<meta name="description" content="[155 chars with primary keyword, unique value prop, specifics]">

<!-- Additional Meta Tags -->
<meta name="keywords" content="[ALL primary + secondary keywords]">
<meta name="author" content="[Lewis/Tom/Gustavo]">
<link rel="canonical" href="https://www.topendsports.com/sport/betting/[market]/[page].htm">

<!-- Open Graph Tags -->
<meta property="og:title" content="[Title]">
<meta property="og:description" content="[Description]">
<meta property="og:type" content="article">
<meta property="og:url" content="[Canonical URL]">
```

### SERP Analysis to Document:
```markdown
## SERP Title Analysis
- Competitor pattern: [what top 10 titles have in common]
- Our differentiation: [what we add that's unique]
- Power words used: [Best, Top, Expert, etc.]
- Keyword placement: [how competitors start titles]
```

---

## Step 2: Last Updated Badge (ALWAYS FIRST)

Place immediately after H1:

```html
<div style="background: #e8f5e9; padding: 0.75rem 1.25rem; border-left: 4px solid #2e7d32; margin-bottom: 1.5rem; border-radius: 4px;">
  <p style="margin: 0; font-size: 14px; color: #2e7d32;">
    <strong>✓ Last Updated:</strong> [Current Date]
  </p>
</div>
```

---

## Step 3: Comparison Table

```html
<div style="overflow-x: auto; margin: 2rem 0;">
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr style="background: #2e7d32;">
        <th style="color: white; padding: 1rem; text-align: left;">Sportsbook</th>
        <th style="color: white; padding: 1rem; text-align: left;">Best For</th>
        <th style="color: white; padding: 1rem; text-align: left;">Current Bonus</th>
        <th style="color: white; padding: 1rem; text-align: center;">Rating</th>
      </tr>
    </thead>
    <tbody>
      <tr style="background: #f9f9f9;">
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;"><strong>FanDuel</strong></td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;">[USP]</td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;">[Bonus]*</td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd; text-align: center;">⭐⭐⭐⭐⭐</td>
      </tr>
      <!-- Continue for all brands -->
    </tbody>
  </table>
  <p style="font-size: 12px; color: #666;">*21+ only. T&Cs apply.</p>
</div>
```

---

## Step 4: Quick Answer Box

```html
<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left: 4px solid #2e7d32; padding: 1.5rem; margin: 2rem 0; border-radius: 8px;">
  <h2 style="color: #2e7d32; margin-top: 0; font-size: 1.25rem;">Quick Answer</h2>
  <p style="font-size: 1.1rem; margin-bottom: 1rem;">[Direct 2-3 sentence answer]</p>
  <ul style="line-height: 1.8; margin: 0; padding-left: 1.25rem;">
    <li><strong>[Key fact 1]</strong></li>
    <li><strong>[Key fact 2]</strong></li>
  </ul>
</div>
```

---

## Step 5: Complete T&Cs Section

**Required for:** Template 1, 2, 4 (Reviews, Comparisons, State Pages)

```html
<div style="background: #f8f9fa; padding: 2rem; margin: 2rem 0; border-radius: 8px; border: 2px solid #2e7d32;">
  
  <h3 style="margin-top: 0; color: #2e7d32;">Complete Bonus Terms & Conditions</h3>
  
  <h4 style="color: #333; border-bottom: 2px solid #2e7d32; padding-bottom: 0.5rem;">[Brand Name]</h4>
  
  <div style="background: #e8f5e9; padding: 1.25rem; border-radius: 6px; margin: 1rem 0;">
    <p style="margin: 0; font-weight: 600; color: #2e7d32; font-size: 16px;">
      [EXACT BONUS TEXT - VERBATIM]
    </p>
  </div>
  
  <h5 style="color: #333; margin-top: 1.5rem;">Eligibility:</h5>
  <ul style="line-height: 1.8;">
    <li>Must be 21+ years old</li>
    <li>New customers only</li>
    <li>Physically located in eligible state</li>
  </ul>
  
  <h5 style="color: #333; margin-top: 1.5rem;">How to Qualify:</h5>
  <ul style="line-height: 1.8;">
    <li>Opt-in during registration</li>
    <li>Deposit $[X]+</li>
    <li><strong>[KEY CONDITION]</strong></li>
  </ul>
  
  <h5 style="color: #333; margin-top: 1.5rem;">Bonus Terms:</h5>
  <ul style="line-height: 1.8;">
    <li>$[X] in bonus bets within [timeframe]</li>
    <li>Non-withdrawable</li>
    <li>Expires [X] days</li>
  </ul>
  
  <h5 style="color: #333; margin-top: 1.5rem;">Eligible States:</h5>
  <p>[COMPLETE LIST]</p>
  
  <div style="background: #fff3cd; padding: 1rem; border-radius: 6px; margin: 1.5rem 0; border-left: 4px solid #ffc107;">
    <p style="margin: 0; font-size: 14px; color: #856404;">
      <strong>⚠️ Critical:</strong> [KEY DISTINCTION]
    </p>
  </div>
  
  <p style="font-size: 13px; color: #666; margin-top: 1rem;">
    <strong>Last Verified:</strong> [Date]
  </p>
  
</div>

<hr style="margin: 2rem 0;">
<!-- REPEAT FOR EACH BRAND -->
```

---

## Step 6: Schema Markup

### Article Schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Title]",
  "author": {"@type": "Person", "name": "[Author]"},
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[Current Date]",
  "publisher": {
    "@type": "Organization",
    "name": "Topend Sports"
  }
}
</script>
```

### FAQ Schema (Use Optimized Questions)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is [Brand] legal in my state?",
      "acceptedAnswer": {"@type": "Answer", "text": "[Answer]"}
    },
    {
      "@type": "Question",
      "name": "Do I need a [Brand] promo code?",
      "acceptedAnswer": {"@type": "Answer", "text": "[Answer]"}
    }
    // Continue for all 7 FAQs
  ]
}
</script>
```

### Breadcrumb Schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.topendsports.com/"},
    {"@type": "ListItem", "position": 2, "name": "Betting", "item": "https://www.topendsports.com/sport/betting/"},
    {"@type": "ListItem", "position": 3, "name": "[Title]", "item": "[Full URL]"}
  ]
}
</script>
```

---

## Step 7: Compliance Sections

**NOTE:** Affiliate disclosure is NOT included in content - it's already in the website sidebar.

### Responsible Gambling (Bottom - REQUIRED)
```html
<div style="background: #fff3cd; padding: 1.5rem; margin: 2rem 0; border-radius: 8px;">
  <h3 style="margin-top: 0; color: #856404;">Gamble Responsibly</h3>
  <ul style="line-height: 1.8;">
    <li><strong>National Hotline:</strong> 1-800-522-4700 (24/7)</li>
    <li><strong>Chat:</strong> ncpgambling.org/chat</li>
  </ul>
  <p style="font-size: 14px; color: #666;">
    Must be 21+ to bet. Check local laws before wagering.
  </p>
</div>
```

---

## Step 8: Interactive Elements (Based on Gaps)

### Bonus Calculator
```html
<div style="background: #f8f9fa; padding: 2rem; border-radius: 8px; margin: 2rem 0;">
  <h3 style="margin-top: 0; color: #2e7d32;">Bonus Calculator</h3>
  <div style="margin-bottom: 1rem;">
    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">First Bet ($):</label>
    <input type="number" id="betAmount" value="5" style="padding: 0.5rem; width: 200px; border: 1px solid #ddd; border-radius: 4px;">
  </div>
  <button onclick="calculateBonus()" style="background: #2e7d32; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer;">Calculate</button>
  <div id="result" style="margin-top: 1rem; padding: 1rem; background: #e8f5e9; border-radius: 4px; display: none;">
    <strong>Potential Bonus:</strong> $<span id="bonusAmount">0</span>
  </div>
</div>
<script>
function calculateBonus() {
  document.getElementById('bonusAmount').textContent = '300';
  document.getElementById('result').style.display = 'block';
}
</script>
```

---

## Output: AI Enhancement Brief

```markdown
# AI ENHANCEMENT BRIEF: [Page Title]

## META TAGS
[Complete meta tags]

## LAST UPDATED BADGE
[Complete HTML]

## COMPARISON TABLE
[Complete HTML]

## QUICK ANSWER BOX
[Complete HTML]

## COMPLETE T&Cs
[Complete HTML for each brand]

## INTERACTIVE ELEMENTS
[Complete HTML/JS]

## SCHEMA MARKUP
- Article Schema: [JSON-LD]
- FAQ Schema: [JSON-LD with optimized questions]
- Breadcrumb Schema: [JSON-LD]

## COMPLIANCE SECTIONS
[Complete HTML]

---
END OF AI ENHANCEMENT BRIEF
```

---

## Self-Check

### Meta Tags (SERP-Optimized)
- [ ] SERP analysis documented for primary keyword
- [ ] Title under 60 characters
- [ ] Primary keyword at START of title
- [ ] **NO YEAR in title**
- [ ] Location/market specified
- [ ] Description under 155 characters
- [ ] Description has unique value proposition
- [ ] Meta keywords include ALL secondary keywords

### Content Elements
- [ ] Last Updated badge built
- [ ] Comparison table uses researched brands
- [ ] Quick Answer Box included
- [ ] Complete T&Cs for ALL brands (Template 1/2/4)
- [ ] Interactive elements from gaps built

### Schema & Compliance
- [ ] Article schema complete
- [ ] FAQ schema uses optimized questions
- [ ] Breadcrumb schema complete
- [ ] Responsible gambling section included
- [ ] NO affiliate disclosure in content (it's in sidebar)
- [ ] All HTML is complete (no placeholders)
