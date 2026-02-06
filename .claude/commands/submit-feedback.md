# Submit Feedback for Content Brief System

**Feedback Type:** $ARGUMENTS

---

## Instructions

You are collecting feedback to improve the content brief generation system. Follow this process:

### Step 1: Identify Feedback Category

Based on the user's input, categorize the feedback:

| Category | Description | Updates |
|----------|-------------|---------|
| `keyword` | Keyword research issues, cannibalization, missing keywords | `phase1-research.md` |
| `writer` | Unclear instructions, missing info, writer experience | `phase2-writer.md` |
| `technical` | HTML/code issues, schema problems, interactive elements | `phase3-technical.md` |
| `template` | Content structure issues, outline problems | `content-templates.md` |
| `quality` | Quality standard violations, checklist gaps | `quality-checklist.md` |
| `workflow` | Process issues, timing, phase transitions | `ORCHESTRATOR.md` |
| `brand` | Brand positioning errors, missing brands | `reference-library.md` |
| `edge-case` | Unusual scenarios not covered | `lessons-learned.md` |

If no category provided in $ARGUMENTS, ask the user which category applies.

---

### Step 2: Collect Feedback Details

Ask the user for:

1. **What brief is this about?** (page name or URL)
2. **What worked well?** (1-3 items)
3. **What was confusing or unclear?** (1-3 items)
4. **Any edge cases encountered?** (scenarios not handled)
5. **Suggestions for improvement?** (specific recommendations)
6. **Priority:** Critical / Important / Nice-to-have

---

### Step 3: Create Feedback File

Create a feedback file at:
```
content-briefs-skill/feedback/submitted/[page-name]-feedback-[YYYYMMDD].md
```

Use this format:

```markdown
# Feedback: [Page Name]

**Date:** [YYYY-MM-DD]
**Submitter:** [Name/Role]
**Category:** [category from Step 1]
**Priority:** [Critical/Important/Nice-to-have]

## Brief Information
- **Page:** [page name]
- **Date Generated:** [date]

## What Worked Well
1. [item]
2. [item]

## What Was Confusing/Unclear
1. [item]
2. [item]

## Edge Cases Encountered
- [description]

## Suggestions for Improvement
1. [suggestion]

## Recommended Documentation Updates
- **File:** [filename from routing table]
- **Section:** [section to update]
- **Proposed Change:** [what to add/modify]

---
**Status:** SUBMITTED
```

---

### Step 4: Update Feedback Log

Append entry to `content-briefs-skill/feedback/FEEDBACK-LOG.md`:

```markdown
| [YYYY-MM-DD] | [page-name] | [category] | [priority] | SUBMITTED |
```

---

### Step 5: Notify About Next Steps

Tell the user:

> **Feedback submitted!** Your feedback has been saved to:
> `feedback/submitted/[filename]`
>
> **What happens next:**
> 1. Weekly review will validate this feedback
> 2. If actionable, it will update: `[target file from routing]`
> 3. Future briefs will use the improved instructions
>
> **To run feedback ingestion manually:**
> ```bash
> python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons
> ```

---

### Step 6: Offer MCP Submission (Optional)

If appropriate, also submit via MCP tool:

```
mcp__topendsports-briefs__submit_feedback with:
- page_name: "[page]"
- rating: [1-5]
- submitter: "[name]"
- issues: ["issue1", "issue2"]
- improvements: ["suggestion1", "suggestion2"]
```

---

## Quick Examples

### Example 1: Keyword Issue
```
/submit-feedback keyword

User: "The NFL betting sites brief was missing 'NFL player props' keyword which competitors rank for"

→ Creates feedback file
→ Routes to phase1-research.md
→ Suggests adding competitor props keyword check
```

### Example 2: Writer Confusion
```
/submit-feedback writer

User: "The intro format instructions were unclear about affiliate disclosure placement"

→ Creates feedback file
→ Routes to phase2-writer.md
→ Suggests clarifying disclosure position in intro
```

### Example 3: Edge Case
```
/submit-feedback edge-case

User: "Brief for state-specific page needed different compliance text but template didn't account for this"

→ Creates feedback file
→ Routes to lessons-learned.md
→ Documents state-specific compliance variation
```

---

## Category Routing Reference

| Issue Type | Target Document | Section to Update |
|------------|-----------------|-------------------|
| Missing keywords | `references/phase1-research.md` | Keyword Research Steps |
| Keyword cannibalization | `references/lessons-learned.md` | Anti-patterns |
| Unclear writer instructions | `references/phase2-writer.md` | Writer Guidelines |
| Missing source requirements | `references/phase2-writer.md` | Source Requirements |
| HTML/CSS bugs | `references/phase3-technical.md` | Technical Requirements |
| Schema errors | `references/phase3-technical.md` | Schema Markup |
| Template structure | `references/content-templates.md` | Template Definitions |
| Brand positioning | `references/reference-library.md` | Brand Rules |
| Quality failures | `references/quality-checklist.md` | Checklist Items |
| Process bottlenecks | `content-briefs-skill/ORCHESTRATOR.md` | Workflow Steps |
| Unusual scenarios | `references/lessons-learned.md` | Edge Cases |

---

## NOW EXECUTE

1. Determine category from $ARGUMENTS or ask user
2. Collect feedback details interactively
3. Create feedback file
4. Update feedback log
5. Confirm submission and next steps
