# CI/CD Integration for Testing and Error Tracking

**Created**: 2025-12-11
**Status**: Implemented

## Overview

This document describes the comprehensive CI/CD integration for the testing and error tracking system. The integration automatically tracks errors, analyzes patterns, generates lessons, and creates pull requests for documentation updates.

## Architecture

```
┌─────────────────┐
│   Test Suite    │
│   (pytest)      │
└────────┬────────┘
         │
         ├──> Error Tracking Plugin
         │    (--error-tracking flag)
         │
         ├──> Error Logs
         │    (logs/errors/error_log.json)
         │
         ├──> Pattern Analysis
         │    (logs/errors/patterns.json)
         │
         └──> Threshold Checks
              (pass/warn/fail)

┌─────────────────┐
│  Weekly Cron    │
│  (Mondays 9AM)  │
└────────┬────────┘
         │
         ├──> Analyze Accumulated Errors
         │
         ├──> Generate Lessons
         │    (if patterns found)
         │
         ├──> Create PR
         │    (auto-update lessons-learned.md)
         │
         └──> Send Notifications
              (if critical)
```

## Workflows

### 1. Test Workflow (`test.yml`)

**Triggers**: Push/PR to main/master/develop branches

**Features**:
- Runs pytest with `--error-tracking` flag
- Generates code coverage reports (uploaded to Codecov)
- Analyzes error patterns after tests
- Checks error thresholds (fail build if exceeded)
- Uploads error logs and test results as artifacts

**Error Tracking Integration**:
```yaml
- pytest --error-tracking --cov=scripts --cov=tests
- python3 scripts/error_tracker.py analyze
- python3 scripts/check_error_thresholds.py
```

**Artifacts**:
- `error-logs`: Error logs and patterns (30-day retention)
- `pytest-results`: Coverage reports (30-day retention)

**Exit Codes**:
- `0`: All tests passed, thresholds met
- `1`: Tests failed OR warnings detected
- `2`: Critical error thresholds exceeded (build fails)

---

### 2. Weekly Error Analysis Workflow (`error-analysis.yml`)

**Triggers**:
- Schedule: Every Monday at 9:00 AM UTC
- Manual: `workflow_dispatch` with options

**Workflow Steps**:

1. **Analyze Errors**
   - Load accumulated error data
   - Generate statistics report
   - Run pattern analysis
   - Check thresholds

2. **Generate Lessons**
   - Detect recurring patterns (3+ occurrences)
   - Create lesson entries automatically
   - Append to `lessons-learned.md`

3. **Create Pull Request**
   - Create branch: `automated/error-lessons-YYYYMMDD-HHMMSS`
   - Commit lesson changes
   - Open PR with detailed description
   - Tag for review

4. **Generate Report**
   - Weekly analysis summary
   - Error distribution by category
   - Threshold status
   - Recommendations

5. **Archive Old Data**
   - Clear errors older than 90 days
   - Commit archived data

**Inputs**:
- `force_lesson_generation`: Force generation even if already processed
- `min_occurrences`: Minimum pattern count (default: 3)

**Outputs**:
- Pull request with auto-generated lessons
- Weekly analysis report (90-day retention)
- Critical error notifications (if applicable)

---

### 3. Feedback Ingestion Workflow (`feedback-ingestion.yml`)

**Triggers**:
- Push to `content-briefs-skill/feedback/submitted/**`
- Push to `content-briefs-skill/feedback/validated/**`
- Manual: `workflow_dispatch`

**Enhanced Features**:

1. **Validate Feedback**
   - Check submitted feedback files
   - Validate format and completeness

2. **Ingest Feedback**
   - Process validated feedback
   - Update feedback log
   - Generate lessons (if requested)

3. **Analyze Errors** (NEW)
   - Count recent errors (7-day window)
   - Run pattern analysis
   - Check error thresholds
   - Upload error data as artifacts

4. **Generate Combined Report** (NEW)
   - Feedback processing summary
   - Error tracking statistics
   - Combined recommendations
   - Actionable next steps

**Outputs**:
- `error-tracker-data`: Error logs (30-day retention)
- `combined-analysis-report`: Unified report (90-day retention)

---

## Error Threshold Configuration

File: `scripts/check_error_thresholds.py`

### Thresholds

| Metric | Warning | Failure | Action |
|--------|---------|---------|--------|
| Critical Errors | - | 0 | Immediate fix required |
| Recurring Patterns (5+) | 3 | 5 | Generate lessons |
| Patterns Needing Attention | 3 | 10 | Run lesson generation |
| Error Surge (7-day) | 50% increase | - | Investigate root cause |

### Exit Codes

- `0`: All thresholds met
- `1`: Warnings detected (non-blocking)
- `2`: Thresholds exceeded (blocking)

---

## Error Tracking Plugin

File: `tests/python/conftest_error_tracking.py`

### Usage

```bash
# Enable error tracking
pytest --error-tracking

# Enable with verbose output
pytest --error-tracking --verbose-tracking
```

### Features

- Automatic test failure logging
- Category detection (api, validation, file, content, test)
- Severity inference (critical, high, medium, low)
- Fingerprint generation for deduplication
- Pattern detection
- Real-time recommendations

---

## Error Tracker CLI

File: `scripts/error_tracker.py`

### Commands

```bash
# Log an error manually
python3 scripts/error_tracker.py log \
  --source "test_ahrefs" \
  --error "API 403" \
  --context "keywords lookup"

# Analyze patterns
python3 scripts/error_tracker.py analyze

# Generate lessons from patterns
python3 scripts/error_tracker.py generate-lessons

# Show statistics
python3 scripts/error_tracker.py stats

# Clear old errors (30+ days)
python3 scripts/error_tracker.py clear --days 30
```

---

## Data Storage

### Directory Structure

```
logs/
└── errors/
    ├── error_log.json          # All logged errors
    ├── patterns.json           # Pattern analysis data
    └── weekly-report-*.md      # Weekly analysis reports

content-briefs-skill/
└── references/
    └── lessons-learned.md      # Auto-updated lessons
```

### Error Log Schema

```json
{
  "last_updated": "2025-12-11T10:30:00Z",
  "total_count": 150,
  "errors": [
    {
      "timestamp": "2025-12-11T10:25:00Z",
      "source": "pytest:tests/test_ahrefs.py::test_api_call",
      "error_message": "HTTP 403 Forbidden - API access denied",
      "context": "keywords-explorer/overview",
      "category": "api",
      "severity": "high",
      "stack_trace": "...",
      "metadata": {},
      "fingerprint": "a1b2c3d4e5f6"
    }
  ]
}
```

### Pattern Schema

```json
{
  "a1b2c3d4e5f6": {
    "first_seen": "2025-12-01T10:00:00Z",
    "last_seen": "2025-12-11T10:25:00Z",
    "count": 12,
    "source": "pytest:tests/test_ahrefs.py",
    "category": "api",
    "severity": "high",
    "sample_message": "HTTP 403 Forbidden - API access denied",
    "sample_context": "keywords-explorer/overview",
    "occurrences": [
      {
        "timestamp": "2025-12-11T10:25:00Z",
        "context": "keywords-explorer/overview"
      }
    ],
    "lesson_generated": true
  }
}
```

---

## Lesson Generation

### Automatic Lesson Format

```markdown
## Auto-Generated Lessons (2025-12-11)
*Generated from error pattern analysis*

### Handle API Authentication Errors
**Problem**: API calls failing with auth errors (12 occurrences)
**Solution**: Use Python fallback (ahrefs-api.py) when MCP returns 403. Check API credentials and rate limits.
*Category: api | Source: pytest:tests/test_ahrefs.py | Occurrences: 12*
```

### Categories

- `api`: API errors (403, 401, timeout, rate limits)
- `validation`: Schema and input validation failures
- `file`: File operation errors
- `content`: Content processing errors
- `test`: Test assertion failures
- `process`: Workflow and process errors

---

## Pull Request Automation

### Automated PR Format

**Title**: `Add N auto-generated lessons from error patterns`

**Body**:
- Summary of lessons generated
- Source: Weekly error analysis
- What to review
- Files changed
- Next steps

**Labels**: (manual tagging recommended)
- `automated`
- `documentation`
- `lessons-learned`

---

## Notifications

### Critical Error Notifications

When error thresholds are exceeded:
- GitHub Actions annotation: `::error::`
- Artifact upload with details
- Exit code 2 (build failure)

### Weekly Summary

Delivered via:
- Workflow summary
- Artifact upload (90-day retention)
- Pull request (if lessons generated)

---

## Maintenance

### Cleanup Schedule

- **Error logs**: Cleared after 90 days
- **Artifacts**: Retained for 30-90 days (varies by type)
- **Reports**: Retained for 90 days

### Manual Cleanup

```bash
# Clear errors older than 30 days
python3 scripts/error_tracker.py clear --days 30

# Archive old patterns
python3 scripts/archive_old_patterns.py
```

---

## Monitoring

### Key Metrics

1. **Error Rate**: Total errors logged per week
2. **Pattern Count**: Unique error patterns detected
3. **Recurring Issues**: Patterns with 5+ occurrences
4. **Lesson Generation**: Auto-generated lessons per week
5. **Threshold Violations**: Warning vs. critical failures

### Dashboards

- GitHub Actions workflow runs
- Artifact downloads
- Pull request merge rate

---

## Best Practices

### For Developers

1. **Always run tests with error tracking** in CI/CD
2. **Review weekly PRs** for auto-generated lessons
3. **Investigate recurring patterns** (3+ occurrences)
4. **Update thresholds** as project matures
5. **Archive old data** to keep logs manageable

### For CI/CD

1. **Don't skip error analysis** even if tests pass
2. **Upload artifacts** for debugging
3. **Set retention periods** appropriately
4. **Monitor threshold violations** closely

---

## Troubleshooting

### Issue: Error tracker not logging

**Check**:
- Pytest plugin installed: `--error-tracking` flag recognized?
- Error log directory exists: `logs/errors/`
- Permissions correct

**Fix**:
```bash
mkdir -p logs/errors
chmod 755 logs/errors
```

### Issue: Thresholds always failing

**Check**:
- Current threshold values in `check_error_thresholds.py`
- Recent error counts
- Pattern accumulation

**Fix**:
- Adjust thresholds if too strict
- Clear old patterns
- Investigate root cause of errors

### Issue: Lessons not generated

**Check**:
- Pattern count >= minimum (default: 3)
- `lesson_generated` flag not already set
- Workflow permissions

**Fix**:
```bash
# Force lesson generation
python3 scripts/error_tracker.py generate-lessons --min-occurrences 2
```

---

## Future Enhancements

- [ ] Slack/Discord notifications for critical errors
- [ ] Trend analysis graphs
- [ ] Error categorization ML model
- [ ] Auto-fix suggestions
- [ ] Integration with issue tracker

---

## References

- Error Tracker: `scripts/error_tracker.py`
- Threshold Checker: `scripts/check_error_thresholds.py`
- Test Plugin: `tests/python/conftest_error_tracking.py`
- Test Workflow: `.github/workflows/test.yml`
- Error Analysis Workflow: `.github/workflows/error-analysis.yml`
- Feedback Ingestion: `.github/workflows/feedback-ingestion.yml`
