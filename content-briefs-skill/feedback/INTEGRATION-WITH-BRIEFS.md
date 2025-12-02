# How Feedback Integrates with Brief Generation

This document explains how the feedback system connects to the brief generation workflow.

---

## The Learning Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTINUOUS IMPROVEMENT LOOP               │
└─────────────────────────────────────────────────────────────┘

  1. Generate Brief
         ↓
  2. User submits feedback → feedback/submitted/
         ↓
  3. Weekly review → validate feedback → feedback/validated/
         ↓
  4. Extract lessons → update reference docs
         ↓
  5. Move to feedback/applied/
         ↓
  6. Next brief generation reads updated docs
         ↓
  7. Brief quality improves (Go to step 1)
```

---

## What Gets Updated Based on Feedback

### 1. Lessons Learned (`references/lessons-learned.md`)

**Updated when**: Recurring mistakes identified (3+ similar issues)

**Examples**:
- "Always check site-structure CSV for keyword cannibalization"
- "Include specific bonus wagering requirements in writer brief"
- "Never assign 'nfl player props' keyword if dedicated props page exists"

**Format**:
```markdown
### Mistake X: [Issue Name] (Added: YYYY-MM-DD)
**Problem:** [What went wrong]
**Should:** [Correct approach]
**Impact:** [Why it matters]
**Fix:** [How to prevent]
**Source:** feedback/validated/[filename]
```

---

### 2. Quality Checklist (`references/quality-checklist.md`)

**Updated when**: New quality standards emerge

**Examples**:
- Add: "Schema markup validated (no syntax errors)"
- Add: "Word count specified within 100-word range"
- Add: "Bonus T&Cs include wagering requirements"

**Format**:
```markdown
- [ ] [New quality check item]
```

---

### 3. Phase Instructions

**Phase 1 Research** (`references/phase1-research.md`)

**Updated when**: Research methodology improvements identified

**Examples from feedback**:
- Add keyword cannibalization check step
- Specify checking existing site structure before assigning keywords
- Add step to verify bonus details from official T&Cs

**Phase 2 Writer Brief** (`references/phase2-writer.md`)

**Updated when**: Writer clarity issues identified

**Examples from feedback**:
- Narrow word count ranges (was: 2,500-3,500, now: 2,800-2,900)
- Specify which sections need schema markup
- Include specific bonus wagering requirements

**Phase 3 Technical** (`references/phase3-technical.md`)

**Updated when**: Technical implementation issues found

**Examples from feedback**:
- Add schema validation step
- Specify table formatting standards
- Include T&C URL requirements

---

## How Claude Uses This Information

### During Brief Generation

**Phase 1 (Research)**:
```
Claude reads:
├── phase1-research.md (process to follow)
├── lessons-learned.md (mistakes to avoid)
└── reference-library.md (quick lookups)

Applies feedback:
- Checks site-structure CSV for keyword conflicts
- Verifies bonus details from official sources
- Follows updated research protocols
```

**Phase 2 (Writer Brief)**:
```
Claude reads:
├── phase2-writer.md (process to follow)
├── lessons-learned.md (mistakes to avoid)
├── content-templates.md (structure)
└── Phase 1 JSON data

Applies feedback:
- Uses narrow word count ranges
- Includes specific bonus T&Cs
- Clarifies schema markup requirements
```

**Phase 3 (Technical)**:
```
Claude reads:
├── phase3-technical.md (process to follow)
├── lessons-learned.md (mistakes to avoid)
├── verification-standards.md (T&Cs standards)
├── Phase 1 JSON data
└── Phase 2 JSON data

Applies feedback:
- Validates schema syntax
- Follows table formatting standards
- Includes all required T&C elements
```

---

## Real Example: Keyword Cannibalization

### The Problem (From Feedback)

**Week 1**: Writer submits feedback:
> "Brief included 'nfl player props' keyword, but we already have a dedicated page at /sport/betting/nfl/props/player-props.htm. Had to remove all references and find alternative keywords. Wasted 30 minutes."

### The Solution (Applied to System)

**1. Updated lessons-learned.md**:
```markdown
### Mistake 8: Keyword Cannibalization (Added: 2025-11-28)

**Problem:** Assigned secondary keyword that conflicts with existing page
**Should:** Check site-structure CSV before assigning any keyword
**Impact:** Writer has to remove references, find alternatives, wastes time

**Fix:**
Before adding any secondary keyword to keyword cluster:
1. Search site-structure CSV: grep -i "[keyword]" assets/data/site-structure-english.csv
2. If exact match found → skip this keyword
3. If partial match found → verify it won't compete
4. Document any potential conflicts in Phase 1 notes

**Source:** feedback/validated/nfl-betting-sites-feedback-20251128.md
```

**2. Updated phase1-research.md** (Step 5: Keyword Research):
```markdown
### Step 5C: Verify No Cannibalization (NEW)

For each secondary keyword:
1. Search site structure CSV: grep -i "[keyword]" assets/data/site-structure-english.csv
2. If found:
   - Same page: OK to use
   - Different page: DO NOT USE (cannibalization risk)
3. Document check in Phase 1 JSON
```

**3. Updated quality-checklist.md**:
```markdown
### Phase 1 Checklist
- [ ] All secondary keywords checked against site-structure CSV
- [ ] No keyword cannibalization conflicts identified
```

### The Result

**Week 2+**: Next brief generation:
- Claude reads updated lessons-learned.md
- Follows new Step 5C in phase1-research.md
- Checks keywords against CSV before assigning
- Avoids cannibalization issue
- Writer saves 30 minutes per brief

---

## Measuring Impact

### Key Metrics (Updated Monthly)

| Metric | Target | How Feedback Helps |
|--------|--------|-------------------|
| Brief generation time | -25% | Clearer instructions, fewer writer questions |
| Writer satisfaction | 4.0+ / 5.0 | Better clarity, less missing information |
| Keyword cannibalization | <1 per 10 briefs | CSV checking now mandatory |
| Briefs needing revision | <10% | Quality checklist catches issues early |
| Schema errors | 0 | Validation step added to Phase 3 |

### Tracking in FEEDBACK-LOG.md

```markdown
### 2025-12-31 - End of Month 1

**Improvements applied this month**: 8

**Top issues resolved**:
1. Keyword cannibalization (7 reports) → Now checked automatically
2. Vague word counts (5 reports) → Now within 100-word range
3. Missing bonus T&Cs (4 reports) → Now required in Phase 1

**Metrics**:
- Avg brief generation time: 6 hours → 5 hours (-16%)
- Writer satisfaction: 3.2 → 3.8 (+18%)
- Cannibalization incidents: 3 → 0 (-100%)

**Next month focus**: Schema validation, table formatting standards
```

---

## For Developers: Adding New Feedback Categories

If you want to add a new type of feedback (e.g., "Conversion Performance"):

**1. Update FEEDBACK-TEMPLATE.md**:
```markdown
## Conversion Performance

**Conversions tracked**: [Yes / No]
**Conversion rate**: [X%]
**Top converting elements**:
1. [Element]
2. [Element]

**Underperforming elements**:
1. [Element]
```

**2. Update FEEDBACK-PROCESS.md**:
```markdown
| Conversion issues | phase3-technical.md | CTA optimization |
```

**3. Create new reference section** (if needed):
```markdown
# references/conversion-optimization.md
```

**4. Update lessons-learned.md** (when patterns emerge):
```markdown
### Mistake X: Poor CTA Placement
**Problem:** [Description]
**Fix:** [Solution]
```

---

## Common Questions

**Q: How long before feedback improves briefs?**
A: Immediately for critical issues (same day), 1 week for validated feedback (after weekly review)

**Q: Can writers see what changed based on their feedback?**
A: Yes! Check FEEDBACK-LOG.md for "Source: [your-feedback-file]" references

**Q: What if my feedback isn't applied?**
A: Reviewer will add notes explaining why (e.g., "one-off issue, not systemic")

**Q: Do I need technical knowledge to submit feedback?**
A: No! Writers focus on clarity/completeness, SEO on keywords, managers on strategy. All perspectives valuable.

---

Last Updated: 2025-11-28
