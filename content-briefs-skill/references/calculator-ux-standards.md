# Calculator & Interactive UX Standards

**Purpose:** Standards for calculator pages and interactive elements
**Source:** Team feedback compilation (Issues #6-13, December 2024)
**Priority:** HIGH - Prevents common UX issues

---

## Core Principles

1. **Every "Add" needs a "Remove"** - Reversible actions
2. **Debounce all validation** - Don't interrupt typing
3. **Handle large numbers** - Abbreviate K/M format
4. **Mobile-first** - Test at 320px width
5. **Accessible** - 44px touch targets, WCAG AA colors

---

## 1. Search Functionality

### Required Elements
```html
<div class="search-container" style="display: flex; gap: 10px;">
  <input class="search-box" type="text" placeholder="Search...">
  <button class="search-btn">🔍 Search</button>
</div>

<!-- Results feedback banner -->
<div id="search-results-info" style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px;">
  Showing X results for "search term"
</div>
```

### Requirements
- [ ] Search button present (not just Enter key)
- [ ] Results count feedback shown
- [ ] Auto-scroll to results
- [ ] Clear visual separation

---

## 2. Add/Remove Functionality

### Rule: All "Add" MUST Have "Remove"

```html
<div class="leg-container" id="leg-1">
  <div class="leg-inputs">
    <!-- inputs here -->
  </div>
  <button class="remove-leg-btn" onclick="removeLeg(1)">✕ Remove</button>
</div>

<button class="add-leg-btn" onclick="addLeg()">+ Add Leg</button>
<button class="reset-btn" onclick="resetToDefault()">Reset to Default</button>
```

### Requirements
- [ ] Add button adds only 1 item (not 3)
- [ ] Remove button for each added item
- [ ] Reset to default option
- [ ] Visual feedback when adding/removing

---

## 3. Input Validation

### Rule: Debounce All Validation (500ms minimum)

```javascript
let validationTimeout;
function validateInput(input) {
  clearTimeout(validationTimeout);
  validationTimeout = setTimeout(() => {
    // Actual validation here
    if (!isValid(input.value)) {
      showError("American odds must be greater than 100 or less than -100");
    }
  }, 500); // 500ms delay
}
```

### Requirements
- [ ] 500ms minimum debounce delay
- [ ] Match validation rules to UI labels
- [ ] Helpful error messages (explain what's valid)
- [ ] Don't interrupt typing

### Error Message Format
```
❌ Bad: "Invalid input"
✅ Good: "American odds must be greater than +100 or less than -100 (e.g., +150 or -110)"
```

---

## 4. Number Formatting

### Rule: Abbreviate Large Numbers

```javascript
function formatCurrency(value) {
  if (value >= 1000000) return '$' + (value/1000000).toFixed(1) + 'M';
  if (value >= 1000) return '$' + (value/1000).toFixed(1) + 'K';
  return '$' + value.toFixed(2);
}

// Examples:
// 1500000 → "$1.5M"
// 25000 → "$25.0K"
// 150.50 → "$150.50"
```

### Requirements
- [ ] Abbreviate values 1000+ (K for thousands)
- [ ] Abbreviate values 1000000+ (M for millions)
- [ ] Test with extreme values (10+ digit numbers)
- [ ] Overflow handling in containers

### CSS for Overflow
```css
.result-value {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: clamp(10px, 2vw, 14px);
}
```

---

## 5. Mobile Display

### Test at 320px Width Minimum

```css
@media (max-width: 768px) {
  /* Banner alignment */
  #headline {
    display: flex;
    align-items: center;
    gap: 15px;
  }

  /* Horizontal scroll for buttons */
  .button-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    flex-wrap: nowrap;
  }

  /* Responsive fonts */
  .data-label {
    font-size: clamp(10px, 2vw, 14px);
  }

  /* Stack layouts */
  .calculator-row {
    flex-direction: column;
  }
}
```

### Requirements
- [ ] Test at 320px width
- [ ] No horizontal scroll on main content
- [ ] Buttons accessible (horizontal scroll OK for button rows)
- [ ] Touch targets 44px minimum
- [ ] No overlapping elements

---

## 6. Accessibility

### TES Accessible Color Palette
```css
:root {
  /* Primary - Use These */
  --primary-green: #2e7d32;
  --text-primary: #333333;
  --text-secondary: #495057;

  /* DO NOT USE */
  /* --muted: #6c757d; - Fails contrast */
}
```

### Touch Target Minimums
```css
button, .interactive, input, select {
  min-height: 44px;
  min-width: 44px;
}
```

### Requirements
- [ ] Color contrast WCAG AA (4.5:1 minimum)
- [ ] 44px minimum touch targets
- [ ] 16px minimum font on mobile
- [ ] ARIA labels on interactive elements

---

## 7. Side Panel (.extra class)

### Standard CSS (Always Include)
```css
#grouping .extra {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #2e7d32;
}

#grouping .extra h3 {
  margin-top: 0;
  color: #2e7d32;
}

#grouping .extra ul {
  padding-left: 25px;
  margin-left: 0;
}

#grouping .extra ul li {
  margin-bottom: 8px;
  padding-left: 5px;
  line-height: 1.6;
}

#grouping .extra ul li::before {
  margin-right: 8px !important;
}
```

### Requirements
- [ ] Use `#grouping .extra` selector (not just `.extra`)
- [ ] Include complete CSS in all calculator templates
- [ ] Use `!important` for properties that may conflict

---

## Pre-Output Checklist for Calculators

Before outputting calculator code:

**Functionality:**
- [ ] All "Add" has corresponding "Remove"
- [ ] Search has button (not just Enter)
- [ ] Validation debounced (500ms+)
- [ ] Reset to default option

**Display:**
- [ ] Large numbers abbreviated (K/M)
- [ ] Overflow handling on result displays
- [ ] Mobile tested at 320px
- [ ] No overlapping elements

**Accessibility:**
- [ ] Touch targets 44px minimum
- [ ] Color contrast passes WCAG AA
- [ ] ARIA labels present
- [ ] 16px minimum mobile font

**Side Panel:**
- [ ] Complete .extra CSS included
- [ ] Proper selector specificity

---

**Document Version:** 1.0
**Last Updated:** December 2024
