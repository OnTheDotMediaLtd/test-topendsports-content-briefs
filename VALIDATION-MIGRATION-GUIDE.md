# Content Briefs - Tiered Validation Migration Guide

## Overview

This repository now implements the tiered validation system with three levels of severity:
- **BLOCKING**: Must pass - CI fails if these checks fail
- **ADVISORY**: Should pass - CI warns but doesn't fail
- **INFO**: Nice to have - CI logs only

## Validators Implemented

### 1. Content Brief Validator (`validate_brief_tiered.py`)

Validates markdown content briefs (writer briefs, control sheets, AI enhancement docs).

**BLOCKING Checks (3):**
- Required sections present (keywords, URL, content structure*)
- Keyword data complete (volume/difficulty/keywords)
- CSV file referenced exists (if applicable)

*Content structure only required for writer briefs and AI enhancement, not control sheets

**ADVISORY Checks (2):**
- SEO recommendations present
- Competitor analysis included

**INFO Checks (1):**
- Analysis depth (500+ words indicates thorough brief)

**Usage:**
```bash
# Validate content brief
python content-briefs-skill/scripts/validate_brief_tiered.py content-briefs-skill/output/[page]-writer-brief.md

# Strict mode (fail on any warning)
python content-briefs-skill/scripts/validate_brief_tiered.py --strict content-briefs-skill/output/[page]-writer-brief.md

# JSON output
python content-briefs-skill/scripts/validate_brief_tiered.py --output-format json content-briefs-skill/output/[page]-writer-brief.md
```

### 2. CSV Configuration Validator (`validate_csv_tiered.py`)

Validates CSV data files (site structure, keywords, state pages).

**BLOCKING Checks (3):**
- CSV format valid (can be parsed)
- Required columns present (URL, keywords for site structure)
- No data corruption (no completely empty rows)

**ADVISORY Checks (1):**
- Data completeness (some fields may be empty)

**INFO Checks (1):**
- Data quality suggestions (duplicate detection)

**Usage:**
```bash
# Validate site structure CSV
python content-briefs-skill/scripts/validate_csv_tiered.py content-briefs-skill/assets/data/site-structure-english.csv

# Validate keyword data
python content-briefs-skill/scripts/validate_csv_tiered.py content-briefs-skill/output/keywords.csv

# JSON output
python content-briefs-skill/scripts/validate_csv_tiered.py --output-format json data/file.csv
```

### 3. Phase JSON Validator (`validate_phase_json_tiered.py`)

Validates phase JSON files (phase1.json, phase2.json).

**BLOCKING Checks (3):**
- JSON syntax valid
- Required fields present (pageName, url, primaryKeyword, etc.)
- Schema compliance (proper structure for keywords, FAQs, etc.)

**ADVISORY Checks (1):**
- Best practices followed (8+ secondary keywords, 7+ FAQs)

**INFO Checks (1):**
- Optimization opportunities (keyword placement, internal links)

**Usage:**
```bash
# Validate phase 1 JSON
python content-briefs-skill/scripts/validate_phase_json_tiered.py content-briefs-skill/active/[page]-phase1.json

# Validate phase 2 JSON
python content-briefs-skill/scripts/validate_phase_json_tiered.py content-briefs-skill/active/[page]-phase2.json

# Strict mode
python content-briefs-skill/scripts/validate_phase_json_tiered.py --strict active/[page]-phase1.json
```

## Validation Summary

| Validator | BLOCKING | ADVISORY | INFO | Total |
|-----------|----------|----------|------|-------|
| Content Brief | 3 | 2 | 1 | 6 |
| CSV | 3 | 1 | 1 | 5 |
| Phase JSON | 3 | 1 | 1 | 5 |
| **TOTAL** | **9** | **4** | **3** | **16** |

## Integration with Shared Infrastructure

All validators use the shared `TieredValidator` base class from `tes-shared-infrastructure`:

```python
from tes_shared.validation.tiered_validator import (
    TieredValidator, ValidationLevel
)
```

If the shared infrastructure is not available, each validator includes a fallback implementation.

## Exit Codes

- **0**: All BLOCKING checks passed (CI should succeed)
- **1**: One or more BLOCKING checks failed (CI should fail)

In strict mode (`--strict`), the validators will exit with code 1 if ANY check fails (including ADVISORY and INFO).

## Output Formats

### Text Format (default)

```
======================================================================
VALIDATION REPORT
======================================================================

BLOCKING CHECKS (3):
----------------------------------------------------------------------
  [PASS] [BLOCK] [BLOCKING] required_sections: All required sections present
    → These sections are essential for content creation
  [PASS] [BLOCK] [BLOCKING] keyword_data: Keyword data present
    → Volume, difficulty, or keyword list required
  [PASS] [BLOCK] [BLOCKING] csv_reference: No CSV file referenced (optional)
    → CSV data files are optional for content briefs

ADVISORY CHECKS (2):
----------------------------------------------------------------------
  [PASS] [WARN]  [ADVISORY] seo_recommendations: SEO recommendations present
    → SEO guidance improves content quality
  [FAIL] [WARN]  [ADVISORY] competitor_analysis: Consider adding competitor analysis
    → Understanding competition improves content strategy

INFO CHECKS (1):
----------------------------------------------------------------------
  [PASS] [INFO]  [INFO] analysis_depth: Brief is detailed (3232 words)
    → 500+ words indicates thorough analysis

======================================================================
SUMMARY: 0 blocking failures, 1 advisory warnings, 0 info notices
STATUS: PASSED - CI should succeed
======================================================================
```

### JSON Format

```json
{
  "results": [
    {
      "level": "blocking",
      "check_name": "required_sections",
      "passed": true,
      "message": "All required sections present",
      "details": "These sections are essential for content creation"
    }
  ],
  "should_fail_ci": false
}
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Validate Content Briefs

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Validate content briefs
        run: |
          for file in content-briefs-skill/output/*.md; do
            python3 content-briefs-skill/scripts/validate_brief_tiered.py "$file"
          done

      - name: Validate CSV files
        run: |
          for file in content-briefs-skill/assets/data/*.csv; do
            python3 content-briefs-skill/scripts/validate_csv_tiered.py "$file"
          done

      - name: Validate phase JSON files
        run: |
          for file in content-briefs-skill/active/*.json; do
            python3 content-briefs-skill/scripts/validate_phase_json_tiered.py "$file"
          done
```

## Testing the Validators

Run the validators on sample files to verify they work correctly:

```bash
# Test content brief validator
python3 content-briefs-skill/scripts/validate_brief_tiered.py \
  content-briefs-skill/output/apuestas-deportivas-chile-writer-brief.md

# Test CSV validator
python3 content-briefs-skill/scripts/validate_csv_tiered.py \
  content-briefs-skill/assets/data/site-structure-english.csv

# Test phase JSON validator
python3 content-briefs-skill/scripts/validate_phase_json_tiered.py \
  content-briefs-skill/active/best-apps-phase1.json
```

## Common Validation Scenarios

### Scenario 1: New Content Brief Created

After creating a new brief, validate all three components:

```bash
PAGE="new-page"

# Validate control sheet
python3 content-briefs-skill/scripts/validate_brief_tiered.py \
  "content-briefs-skill/output/${PAGE}-brief-control-sheet.md"

# Validate writer brief
python3 content-briefs-skill/scripts/validate_brief_tiered.py \
  "content-briefs-skill/output/${PAGE}-writer-brief.md"

# Validate phase JSONs
python3 content-briefs-skill/scripts/validate_phase_json_tiered.py \
  "content-briefs-skill/active/${PAGE}-phase1.json"

python3 content-briefs-skill/scripts/validate_phase_json_tiered.py \
  "content-briefs-skill/active/${PAGE}-phase2.json"
```

### Scenario 2: CSV Data Update

After updating site structure or keyword data:

```bash
python3 content-briefs-skill/scripts/validate_csv_tiered.py \
  content-briefs-skill/assets/data/site-structure-english.csv
```

### Scenario 3: Pre-commit Validation

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Validate all modified markdown files
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.md$'); do
  if [[ $file == content-briefs-skill/output/* ]]; then
    python3 content-briefs-skill/scripts/validate_brief_tiered.py "$file"
    if [ $? -ne 0 ]; then
      echo "Validation failed for $file"
      exit 1
    fi
  fi
done

# Validate all modified JSON files
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.json$'); do
  if [[ $file == content-briefs-skill/active/* ]]; then
    python3 content-briefs-skill/scripts/validate_phase_json_tiered.py "$file"
    if [ $? -ne 0 ]; then
      echo "Validation failed for $file"
      exit 1
    fi
  fi
done
```

## Customization

### Adding New Checks

To add a new validation check:

1. Add a new method to the appropriate validator class
2. Call it from `validate_all()`
3. Use `self.add_result()` to record the check result

Example:

```python
def validate_new_check(self) -> bool:
    """INFO: Description of the check."""
    # Your validation logic here
    passed = True  # or False

    self.add_result(
        ValidationLevel.INFO,
        "new_check",
        passed,
        "Success message" if passed else "Failure message",
        details="Additional context about the check"
    )
    return passed
```

### Changing Check Severity

To change a check from ADVISORY to BLOCKING:

```python
# Before
self.add_result(ValidationLevel.ADVISORY, ...)

# After
self.add_result(ValidationLevel.BLOCKING, ...)
```

## Troubleshooting

### ImportError: No module named 'tes_shared'

The validators will automatically fall back to the embedded implementation. No action needed.

### UnicodeEncodeError on Windows

Set the environment variable:

```bash
export TES_VALIDATION_ASCII=1
```

This will use ASCII-safe output instead of Unicode symbols.

### Validators Always Pass/Fail

Check the exit code:

```bash
python3 script.py file.md
echo $?  # Should be 0 for pass, 1 for fail
```

## Migration Checklist

- [x] Content brief validator created (`validate_brief_tiered.py`)
- [x] CSV validator created (`validate_csv_tiered.py`)
- [x] Phase JSON validator created (`validate_phase_json_tiered.py`)
- [x] All validators tested on sample files
- [x] Documentation created (this file)
- [ ] CI/CD integration configured (if applicable)
- [ ] Pre-commit hooks added (if applicable)
- [ ] Team notified of new validation system

## Resources

- Shared infrastructure: `C:/Users/AndreBorg/OnTheDotMediaLtd/tes-shared-infrastructure`
- Validator base class: `src/tes_shared/validation/tiered_validator.py`
- Other implementations: See `topendsports-url-research`, `topendsports-content-optimizer` for examples

## Support

For issues or questions about the validation system:
1. Check this guide first
2. Review the validator source code (includes docstrings)
3. Check the shared infrastructure documentation
4. Review similar validators in other repositories
