# Interactive Elements Skill

## Description
Comprehensive skill for adding 7 types of interactive elements that break up text-heavy content, enhance user engagement, and improve page performance. All elements designed for mobile-first experience with proper JavaScript placement in HEAD section.

## When to Use This Skill
- For pages over 1,500 words (minimum 3-4 elements)
- When breaking up text-heavy sections
- To improve engagement metrics
- For enhancing mobile user experience
- When adding visual variety to content

## Core Interactive Philosophy

**ENGAGEMENT > DECORATION**

Every interactive element must add genuine value, not just visual appeal. If an element doesn't help the user, don't add it.

## The 7 Interactive Element Types

### 1. Decision Tool / Flowchart

**Purpose:** Guide users through betting decisions

**When to Use:**
- Complex decision-making scenarios
- "Should I bet X or Y?" questions
- Multi-step thought processes

**Example Use Case:**
```
"Should I bet the over or under?"
  → Check average score
    → Is it higher than line?
      → YES: Consider over
      → NO: Consider under
```

**Implementation:**
```html
<div class="decision-tool">
    <h3>Find Your Best Bet Type</h3>
    <div class="decision-step" id="step1">
        <p>What's your betting goal?</p>
        <button onclick="showStep(2, 'higher-payout')">Higher Payout</button>
        <button onclick="showStep(2, 'safer-bet')">Safer Bet</button>
    </div>
    <div class="decision-step" id="step2" style="display:none;">
        <!-- Next step -->
    </div>
</div>
```

### 2. Interactive Checklist

**Purpose:** Help users prepare or verify readiness

**When to Use:**
- Pre-game betting preparation
- Verification workflows
- Step-by-step processes

**Example Use Case:**
```
Pre-Game Betting Checklist:
☐ Reviewed team stats
☐ Checked injury reports
☐ Compared odds across books
☐ Set betting limit
☐ Identified value bets
```

**Implementation:**
```html
<div class="interactive-checklist">
    <h3>Pre-Game Checklist</h3>
    <div class="checklist-item">
        <input type="checkbox" id="check1" onchange="updateProgress()">
        <label for="check1">Reviewed team statistics</label>
    </div>
    <div class="checklist-item">
        <input type="checkbox" id="check2" onchange="updateProgress()">
        <label for="check2">Checked injury reports</label>
    </div>
    <div class="checklist-progress">
        <span id="progress-text">0 of 5 complete</span>
    </div>
    <button onclick="window.print()">Print Checklist</button>
</div>
```

### 3. Scenario Cards

**Purpose:** Present betting scenarios with analysis

**When to Use:**
- Explaining betting situations
- Example scenarios
- Case studies

**Example Use Case:**
```
FRONT: Lakers -7.5 vs Suns
BACK: Lakers must win by 8+ for bet to win. Consider:
- Lakers home record
- Suns defensive stats
- Recent head-to-head
```

**Implementation:**
```html
<div class="scenario-card" onclick="this.classList.toggle('expanded')">
    <div class="scenario-question">
        <h4>Scenario 1: Lakers -7.5 vs Suns</h4>
        <p>Should you bet the spread?</p>
    </div>
    <div class="scenario-answer">
        <p><strong>Analysis:</strong> Lakers must win by 8+ points...</p>
        <ul>
            <li>Lakers: 12-5 at home</li>
            <li>Suns: Allowing 110 PPG away</li>
            <li>H2H: Lakers won by 12 last meeting</li>
        </ul>
        <p><strong>Verdict:</strong> Spread has value</p>
    </div>
</div>
```

### 4. Stat Callout Boxes

**Purpose:** Highlight key statistics visually

**When to Use:**
- Important numbers/percentages
- Breaking up text walls
- Emphasizing key data points

**Example Use Case:**
```
╔════════════════╗
║      73%       ║
║   Home Wins    ║
╚════════════════╝
```

**Implementation:**
```html
<div class="stat-callout">
    <div class="big-number">73%</div>
    <div class="stat-label">of NBA games won by home team in 2024</div>
    <div class="stat-context">Consider home advantage when betting</div>
</div>
```

### 5. Definition Boxes

**Purpose:** Explain betting terminology

**When to Use:**
- First mention of technical terms
- Jargon that needs explanation
- Beginner-focused content

**Example Use Case:**
```
┌──────────────────────────────────────┐
│ Point Spread: A margin set by        │
│ oddsmakers that the favorite must     │
│ win by for the bet to pay out.        │
└──────────────────────────────────────┘
```

**Implementation:**
```html
<div class="definition-box">
    <strong>Point Spread:</strong> A margin set by oddsmakers that
    the favorite must win by for the bet to pay out. For example,
    if the Lakers are -7.5, they must win by 8 or more points.
</div>
```

### 6. Key Takeaway Boxes

**Purpose:** Summarize sections for AI/LLM pickup and scanning users

**When to Use:**
- End of major sections
- Complex explanations
- Quick reference summaries

**Example Use Case:**
```
🎯 Key Takeaway
• Always compare odds across multiple books
• Home teams win 55% of NBA games
• Bankroll management is critical
```

**Implementation:**
```html
<div class="key-takeaway">
    <h4>Key Takeaway</h4>
    <ul>
        <li>Always compare odds across multiple sportsbooks</li>
        <li>Home teams have 55% win rate in NBA</li>
        <li>Never bet more than 5% of bankroll on single game</li>
    </ul>
</div>
```

### 7. Comparison Tables

**Purpose:** Compare options side-by-side

**When to Use:**
- Sportsbook comparisons
- Bet type comparisons
- Feature comparisons

**Example Use Case:**
```
╔════════════╦═══════╦═══════╦══════════╗
║ Sportsbook ║ Bonus ║ App   ║ Promos   ║
╠════════════╬═══════╬═══════╬══════════╣
║ FanDuel    ║ $1000 ║ 4.8★  ║ Daily    ║
║ BetMGM     ║ $1000 ║ 4.7★  ║ Weekly   ║
║ DraftKings ║ $1200 ║ 4.6★  ║ Daily    ║
╚════════════╩═══════╩═══════╩══════════╝
```

**Implementation:**
```html
<div class="comparison-table-wrapper">
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Sportsbook</th>
                <th>Bonus Offer</th>
                <th>App Rating</th>
                <th>Promotions</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>FanDuel</strong></td>
                <td>Up to $1,000</td>
                <td>4.8★</td>
                <td>Daily promos</td>
            </tr>
            <!-- More rows -->
        </tbody>
    </table>
</div>
```

## JavaScript Placement Rules

**CRITICAL: All JavaScript MUST go in <head> section for Dreamweaver compatibility**

### CORRECT Approach:

```html
<head>
    <title>Page Title</title>
    <meta charset="UTF-8">

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // All interactive element code goes here

        // Checklist functionality
        window.updateProgress = function() {
            var checkboxes = document.querySelectorAll('.checklist-item input');
            var checked = document.querySelectorAll('.checklist-item input:checked').length;
            var total = checkboxes.length;
            document.getElementById('progress-text').textContent =
                checked + ' of ' + total + ' complete';
        };

        // Scenario cards
        var cards = document.querySelectorAll('.scenario-card');
        cards.forEach(function(card) {
            card.addEventListener('click', function() {
                this.classList.toggle('expanded');
            });
        });
    });
    </script>
</head>
```

### WRONG Approach (DO NOT DO THIS):

```html
<body>
    <div class="checklist">...</div>
    <script>
        // This breaks Dreamweaver - NEVER DO THIS
    </script>
</body>
```

## CSS for Interactive Elements

**Add all CSS in <head> section:**

```html
<style>
/* Stat Callout Box */
.stat-callout {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #fff;
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin: 1.5rem 0;
}
.stat-callout .big-number {
    font-size: 3rem;
    font-weight: 700;
    color: #4ade80;
}
.stat-callout .stat-label {
    font-size: 0.9rem;
    opacity: 0.8;
    margin-top: 0.5rem;
}

/* Definition Box */
.definition-box {
    background: #f0f9ff;
    border-left: 4px solid #0ea5e9;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    border-radius: 0 8px 8px 0;
}
.definition-box strong {
    color: #0369a1;
}

/* Key Takeaway Box */
.key-takeaway {
    background: #f0fdf4;
    border: 2px solid #22c55e;
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 8px;
}
.key-takeaway h4 {
    color: #15803d;
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
}

/* Interactive Checklist */
.interactive-checklist {
    background: #fefce8;
    border: 2px solid #eab308;
    padding: 1.5rem;
    margin: 1.5rem 0;
    border-radius: 10px;
}
.checklist-item {
    display: flex;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #fef08a;
}
.checklist-item:last-child {
    border-bottom: none;
}
.checklist-item input[type="checkbox"] {
    width: 20px;
    height: 20px;
    margin-right: 12px;
}
.checklist-progress {
    background: #fef08a;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    margin-top: 1rem;
    text-align: center;
    font-weight: 600;
}

/* Scenario Cards */
.scenario-card {
    background: #fff;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}
.scenario-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}
.scenario-card .scenario-answer {
    display: none;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}
.scenario-card.expanded .scenario-answer {
    display: block;
}

/* Comparison Table */
.comparison-table-wrapper {
    overflow-x: auto;
    margin: 1.5rem 0;
}
.comparison-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 600px;
}
.comparison-table thead {
    background: #2e7d32;
    color: #fff;
}
.comparison-table th,
.comparison-table td {
    padding: 12px;
    text-align: left;
    border: 1px solid #e5e7eb;
}
.comparison-table tbody tr:nth-child(even) {
    background: #f9fafb;
}
</style>
```

## Element Placement Guidelines

### For 1,500-2,000 Word Content:

**Minimum: 3-4 interactive elements**

```
[Intro] (0-200 words)
[Section 1] (200-500 words)
[STAT CALLOUT] ← Element #1
[Section 2] (500-800 words)
[DEFINITION BOX] ← Element #2
[Section 3] (800-1,100 words)
[INTERACTIVE CHECKLIST] ← Element #3
[Section 4] (1,100-1,400 words)
[KEY TAKEAWAY] ← Element #4
[FAQ] (1,400-1,600 words)
[Conclusion] (1,600-1,800 words)
```

**Placement Rules:**
- One element every 400-600 words
- Alternate between different types
- Don't use same element type twice in a row
- Place at natural content breaks

## Mobile Optimization

**All elements must work on touch devices:**

### Mobile-Specific Considerations:

1. **Touch Targets:**
   - Minimum 44x44px tap targets
   - Adequate spacing between clickable elements

2. **Horizontal Scrolling:**
   - Tables must scroll horizontally on mobile
   - Use `overflow-x: auto` wrapper

3. **Expandable Sections:**
   - Test accordion functionality on iOS and Android
   - Ensure smooth animations

4. **Form Inputs:**
   - Checkboxes large enough to tap
   - Labels associated with inputs

### Mobile CSS Example:

```css
@media (max-width: 768px) {
    .stat-callout {
        padding: 1rem;
    }

    .stat-callout .big-number {
        font-size: 2.5rem;
    }

    .scenario-card {
        padding: 1rem;
    }

    .checklist-item {
        padding: 0.75rem 0;
    }

    .checklist-item input[type="checkbox"] {
        width: 24px;
        height: 24px;
    }
}
```

## Validation Checklist

### Before Delivery:

- [ ] 3-4 interactive elements for 1,500+ word content
- [ ] Elements placed every 400-600 words
- [ ] Different element types used (no repetition)
- [ ] ALL JavaScript in <head> section (not inline in body)
- [ ] ALL CSS in <head> section
- [ ] Mobile-friendly (tested on touch devices)
- [ ] Tables scroll horizontally on mobile
- [ ] Touch targets minimum 44x44px
- [ ] Elements add value (not just decoration)
- [ ] Smooth animations and transitions

## Common Mistakes to Avoid

### Mistake 1: Inline Body Scripts
```
WRONG:
<body>
    <div class="checklist">...</div>
    <script>// Inline script</script>
</body>

RIGHT:
<head>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // All scripts here
    });
    </script>
</head>
```

### Mistake 2: Same Element Type Repeated
```
WRONG:
[Definition Box]
[200 words]
[Definition Box]
[200 words]
[Definition Box]

RIGHT:
[Definition Box]
[400 words]
[Stat Callout]
[400 words]
[Interactive Checklist]
```

### Mistake 3: Decorative Elements
```
WRONG:
Adding stat callout just for visual appeal without relevant stat

RIGHT:
Adding stat callout with meaningful, actionable statistic
```

### Mistake 4: Poor Mobile Experience
```
WRONG:
Table with 8 columns that doesn't scroll horizontally

RIGHT:
Table wrapped in scrollable container with overflow-x: auto
```

## Success Criteria

Interactive elements are successful when:

1. 3-4 elements present for 1,500+ word content
2. Elements distributed evenly (every 400-600 words)
3. Different element types used throughout
4. All JavaScript in HEAD section
5. All CSS in HEAD section
6. Mobile-optimized (touch-friendly, scrollable tables)
7. Elements add genuine value to user experience
8. Smooth functionality across all devices
9. No inline scripts in BODY
10. Proper semantic HTML structure

## Related Skills
- validation-html-structure.md - Proper HTML structure for elements
- content-preservation.md - Add elements without disrupting expert content
- cta-placement-strategy.md - Coordinate CTAs with interactive elements
- seo-keyword-integration.md - Use keywords in element content
- research-workflow.md - Complete workflow including interactive element planning
