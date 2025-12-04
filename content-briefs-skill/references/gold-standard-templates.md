# GOLD STANDARD TEMPLATES v1.0

**Purpose:** Exact HTML/CSS/JS templates for page uniformity across all betting content pages
**Source:** Team feedback and Claude AI session patterns (December 2024)
**Note:** These templates are MANDATORY for all betting content pages

---

## CORE BRAND LIST (December 2025)

| # | Brand | Badge Code | Color | Status |
|---|-------|------------|-------|--------|
| 1 | FanDuel | FD | #1493ff | Active |
| 2 | DraftKings | DK | #53d337 | Active |
| 3 | BetMGM | MGM | #bfa36b | Active |
| 4 | Caesars | CZR | #0a2240 | Active |
| 5 | bet365 | 365 | #0e7b46 | Active |
| 6 | Fanatics | FAN | #0050c8 | Active |
| 7 | theScore BET | SCR | #6B2D5B | Active (formerly ESPN BET - rebranded Dec 2025) |
| 8 | BetRivers | BR | #ff6b00 | Secondary |

> **CRITICAL:** ESPN BET shut down on December 1, 2025. It is now theScore BET. All new pages must use theScore BET branding.

---

## TECHNICAL FOUNDATION (V3 Approach - Dreamweaver Compatible)

### JavaScript Location Rules
- ALL JavaScript must be placed in the `<head>` section in ONE `<script>` tag
- Use DOMContentLoaded wrapper for proper initialization
- Dreamweaver-compatible structure (no inline JS in body except onclick/onchange)
- No localStorage/sessionStorage (won't work in artifacts/preview environments)

### Initialization Pattern
```javascript
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Interactive elements initialized');

    // Initialize all interactive components
    initCollapsibleIntro();
    initStateFilter();
    initBrandCards();
    initTabbedContent();
    initStickyBar();
    initAccordions();
    initQuiz();
    // etc.
});
```

### Console Logging for Debugging
- Include extensive console.log statements during development
- Format: `console.log('🔍 Function: action performed');`
- Use emojis for easy visual identification in console

---

## LETTER BADGE LOGOS (NO Images)

Use text-based letter badges instead of image logos. Prevents 404 errors, faster loading, more reliable.

### Badge CSS
```css
.letter-badge {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 16px;
    color: white;
    flex-shrink: 0;
}

/* Brand-specific colors */
.badge-fd { background: #1493ff; }  /* FanDuel - Blue */
.badge-dk { background: #53d337; }  /* DraftKings - Green */
.badge-mgm { background: #bfa36b; } /* BetMGM - Gold/Brown */
.badge-czr { background: #0a2240; } /* Caesars - Dark Blue */
.badge-365 { background: #0e7b46; } /* bet365 - Green */
.badge-fan { background: #0050c8; } /* Fanatics - Blue */
.badge-scr { background: #6B2D5B; } /* theScore BET - Purple */
.badge-br { background: #ff6b00; }  /* BetRivers - Orange */
```

---

## GOLD STANDARD: COMPARISON TABLE

### Container HTML
```html
<div class="wc-comparison">
    <div class="table-header">
        <h2>Top 7 [Topic] Betting Sites</h2>
    </div>
    <div class="mobile-scroll-hint">
        ⟵ Swipe left to see full details ⟶
    </div>
    <div class="table-wrapper">
        <table>
            <thead>
                <tr>
                    <th>Sportsbook</th>
                    <th>[Topic] Features</th>
                    <th>Terms & Conditions</th>
                </tr>
            </thead>
            <tbody>
                <!-- Brand rows go here -->
            </tbody>
        </table>
    </div>
    <p class="table-disclaimer">*21+ only. Must be physically located in legal state. T&Cs apply. Gamble responsibly.</p>
</div>
```

### Individual Row Template
```html
<tr>
    <td>
        <div class="sportsbook-cell">
            <div class="book-logo badge-fd">FD</div>
            <div class="book-info">
                <span class="book-name">FanDuel</span>
                <div class="book-rating">
                    <span class="rating-stars">★★★★★</span>
                    <span class="rating-number">4.9/5</span>
                </div>
            </div>
        </div>
        <div class="bonus-cell">
            <span class="bonus-amount">Bet $5, Get $150</span>
            <span class="bonus-details">in Bonus Bets if you win</span>
            <a href="#" class="cta-button">Visit FanDuel →</a>
        </div>
    </td>
    <td>
        <span class="wc-highlight">[KEY DIFFERENTIATOR]</span>
        <div class="features-list">
            <span class="feature-tag">[Feature 1]</span>
            <span class="feature-tag">[Feature 2]</span>
            <span class="feature-tag">[Feature 3]</span>
            <span class="feature-tag">[Feature 4]</span>
        </div>
        <p>[Brief 1-2 sentence description]</p>
    </td>
    <td>
        <div class="terms-box">
            <strong>Welcome Offer Terms</strong>
            <ul>
                <li>[Term 1]</li>
                <li>[Term 2]</li>
                <li>[Term 3]</li>
            </ul>
            <p class="gambling-warning">GAMBLING PROBLEM? Call 1-800-GAMBLER. Must be 21+. T&Cs apply.</p>
        </div>
    </td>
</tr>
```

### Comparison Table CSS
```css
.wc-comparison {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 2rem 0;
}

.table-header h2 {
    margin-top: 0;
    color: #2e7d32;
}

.mobile-scroll-hint {
    display: none;
    background: #fff3cd;
    padding: 0.75rem;
    border-radius: 4px;
    text-align: center;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #856404;
}

@media (max-width: 768px) {
    .mobile-scroll-hint {
        display: block;
        animation: pulse 2s infinite;
    }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.wc-comparison table {
    width: 100%;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-collapse: collapse;
    table-layout: fixed;
}

.wc-comparison th {
    background: #2e7d32;
    color: white;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
}

.wc-comparison td {
    padding: 1rem 0.75rem;
    border-bottom: 1px solid #dee2e6;
    vertical-align: top;
}

.sportsbook-cell {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.book-logo {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-weight: bold;
    font-size: 0.9rem;
    color: white;
    flex-shrink: 0;
}

.book-name {
    font-weight: 700;
    font-size: 1.1rem;
    color: #333;
}

.bonus-amount {
    font-weight: 700;
    font-size: 1rem;
    color: #2e7d32;
    display: block;
}

.bonus-details {
    font-size: 0.85rem;
    color: #666;
    display: block;
    margin-bottom: 0.5rem;
}

.cta-button {
    display: inline-block;
    background: #2e7d32;
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    transition: background 0.3s ease;
}

.cta-button:hover {
    background: #1b5e20;
}

.wc-highlight {
    display: block;
    font-weight: 700;
    color: #2e7d32;
    margin-bottom: 0.5rem;
}

.feature-tag {
    display: inline-block;
    background: #e8f5e9;
    color: #2e7d32;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    margin: 0.2rem;
    border: 1px solid #c8e6c9;
}

.terms-box {
    background: #fff3cd;
    padding: 0.75rem;
    border-radius: 6px;
    border-left: 4px solid #ffc107;
    font-size: 0.85rem;
}

.gambling-warning {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 2px solid #ffc107;
    font-weight: 600;
    color: #d32f2f;
}
```

---

## GOLD STANDARD: BRAND CARDS

### Complete Brand Card Template
```html
<div class="brand-card">
    <div class="brand-card-header">
        <div class="letter-badge badge-fd">FD</div>
        <h3 class="brand-card-title">FanDuel - [Unique Value Proposition]</h3>
    </div>

    <p class="brand-intro">[Brief introduction explaining why this brand excels for this specific topic. Should be unique to the page topic, not generic copy.]</p>

    <div class="brand-features">
        <div class="feature-item">
            <span class="feature-icon">✓</span>
            <span>[Key feature 1 relevant to page topic]</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">✓</span>
            <span>[Key feature 2 relevant to page topic]</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">✓</span>
            <span>[Key feature 3 relevant to page topic]</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">✓</span>
            <span>[Key feature 4 relevant to page topic]</span>
        </div>
    </div>

    <button class="unique-features-toggle" onclick="toggleUniqueFeatures('fanduel')">
        <span>View Detailed Unique Features</span>
        <span class="toggle-icon">▶</span>
    </button>

    <div id="unique-features-fanduel" class="unique-features-content">
        <h4>[Feature Title 1] - [Descriptive Subtitle]</h4>
        <p>[Detailed explanation of this unique feature. Include specific numbers, comparisons to competitors, and practical examples. Approximately 150-200 words.]</p>

        <h4>[Feature Title 2] - [Descriptive Subtitle]</h4>
        <p>[Detailed explanation with specific data points.]</p>

        <h4>[Feature Title 3] - [Descriptive Subtitle]</h4>
        <p>[Detailed explanation focusing on user benefits.]</p>

        <!-- PROS/CONS TABLE (MANDATORY) -->
        <table class="pros-cons-table">
            <thead>
                <tr>
                    <th>Pros</th>
                    <th>Cons</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <ul>
                            <li>[Pro 1]</li>
                            <li>[Pro 2]</li>
                            <li>[Pro 3]</li>
                            <li>[Pro 4]</li>
                            <li>[Pro 5]</li>
                        </ul>
                    </td>
                    <td>
                        <ul>
                            <li>[Con 1]</li>
                            <li>[Con 2]</li>
                            <li>[Con 3]</li>
                        </ul>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="brand-ctas">
        <a href="#" class="cta-primary">Claim FanDuel Bonus</a>
        <a href="/sport/betting/sportsbook-reviews/fanduel/index.htm" class="cta-secondary">Read Full Review</a>
    </div>

    <!-- T&Cs Section (MANDATORY) -->
    <div class="brand-terms">
        <h4>Complete Terms & Conditions - FanDuel Sportsbook</h4>
        <div class="terms-content">
            <p class="offer-headline">[Welcome Offer Headline]</p>
            <h5>Eligibility Requirements</h5>
            <ul>
                <li>[Requirement 1]</li>
                <li>[Requirement 2]</li>
                <li>[Requirement 3]</li>
            </ul>
            <h5>Bonus Terms</h5>
            <ul>
                <li>[Term 1]</li>
                <li>[Term 2]</li>
                <li>[Term 3]</li>
            </ul>
            <p class="critical-note"><strong>Critical:</strong> [Important caveat about the offer]</p>
            <p class="legal-terms">Complete Legal Terms: [Full legal disclaimer text]</p>
            <p class="last-verified">Last Verified: [Current Month Year]</p>
        </div>
    </div>
</div>
```

### Brand Card CSS
```css
.brand-card {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 4px solid #2e7d32;
}

.brand-card-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.brand-card-title {
    margin: 0;
    color: #333;
    font-size: 1.5rem;
}

.brand-features {
    margin: 1.5rem 0;
}

.feature-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.5rem 0;
    line-height: 1.6;
}

.feature-icon {
    font-size: 1.2rem;
    flex-shrink: 0;
    min-width: 24px;
    color: #2e7d32;
}

.brand-ctas {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.cta-primary {
    background: #2e7d32;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    transition: background 0.3s ease;
}

.cta-primary:hover {
    background: #1b5e20;
}

.cta-secondary {
    background: white;
    color: #2e7d32;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    border: 2px solid #2e7d32;
    transition: all 0.3s ease;
}

.cta-secondary:hover {
    background: #e8f5e9;
}

.unique-features-toggle {
    background: #f1f8f4;
    border: 2px solid #2e7d32;
    color: #2e7d32;
    padding: 0.7rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.unique-features-toggle:hover {
    background: #e8f5e9;
}

.toggle-icon {
    font-size: 1.2rem;
    transition: transform 0.3s ease;
}

.unique-features-toggle.active .toggle-icon {
    transform: rotate(90deg);
}

.unique-features-content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.5s ease;
}

.unique-features-content.active {
    max-height: 2000px;
    padding: 1rem 0;
}

.pros-cons-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

.pros-cons-table th {
    background: #f8f9fa;
    padding: 0.75rem;
    text-align: left;
}

.pros-cons-table td {
    padding: 0.75rem;
    vertical-align: top;
}

.pros-cons-table ul {
    margin: 0;
    padding-left: 1.5rem;
}
```

### JavaScript for Expandable Features
```javascript
function toggleUniqueFeatures(brandId) {
    const content = document.getElementById('unique-features-' + brandId);
    const toggle = content.previousElementSibling;

    toggle.classList.toggle('active');
    content.classList.toggle('active');
    console.log('🔄 Feature toggle clicked for: ' + brandId);
}
```

---

## GOLD STANDARD: TABBED REVIEW SYSTEM

### Tab Navigation HTML
```html
<div class="review-tabs-container">
    <h2>Detailed Analysis of the Best [Topic] Sportsbooks</h2>
    <p>Click on each sportsbook below to see detailed features, pros/cons, and complete bonus terms.</p>

    <div class="review-tabs">
        <button class="review-tab active" data-tab="tab-fanduel">FanDuel</button>
        <button class="review-tab" data-tab="tab-draftkings">DraftKings</button>
        <button class="review-tab" data-tab="tab-betmgm">BetMGM</button>
        <button class="review-tab" data-tab="tab-caesars">Caesars</button>
        <button class="review-tab" data-tab="tab-bet365">bet365</button>
        <button class="review-tab" data-tab="tab-fanatics">Fanatics</button>
        <button class="review-tab" data-tab="tab-thescore">theScore BET</button>
    </div>

    <div id="tab-fanduel" class="review-tab-content active">
        <!-- Brand card content here -->
    </div>
    <div id="tab-draftkings" class="review-tab-content">
        <!-- Brand card content here -->
    </div>
    <!-- Additional tabs... -->
</div>
```

### Tab CSS
```css
.review-tabs {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 2rem 0 1rem 0;
    border-bottom: 2px solid #ddd;
    padding-bottom: 0.5rem;
}

.review-tab {
    background: white;
    border: 2px solid #ddd;
    padding: 0.7rem 1.2rem;
    border-radius: 6px 6px 0 0;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    color: #666;
}

.review-tab:hover {
    border-color: #2e7d32;
    color: #2e7d32;
}

.review-tab.active {
    background: #2e7d32;
    color: white;
    border-color: #2e7d32;
}

.review-tab-content {
    display: none;
}

.review-tab-content.active {
    display: block;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

### Tab JavaScript
```javascript
function initReviewTabs() {
    const tabs = document.querySelectorAll('.review-tab');
    const contents = document.querySelectorAll('.review-tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetId = this.getAttribute('data-tab');

            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            document.getElementById(targetId).classList.add('active');

            console.log('📑 Tab switched to: ' + targetId);
        });
    });
}

// Call in DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    initReviewTabs();
});
```

---

## INTERACTIVE ELEMENTS CATALOG

### 1. Collapsible Intro Section
**Purpose:** Reduce initial page height, push comparison table/CTAs above the fold

```javascript
function toggleIntroContent() {
    var fullContent = document.getElementById('introFullContent');
    var toggleBtn = document.getElementById('introToggleBtn');

    if (fullContent.style.display === 'none' || fullContent.style.display === '') {
        fullContent.style.display = 'block';
        toggleBtn.innerHTML = 'Read Less ▲';
        console.log('✅ Intro expanded');
    } else {
        fullContent.style.display = 'none';
        toggleBtn.innerHTML = 'Read More ▼';
        console.log('✅ Intro collapsed');
    }
}
```

```css
.intro-wrapper {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    border-left: 4px solid #2e7d32;
}

.intro-toggle-btn {
    background: #2e7d32;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;
}

.intro-toggle-btn:hover {
    background: #1b5e20;
    transform: translateY(-2px);
}
```

### 2. State Availability Filter
**Purpose:** Compliance feature - users can check which sportsbooks are legal in their state

```javascript
function checkState() {
    var stateCode = document.getElementById('state-select').value;
    var resultsDiv = document.getElementById('state-results');
    var clearBtn = document.getElementById('clear-state-btn');

    if (!stateCode) {
        resultsDiv.innerHTML = 'Please select a state';
        clearBtn.style.display = 'none';
        return;
    }

    var stateInfo = stateData[stateCode];
    if (stateInfo) {
        var html = '<strong>Available in ' + stateInfo.name + ':</strong><br>';
        stateInfo.books.forEach(function(book) {
            html += '<span class="available-book">' + book + '</span>';
        });
        resultsDiv.innerHTML = html;
        clearBtn.style.display = 'inline-block';
        console.log('✅ State filter applied: ' + stateCode);
    }
}

function clearStateFilter() {
    document.getElementById('state-select').value = '';
    document.getElementById('state-results').innerHTML = '';
    document.getElementById('clear-state-btn').style.display = 'none';
    console.log('✅ State filter cleared');
}
```

### 3. FAQ Accordion
```javascript
function initAccordions() {
    var faqItems = document.querySelectorAll('.faq-accordion');

    faqItems.forEach(function(item) {
        var question = item.querySelector('.faq-question');

        if (question) {
            question.addEventListener('click', function() {
                var wasActive = item.classList.contains('active');

                // Optional: Close all other FAQs
                faqItems.forEach(function(faq) {
                    faq.classList.remove('active');
                });

                // Toggle clicked FAQ
                if (!wasActive) {
                    item.classList.add('active');
                }
            });
        }
    });
}
```

```css
.faq-accordion {
    background: white;
    margin-bottom: 1rem;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    overflow: hidden;
}

.faq-question {
    background: #f8f9fa;
    padding: 1.5rem;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s;
}

.faq-question:hover {
    background: #e9ecef;
}

.faq-icon {
    color: #2e7d32;
    font-size: 1.5rem;
    transition: transform 0.3s;
}

.faq-accordion.active .faq-icon {
    transform: rotate(180deg);
}

.faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
    padding: 0 1.5rem;
}

.faq-accordion.active .faq-answer {
    max-height: 500px;
    padding: 1.5rem;
}
```

### 4. Sticky Bottom CTA Bar
```javascript
function initStickyBar() {
    var stickyBar = document.getElementById('sticky-cta-bar');
    if (!stickyBar) return;

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 800) {
            stickyBar.classList.add('show');
        } else {
            stickyBar.classList.remove('show');
        }
    });

    var closeBtn = stickyBar.querySelector('.sticky-close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            stickyBar.style.display = 'none';
        });
    }
}
```

```css
#sticky-cta-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
    padding: 1rem;
    box-shadow: 0 -4px 12px rgba(0,0,0,0.2);
    transform: translateY(100%);
    transition: transform 0.3s;
    z-index: 1000;
    display: none;
}

#sticky-cta-bar.show {
    transform: translateY(0);
    display: block;
}

.sticky-cta-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

@media (max-width: 768px) {
    .sticky-cta-content {
        flex-direction: column;
        text-align: center;
    }
}
```

---

## CSS COLOR SCHEME & BRANDING

### Primary Color Palette
```css
:root {
    --primary-green: #2e7d32;
    --primary-green-dark: #1b5e20;
    --primary-green-light: #4caf50;
    --success-green: #28a745;
    --warning-yellow: #ffc107;
    --danger-red: #d32f2f;
    --info-blue: #1976d2;
    --neutral-gray: #6c757d;
    --light-gray: #f8f9fa;
    --border-gray: #dee2e6;
}
```

### Box Shadows & Borders
```css
/* Standard card shadow */
box-shadow: 0 4px 12px rgba(0,0,0,0.1);

/* Hover shadow */
box-shadow: 0 6px 16px rgba(0,0,0,0.15);

/* Standard border radius */
border-radius: 8px;  /* Small elements */
border-radius: 12px; /* Cards, containers */
border-radius: 25px; /* Buttons, pills */
```

---

## COMPLIANCE REQUIREMENTS

### Mandatory Elements for Every Page
1. **Visible T&Cs for Every Bonus** - Terms must be accessible (expandable is fine)
2. **State Availability Documentation** - List all legal states clearly
3. **Responsible Gambling Messaging** - Include 1-800-GAMBLER reference
4. **Affiliate Disclosure** - Visible disclosure near top of page

### Standard T&Cs Format
```
Terms: 21+ (18+ D.C.). New customers only.
AZ, CO, CT, DC, IL, IN, IA, KS, KY, LA, MA, MD, MI, NC, NJ, NY,
OH, PA, TN, VA, VT, WV, WY only. First online real money wager only.
$5 first deposit required. Bonus issued as nonwithdrawable bonus bets.
Expires 7 days after issuance. See terms at sportsbook.fanduel.com.
Gambling Problem? Call 1-800-GAMBLER.
```

---

## STYLE GUIDE VIOLATIONS TO AVOID

### Prohibited
- Emojis in headings or professional content
- "Q:" or "A:" prefix in FAQ sections
- Excessive colons in headers
- Fictional expert quotes
- High contrast/clashing colors
- Box within box within box (nesting madness)
- Trailing colons in headers
- max-width CSS on elements (site handles this)

### Required
- Consistent green theme (#2e7d32)
- Letter badges instead of images
- Mobile-first responsive design
- Console logging for debugging
- Complete T&Cs for compliance

---

## MOBILE RESPONSIVENESS

### Key Breakpoint: 768px
```css
@media (max-width: 768px) {
    /* Stack layouts vertically */
    .flex-row { flex-direction: column; }

    /* Full-width inputs */
    .input-field { width: 100%; }

    /* Adjust padding */
    .container { padding: 15px; }

    /* Tab navigation scroll */
    .tab-nav {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    /* Sticky bar stacks */
    .sticky-cta-content {
        flex-direction: column;
        text-align: center;
    }

    /* Table horizontal scroll */
    .table-wrapper {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}
```

---

## INTERNAL LINK FORMAT

### URL Format Rules
```
❌ /sport/betting/
✅ /sport/betting/index.htm

❌ /sport/betting/sportsbook-reviews/
✅ /sport/betting/sportsbook-reviews/index.htm
```

Always use complete URLs with `index.htm` suffix.

---

**Document Version:** 1.0
**Last Updated:** December 2024
**Source:** Team feedback compilation
