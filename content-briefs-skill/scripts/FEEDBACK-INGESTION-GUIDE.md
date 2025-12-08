# Feedback Ingestion Integration Guide

## How This Script Fits In

The `ingest-feedback.py` script is the **automated harvest and synthesis** step in the TopEndSports feedback system.

```
FEEDBACK LIFECYCLE
├─ Phase 1: Collection
│  └─ Writers/SEO fill FEEDBACK-TEMPLATE.md
│     → Place in feedback/submitted/
│
├─ Phase 2: Validation
│  └─ Reviewer validates feedback completeness
│     → Move to feedback/validated/
│
├─ Phase 3: Ingestion [THIS SCRIPT]
│  └─ ingest-feedback.py extracts lessons
│     → Generates report
│     → Optionally updates lessons-learned.md
│
└─ Phase 4: Integration
   └─ Team reviews report
      → Updates reference docs
      → Next brief uses improved instructions
```

## Step-by-Step: From Feedback to Implementation

### 1. Feedback Submission (Writer/SEO)

Writer completes a brief and submits feedback:
```bash
# Copy template
cp feedback/FEEDBACK-TEMPLATE.md \
   feedback/submitted/nfl-betting-sites-feedback-20251208.md

# Fill out form with details
# Submit by noting in FEEDBACK-LOG.md
```

### 2. Feedback Validation (Manager/Lead)

Manager validates feedback is complete:
```bash
# Check for completeness
python3 content-briefs-skill/scripts/validate_feedback.py

# If all looks good, move to validated
mv feedback/submitted/nfl-betting-*.md feedback/validated/
```

### 3. Run Ingestion Script (Automated Weekly)

```bash
# Weekly ingestion
python3 content-briefs-skill/scripts/ingest-feedback.py \
  > /tmp/weekly-feedback-report-$(date +%Y%m%d).txt

# Email report to team
mail -s "Weekly Feedback Report" team@example.com < /tmp/weekly-feedback-report-*.txt
```

### 4. Review Report and Decide

Team reviews report:
```
LESSONS BY CATEGORY

### KEYWORD RESEARCH (6 lessons)
[CRITICAL] Always check for keyword cannibalization...
[CRITICAL] Add missing keyword: nfl moneyline...
[IMPORTANT] Narrow word count guidance to 100-word range...
```

**Decide**: Should this update `lessons-learned.md`?
- If yes → Continue to step 5
- If no → Archive feedback and move on

### 5. Preview and Apply Changes

Preview changes:
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py \
  --update-lessons --dry-run
```

See proposed additions to `lessons-learned.md`.

Apply changes:
```bash
python3 content-briefs-skill/scripts/ingest-feedback.py \
  --update-lessons
```

### 6. Use Updated Lessons in Next Brief

Brief generator reads `lessons-learned.md` for:
- Common mistakes to avoid
- Research depth requirements
- Quality standards to meet

Next brief automatically incorporates lessons!

## Real-World Example: Keyword Cannibalization

Let's trace a real example through the system:

### Week 1: Feedback Submission
Writer Sarah completes "NFL betting" brief and notices:
> "Added 'nfl moneyline' as secondary keyword, but we already have /sport/betting/nfl/moneyline-bets.html"

She fills feedback form:
```markdown
**Cannibalization Concerns**:
- [X] Potential cannibalization with: /sport/betting/nfl/moneyline-bets.html

**Priority 1 (Critical)**:
1. Check for keyword cannibalization with existing props page before publishing
```

### Week 2: Feedback Validation
Manager Mike reviews feedback:
- Checks: Is this valid? YES ✓
- Checks: Is this critical? YES ✓
- Moves file to `feedback/validated/`

### Week 2 (Evening): Ingestion
Script runs and extracts lesson:
```
[CRITICAL] Check for keyword cannibalization with existing moneyline page
Why: Keyword cannibalization dilutes ranking power across multiple pages
Source: nfl-betting-sites (sarah-nfl-feedback-20251208.md)
```

Report generated showing this is critical.

### Week 3: Implementation
- System improvements identified in report
- Lesson proposed for `lessons-learned.md`:

```markdown
### Keyword Research

**[CRITICAL]** Always check for keyword cannibalization
> Before finalizing secondary keywords, search site-structure CSV for existing pages.
> If keyword already covered elsewhere, choose different variant.
> Source: nfl-betting-sites feedback
```

### Week 4: Application
New brief generator reads `lessons-learned.md` and knows:
- Phase 1 research must include cannibalization check
- Generate warning if potential conflicts found
- Recommend alternative keywords for conflicts

**Result**: No cannibalization issues in next brief! ✓

## Running on a Schedule

### Weekly Automated Ingestion

Create a cron job:

```bash
# Edit crontab
crontab -e

# Add this line to run every Monday at 9 AM
0 9 * * 1 cd /home/user/topendsports-content-briefs && \
  python3 content-briefs-skill/scripts/ingest-feedback.py \
  > logs/feedback-ingestion-$(date +\%Y\%m\%d).log 2>&1
```

### Manual Trigger

Run anytime:
```bash
# From project root
python3 content-briefs-skill/scripts/ingest-feedback.py

# With verbose output
python3 content-briefs-skill/scripts/ingest-feedback.py -v

# To update docs
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons
```

## Key Integration Points

### 1. Input: Feedback Files
- **Source**: `feedback/validated/` directory
- **Format**: Markdown files following FEEDBACK-TEMPLATE.md
- **Naming**: `[page-name]-feedback-[YYYYMMDD].md`

### 2. Processing: Lesson Extraction
- **Parser**: Extracts structured data from feedback
- **Extractor**: Converts feedback to actionable lessons
- **Categorizer**: Groups lessons by type

### 3. Output: Report
- **Console Report**: Summary with statistics
- **Optional**: Updates to `lessons-learned.md`

### 4. Downstream: Using Lessons
- **Phase 1 Research**: Queries `lessons-learned.md` for depth requirements
- **Phase 2 Writer Brief**: Checks lessons for quality standards
- **Phase 3 AI Enhancement**: References lessons for completeness checks
- **Quality Checklist**: Updated with new lessons automatically

## Feedback Categories Detected

The script automatically categorizes feedback:

| Category | Triggers | Examples |
|----------|----------|----------|
| **Keyword Research** | Cannibalization, gaps, volume | "Add nfl moneyline keyword" |
| **Content Structure** | Word count, outline, sections | "Word count range too broad" |
| **Brand Selection** | Features, positioning, bonus details | "Missing bonus T&Cs" |
| **Technical** | HTML, schema, code issues | "Schema markup syntax error" |
| **Writer Experience** | Instructions, sources, clarity | "Unclear word count guidance" |
| **Process Improvement** | System documentation updates | "Update lessons-learned.md" |

## Data Preservation

The script maintains data integrity:

### What Gets Preserved
- Original feedback files (not modified)
- Complete feedback history (can re-run anytime)
- Audit trail (source tracking in lessons)

### What Gets Created/Modified
- Report output (stdout, can redirect to file)
- `lessons-learned.md` (only with `--update-lessons`)
- Directory structure (creates if missing)

### Idempotency
- Safe to run multiple times (doesn't create duplicates)
- Dry-run mode for safety (`--dry-run`)
- Version control friendly (git can track changes)

## Error Handling & Recovery

### Scenario 1: Feedback File Parsing Error
**What happens**:
```
[ERROR] Could not read nfl-betting-feedback.md: [reason]
```

**Recovery**:
1. Check file is valid UTF-8: `file nfl-betting-feedback.md`
2. Check file is readable: `chmod 644 nfl-betting-feedback.md`
3. Try again: `python3 ingest-feedback.py --verbose`

### Scenario 2: lessons-learned.md Write Fails
**What happens**:
```
[ERROR] Could not write to lessons file: [reason]
```

**Recovery**:
1. Check permissions: `ls -l references/lessons-learned.md`
2. Try with elevated privileges if needed: `sudo python3 ...`
3. Or run with `--dry-run` first to debug

### Scenario 3: No Feedback Files Found
**What happens**:
```
[NOTICE] No feedback files found in ...
```

**Recovery**:
1. Verify validated directory exists: `ls feedback/validated/`
2. Check files are there: `ls feedback/validated/*.md`
3. Run with verbose to debug: `python3 ingest-feedback.py --verbose`

## Best Practices

### For Feedback Submitters
1. **Be Specific**: "Word count too broad" → "Narrow 2,500-3,500 to 2,800-3,000"
2. **Link to Problems**: Reference specific sections or features
3. **Suggest Solutions**: Include actionable recommendations
4. **Provide Context**: Explain why something matters

### For Feedback Reviewers
1. **Validate Completeness**: Use `validate_feedback.py` before moving to validated/
2. **Check Priority Accuracy**: Do P1 items truly need immediate action?
3. **Look for Patterns**: Are multiple briefs reporting same issue?

### For Report Users
1. **Review Weekly**: Don't let feedback backlog accumulate
2. **Act on P1 Items**: Critical issues should trigger immediate response
3. **Update Lessons**: Apply lessons to reference docs regularly
4. **Close the Loop**: Tell submitters how their feedback was used

## Automation Opportunities

Possible future enhancements:

```python
# Auto-categorize feedback by brief type
if brief_type == "comparison":
    apply_comparison_lessons()

# Alert on patterns
if same_issue_in_3_briefs:
    send_alert("Pattern detected in feedback")

# Metrics dashboard
track_metrics([
    "avg_quality_rating",
    "issues_per_brief",
    "time_to_fix",
    "lessons_implemented"
])

# Integration with brief generator
load_lessons_automatically()
check_against_lessons()
warn_on_violations()
```

## Troubleshooting Integration

### Problem: Lessons aren't being used in new briefs

**Check**:
1. Did the script actually update `lessons-learned.md`?
   ```bash
   git diff references/lessons-learned.md
   ```

2. Is the brief generator reading the file?
   ```bash
   grep -r "lessons-learned" content-briefs-skill/*.py
   ```

3. Is it checking the lessons?
   ```bash
   python3 [brief-generator] --verbose | grep lessons
   ```

### Problem: Same issue reported multiple times

**Diagnosis**:
1. Run script to see pattern: `python3 ingest-feedback.py`
2. Check if issue is already in `lessons-learned.md`
3. If so, verify brief generator is reading it

**Action**:
1. Create ticket for this recurring issue
2. Prioritize fixing in next sprint
3. Add to pre-flight checklist

### Problem: Feedback files not being ingested

**Checklist**:
- [ ] Files in correct directory: `feedback/validated/`
- [ ] Files have `.md` extension
- [ ] Files are valid feedback format (check example)
- [ ] File permissions allow reading: `chmod 644 *.md`
- [ ] Run with `--verbose` to see errors

## Getting Help

For issues with the script:

1. **Check documentation**: Start with README-FEEDBACK-INGESTION.md
2. **Run verbose mode**: `python3 ingest-feedback.py --verbose`
3. **Check error messages**: Usually clear about what's wrong
4. **Review example feedback**: Compare your format to EXAMPLE-FEEDBACK.md
5. **Test with dry-run**: `python3 ingest-feedback.py --update-lessons --dry-run`

For issues with the feedback system:

1. **Read**: `feedback/FEEDBACK-PROCESS.md`
2. **Check**: `feedback/README.md`
3. **Reference**: `feedback/INTEGRATION-WITH-BRIEFS.md`

## Success Metrics

The feedback system is working well if:

- ✅ Weekly ingestion runs without errors
- ✅ `lessons-learned.md` grows with quality insights
- ✅ No repeated issues in consecutive briefs
- ✅ Writer feedback indicates improved instructions
- ✅ Quality ratings trend upward over time

Track these metrics to measure system health!
