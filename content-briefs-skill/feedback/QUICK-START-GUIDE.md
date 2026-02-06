# Feedback System - Quick Start Guide

Get started submitting feedback in under 5 minutes.

---

## For Writers

### When to Submit Feedback
- **Immediately after completing an article** - while details are fresh
- Focus on: clarity of instructions, missing information, time spent

### How to Submit (3 steps)

**Step 1**: Copy the template
```bash
# Navigate to project folder
cd C:\Users\AndreBorg\tes-content-briefs-skill\tes-content-briefs\feedback

# Copy template
copy FEEDBACK-TEMPLATE.md submitted\nfl-betting-sites-feedback-20251128.md
```

**Step 2**: Fill out these sections (5 minutes)
- Overall Rating
- Category Ratings (focus on "Writer Instructions Clarity")
- What Worked Well (3-5 items)
- What Needs Improvement (3-5 items)
- Writer Experience (time to complete, unclear instructions, missing info)
- Actionable Changes Recommended

**Step 3**: Save and notify
- Save the file
- Email/Slack your manager: "Submitted feedback for [page-name]"

**See example**: `EXAMPLE-FEEDBACK.md`

---

## For SEO Team

### When to Submit Feedback
- **Before publishing** - keyword validation
- **30/60/90 days after publishing** - ranking performance

### How to Submit

**Before Publishing** (5 minutes):
1. Copy template to `submitted/[page-name]-feedback-prepublish.md`
2. Fill out: Keyword Issues section (check for cannibalization)
3. Verify keyword placement matches search intent
4. Submit for review

**After Publishing** (10 minutes):
1. Copy template to `submitted/[page-name]-feedback-30day.md`
2. Fill out: SEO Performance section
   - Primary keyword ranking
   - Secondary keywords in top 20
   - Organic traffic numbers
   - Conversion rate
3. Compare to projections
4. Submit with recommendations

---

## For Project Managers

### Weekly Review Workflow (30 minutes)

**Every Monday morning:**

1. **Check submitted folder**
   ```bash
   dir feedback\submitted\
   ```

2. **Review each feedback file**
   - Read through all sections
   - Look for patterns (3+ similar issues = systemic problem)
   - Validate issues are legitimate

3. **Move validated feedback**
   ```bash
   move feedback\submitted\[filename] feedback\validated\
   ```

4. **Extract lessons**
   - What needs to change in reference docs?
   - What patterns emerged this week?
   - Update `FEEDBACK-LOG.md` with summary

5. **Update documentation** (or delegate to Claude)
   - Add new sections to `lessons-learned.md`
   - Update `quality-checklist.md`
   - Update phase instructions if needed

6. **Move applied feedback**
   ```bash
   move feedback\validated\[filename] feedback\applied\
   ```

7. **Report improvements**
   - Email team with changes made
   - Update `FEEDBACK-LOG.md` metrics

---

## File Naming Convention

Use this format for all submitted feedback:

```
[page-name]-feedback-[YYYYMMDD]-[optional-suffix].md
```

**Examples**:
- `nfl-betting-sites-feedback-20251128.md` (general feedback)
- `nfl-betting-sites-feedback-20251128-writer.md` (from writer)
- `nfl-betting-sites-feedback-20251228-30day.md` (30-day SEO performance)
- `fanduel-review-feedback-20251130-prepublish.md` (pre-publish SEO check)

---

## Priority Levels

### Priority 1 (Critical) - Fix Immediately
- Keyword cannibalization with existing pages
- Major missing keywords (1000+/month that competitors rank for)
- Incorrect brand information
- Compliance violations (age, disclaimers, T&Cs)
- Syntax errors in code/schema

### Priority 2 (Important) - Fix This Week
- Unclear instructions that slow writers down
- Missing information that requires additional research
- Word count guidance too vague
- Template structural issues
- Quality standard gaps

### Priority 3 (Nice to Have) - Fix When Possible
- Minor formatting inconsistencies
- Additional features to add
- Nice-to-have information
- Style improvements
- Documentation clarity

---

## Common Questions

**Q: How long does feedback take to submit?**
A: 5-10 minutes for writers, 10-15 minutes for comprehensive feedback

**Q: Do I need to fill out every section?**
A: No - fill out what's relevant to you. Writers focus on Writer Experience, SEO focuses on Keyword Issues, etc.

**Q: What if I have feedback on multiple briefs?**
A: Submit separate feedback files for each brief

**Q: When will my feedback be applied?**
A: Weekly review cycle. Critical issues (Priority 1) may be applied immediately.

**Q: Can I see what changed based on my feedback?**
A: Yes! Check `FEEDBACK-LOG.md` for changelog and `lessons-learned.md` for new guidelines

**Q: What if my feedback contradicts someone else's?**
A: Reviewer will discuss with team to reach consensus. Both perspectives will be documented.

---

## Templates for Common Feedback

### Quick Writer Feedback (2 minutes)

```markdown
## Brief Information
- Brief ID: [page-name]
- Reviewer: [Your Name]
- Role: Writer

## Quick Feedback
**Time to Complete**: [X hours]

**What Worked**:
1. [One thing]
2. [Another thing]

**What Slowed Me Down**:
1. [Issue]
2. [Issue]

**Would save time if**:
1. [Suggestion]
```

### Quick SEO Cannibalization Check (3 minutes)

```markdown
## Brief Information
- Brief ID: [page-name]
- Reviewer: [Your Name]
- Role: SEO

## Keyword Check
**Cannibalization Issues**:
- Keyword: [keyword] conflicts with [URL]
- Keyword: [keyword] conflicts with [URL]

**Recommendation**: [Remove / Modify / Proceed]
```

---

## Getting Help

- **Process questions**: See `FEEDBACK-PROCESS.md`
- **Template help**: See `EXAMPLE-FEEDBACK.md`
- **System overview**: See `README.md`
- **Track changes**: See `FEEDBACK-LOG.md`

---

Last Updated: 2025-11-28
