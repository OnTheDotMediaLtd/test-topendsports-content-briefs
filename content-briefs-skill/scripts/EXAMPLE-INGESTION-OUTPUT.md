# Example Feedback Ingestion Output

This document shows what the ingestion script produces in real-world scenarios.

## Scenario 1: First Run (Empty Directory)

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py
```

### Output
```
[NOTICE] Feedback directory not found: /home/user/topendsports-content-briefs/content-briefs-skill/feedback/validated
Creating directory structure...
[OK] Created /home/user/topendsports-content-briefs/content-briefs-skill/feedback/validated

No validated feedback files to process.
```

**What it means**: Everything is working, but there's no feedback to process yet.

---

## Scenario 2: Single Feedback File

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py
```

### Input
One feedback file: `nfl-betting-sites-feedback-20251208.md` in `feedback/validated/`

### Output
```
[INFO] Found 1 feedback file(s)
[OK] Successfully parsed 1 file(s)
[OK] Extracted 13 lessons
================================================================================
FEEDBACK INGESTION REPORT
================================================================================

Generated: 2025-12-08 14:34:00
Files processed: 1
Total lessons extracted: 13
Priority 1 items: 3
Priority 2 items: 2
Average quality rating: 3.0/5

================================================================================
LESSONS BY CATEGORY
================================================================================

### KEYWORD RESEARCH (6 lessons)
--------------------------------------------------------------------------------

1. [CRITICAL] Add missing keyword: nfl moneyline - Volume: 4,200/month
   Why: Competitors rank for this keyword; missing it creates content gap
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

2. [CRITICAL] Add missing keyword: nfl live betting - Volume: 3,100/month
   Why: Competitors rank for this keyword; missing it creates content gap
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

3. [CRITICAL] Check for keyword cannibalization with existing moneyline page
   Why: Keyword cannibalization dilutes ranking power across multiple pages
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

4. [IMPORTANT] Word count guidance too broad - should narrow to 100-word range
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

5. [IMPORTANT] Missing "nfl moneyline" keyword that competitors all rank for
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

   ... and 1 more lessons in this category

### TECHNICAL (2 lessons)
--------------------------------------------------------------------------------

1. [CRITICAL] Fix schema markup syntax errors
   Why: Schema markup validation is essential for search appearance
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

2. [CRITICAL] Validate comparison table mobile alignment
   Why: Malformed HTML can affect rendering and SEO
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

### BRAND SELECTION (3 lessons)
--------------------------------------------------------------------------------

1. [IMPORTANT] T&Cs formatting inconsistent between brands
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

2. [IMPORTANT] Missing specific wagering requirements for bonus offers
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

   ... and 1 more lessons in this category

### PROCESS IMPROVEMENT (2 lessons)
--------------------------------------------------------------------------------

1. [IMPORTANT] Update lessons-learned.md: Keyword Research
   Why: Proposed: "Always check for keyword cannibalization by searching..."
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

2. [IMPORTANT] Update quality-checklist.md: Pre-Delivery Checklist
   Why: Proposed: Add item "Schema markup validated (no syntax errors)"
   Source: nfl-betting-sites (nfl-betting-sites-feedback-20251208.md)

================================================================================
FEEDBACK FILES PROCESSED
================================================================================

- nfl-betting-sites: 3/5 (Sarah Johnson - Content Writer)
  File: nfl-betting-sites-feedback-20251208.md
  Date: 2025-12-08
  Categories: Keyword Research, Technical, Brand Selection

================================================================================
RECOMMENDATIONS
================================================================================

Documentation files that need updating:
  - lessons-learned.md
  - quality-checklist.md

Use --update-lessons flag to apply changes automatically.

ATTENTION: 3 Priority 1 (Critical) items identified
These require immediate attention before next brief generation.

================================================================================
```

---

## Scenario 3: Multiple Feedback Files

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py
```

### Input
Three feedback files processed:
1. `nfl-betting-sites-feedback-20251208.md`
2. `best-betting-apps-feedback-20251206.md`
3. `us-sportsbooks-feedback-20251205.md`

### Output (Partial)
```
[INFO] Found 3 feedback file(s)
[OK] Successfully parsed 3 file(s)
[OK] Extracted 28 lessons
================================================================================
FEEDBACK INGESTION REPORT
================================================================================

Generated: 2025-12-08 14:45:22
Files processed: 3
Total lessons extracted: 28
Priority 1 items: 7
Priority 2 items: 12
Priority 3 items: 9
Average quality rating: 3.7/5

================================================================================
LESSONS BY CATEGORY
================================================================================

### KEYWORD RESEARCH (9 lessons)
--------------------------------------------------------------------------------

1. [CRITICAL] Add missing keyword: nfl moneyline
   ...

### CONTENT STRUCTURE (8 lessons)
--------------------------------------------------------------------------------

1. [IMPORTANT] Mobile Experience section needs 200+ words
   ...

### TECHNICAL (5 lessons)
--------------------------------------------------------------------------------

1. [CRITICAL] Fix schema markup syntax errors
   ...

### BRAND SELECTION (4 lessons)
--------------------------------------------------------------------------------

1. [IMPORTANT] Update all brand T&Cs with current information
   ...

### WRITER EXPERIENCE (2 lessons)
--------------------------------------------------------------------------------

1. [IMPORTANT] Word count guidance too broad
   ...

================================================================================
FEEDBACK FILES PROCESSED
================================================================================

- nfl-betting-sites: 3/5 (Sarah Johnson - Content Writer)
  File: nfl-betting-sites-feedback-20251208.md
  Date: 2025-12-08
  Categories: Keyword Research, Technical, Brand Selection

- best-betting-apps: 4/5 (Mike Chen - SEO Manager)
  File: best-betting-apps-feedback-20251206.md
  Date: 2025-12-06
  Categories: Content Structure, Keyword Research, Brand Selection

- us-sportsbooks: 3/5 (Lisa Rodriguez - Editor)
  File: us-sportsbooks-feedback-20251205.md
  Date: 2025-12-05
  Categories: Writer Experience, Content Structure, Keyword Research

================================================================================
RECOMMENDATIONS
================================================================================

Documentation files that need updating:
  - lessons-learned.md
  - quality-checklist.md
  - phase2-writer.md

Use --update-lessons flag to apply changes automatically.

ATTENTION: 7 Priority 1 (Critical) items identified
These require immediate attention before next brief generation.

================================================================================
```

---

## Scenario 4: Verbose Output

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py --verbose
```

### Output (Key Sections)
```
[DEBUG] Parsing nfl-betting-sites-feedback-20251208.md
[DEBUG]   → Parsed successfully: nfl-betting-sites
[DEBUG] Parsing best-betting-apps-feedback-20251206.md
[DEBUG]   → Parsed successfully: best-betting-apps
[DEBUG] Parsing us-sportsbooks-feedback-20251205.md
[DEBUG]   → Parsed successfully: us-sportsbooks
[INFO] Found 3 feedback file(s)
[OK] Successfully parsed 3 file(s)
[OK] Extracted 28 lessons

[Full report output as shown above...]
```

**What it shows**: Detailed feedback about which files were parsed and what was found.

---

## Scenario 5: Dry-Run Preview

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py \
  --update-lessons --dry-run
```

### Output
```
[INFO] Found 1 feedback file(s)
[OK] Successfully parsed 1 file(s)
[OK] Extracted 13 lessons

[Full report as before...]

[INFO] Updating lessons-learned.md...

================================================================================
PROPOSED CHANGES TO lessons-learned.md
================================================================================

## New Lessons (2025-12-08)
*Extracted from validated user feedback*

### Keyword Research

**[CRITICAL]** Always check for keyword cannibalization
> Before finalizing secondary keywords, search site-structure CSV for existing pages.
> If keyword already has dedicated page, use different variant or note conflict.
*Source: nfl-betting-sites*

**[CRITICAL]** Verify secondary keywords don't duplicate primary keyword targets
> Keyword cannibalization dilutes ranking power across multiple pages
*Source: nfl-betting-sites*

**[IMPORTANT]** Narrow word count guidance to specific ranges
> Broad ranges like 2,500-3,500 make content completion unpredictable
*Source: nfl-betting-sites*

### Technical

**[CRITICAL]** Validate all schema markup before publishing
> Schema markup validation is essential for search appearance and rich snippets
*Source: nfl-betting-sites*

**[CRITICAL]** Test table layouts on mobile views
> Ensure comparison tables and data tables render correctly on all screen sizes
*Source: nfl-betting-sites*

### Process Improvement

**[IMPORTANT]** Update Phase 2 writer instructions for Mobile Experience section
> Should be 200-300 words including app-specific features and performance metrics
*Source: best-betting-apps*

================================================================================
[OK] Dry run complete - no changes made
```

**What it means**: These are the exact changes that would be made if you removed `--dry-run`.

---

## Scenario 6: Applying Changes

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons
```

### Output
```
[INFO] Found 1 feedback file(s)
[OK] Successfully parsed 1 file(s)
[OK] Extracted 13 lessons

[Full report...]

[INFO] Updating lessons-learned.md...
[OK] Successfully updated /home/user/topendsports-content-briefs/content-briefs-skill/references/lessons-learned.md
```

**What happened**: The file `lessons-learned.md` was modified. You can verify with:
```bash
git diff content-briefs-skill/references/lessons-learned.md
```

---

## Scenario 7: Error - Invalid Feedback File

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py
```

### Input
A malformed feedback file (missing required fields)

### Output
```
[INFO] Found 1 feedback file(s)
[ERROR] Could not parse feedback: Missing required field: Brief ID
[ERROR] No valid feedback files could be parsed
```

**What to do**: Check the feedback file format against `EXAMPLE-FEEDBACK.md`

---

## Scenario 8: Error - Can't Update Lessons File

### Command
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons
```

### Output
```
[INFO] Found 1 feedback file(s)
[OK] Successfully parsed 1 file(s)
[OK] Extracted 13 lessons

[Full report...]

[INFO] Updating lessons-learned.md...
[ERROR] Could not write to lessons file: Permission denied
```

**What to do**: Check file permissions:
```bash
ls -l content-briefs-skill/references/lessons-learned.md
chmod 644 content-briefs-skill/references/lessons-learned.md
```

---

## Interpretation Guide

### Quality Ratings
- **5/5**: Excellent - Minimal feedback, well-documented brief
- **4/5**: Very Good - Minor improvements needed
- **3/5**: Good - Moderate improvements would help
- **2/5**: Needs Work - Significant issues found
- **1/5**: Poor - Major rework required

### Priority Levels
- **[CRITICAL]** - MUST be fixed before next brief
- **[IMPORTANT]** - SHOULD be addressed in next cycle
- **[NOTE]** - Nice-to-have improvements

### Categories
- **Keyword Research**: Keywords, cannibalization, volume, gaps
- **Content Structure**: Outline, word count, sections, organization
- **Brand Selection**: Brand features, positioning, bonus details
- **Technical**: Code, schema, interactive elements
- **Writer Experience**: Instruction clarity, sources, information
- **Process Improvement**: System documentation, methodology

### Source Information
Each lesson includes:
- **Brief ID**: Which brief this feedback came from
- **File**: Which feedback file contained this
- **Date**: When the feedback was submitted
- **Reviewer**: Who provided the feedback and their role

---

## Using the Report

### For Team Leaders
1. **Review quality ratings** - Are they trending upward?
2. **Check Priority 1 items** - Do they need immediate action?
3. **Identify patterns** - What issues appear multiple times?
4. **Plan improvements** - Which docs need updating?

### For Brief Generators
1. **Read recommendations** - What docs are flagged for update?
2. **Check lessons-learned** - What patterns to avoid?
3. **Verify compliance** - Are we meeting quality standards?

### For Writers
1. **Review your feedback** - What did reviewers note about your briefs?
2. **Learn from others** - What issues are appearing across briefs?
3. **Improve next brief** - Use lessons to avoid past mistakes

---

## Sample Lesson Applications

### Lesson: "Always check for keyword cannibalization"
**Applied in**: Phase 1 research
- Brief generator checks site-structure.csv before adding secondary keywords
- Warns writer about potential conflicts
- Suggests alternative keywords if conflict found

### Lesson: "Mobile Experience section needs 200+ words"
**Applied in**: Phase 2 writer brief template
- Updated outline to show "Mobile Experience: 200-300 words"
- Added examples to quality checklist
- Writer can now follow clear guidance

### Lesson: "Narrow word count guidance to 100-word range"
**Applied in**: Phase 2 writer instructions
- Changed "2,500-3,500 words" to "2,800-2,900 words"
- Includes rationale in brief
- Reduces writer uncertainty

---

## Common Report Patterns

### Pattern 1: Consistent Keyword Issues Across Briefs
```
Lesson appears 3+ times:
- "Check for keyword cannibalization"
- "Add missing high-volume keywords"

Action: Add to Phase 1 checklist, make automatic
```

### Pattern 2: Technical Quality Issues
```
Multiple briefs report:
- "Schema markup errors"
- "Mobile alignment issues"

Action: Add HTML/schema validation to automated checks
```

### Pattern 3: Writer Feedback on Instructions
```
Repeated feedback:
- "Word count guidance unclear"
- "Missing information about X"

Action: Update Phase 2 template, be more specific
```

---

## Next Steps After Report

1. **Read Report**: Understand what feedback says
2. **Review Lessons**: Prioritize by category and severity
3. **Plan Changes**: Decide which lessons to implement
4. **Preview Changes**: Use `--dry-run` to see proposed updates
5. **Apply Changes**: Use `--update-lessons` to modify docs
6. **Communicate**: Let feedback submitters know their input was valued
7. **Measure Impact**: Check if new briefs improve based on lessons

---

This example document should help you understand exactly what the ingestion script produces and how to interpret the output!
