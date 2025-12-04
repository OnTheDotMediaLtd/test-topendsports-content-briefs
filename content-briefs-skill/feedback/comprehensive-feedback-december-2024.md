# Comprehensive Feedback - December 2024

**Source:** Team feedback and Claude AI session patterns
**Compiled:** December 2024
**Note:** Team colleague feedback takes priority over AI session patterns where conflicts exist

---

## TEAM COLLEAGUE FEEDBACK (Priority)

### Key Issues Reported

| Issue | Severity | Reported By |
|-------|----------|-------------|
| Content shortening/skipping | CRITICAL | Gustavo, Lewis, Daniel |
| Long conversation limits | HIGH | Lewis, Daniel |
| CSS max-width conflicts | RESOLVED | Dev team |
| Response wait times | MEDIUM | Multiple |

### Colleague Pain Points

1. **Content Shortening/Skipping (CRITICAL)**
   - Claude tends to shorten responses
   - Skips key points that were mentioned
   - Sometimes refuses to break up extra long text into artifacts

2. **Long Conversation Limits**
   - Chat resets mid-conversation
   - Conversation gets too long and can't continue

3. **CSS Conflicts (RESOLVED)**
   - max-width CSS conflicts with site styling
   - **Fix:** Add rule "Do not include max-width CSS on elements"

### Project Ideas from Team
- **Bonus Update Automation** (Daniel) - Auto-edit bonuses across pages
- **Internal Linking Assistant** (Lewis) - On-page linking strategy

---

## TECHNICAL REQUIREMENTS (V3 Approach)

### Dreamweaver Compatibility
- ALL JavaScript must be in `<head>` section in ONE `<script>` tag
- Use DOMContentLoaded wrapper for initialization
- No inline JavaScript in body (only onclick/onchange attributes)
- No localStorage/sessionStorage

### Letter Badge System (NO Images)
Use text-based letter badges instead of image logos:

| Brand | Code | Color |
|-------|------|-------|
| FanDuel | FD | #1493ff |
| DraftKings | DK | #53d337 |
| BetMGM | MGM | #bfa36b |
| Caesars | CZR | #0a2240 |
| bet365 | 365 | #0e7b46 |
| Fanatics | FAN | #0050c8 |
| theScore BET | SCR | #6B2D5B |
| BetRivers | BR | #ff6b00 |

> **CRITICAL:** ESPN BET shut down December 1, 2025. Now theScore BET.

---

## CONTENT OUTPUT RULES (MANDATORY)

1. **NEVER shorten, compress, or skip content** - Output ALL content in full
2. **Do NOT include max-width CSS** - Site handles this
3. **No placeholders** - Deliver complete, working code
4. **Break into multiple artifacts if needed** - Each must be complete
5. **Use Gold Standard Templates** - See references/gold-standard-templates.md

---

## GOLD STANDARD TEMPLATES

### Required for All Pages

1. **Comparison Table** - 3-column layout with letter badges
2. **Brand Cards** - Expandable features with pros/cons
3. **Tabbed Reviews** - Click navigation between brands
4. **State Filter** - Compliance dropdown
5. **FAQ Accordion** - Collapsible Q&A

### Key CSS Color Scheme
```css
--primary-green: #2e7d32;
--primary-green-dark: #1b5e20;
--warning-yellow: #ffc107;
--danger-red: #d32f2f;
```

---

## COMPLIANCE REQUIREMENTS

Every page MUST have:
- Age requirement (21+ most states, 18+ for DC, MT, NH, RI, WY)
- Gambling hotline: 1-800-522-4700
- Affiliate disclosure (top)
- Responsible gambling section (bottom)
- State availability disclaimer
- Visible T&Cs for all bonuses

---

## STYLE GUIDE VIOLATIONS TO AVOID

### Prohibited
- Emojis in headings or professional content
- "Q:" or "A:" prefix in FAQ sections
- Excessive colons in headers
- Fictional expert quotes
- High contrast/clashing colors
- Box within box within box (nesting)
- max-width CSS on elements

### Required
- Consistent green theme (#2e7d32)
- Letter badges instead of images
- Mobile-first responsive design
- Console logging for debugging
- Complete T&Cs for compliance

---

## INTERNAL LINK FORMAT

```
❌ /sport/betting/
✅ /sport/betting/index.htm

❌ /sport/betting/sportsbook-reviews/
✅ /sport/betting/sportsbook-reviews/index.htm
```

Always use complete URLs with `index.htm` suffix.

---

## IMPLEMENTATION CHECKLIST

Before delivering any page enhancement:

- [ ] All JavaScript functions defined AND wired to HTML
- [ ] All CSS styles present for every component
- [ ] No placeholder text anywhere
- [ ] All original content preserved
- [ ] Internal links use complete URLs
- [ ] T&Cs visible for compliance
- [ ] Mobile responsive breakpoints included
- [ ] Letter badges have correct colors
- [ ] Console logging included
- [ ] State filter has accurate data
- [ ] theScore BET used (not ESPN BET)

---

**Document Version:** 1.0
**Last Updated:** December 2024
