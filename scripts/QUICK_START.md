# Validation Scripts - Quick Start Guide

## Installation

1. Copy scripts to your project:
   ```bash
   cp scripts/*.py your-project/scripts/
   ```

2. Make scripts executable (Linux/Mac):
   ```bash
   chmod +x scripts/validate_*.py
   ```

## Script 1: CSV Data Validation

**Purpose:** Validate site structure CSV files

### Basic Usage
```bash
python validate_csv_data.py site-structure-english.csv
```

### Check Everything
```bash
python validate_csv_data.py --all
```

### JSON Output (for CI/CD)
```bash
python validate_csv_data.py site-structure-english.csv --json
```

### What It Checks
- Duplicate URLs (reports line numbers)
- Missing required columns: URL, Keyword, Writer, Priority
- Invalid writer names (must be: Lewis, Tom, Gustavo Cantella)
- Invalid priorities (must be: High, Medium, Low)
- URL format (must start with /sport/)
- Empty required fields

---

## Script 2: Phase JSON Validation

**Purpose:** Validate Phase 1, 2, 3 JSON outputs

### Phase 1 Validation
```bash
python validate_phase_json.py phase1-output.json --phase 1
```

### Phase 2 Validation
```bash
python validate_phase_json.py phase2-output.json --phase 2
```

### Phase 3 Validation
```bash
python validate_phase_json.py phase3-output.json --phase 3
```

### Auto-Detect Phase
```bash
python validate_phase_json.py phase1-output.json
```

### Batch Validate All
```bash
python validate_phase_json.py --all --json
```

### What It Checks

**Phase 1:**
- Primary keyword present
- 8-15 secondary keywords
- Volume data for all keywords
- 3+ competitors
- FanDuel #1, BetMGM #2, research #3-10
- Valid writer assignment

**Phase 2:**
- Content outline present
- H2 sections mapped to high-volume keywords
- H3 sections mapped to medium-volume keywords
- 5-7 FAQ questions (for articles)
- FAQ questions mapped to keywords
- TIER 1 source preference specified

**Phase 3:**
- HTML content present
- Schema markup complete (Article, FAQ, Breadcrumb)
- T&Cs for all featured brands
- Interactive elements
- Responsible gambling section

---

## Script 3: Feedback Validation

**Purpose:** Validate feedback submission format

### Validate Single Feedback
```bash
python validate_feedback.py feedback/2024-12-09-improvement.md
```

### Validate All Feedback
```bash
python validate_feedback.py --all
```

### JSON Output
```bash
python validate_feedback.py --all --json
```

### Required Feedback Format

Filename: `YYYY-MM-DD-topic.md`
- Valid date in format YYYY-MM-DD
- Topic in lowercase with hyphens
- Example: `2024-12-09-performance-boost.md`

Content Structure:
```markdown
## Issue/Improvement

Describe the issue in 50+ words. Provide context and explain
why this matters. Use clear, professional language. Ensure
you explain the problem thoroughly so the team understands
the scope and impact of the issue.

## Impact

Impact Level: High

Explain how this issue affects the project, team, or users.
Quantify the impact if possible (e.g., delays, cost).

## Suggested Solution

Provide a clear, actionable solution to the problem.
Include specific steps or recommendations.

## Example

Optional section showing a concrete example of the issue
or how the solution would work in practice.
```

### What It Checks
- Filename format: YYYY-MM-DD-topic.md
- Valid date (no future dates)
- All required sections present
- Minimum 50 words in Issue/Improvement section
- Impact level specified (Critical, High, Medium, Low)
- Valid markdown syntax
- Balanced code blocks and formatting

---

## Understanding Exit Codes

All scripts use standard exit codes:
- **Exit 0:** Validation passed
- **Exit 1:** Validation failed

Use in shell scripts:
```bash
python validate_csv_data.py all --json
if [ $? -eq 0 ]; then
    echo "Validation passed"
    # Continue with next step
else
    echo "Validation failed"
    exit 1
fi
```

---

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Validate CSVs
  run: python scripts/validate_csv_data.py --all --json

- name: Validate Phase JSON
  run: python scripts/validate_phase_json.py --all --json

- name: Validate Feedback
  run: python scripts/validate_feedback.py --all --json
```

### Save Reports
```bash
python scripts/validate_csv_data.py --all --json > csv-report.json
python scripts/validate_phase_json.py --all --json > phase-report.json
python scripts/validate_feedback.py --all --json > feedback-report.json
```

---

## JSON Output Format

All scripts produce consistent JSON output:

```json
{
  "validation_type": "csv_data",
  "timestamp": "2025-12-09T12:10:02.945710",
  "all_valid": true,
  "total_files": 1,
  "reports": [
    {
      "file": "path/to/file",
      "valid": true,
      "error_count": 0,
      "warning_count": 0,
      "errors": [],
      "warnings": []
    }
  ]
}
```

---

## Common Issues

### "File not found"
Ensure the file path is correct and the file exists.

### "Invalid date in filename"
Feedback filenames must be YYYY-MM-DD format. Example: `2024-12-09`

### "Empty required field"
CSV validation found empty values. Check line numbers in error message.

### "Invalid writer name"
Writer must be: Lewis, Tom, or Gustavo Cantella (exact spelling)

### "Duplicate URL"
Two rows have the same URL. Check line numbers in error.

---

## Help & Options

View all options:
```bash
python validate_csv_data.py --help
python validate_phase_json.py --help
python validate_feedback.py --help
```

---

## Test Data

Sample test files are in `test_data/` directory:
- `test_site_structure.csv` - Valid CSV
- `test_invalid_data.csv` - CSV with errors
- `phase1_example.json` - Phase 1 example
- `phase2_example.json` - Phase 2 example
- `phase3_example.json` - Phase 3 example
- `2024-12-09-performance-improvement.md` - Feedback example

Try validating these to see how scripts work:
```bash
cd test_data
python ../scripts/validate_csv_data.py test_site_structure.csv
python ../scripts/validate_csv_data.py test_invalid_data.csv  # Shows errors
python ../scripts/validate_phase_json.py phase1_example.json --phase 1
python ../scripts/validate_feedback.py 2024-12-09-performance-improvement.md
```

---

## Summary

| Script | Purpose | Checks |
|--------|---------|--------|
| validate_csv_data.py | CSV data quality | Duplicates, columns, values |
| validate_phase_json.py | Phase outputs | Structure, content, requirements |
| validate_feedback.py | Feedback format | Filename, sections, content |

All scripts:
- Support `--help` flag
- Have `--json` output mode
- Use exit codes 0/1
- Handle errors gracefully
- Provide helpful messages

For full documentation, see README.md
