# Feedback System

This directory tracks feedback on brief generation quality to continuously improve the system.

## Directory Structure

```
feedback/
├── submitted/       # New feedback awaiting review
├── validated/       # Reviewed and confirmed feedback
├── applied/         # Feedback that updated documentation
├── FEEDBACK-LOG.md  # Changelog of all feedback
└── README.md        # This file
```

## How to Submit Feedback

### Via Slash Command
```bash
/submit-feedback [category]
```

### Categories

| Category | Use When |
|----------|----------|
| `keyword` | Missing keywords, research gaps, cannibalization |
| `writer` | Unclear writer instructions, missing information |
| `technical` | HTML/code bugs, schema errors, broken features |
| `template` | Outline structure problems, missing sections |
| `workflow` | Process bottlenecks, timing issues, efficiency |
| `edge-case` | Unusual scenarios not covered in docs |

### Feedback File Format

Feedback files should be named: `YYYY-MM-DD-[category]-[brief-slug].md`

**Example:** `2025-12-16-keyword-nfl-week-1.md`

## Feedback Workflow

```
1. Submit
   ↓
   feedback/submitted/
   ↓
2. Weekly Review (Mondays)
   ↓
   Validate & Categorize
   ↓
   feedback/validated/
   ↓
3. Update Documentation
   ↓
   references/[relevant-doc].md
   ↓
4. Mark Applied
   ↓
   feedback/applied/
```

## Routing Table

Feedback automatically updates the right documentation:

| Feedback Category | Updates Document |
|-------------------|------------------|
| `keyword` | `references/phase1-research.md` |
| `writer` | `references/phase2-writer.md` |
| `technical` | `references/phase3-technical.md` |
| `template` | `references/content-templates.md` |
| `workflow` | `ORCHESTRATOR.md` |
| `edge-case` | `references/lessons-learned.md` |

## Manual Processing

If slash command not available, manually process feedback:

```bash
# Validate submitted feedback
python3 content-briefs-skill/scripts/validate-feedback.py feedback/submitted/

# Apply validated feedback to docs
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons

# Update changelog
python3 content-briefs-skill/scripts/update-feedback-log.py
```

## Metrics

Track feedback metrics in `FEEDBACK-LOG.md`:

- Total submitted
- Total validated
- Total applied
- Resolution rate
- Category breakdown
- Impact tracking (high-impact vs quick wins)

## Integration with Shared Infrastructure

This feedback system can optionally integrate with `tes-shared-infrastructure` for cross-project improvements:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent / 'tes-shared-infrastructure' / 'src'))
from tes_shared.feedback import FeedbackProcessor

processor = FeedbackProcessor()
results = processor.process_feedback("feedback/submitted/")
```

## Weekly Review Checklist

Every Monday:

- [ ] Review `feedback/submitted/` files
- [ ] Validate and move to `feedback/validated/`
- [ ] Extract lessons learned
- [ ] Update relevant reference documents
- [ ] Move to `feedback/applied/` when done
- [ ] Update `FEEDBACK-LOG.md`
- [ ] Commit changes with message: `docs: apply feedback from [date] review`
