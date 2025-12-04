# Ahrefs Keyword Research Workflow

**Purpose:** MANDATORY competitor keyword analysis before content brief generation
**Source:** Critical gap identified in team feedback (December 2024)
**Priority:** CRITICAL - This is the #1 identified improvement

---

## Why This Matters

Content briefs created WITHOUT competitor keyword analysis are missing:
- Keywords competitors rank for
- Content gap opportunities
- Proper H2/H3 structure based on search data
- FAQ questions people actually search for

---

## MANDATORY 7-Step Workflow

### Before ANY Content Brief Generation:

**Step 1: Identify Topic**
- Get primary keyword from user request
- Identify page type (comparison, review, how-to, state)

**Step 2: Find Competitor URLs**
- Identify 3-5 top competitor URLs ranking for the topic
- Focus on affiliate competitors: actionnetwork.com, covers.com, thelines.com
- NOT brand pages (FanDuel, DraftKings official sites)

**Step 3: Run Ahrefs Competitor Analysis**
Use these Ahrefs tools:
```
ahrefs:site-explorer-organic-keywords - Get keywords competitor ranks for
ahrefs:site-explorer-organic-competitors - Find competing domains
ahrefs:site-explorer-top-pages - Find best performing pages
```

**Step 4: Extract Keyword Data**
For each competitor, gather:
- Top ranking keywords
- Search volume
- Keyword difficulty
- Current ranking position

**Step 5: Identify Content Gaps**
- Keywords competitors rank for that TopEndSports doesn't
- High-volume keywords with low difficulty
- Question keywords for FAQ section

**Step 6: Build Keyword Cluster**
Map keywords to content structure:
| Volume | Placement |
|--------|-----------|
| 500+/mo | H2 section title |
| 200-500/mo | H2 or H3 |
| 100-200/mo | H3 subsection |
| 50-100/mo | FAQ or natural |
| Questions | FAQ section |

**Step 7: Document in Brief**
Include keyword research section in every brief (see template below)

---

## Ahrefs API Tools Reference

### Primary Tools
```
ahrefs:site-explorer-organic-keywords
- Get all keywords a URL ranks for
- Returns: keyword, volume, position, traffic

ahrefs:site-explorer-organic-competitors
- Find domains competing for same keywords
- Returns: domain, keywords in common, traffic

ahrefs:site-explorer-top-pages
- Find competitor's best performing pages
- Returns: URL, traffic, keywords
```

### Keyword Research Tools
```
ahrefs:keywords-explorer-overview
- Get search volume and difficulty for keyword
- Returns: volume, KD, CPC, clicks

ahrefs:keywords-explorer-matching-terms
- Find keyword variations
- Returns: related keywords with volume

ahrefs:keywords-explorer-related-terms
- Discover "also rank for" keywords
- Returns: semantically related keywords
```

---

## Content Brief Keyword Section Template

Add this section to every content brief:

```markdown
## Keyword Research Summary

### Primary Keyword
- **Keyword:** [main target keyword]
- **Search Volume:** [monthly searches]
- **Keyword Difficulty:** [0-100]
- **Current Ranking:** [position or "not ranking"]

### Secondary Keywords (8-15 required)
| Keyword | Volume | KD | Placement |
|---------|--------|----|-----------|
| [keyword 1] | [vol] | [kd] | H2 |
| [keyword 2] | [vol] | [kd] | H3 |
| [keyword 3] | [vol] | [kd] | FAQ |

### Content Gap Keywords
Keywords competitors rank for that we don't:
| Keyword | Volume | Top Competitor | Their Position |
|---------|--------|----------------|----------------|

### FAQ Target Questions
- [question keyword 1] - [volume]
- [question keyword 2] - [volume]

### Total Keyword Cluster Volume
- Primary: [X] searches/month
- Secondary total: [Y] searches/month
- **Combined opportunity:** [X+Y] searches/month
```

---

## Validation Checklist

Before finalizing any brief:
- [ ] Primary keyword has search volume data
- [ ] At least 8 secondary keywords identified
- [ ] Content gap analysis completed
- [ ] H2 structure targets keyword clusters
- [ ] FAQs target question keywords
- [ ] Total cluster volume calculated

---

## Quick Reference: Keyword → Placement

| Monthly Volume | Where to Place |
|----------------|----------------|
| 1000+ | H2 (dedicated section) |
| 500-1000 | H2 or prominent H3 |
| 200-500 | H3 subsection |
| 100-200 | Within content naturally |
| Question format | FAQ section |

---

**Document Version:** 1.0
**Last Updated:** December 2024
