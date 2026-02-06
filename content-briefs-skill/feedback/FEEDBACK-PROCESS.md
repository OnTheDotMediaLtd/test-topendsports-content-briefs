# Feedback Collection & Learning Process

## Overview

This system allows the brief generation system to improve over time by systematically collecting, validating, and applying feedback from all users.

---

## Workflow

```
[User submits feedback]
    ↓
[Review & validate]
    ↓
[Extract lessons learned]
    ↓
[Update reference docs]
    ↓
[Next brief uses improved instructions]
```

---

## Roles

### 1. Feedback Submitters
- **Writers**: Report unclear instructions, missing info, time to complete
- **SEO Team**: Report keyword issues, cannibalization, ranking performance
- **Editors**: Report quality issues, structural problems
- **Project Manager**: Overall quality assessment, prioritize improvements

### 2. Feedback Reviewer
- Validates submitted feedback
- Identifies patterns across multiple briefs
- Decides which feedback should update system docs
- Maintains feedback changelog

---

## Step-by-Step Process

### Step 1: Submit Feedback

**Who**: Anyone who works with the briefs
**When**: After using a brief (immediately for writers, after 30/60/90 days for SEO)
**How**:

1. Copy `feedback/FEEDBACK-TEMPLATE.md`
2. Rename to: `feedback/submitted/[page-name]-feedback-[YYYYMMDD].md`
3. Fill out all relevant sections
4. Save file
5. (Optional) Notify reviewer via email/Slack

**Example filename**: `feedback/submitted/nfl-betting-sites-feedback-20251128.md`

---

### Step 2: Review & Validate Feedback

**Who**: Project manager or designated reviewer
**When**: Weekly review session
**How**:

1. Read all new feedback in `feedback/submitted/`
2. For each feedback file:
   - Verify issues are legitimate
   - Check if issues are systemic (not one-off)
   - Determine if changes needed to reference docs
   - Add validation notes at bottom of file
3. Move validated feedback to `feedback/validated/`
4. Update `feedback/FEEDBACK-LOG.md` with summary

**Validation Questions**:
- Is this feedback actionable?
- Does it represent a pattern (3+ similar issues)?
- Will fixing this improve future briefs?
- Is it within scope of the system?

---

### Step 3: Extract Lessons Learned

**Who**: System maintainer (you) or Claude in next session
**When**: After validation
**How**:

1. Review validated feedback
2. Identify patterns and recurring issues
3. Draft specific rule changes or additions
4. Determine which reference files need updates:
   - `references/lessons-learned.md` - Mistakes to avoid
   - `references/quality-checklist.md` - Quality standards
   - `references/phase1-research.md` - Research improvements
   - `references/phase2-writer.md` - Writer brief improvements
   - `references/phase3-technical.md` - Technical improvements

---

### Step 4: Update Reference Documentation

**Who**: You or Claude
**When**: After extracting lessons
**How**:

1. Open relevant reference file
2. Add new section or update existing section
3. Use clear, actionable language
4. Include example of what to do / what not to do
5. Reference the feedback ticket that prompted the change
6. Update file's "Last Updated" date
7. Move feedback file to `feedback/applied/`

**Documentation Format**:
```markdown
### [Issue Title] (Added: YYYY-MM-DD)

**Problem**: [Brief description]

**Example of incorrect approach**:
[What was done wrong]

**Correct approach**:
[What should be done instead]

**Source**: feedback/validated/[filename]
```

---

### Step 5: Monitor Impact

**Who**: SEO team, project manager
**When**: Ongoing
**How**:

Track these metrics over time:
- Average brief generation time (should decrease)
- Writer satisfaction scores (should increase)
- Keyword cannibalization incidents (should decrease)
- SEO performance of published pages
- Number of revisions needed per brief (should decrease)

Document improvements in `feedback/FEEDBACK-LOG.md`

---

## Feedback Categories & Routing

| Category | Goes To | Update File |
|----------|---------|-------------|
| Keyword cannibalization | phase1-research.md | Research protocol |
| Unclear writer instructions | phase2-writer.md | Writer brief format |
| Missing technical elements | phase3-technical.md | Technical requirements |
| Template structure issues | content-templates.md | Template definitions |
| Quality standard violations | quality-checklist.md | Pre-delivery checks |
| Recurring mistakes | lessons-learned.md | Anti-patterns |
| Brand positioning errors | reference-library.md | Brand rules |

---

## Quick Reference Commands

### For Users Submitting Feedback:
```bash
# Copy template and create new feedback file
cp feedback/FEEDBACK-TEMPLATE.md feedback/submitted/[page-name]-feedback-20251128.md

# Edit the file
notepad feedback/submitted/[page-name]-feedback-20251128.md
```

### For Reviewer:
```bash
# List all submitted feedback
dir feedback/submitted/

# After validation, move to validated folder
move feedback/submitted/[filename] feedback/validated/

# After applying changes, move to applied folder
move feedback/validated/[filename] feedback/applied/
```

---

## Integration with Brief Generation

When Claude generates a new brief, it will:

1. **Read lessons-learned.md** - Avoid known mistakes
2. **Read quality-checklist.md** - Meet current quality standards
3. **Apply updated phase instructions** - Use refined processes
4. **Reference recent feedback** - Context on recent improvements

This creates a continuous improvement loop where each brief is better than the last.

---

## Example Feedback Flow

**Week 1**: Writer reports "NFL player props keyword wasn't included but competitors rank for it"
→ Validates as real issue
→ Updates phase1-research.md: "Always check competitor pages for high-volume props keywords"
→ Next brief includes props keywords

**Week 2**: SEO finds keyword cannibalization between two betting pages
→ Validates issue
→ Updates lessons-learned.md: "Before assigning keyword, check site-structure CSV for existing pages targeting same keyword"
→ Next brief checks for conflicts first

**Week 3**: Writer completes brief 2 hours faster due to clearer instructions
→ Documents improvement in FEEDBACK-LOG.md
→ System is measurably better

---

## Best Practices

### For Submitters:
- Submit feedback within 24 hours while details are fresh
- Be specific - "keyword X missing" not just "keywords bad"
- Include examples and evidence
- Focus on systemic issues, not one-off typos

### For Reviewers:
- Review feedback weekly, not daily (allows pattern recognition)
- Look for trends across multiple briefs
- Prioritize changes that affect multiple briefs
- Don't change system based on single feedback instance

### For System Maintainers:
- Keep documentation concise and actionable
- Use examples in lessons-learned.md
- Date all changes so impact can be tracked
- Test changes with next brief generation

---

## Troubleshooting

**"Too much feedback to process"**
→ Focus on Priority 1 items only
→ Group similar feedback together
→ Process in batches during weekly review

**"Feedback contradicts itself"**
→ Discuss with team to reach consensus
→ May need A/B testing different approaches
→ Document decision and rationale

**"Changes not improving output"**
→ Review applied changes in last 4 weeks
→ May need to revert some changes
→ Check if instructions are too complex

---

Last Updated: 2025-11-28
