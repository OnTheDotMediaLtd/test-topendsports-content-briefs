# CTA Placement Strategy Skill

## Description
Strategic skill for placing calls-to-action (CTAs) that improve conversion without harming user experience. Focuses on value-first approach where users receive value before being asked to take action.

## When to Use This Skill
- After completing content optimization
- When adding affiliate links
- During final layout review
- When improving conversion rates
- Before delivering optimized pages

## Core CTA Philosophy

**VALUE FIRST, THEN CTAs**

CTAs should NOT appear until the user has received value. Immediate CTAs harm user experience and trust.

## The Value-First Rule

**PLACEMENT RULES:**

### FIRST CTA
- **MINIMUM:** After at least 400-500 words of valuable content
- **IDEAL:** After first major section or comparison
- **LOCATION:** After user understands the topic

### SECOND CTA
- **LOCATION:** After a major comparison or recommendation section
- **SPACING:** At least 300-400 words after first CTA

### THIRD CTA
- **LOCATION:** Before FAQ section
- **SPACING:** At least 300-400 words after second CTA

### FINAL CTA
- **LOCATION:** After FAQ, before footer
- **PURPOSE:** Last opportunity for conversion

## What NOT To Do

### NEVER Place CTA:
- Immediately after H1 or Quick Answer
- Above the fold (first screen)
- Before providing substantial value
- Adjacent to another CTA (both visible on same screen)
- Clustered consecutively (multiple CTAs in row)

## CTA Messaging Variation

**THE RULE: Never use identical CTA copy throughout page**

### Early CTAs (After 400-500 words):
- "Compare Sportsbooks"
- "See Bonuses"
- "Find the Best Odds"
- "Explore Betting Options"

### Middle CTAs (After comparison/analysis):
- "Get Started"
- "Claim Bonus"
- "Start Betting Today"
- "Join Now"

### Late CTAs (Before/after FAQ):
- "Start Betting Today"
- "Don't Miss Out"
- "Claim Your Bonus"
- "Get Started Now"

## CTA Content Structure

### Standard CTA Block Format:

```html
<div class="cta-block">
    <h3>Ready to Start Betting?</h3>
    <p>FanDuel offers new players up to $1,000 in bonus bets. Get started today.</p>
    <a href="[AFFILIATE-URL]" rel="nofollow sponsored" target="_blank" class="cta-button">
        Claim FanDuel Bonus
    </a>
    <p class="disclaimer">21+ only. Gambling Problem? Call 1-800-GAMBLER.</p>
</div>
```

### Required Elements:
1. **Headline** - Compelling, action-oriented
2. **Value proposition** - Why should they click?
3. **Button** - Clear action with brand name
4. **Disclaimer** - Responsible gambling info

## Responsible Gambling Disclaimer

**REQUIRED with EVERY CTA block:**

```
21+ only. Gambling Problem? Call 1-800-GAMBLER.
```

**Variations by state (if applicable):**
- AZ: 1-800-NEXT-STEP
- CT: 888-789-7777
- IL: 1-800-GAMBLER
- IN: 1-800-9-WITH-IT
- (See full list in CLAUDE.md)

## CTA Spacing Examples

### Example 1: 1,500-Word Article

```
[H1 + Quick Answer] (0 words)
[Introduction] (0-100 words)
[Section 1] (100-400 words)
[Section 2] (400-600 words)
[CTA #1] ← First CTA after 400-600 words
[Section 3] (600-900 words)
[Interactive Element] (900-1,000 words)
[CTA #2] ← Second CTA after another 300-400 words
[Section 4] (1,000-1,200 words)
[FAQ Section] (1,200-1,400 words)
[CTA #3] ← Final CTA before conclusion
[Conclusion] (1,400-1,500 words)
```

### Example 2: 2,500-Word Article

```
[H1 + Quick Answer] (0 words)
[TOC] (0-50 words)
[Introduction] (50-150 words)
[Section 1] (150-400 words)
[Section 2] (400-700 words)
[CTA #1] ← First CTA at ~600 words
[Section 3] (700-1,000 words)
[Interactive Element] (1,000-1,100 words)
[Section 4] (1,100-1,500 words)
[CTA #2] ← Second CTA at ~1,400 words
[Section 5] (1,500-1,800 words)
[Comparison Table] (1,800-2,000 words)
[Section 6] (2,000-2,200 words)
[CTA #3] ← Third CTA at ~2,100 words
[FAQ Section] (2,200-2,400 words)
[CTA #4] ← Final CTA before conclusion
[Conclusion] (2,400-2,500 words)
```

## Affiliate Link Requirements

### For FanDuel:
```html
<a href="https://wlfanduelus.adsrv.eacdn.com/C.ashx?btag=a_44387b_95c_&affid=21729&siteid=44387&adid=95&c="
   rel="nofollow sponsored"
   target="_blank">
   Claim FanDuel Bonus
</a>
```

### For BetMGM:
```html
<a href="https://mediaserver.betmgmpartners.com/renderBanner.do?zoneId=1739687"
   rel="nofollow sponsored"
   target="_blank">
   Claim BetMGM Bonus
</a>
```

### Required Attributes:
- `rel="nofollow sponsored"` (ALWAYS)
- `target="_blank"` (ALWAYS)

## CTA Design Guidelines

### Button Styling (CSS):

```css
.cta-button {
    display: inline-block;
    padding: 12px 24px;
    background-color: #2e7d32; /* Green, not red */
    color: #ffffff;
    text-decoration: none;
    border-radius: 5px;
    font-weight: 600;
    text-align: center;
    transition: background-color 0.3s ease;
}

.cta-button:hover {
    background-color: #1b5e20; /* Darker green */
}
```

### CTA Block Styling:

```css
.cta-block {
    background: #f0f9ff;
    border: 2px solid #0ea5e9;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 2rem 0;
    text-align: center;
}

.cta-block h3 {
    color: #0369a1;
    margin: 0 0 1rem 0;
}

.cta-block .disclaimer {
    font-size: 0.85rem;
    color: #666;
    margin-top: 1rem;
}
```

## Mobile Optimization

### Mobile-Friendly CTAs:

- **Minimum tap target:** 44x44px
- **Spacing:** Extra spacing on mobile (50px above/below)
- **Button width:** Full width on mobile OR centered with min-width
- **Font size:** Minimum 16px (prevents auto-zoom on iOS)

### Mobile CTA Example:

```css
@media (max-width: 768px) {
    .cta-button {
        width: 100%;
        max-width: 300px;
        padding: 14px 20px;
        font-size: 16px;
    }

    .cta-block {
        margin: 2.5rem 0;
        padding: 2rem 1rem;
    }
}
```

## CTA Conversion Best Practices

### 1. Specificity Wins
**GOOD:** "Claim $1,000 FanDuel Bonus"
**BAD:** "Click Here"

### 2. Urgency (When Appropriate)
**GOOD:** "Limited Time: Get $500 Bonus"
**AVOID:** "Guaranteed to Win" (compliance violation)

### 3. Social Proof
**GOOD:** "Join 1M+ FanDuel Bettors"
**AVOID:** "Everyone is using this"

### 4. Value First
**GOOD:** [After explaining betting types] "Ready to compare these betting sites?"
**BAD:** [Immediately after H1] "Sign up now!"

## Validation Checklist

### CTA Placement:
- [ ] FIRST CTA appears after minimum 400 words
- [ ] NO CTA immediately after H1 or Quick Answer
- [ ] NO CTAs above the fold
- [ ] CTAs distributed throughout (not clustered)
- [ ] Minimum 300-400 words between CTAs
- [ ] FINAL CTA after FAQ section

### CTA Quality:
- [ ] Each CTA has unique messaging (not identical copy)
- [ ] All CTAs include responsible gambling disclaimer
- [ ] Affiliate links have `rel="nofollow sponsored"`
- [ ] Affiliate links have `target="_blank"`
- [ ] CTAs are specific (not "Click Here")
- [ ] Mobile-friendly tap targets (44x44px minimum)

### Content Integration:
- [ ] CTAs appear after user receives value
- [ ] CTAs contextually relevant to surrounding content
- [ ] No more than 3-4 of same affiliate link per page
- [ ] CTA messaging varies (early vs middle vs late)

## Common Mistakes to Avoid

### Mistake 1: CTAs Too Early
```
WRONG:
[H1: Best Sports Betting Sites]
[CTA: Sign Up Now!] ← Appears immediately

RIGHT:
[H1: Best Sports Betting Sites]
[Quick Answer explaining what makes a good betting site]
[Section 1: Key features to look for]
[Section 2: Top sites comparison]
[CTA: Compare Sportsbooks] ← Appears after value provided
```

### Mistake 2: Clustering CTAs
```
WRONG:
[CTA #1: FanDuel]
[CTA #2: BetMGM] ← Both visible on same screen
[CTA #3: DraftKings]

RIGHT:
[CTA #1: FanDuel]
[300-400 words of content]
[CTA #2: BetMGM]
[300-400 words of content]
[CTA #3: DraftKings]
```

### Mistake 3: Identical CTA Copy
```
WRONG:
[CTA #1: "Get Started Today"]
[CTA #2: "Get Started Today"]
[CTA #3: "Get Started Today"]

RIGHT:
[CTA #1: "Compare Sportsbooks"]
[CTA #2: "Claim Your Bonus"]
[CTA #3: "Start Betting Today"]
```

### Mistake 4: Missing Disclaimer
```
WRONG:
[CTA with just button, no disclaimer]

RIGHT:
[CTA with button]
"21+ only. Gambling Problem? Call 1-800-GAMBLER."
```

## Multi-Brand CTA Strategy

**When featuring multiple sportsbooks:**

### Strategy 1: Sequential CTAs
```
[Section comparing FanDuel features]
[CTA: FanDuel]
[Section comparing BetMGM features]
[CTA: BetMGM]
[Section comparing DraftKings features]
[CTA: DraftKings]
```

### Strategy 2: Comparison Table + Single CTA
```
[Comparison table showing all brands]
[CTA: "Compare All Sportsbooks"]
```

### Strategy 3: Tiered Recommendations
```
[Best Overall: FanDuel]
[CTA: FanDuel]
[Best for Promos: BetMGM]
[CTA: BetMGM]
[Best for Parlays: DraftKings]
[CTA: DraftKings]
```

## Success Criteria

CTA placement is successful when:

1. First CTA appears after minimum 400 words of value
2. No CTAs above the fold or immediately after H1
3. CTAs distributed evenly throughout content
4. Minimum 300-400 words between CTAs
5. Each CTA has unique messaging
6. All CTAs include responsible gambling disclaimer
7. All affiliate links properly attributed
8. Mobile-friendly with proper tap targets
9. CTAs contextually relevant to surrounding content
10. User receives value before being asked to convert

## Related Skills
- validation-html-structure.md - Proper HTML/CSS for CTAs
- content-preservation.md - Place CTAs without disrupting expert content
- internal-linking-strategy.md - Combine CTAs with internal links
- interactive-elements.md - Enhance CTAs with interactive content
- research-workflow.md - Complete workflow including CTA planning
