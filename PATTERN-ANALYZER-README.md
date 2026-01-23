# Pattern Analyzer - Topendsports Content Briefs

## Overview

The Pattern Analyzer automatically detects recurring validation failures and generates actionable feedback to improve the article formatting process.

## What It Does

- **Analyzes** validation reports from the `output/` directory
- **Detects** recurring failure patterns (issues appearing >2 times in 7 days)
- **Generates** alerts for high-priority issues
- **Creates** auto-feedback submissions for critical patterns
- **Suggests** documentation updates based on recurring mistakes

## How to Run

### Quick Run (Recommended)
```bash
python scripts/run_pattern_analysis.py
```

This runs all 3 phases automatically:
1. Analysis of validation reports
2. Alert generation
3. Auto-feedback creation

### Manual Commands

```bash
# Run analysis only
python scripts/pattern_analyzer.py analyze

# Generate alerts
python scripts/pattern_analyzer.py alerts

# Create auto-feedback
python scripts/pattern_analyzer.py auto-feedback
```

## Configuration

### Pattern Detection Thresholds

Located in `pattern_analyzer.py`:

```python
RECURRENCE_THRESHOLD = 2  # Patterns appearing > 2 times trigger alerts
LOOKBACK_DAYS = 7         # Analyze reports from last 7 days
```

### Failure Categories

The analyzer detects these categories specific to article formatting:

| Category | Description | Example Issues |
|----------|-------------|----------------|
| `word_count` | Articles below 800 words | "Word count 650 < 800 minimum" |
| `attribution` | Generic or missing attributions | "Research shows..." (forbidden) |
| `structure` | Incorrect library placement | Citation Library inside #container |
| `links` | Placeholder or broken links | href="#" not removed |
| `components` | Missing formatting modules | FAQ missing required questions |
| `validation` | Failed validation checks | Test failed: schema validation |
| `encoding` | Character encoding issues | UTF-8 encoding errors |
| `schema` | Meta tag or tracking problems | Missing og:image tag |

### Severity Levels

**Critical** (>50% occurrence rate):
- Word count violations
- Structure errors (library placement)
- Attribution issues

**High** (30-50% occurrence rate):
- Repeated validation failures
- Component quality issues

**Medium** (<30% occurrence rate):
- Minor link issues
- Encoding warnings

## Output Files

### Analysis Report
**Location:** `insights/pattern-analysis.json`

Contains:
- Summary statistics
- Recurring pattern details
- Alert information
- Documentation suggestions

### Alerts
**Location:** `insights/alerts.json`

Contains:
- Alert timestamp
- Category and severity
- Occurrence count
- Specific recommendations

### Auto-Feedback
**Location:** `feedback/submitted/auto-{category}-{timestamp}.json`

Contains:
- Feedback metadata
- Root cause analysis
- Solution recommendations
- Prevention strategies
- Example failures

## Integration with CI/CD

### GitHub Actions

Add to `.github/workflows/pattern-analysis.yml`:

```yaml
name: Pattern Analysis

on:
  schedule:
    - cron: '0 0 * * 0'  # Run weekly
  workflow_dispatch:      # Allow manual trigger

jobs:
  analyze-patterns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run Pattern Analysis
        run: python scripts/run_pattern_analysis.py

      - name: Upload Reports
        uses: actions/upload-artifact@v4
        with:
          name: pattern-analysis-reports
          path: insights/
```

## Alert Thresholds

| Pattern Count | Action |
|---------------|--------|
| >2 occurrences | Pattern detected and logged |
| >3 occurrences (High severity) | Auto-feedback created |
| >5 occurrences (Critical) | Alert + auto-feedback + doc update suggested |

## Common Patterns Detected

### Word Count Violations
**Pattern:** Articles formatted with <800 words
**Solution:** Add word count validation in Phase 1
**Prevention:** "Calculate word count BEFORE formatting"

### Attribution Issues
**Pattern:** Generic phrases like "Research shows"
**Solution:** Replace with specific sources or remove
**Prevention:** "NEVER use generic attribution phrases"

### Structure Errors
**Pattern:** Citation Library inside #container
**Solution:** Move Citation Library outside container
**Prevention:** "Citation Library MUST be OUTSIDE #container"

### Placeholder Links
**Pattern:** Links with href="#" left in output
**Solution:** Remove placeholder links entirely
**Prevention:** "DELETE placeholder links, don't keep them"

## Viewing Results

### Console Output
```bash
$ python scripts/run_pattern_analysis.py

============================================================
TES Article Formatting - Pattern Analyzer
============================================================

Analyzing validation reports from last 7 days...
Found 15 validation files

Loaded 12 reports within timeframe

============================================================
PATTERN ANALYSIS REPORT
============================================================

[SUMMARY]:
   Total Reports Analyzed: 12
   Total Failures Detected: 8
   Recurring Patterns: 2

[DISTRIBUTION] Failure Distribution:
   Word_count: 3 instances
   Attribution: 5 instances

[ALERT] Recurring Patterns (>2 occurrences):

[HIGH] ATTRIBUTION
   Count: 5
   Severity: HIGH
   Message: [ALERT] Attribution Issues: 5 instances of generic/missing attributions
   Recommendation: Review attribution guidelines. Replace generic phrases...

============================================================
```

### JSON Reports
```json
{
  "generated_at": "2025-12-18T10:30:00",
  "lookback_days": 7,
  "analysis": {
    "total_reports": 12,
    "total_failures": 8,
    "patterns": {
      "word_count": 3,
      "attribution": 5
    }
  },
  "recurring_patterns": [
    {
      "category": "attribution",
      "count": 5,
      "severity": "high",
      "failures": [...]
    }
  ]
}
```

## Troubleshooting

### No Validation Reports Found
**Cause:** No files matching `*.validation.json` in `output/`
**Solution:** Run validation first: `python scripts/validate_article.py`

### Import Error: FeedbackProcessor
**Cause:** Feedback system not set up yet
**Solution:** Auto-feedback files are still created in `feedback/submitted/`

### No Recurring Patterns
**Cause:** Quality is consistent OR not enough reports
**Solution:** This is good! If intentional, continue working normally

### Pattern Analysis Taking Too Long
**Cause:** Too many old validation reports
**Solution:** Adjust `LOOKBACK_DAYS` to 3-5 days instead of 7

## Best Practices

1. **Run Weekly:** Schedule pattern analysis to run every Sunday
2. **Review Alerts:** Check `insights/alerts.json` for new patterns
3. **Act on Feedback:** Review auto-generated feedback in `feedback/submitted/`
4. **Update Documentation:** Apply suggested doc updates to prevent recurrence
5. **Adjust Thresholds:** Tune `RECURRENCE_THRESHOLD` based on team size and velocity

## Version History

- **v1.0** (Dec 18, 2025): Initial deployment from tes-internal-linking
  - Adapted failure categories for article formatting
  - Updated severity calculations
  - Added article-specific pattern detection

## Contact

For issues or questions about pattern analysis:
- Check `insights/pattern-analysis.json` for details
- Review auto-feedback in `feedback/submitted/`
- Contact: andre-external@strategie360consulting.com
