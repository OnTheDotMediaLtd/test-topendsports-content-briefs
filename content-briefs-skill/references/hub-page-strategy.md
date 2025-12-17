# Hub Page Strategy & Anti-Cannibalization

**Added:** December 17, 2025
**Purpose:** Prevent internal keyword competition between hub pages and dedicated pages

---

## What is a Hub Page?

Hub pages are market-level landing pages that:
- Provide an overview of an entire market (e.g., "Sports Betting Canada")
- Link prominently to dedicated sub-pages
- Target broad, market-level keywords
- Do NOT compete with dedicated pages for specific keywords

### Hub Page Examples
| Market | Hub Page URL | Purpose |
|--------|--------------|---------|
| Canada | `/canada/index.htm` | Sports betting overview for Canada |
| UK | `/uk/index.htm` | Sports betting overview for UK |
| Ireland | `/ireland/index.htm` | Sports betting overview for Ireland |
| USA | `/index.htm` | Sports betting overview for USA |

---

## Anti-Cannibalization Rules

### Keywords Hub Pages Should TARGET

| Keyword Pattern | Example | Typical Volume |
|-----------------|---------|----------------|
| "sports betting [market]" | sports betting canada | 2,300/mo |
| "online betting [market]" | online betting canada | 1,000/mo |
| "[market] sports betting" | canada sports betting | 700/mo |
| "is sports betting legal in [market]" | is sports betting legal in canada | 350/mo |
| "how to bet on sports in [market]" | how to bet on sports in canada | 200/mo |
| "sports gambling [market]" | sports gambling canada | 200/mo |
| Regional variations | sports betting ontario | 1,100/mo |

### Keywords Hub Pages Should AVOID (Belong on Dedicated Pages)

| Keyword Pattern | Example | Dedicated Page | Why |
|-----------------|---------|----------------|-----|
| "best betting apps [market]" | best betting apps canada | `/betting-apps.htm` | Apps-specific content |
| "betting apps [market]" | betting apps canada | `/betting-apps.htm` | Apps-specific content |
| "best betting sites [market]" | best betting sites canada | `/sports-betting-sites.htm` | Sites comparison |
| "best online betting sites [market]" | best online betting sites canada | `/sports-betting-sites.htm` | Sites comparison |
| "new betting sites [market]" | new betting sites canada | `/new-betting-sites.htm` | New sites focus |
| "[market] betting apps" | canada betting apps | `/betting-apps.htm` | Apps-specific content |
| "best [market] sportsbooks" | best canadian sportsbooks | `/sports-betting-sites.htm` | Sites comparison |

---

## Dedicated Pages by Market

### Canada
| Dedicated Page | Keywords It Owns | URL |
|----------------|------------------|-----|
| Betting Apps | betting apps canada, best betting apps canada | `/canada/betting-apps.htm` |
| Betting Sites | best betting sites canada, canadian betting sites | `/canada/sports-betting-sites.htm` |
| New Sites | new betting sites canada | `/canada/new-betting-sites.htm` |

### UK
| Dedicated Page | Keywords It Owns | URL |
|----------------|------------------|-----|
| Betting Apps | betting apps uk, best betting apps uk | `/uk/betting-apps.htm` |
| New Sites | new betting sites uk | `/uk/new-betting-sites.htm` |
| Free Bets | free bets uk | `/uk/free-bets.htm` |
| Betting Offers | betting offers uk | `/uk/betting-offers.htm` |

### Ireland
| Dedicated Page | Keywords It Owns | URL |
|----------------|------------------|-----|
| Betting Apps | betting apps ireland | `/ireland/betting-apps.htm` |
| Free Bets | free bets ireland | `/ireland/free-bets.htm` |

---

## Hub Page Internal Link Hierarchy

### CRITICAL Links (First 500 Words)
Hub pages MUST link to dedicated pages prominently in the introduction:

```markdown
## Required in Introduction:
1. Link to betting apps page → "best betting apps [market]"
2. Link to betting sites page → "sports betting sites [market]"
3. Link to new sites page (if exists) → "new betting sites [market]"
```

### Link Priority Levels

| Priority | Link Type | Placement | Example Anchor |
|----------|-----------|-----------|----------------|
| **CRITICAL** | Dedicated pages | First 500 words | "Best Betting Apps Canada" |
| **HIGH** | Brand review pages | Brand sections | "[Brand] Review" |
| **MEDIUM** | Sport-specific pages | Sports section | "NHL Betting Guide" |
| **MEDIUM** | Tools | Tools mention | "Parlay Calculator" |
| **LOW** | Related hub pages | Footer/related | "UK Betting Guide" |

---

## Hub Page Word Count

| Page Type | V1 (Incorrect) | V2 (Correct) | Reason |
|-----------|----------------|--------------|--------|
| Hub Page | 9,000+ words | 7,500 words | Hub provides overview, not exhaustive detail |
| Comparison Page | 8,000+ words | 8,000+ words | Comparison pages need depth |
| Review Page | 3,500-4,000 words | 3,500-4,000 words | Single brand focus |

**Hub pages are not comparison pages.** They should link TO comparison pages, not replicate them.

---

## Hub Page Keyword Cluster Calculation

### Correct Approach (V2)

```
Hub Page Cluster = Market-level keywords ONLY

Example: Canada Hub
- sports betting canada: 2,300/mo
- sports betting ontario: 1,100/mo
- online betting canada: 1,000/mo
- canada sports betting: 700/mo
- online sports betting canada: 700/mo
- is sports betting legal in canada: 350/mo
- how to bet on sports in canada: 200/mo

TOTAL: ~6,350/mo (appropriate for hub)
```

### Incorrect Approach (V1)

```
DON'T include these in hub cluster:
- best betting apps canada: 700/mo → belongs to /betting-apps.htm
- betting apps canada: 500/mo → belongs to /betting-apps.htm
- best betting sites canada: 700/mo → belongs to /sports-betting-sites.htm

These inflate the cluster artificially and cause cannibalization.
```

---

## Validation Checklist

Before finalizing a hub page brief:

### Keyword Validation
- [ ] No keywords containing "apps" (belongs on apps page)
- [ ] No keywords containing "sites" comparison terms (belongs on sites page)
- [ ] No keywords containing "new" sites (belongs on new sites page)
- [ ] All keywords are market-level or legal/regulatory

### Internal Link Validation
- [ ] Dedicated pages linked in first 500 words
- [ ] Dedicated page links marked as PROMINENT
- [ ] Brand review links in brand sections
- [ ] No orphaned dedicated pages

### Content Scope Validation
- [ ] Word count target ~7,500 (not 9,000+)
- [ ] Content is overview, not exhaustive comparison
- [ ] Links to dedicated pages for detailed comparisons

---

## Examples

### Good Hub Page Intro (V2 Style)

```markdown
The best sports betting options in Canada are Treasure Spins, Royalistplay,
and Lucky7even for bettors outside Ontario. Our team tested all 9 platforms
with real CAD deposits.

For detailed app comparisons, see our [Best Betting Apps Canada](/canada/betting-apps.htm)
guide. Looking for new options? Check [New Betting Sites Canada](/canada/new-betting-sites.htm).

This guide covers Canadian sports betting laws, provincial differences, and
how to get started with legal betting across all provinces.
```

### Bad Hub Page Intro (V1 Style)

```markdown
Looking for the best betting apps in Canada? We've reviewed the top betting
sites and apps to help you find the perfect sportsbook...

[This competes with dedicated apps and sites pages]
```

---

## Quick Reference

| Question | Answer |
|----------|--------|
| Should hub target "best betting apps"? | NO - dedicated page owns this |
| Should hub target "sports betting [market]"? | YES - market-level keyword |
| Hub word count? | ~7,500 (not 9,000+) |
| Where to link dedicated pages? | First 500 words, marked PROMINENT |
| How to calculate cluster volume? | Market-level keywords only |

---

**Document Version:** 1.0
**Last Updated:** December 2025
