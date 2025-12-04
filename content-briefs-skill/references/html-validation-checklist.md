# HTML Validation Checklist

**Purpose:** Pre-output validation to prevent common HTML/CSS issues
**Source:** Team feedback compilation (December 2024)
**Priority:** CRITICAL - Run before ANY code output

---

## Pre-Output Validation (MANDATORY)

### 1. Document Structure
- [ ] HEAD section present
- [ ] BODY section present
- [ ] `<main>` element properly closed
- [ ] All `<section>` tags closed before opening new ones
- [ ] No nested sections (sections should be siblings)

### 2. HEAD Section Requirements (8-Point Check)
- [ ] `<title>` tag present
- [ ] `<meta name="description">` present
- [ ] GTM tracking code (GTM-PLHR2G)
- [ ] Google Analytics (G-8ENDVN0S6S)
- [ ] Canonical URL
- [ ] Font preloads
- [ ] Schema markup (JSON-LD)
- [ ] Proper charset and viewport

### 3. Sidebar Layout Validation
- [ ] `#content` and `#grouping` are siblings (NOT nested)
- [ ] No duplicate major content blocks
- [ ] CSS uses `box-sizing: border-box`
- [ ] Width calculations don't exceed 100%

**Correct CSS:**
```css
#content {
  float: left;
  width: 70%;
  box-sizing: border-box;
  padding-right: 20px;
}
#grouping {
  float: right;
  width: 30%;
  box-sizing: border-box;
  padding-left: 20px;
}
```

### 4. Library Includes
- [ ] Only ONE sidemenu library per page
- [ ] Correct library for page type:
  - Base pages → base-sidemenu
  - Sport pages → sport-sidemenu
  - Event pages → events-sidemenu
- [ ] No duplicate library includes

### 5. External Links
- [ ] All external links have `target="_blank"`
- [ ] All external links have `rel="noopener"`
- [ ] Affiliate links have `rel="nofollow noopener"`

**Correct format:**
```html
<!-- External link -->
<a href="https://external.com" target="_blank" rel="noopener">Link</a>

<!-- Affiliate link -->
<a href="https://affiliate.com" target="_blank" rel="nofollow noopener">Link</a>
```

### 6. Mobile Responsiveness
- [ ] Mobile CSS included (@media max-width: 768px)
- [ ] Tested at 320px width minimum
- [ ] No fixed widths breaking mobile layout
- [ ] Touch targets minimum 44px

### 7. Accessibility
- [ ] Color contrast meets WCAG AA
- [ ] Minimum 16px base font on mobile
- [ ] ARIA labels on interactive elements
- [ ] Use TES accessible color palette

**TES Accessible Colors:**
```css
/* Primary */
--primary-green: #2e7d32;
--primary-green-dark: #1b5e20;

/* Text */
--text-primary: #333333;
--text-secondary: #495057; /* NOT #6c757d */

/* Accents */
--warning-yellow: #ffc107;
--danger-red: #d32f2f;
```

---

## Common Issues & Fixes

### Issue: Sidebar at Bottom
**Cause:** Nested sections, unclosed tags, duplicate content
**Fix:** Validate structure, ensure siblings not nested

### Issue: Side Panel Styling Broken
**Cause:** Missing CSS, specificity conflicts
**Fix:** Use `#grouping .extra` selector with complete CSS

### Issue: Mobile Display Problems
**Cause:** Missing responsive CSS, fixed widths
**Fix:** Include complete mobile CSS, use clamp() for fonts

---

## Output Format Standard

Always provide COMPLETE code:

```
===== HEAD SECTION =====
[complete HEAD code]

===== BODY SECTION =====
[complete BODY code]
```

- Single copy/paste operation
- NO partial fixes
- NO "replace line X with Y" instructions
- Ready to publish

---

**Document Version:** 1.0
**Last Updated:** December 2024
