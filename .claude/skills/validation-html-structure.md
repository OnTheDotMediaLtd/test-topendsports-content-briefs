# HTML Structure Validation Skill

## Description
Critical skill for validating TopEndSports HTML structure to prevent layout-breaking issues. This site uses a specific HTML architecture that MUST be followed exactly or content will display full-width without sidebar.

## When to Use This Skill
- Before delivering any optimized HTML file
- When creating new page templates
- After making structural changes to existing pages
- When debugging layout issues
- During quality assurance reviews

## Core Validation Rules

### 1. ID Selectors vs Class Selectors (CRITICAL)

**CORRECT:**
```html
<div id="content">
    <!-- Page content here -->
</div>
```

**WRONG:**
```html
<div class="content">
    <!-- This breaks layout! -->
</div>
```

**Why This Matters:**
The site CSS uses ID selectors (#content, #container, #grouping), not class selectors. Using class= instead of id= will cause the page to render full-width without the sidebar, breaking the entire site layout.

### 2. Required Container Hierarchy

```html
<div id="container">
    <div id="content">
        [ALL page content goes here]
    </div>
    <!-- CLOSE content div -->

    <div id="grouping">
        [Sidebar libraries go here]
    </div>
    <!-- CLOSE grouping div -->

    <div class="clearfix"></div>
</div>
<!-- CLOSE container div -->
```

**Hierarchy Validation:**
- container MUST wrap both content and grouping
- content MUST be sibling to grouping (not nested inside)
- clearfix div MUST appear before closing container
- All divs MUST have proper closing tags

### 3. Required Library Items (6 Total)

**Before Container:**
```html
<!-- Header Library -->
<!-- #BeginLibraryItem "/Library/all-header.lbi" -->
{--/Library/all-header.lbi--}
<!-- #EndLibraryItem -->
```

**Inside Grouping Div:**
```html
<!-- #BeginLibraryItem "/Library/all-search.lbi" -->
{--/Library/all-search.lbi--}
<!-- #EndLibraryItem -->

<!-- #BeginLibraryItem "/Library/sport-sidemenu.lbi" -->
{--/Library/sport-sidemenu.lbi--}
<!-- #EndLibraryItem -->

<!-- #BeginLibraryItem "/Library/all-sidebar.lbi" -->
{--/Library/all-sidebar.lbi--}
<!-- #EndLibraryItem -->
```

**After Container:**
```html
<!-- Citation Library -->
<!-- #BeginLibraryItem "/Library/all-citation.lbi" -->
{--/Library/all-citation.lbi--}
<!-- #EndLibraryItem -->

<!-- Footer Library -->
<!-- #BeginLibraryItem "/Library/all-footer.lbi" -->
{--/Library/all-footer.lbi--}
<!-- #EndLibraryItem -->
```

**Library Validation Rules:**
- NEVER modify library code syntax
- NEVER remove library placeholders
- NEVER change library order
- Preserve exact formatting including comments

### 4. JavaScript Placement (Dreamweaver Compatibility)

**CORRECT - All JavaScript in HEAD:**
```html
<head>
    <meta charset="UTF-8">
    <title>Page Title</title>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // All interactive functionality here
    });
    </script>
</head>
```

**WRONG - Inline Scripts in BODY:**
```html
<body>
    <div class="interactive-element"></div>
    <script>
        // This breaks Dreamweaver - NEVER DO THIS
    </script>
</body>
```

**Why:** Dreamweaver has compatibility issues with inline body scripts. All JavaScript must be in the head section.

## Validation Checklist

Run through this checklist before delivering any file:

### Structural Elements
- [ ] Uses `id="content"` NOT `class="content"`
- [ ] Uses `id="container"` as wrapper
- [ ] Uses `id="grouping"` for sidebar
- [ ] Proper nesting: container > (content + grouping)
- [ ] Has `<div class="clearfix"></div>` before closing container
- [ ] No orphaned or unclosed divs

### Library Items
- [ ] all-header.lbi present before container
- [ ] all-search.lbi present in grouping
- [ ] sport-sidemenu.lbi present in grouping
- [ ] all-sidebar.lbi present in grouping
- [ ] all-citation.lbi present after container
- [ ] all-footer.lbi present after container
- [ ] All library codes preserved exactly as-is

### JavaScript & Technical
- [ ] ALL JavaScript in `<head>` section
- [ ] No inline scripts in `<body>`
- [ ] File ends with `</body></html>` (no truncation)
- [ ] All opening tags have matching closing tags
- [ ] HTML validates when checked

## Common Mistakes to Avoid

### Mistake 1: Using Class Instead of ID
```html
<!-- WRONG -->
<div class="content">
<div class="container">
<div class="grouping">
```
**Impact:** Complete layout failure, full-width content, no sidebar

### Mistake 2: Incorrect Nesting
```html
<!-- WRONG -->
<div id="container">
    <div id="content">
        <div id="grouping">  <!-- grouping inside content -->
```
**Impact:** Sidebar appears inside content area instead of beside it

### Mistake 3: Missing Clearfix
```html
<!-- WRONG -->
<div id="container">
    <div id="content">...</div>
    <div id="grouping">...</div>
</div>  <!-- No clearfix before closing -->
```
**Impact:** Float collapse, layout instability

### Mistake 4: Inline Body Scripts
```html
<!-- WRONG -->
<body>
    <script>
        // Inline script
    </script>
</body>
```
**Impact:** Dreamweaver compatibility issues, script may not execute

## Testing Procedure

1. **Visual Inspection:**
   - Search for `class="content"` - should be ZERO results
   - Search for `id="content"` - should be ONE result
   - Search for `id="container"` - should be ONE result
   - Search for `id="grouping"` - should be ONE result

2. **Structure Verification:**
   - Verify container wraps both content and grouping
   - Verify clearfix div exists before closing container
   - Count library items - should be exactly 6

3. **JavaScript Check:**
   - Search for `<script>` tags in body - should be ZERO
   - Verify all scripts are in head section

4. **Completeness Check:**
   - File must end with `</body></html>`
   - No truncation or cut-off content
   - All opening tags have closing tags

## Success Criteria

A file passes HTML structure validation when:
1. Layout renders correctly with sidebar visible
2. All 6 library items are present and functional
3. No layout-breaking class selectors used
4. Proper container > content + grouping hierarchy maintained
5. All JavaScript in head section
6. File is complete with no truncation
7. HTML validates without structural errors

## Quick Reference Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags, title, CSS -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // All JS here
    });
    </script>
</head>
<body>

<!-- #BeginLibraryItem "/Library/all-header.lbi" -->
{--/Library/all-header.lbi--}
<!-- #EndLibraryItem -->

<div id="container">

    <div id="content">
        <!-- PAGE CONTENT -->
    </div>

    <div id="grouping">
        <!-- #BeginLibraryItem "/Library/all-search.lbi" -->
        {--/Library/all-search.lbi--}
        <!-- #EndLibraryItem -->

        <!-- #BeginLibraryItem "/Library/sport-sidemenu.lbi" -->
        {--/Library/sport-sidemenu.lbi--}
        <!-- #EndLibraryItem -->

        <!-- #BeginLibraryItem "/Library/all-sidebar.lbi" -->
        {--/Library/all-sidebar.lbi--}
        <!-- #EndLibraryItem -->
    </div>

    <div class="clearfix"></div>
</div>

<!-- #BeginLibraryItem "/Library/all-citation.lbi" -->
{--/Library/all-citation.lbi--}
<!-- #EndLibraryItem -->

<!-- #BeginLibraryItem "/Library/all-footer.lbi" -->
{--/Library/all-footer.lbi--}
<!-- #EndLibraryItem -->

</body>
</html>
```

## Related Skills
- content-preservation.md - Preserve expert content while fixing structure
- interactive-elements.md - Add interactive elements with proper JS placement
- research-workflow.md - Complete workflow including validation step
