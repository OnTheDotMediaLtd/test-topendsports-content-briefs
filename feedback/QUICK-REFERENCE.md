# Feedback Quick Reference

## Submit Feedback

```bash
/submit-feedback [category]
```

**Categories:** `keyword` | `writer` | `technical` | `template` | `workflow` | `edge-case`

## Process Manually

```bash
# Validate submitted feedback
python3 content-briefs-skill/scripts/validate-feedback.py feedback/submitted/ --move

# Apply validated feedback to docs
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons

# Update changelog
python3 content-briefs-skill/scripts/update-feedback-log.py
```

## Check Status

```bash
# View changelog
cat feedback/FEEDBACK-LOG.md

# Count pending feedback
ls feedback/submitted/ | wc -l

# Count validated feedback
ls feedback/validated/ | wc -l

# Count applied feedback
ls feedback/applied/ | wc -l
```

## Feedback File Naming

```
YYYY-MM-DD-[category]-[brief-slug].md
```

**Examples:**
- `2025-12-16-keyword-nfl-week-1.md`
- `2025-12-17-technical-schema-error.md`
- `2025-12-18-workflow-phase-timing.md`

## Routing Table

| Category | Updates |
|----------|---------|
| `keyword` | `references/phase1-research.md` |
| `writer` | `references/phase2-writer.md` |
| `technical` | `references/phase3-technical.md` |
| `template` | `references/content-templates.md` |
| `workflow` | `ORCHESTRATOR.md` |
| `edge-case` | `references/lessons-learned.md` |

## Weekly Review

**Every Monday:**

1. Review `feedback/submitted/`
2. Validate and move to `feedback/validated/`
3. Update relevant docs
4. Move to `feedback/applied/`
5. Update `FEEDBACK-LOG.md`
6. Commit changes

## Integration with Shared Infrastructure

```python
# Optional: Use shared validation
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent / 'tes-shared-infrastructure' / 'src'))
from tes_shared.feedback import FeedbackProcessor

processor = FeedbackProcessor()
results = processor.process_feedback("feedback/submitted/")
```

## Quick Stats

```bash
# View feedback statistics
grep -A 10 "## Feedback Statistics" feedback/FEEDBACK-LOG.md

# View category breakdown
grep -A 10 "## Categories" feedback/FEEDBACK-LOG.md
```
