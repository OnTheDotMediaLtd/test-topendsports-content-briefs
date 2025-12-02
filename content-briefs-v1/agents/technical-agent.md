# PHASE 3: TECHNICAL AGENT

**Purpose:** Build complete technical implementation with HTML/code
**Input:** `active/[page-name]-phase1.json` + `active/[page-name]-phase2.json`
**Output:** AI Enhancement Brief (5-8 pages with complete HTML)

---

## STEP 1: LOAD PREVIOUS PHASE DATA

Read both JSON files:
```bash
cat active/[page-name]-phase1.json
cat active/[page-name]-phase2.json
```

Extract:
- Technical requirements from Phase 1
- Keyword optimization from Phase 2
- Template type
- Brand selection
- FAQ questions

---

## STEP 2: BUILD META TAGS WITH KEYWORDS

```html
<meta name="title" content="[Page Title - NO dates]">
<meta name="description" content="[160 chars with primary keyword]">
<meta name="keywords" content="[ALL primary + secondary keywords, comma-separated]">
<meta name="author" content="[Lewis Humphries/Tom Goldsmith/Gustavo Cantella]">
<link rel="canonical" href="https://www.topendsports.com/sport/betting/[page].htm">
```

**Example:**
```html
<meta name="keywords" content="fanduel review, fanduel bonus, fanduel promo code, fanduel app review, fanduel withdrawal time, fanduel vs draftkings, is fanduel legal, fanduel states">
```

---

## STEP 3: BUILD "LAST UPDATED" BADGE (ALWAYS FIRST)

Place immediately after H1, before intro:

```html
<div style="background: #e8f5e9; padding: 0.75rem 1.25rem; border-left: 4px solid #2e7d32; margin-bottom: 1.5rem; border-radius: 4px;">
  <p style="margin: 0; font-size: 14px; color: #2e7d32;">
    <strong>✓ Last Updated:</strong> [Current Date]
  </p>
</div>
```

---

## STEP 4: BUILD COMPARISON TABLE

For Reviews/Comparisons/State Pages:

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
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;">[USP from research]</td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;">[Bonus]*</td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd; text-align: center;">⭐⭐⭐⭐⭐</td>
      </tr>
      <tr>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;"><strong>BetMGM</strong></td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;">[USP from research]</td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd;">[Bonus]*</td>
        <td style="padding: 1rem; border-bottom: 1px solid #ddd; text-align: center;">⭐⭐⭐⭐⭐</td>
      </tr>
      <!-- Continue for all brands -->
    </tbody>
  </table>
  <p style="font-size: 12px; color: #666; margin-top: 0.5rem;">
    *21+ only. T&Cs apply. See complete terms below.
  </p>
</div>
```

**Specs:**
- Mobile-responsive (overflow-x: auto)
- Use researched brands from Phase 1 (NOT generic defaults)
- Include brief T&Cs inline

---

## STEP 5: BUILD QUICK ANSWER BOX

```html
<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left: 4px solid #2e7d32; padding: 1.5rem; margin: 2rem 0; border-radius: 8px;">
  <h2 style="color: #2e7d32; margin-top: 0; font-size: 1.25rem;">Quick Answer</h2>
  <p style="font-size: 1.1rem; margin-bottom: 1rem;">[Direct 2-3 sentence answer to main question]</p>
  <ul style="line-height: 1.8; margin: 0; padding-left: 1.25rem;">
    <li><strong>[Key fact 1]</strong></li>
    <li><strong>[Key fact 2]</strong></li>
    <li><strong>[Key fact 3]</strong></li>
  </ul>
</div>
```

---

## STEP 6: BUILD COMPLETE T&Cs SECTION

**Required for:** Template 1, 2, 4
**For each brand featured:**

```html
<div style="background: #f8f9fa; padding: 2rem; margin: 2rem 0; border-radius: 8px; border: 2px solid #2e7d32;">
  
  <h3 style="margin-top: 0; color: #2e7d32;">Complete Bonus Terms & Conditions</h3>
  
  <h4 style="color: #333; border-bottom: 2px solid #2e7d32; padding-bottom: 0.5rem;">
    [Brand Name]
  </h4>
  
  <!-- BONUS HEADLINE -->
  <div style="background: #e8f5e9; padding: 1.25rem; border-radius: 6px; margin: 1rem 0;">
    <p style="margin: 0; font-weight: 600; color: #2e7d32; font-size: 16px;">
      [EXACT BONUS TEXT - COPY VERBATIM]
    </p>
  </div>
  
  <!-- ELIGIBILITY -->
  <h5 style="color: #333; margin-top: 1.5rem;">Eligibility Requirements:</h5>
  <ul style="line-height: 1.8; color: #333;">
    <li>Must be 21+ years old</li>
    <li>New [Brand] customers only</li>
    <li>Physically located in eligible state</li>
    <li>One welcome offer per person/household</li>
  </ul>
  
  <!-- HOW TO QUALIFY -->
  <h5 style="color: #333; margin-top: 1.5rem;">How to Qualify:</h5>
  <ul style="line-height: 1.8; color: #333;">
    <li>Opt-in during registration</li>
    <li>Make first deposit of $[X] or more</li>
    <li>Place first wager of $[X] or more</li>
    <li><strong>[KEY CONDITION]</strong></li>
  </ul>
  
  <!-- BONUS TERMS -->
  <h5 style="color: #333; margin-top: 1.5rem;">Bonus Terms:</h5>
  <ul style="line-height: 1.8; color: #333;">
    <li>$[X] in bonus bets awarded within [timeframe]</li>
    <li>Bonus bets non-withdrawable</li>
    <li>[Stake return policy]</li>
    <li>Expires [X] days after receipt</li>
  </ul>
  
  <!-- ELIGIBLE STATES -->
  <h5 style="color: #333; margin-top: 1.5rem;">Eligible States:</h5>
  <p style="color: #333;">[COMPLETE STATE LIST]</p>
  
  <!-- CRITICAL NOTE -->
  <div style="background: #fff3cd; padding: 1rem; border-radius: 6px; margin: 1.5rem 0; border-left: 4px solid #ffc107;">
    <p style="margin: 0; font-size: 14px; color: #856404;">
      <strong>⚠️ Critical:</strong> [KEY DISTINCTION]
    </p>
  </div>
  
  <!-- LEGAL TERMS -->
  <p style="font-size: 13px; color: #666; padding: 1rem; background: white; border-radius: 4px;">
    <strong>Complete Legal Terms:</strong><br><br>
    [FULL LEGAL LANGUAGE - DO NOT SUMMARIZE]
  </p>
  
  <!-- LINKS -->
  <p style="font-size: 13px; color: #666; margin-top: 1rem;">
    <strong>Official Terms:</strong> <a href="[URL]" target="_blank" rel="noopener">[brand].com/terms</a>
  </p>
  
  <p style="font-size: 13px; color: #666; margin-top: 1rem;">
    <strong>Problem Gambling:</strong> Call 1-800-GAMBLER or visit ncpgambling.org
  </p>
  
  <p style="font-size: 13px; color: #666; margin-top: 1rem; font-weight: 600;">
    <strong>Last Verified:</strong> [Date]
  </p>
  
</div>

<hr style="margin: 2rem 0; border: none; border-top: 1px solid #ddd;">

<!-- REPEAT FOR NEXT BRAND -->
```

---

## STEP 7: BUILD INTERACTIVE ELEMENTS (Based on Gaps)

### If Gap = "No Calculator"
Build working bonus calculator:

```html
<div style="background: #f8f9fa; padding: 2rem; border-radius: 8px; margin: 2rem 0;">
  <h3 style="margin-top: 0; color: #2e7d32;">Bonus Calculator</h3>
  
  <div style="margin-bottom: 1rem;">
    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">First Bet Amount ($):</label>
    <input type="number" id="betAmount" value="5" min="5" style="padding: 0.5rem; width: 100%; max-width: 200px; border: 1px solid #ddd; border-radius: 4px;">
  </div>
  
  <div style="margin-bottom: 1rem;">
    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Sportsbook:</label>
    <select id="sportsbook" style="padding: 0.5rem; width: 100%; max-width: 200px; border: 1px solid #ddd; border-radius: 4px;">
      <option value="300">FanDuel ($300 Bonus Bets)</option>
      <option value="1500">BetMGM ($1,500 First Bet)</option>
      <option value="200">DraftKings ($200 Bonus Bets)</option>
    </select>
  </div>
  
  <button onclick="calculateBonus()" style="background: #2e7d32; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600;">Calculate</button>
  
  <div id="result" style="margin-top: 1rem; padding: 1rem; background: #e8f5e9; border-radius: 4px; display: none;">
    <p style="margin: 0; font-size: 1.1rem;"><strong>Potential Bonus:</strong> $<span id="bonusAmount">0</span></p>
  </div>
</div>

<script>
function calculateBonus() {
  const bet = document.getElementById('betAmount').value;
  const bonus = document.getElementById('sportsbook').value;
  document.getElementById('bonusAmount').textContent = bonus;
  document.getElementById('result').style.display = 'block';
}
</script>
```

### If Gap = "Static Table"
Build sortable table with JavaScript

### If Gap = "Few FAQs"
Build 7 collapsible FAQs (see schema section)

---

## STEP 8: BUILD SCHEMA MARKUP

### Article Schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Page Title]",
  "author": {
    "@type": "Person",
    "name": "[Lewis Humphries/Tom Goldsmith/Gustavo Cantella]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[Current Date YYYY-MM-DD]",
  "publisher": {
    "@type": "Organization",
    "name": "Topend Sports",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.topendsports.com/images/logo.png"
    }
  },
  "description": "[Meta description]"
}
</script>
```

### FAQ Schema (Use Optimized Questions from Phase 2)
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
      "name": "Do I need a [Brand] promo code?",
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

### Breadcrumb Schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.topendsports.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Betting",
      "item": "https://www.topendsports.com/sport/betting/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[Page Title]",
      "item": "https://www.topendsports.com/sport/betting/[page].htm"
    }
  ]
}
</script>
```

---

## STEP 9: BUILD COMPLIANCE SECTIONS

### Affiliate Disclosure (Top of Page)
```html
<div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; margin: 1.5rem 0;">
  <p style="margin: 0; font-size: 14px;">
    <strong>Disclosure:</strong> We may earn commission when you sign up through our links. 
    This doesn't affect our reviews or ratings. Must be 21+ to participate. 
    Gambling problem? Call 1-800-522-4700.
  </p>
</div>
```

### Responsible Gambling (Bottom of Page)
```html
<div style="background: #fff3cd; padding: 1.5rem; margin: 2rem 0; border-radius: 8px;">
  <h3 style="margin-top: 0; color: #856404;">Gamble Responsibly</h3>
  <p style="margin-bottom: 1rem;">If you or someone you know has a gambling problem, help is available.</p>
  <ul style="line-height: 1.8;">
    <li><strong>National Hotline:</strong> 1-800-522-4700 (24/7)</li>
    <li><strong>Text:</strong> 1-800-522-4700</li>
    <li><strong>Chat:</strong> ncpgambling.org/chat</li>
    <li><strong>Resources:</strong> ncpgambling.org</li>
  </ul>
  <p style="margin-top: 1rem; font-size: 14px; color: #666;">
    Must be 21+ to bet. Sports betting is not available in all states. 
    Please check your local laws before wagering.
  </p>
</div>
```

---

## OUTPUT: AI ENHANCEMENT BRIEF

Save to: `output/[page-name]-ai-enhancement.md`

```markdown
# AI ENHANCEMENT BRIEF: [Page Title]

## META TAGS
[Complete meta tags with all keywords]

## "LAST UPDATED" BADGE
[Complete HTML]

## COMPARISON TABLE
[Complete HTML with researched brands]

## QUICK ANSWER BOX
[Complete HTML]

## COMPLETE T&Cs SECTIONS
[Complete HTML for each brand - Template 1/2/4 only]

## INTERACTIVE ELEMENTS
[Complete HTML/JS for each element based on gaps]

## SCHEMA MARKUP
### Article Schema
[Complete JSON-LD]

### FAQ Schema
[Complete JSON-LD with optimized questions]

### Breadcrumb Schema
[Complete JSON-LD]

## COMPLIANCE SECTIONS
### Affiliate Disclosure
[Complete HTML]

### Responsible Gambling
[Complete HTML]

---

## IMPLEMENTATION NOTES
- Place "Last Updated" badge immediately after H1
- Place comparison table after intro
- T&Cs sections go under "Current Welcome Bonus" H2
- FAQ schema questions MUST match optimized questions from Phase 2
- All interactive elements include complete working code

---

END OF AI ENHANCEMENT BRIEF
```

---

## SELF-CHECK BEFORE COMPLETING

- [ ] Meta keywords tag includes ALL secondary keywords
- [ ] "Last Updated" badge built (placed after H1)
- [ ] Comparison table uses researched brands (not defaults)
- [ ] Quick Answer Box included
- [ ] Complete T&Cs for ALL brands (if Template 1/2/4)
- [ ] Interactive elements from Phase 1 gaps built
- [ ] Article schema complete
- [ ] FAQ schema uses optimized questions from Phase 2
- [ ] Breadcrumb schema complete
- [ ] Affiliate disclosure included
- [ ] Responsible gambling section included
- [ ] All HTML is complete and working (no placeholders)
- [ ] Saved to `output/`

---

## COMPLETION MESSAGE

After saving, output:
```
Phase 3 complete. AI Enhancement Brief delivered.

Summary:
- Meta keywords: [X] keywords included
- Interactive elements: [List what was built]
- T&Cs sections: [X] brands covered
- Schema: Article + FAQ (7 questions) + Breadcrumb

Files created:
- output/[page-name]-brief-control-sheet.md (Phase 1)
- output/[page-name]-writer-brief.md (Phase 2)
- output/[page-name]-ai-enhancement.md (Phase 3)

All 3 artifacts complete. Brief generation finished.
```
