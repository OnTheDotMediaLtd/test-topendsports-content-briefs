# Content Briefs Validation Scripts

A comprehensive suite of validation scripts for the topendsports-content-briefs project. These scripts ensure data quality across CSVs, JSON phase outputs, and feedback submissions.

## Scripts Overview

### 1. validate_csv_data.py (322 lines)

Validates site structure CSV files for data quality and consistency.

**Purpose:**
- Detect duplicate URLs across CSV files
- Verify required columns presence
- Validate writer names and priority levels
- Check URL format consistency
- Identify empty required fields

**Features:**
- Single file or batch validation (--all flag)
- JSON output for CI/CD integration
- Detailed error reporting with line numbers
- Exit code 0 (pass) or 1 (fail)
- Comprehensive docstrings

**Usage:**
```bash
# Validate single CSV file
python validate_csv_data.py site-structure-english.csv

# Validate with JSON output
python validate_csv_data.py site-structure-english.csv --json

# Validate all CSV files in directory
python validate_csv_data.py --all --json
```

**Validation Rules:**
- **Duplicate URLs:** Detects and reports URLs appearing in multiple rows
- **Required Columns:** Must have URL, Keyword, Writer, Priority
- **Valid Writers:** Lewis, Tom, Gustavo Cantella
- **Valid Priorities:** High, Medium, Low
- **URL Format:** Must start with /sport/ (e.g., /sport/betting/...)
- **Empty Fields:** All required columns must contain values

**Exit Codes:**
- 0: All validations passed
- 1: One or more validation errors found

---

### 2. validate_phase_json.py (606 lines)

Validates Phase 1, 2, and 3 JSON outputs against specific content requirements.

**Purpose:**
Ensures JSON files meet comprehensive requirements at each phase of content development:

**Phase 1 Validation:**
- Primary keyword present
- Secondary keywords: 8-15 required
- Volume data for all keywords
- Competitor analysis: minimum 3 competitors
- Brand selection: FanDuel #1, BetMGM #2, research brands #3-10
- Writer assignment to valid team members

**Phase 2 Validation:**
- Content outline structure present
- H2 sections mapped to high-volume keywords (1000+)
- H3 sections mapped to medium-volume keywords (100+)
- FAQ questions: 5-7 for articles/reviews
- FAQ mapped to question-type keywords
- Source requirements with TIER 1 preference specified

**Phase 3 Validation:**
- HTML content present
- Schema markup complete (Article, FAQ, Breadcrumb)
- Terms & Conditions for all featured brands
- Interactive elements included
- Responsible gambling section present

**Features:**
- Auto-detect phase from JSON structure
- Single file or batch validation
- JSON output for CI/CD integration
- Detailed validation checks with pass/fail status
- Line-by-line error reporting with suggestions

**Usage:**
```bash
# Validate Phase 1 with explicit phase
python validate_phase_json.py phase1-output.json --phase 1

# Validate Phase 2 with JSON output
python validate_phase_json.py phase2-output.json --phase 2 --json

# Auto-detect phase (no need to specify)
python validate_phase_json.py phase3-output.json --phase 3

# Validate all phase files in directory
python validate_phase_json.py --all --json
```

**Exit Codes:**
- 0: All validations passed
- 1: One or more validation errors found

---

### 3. validate_feedback.py (513 lines)

Validates feedback submission files for correct format and content quality.

**Purpose:**
- Enforce consistent filename format (YYYY-MM-DD-topic.md)
- Verify required markdown sections
- Validate impact levels
- Check minimum word count in Issue section
- Validate markdown syntax

**Features:**
- Single file or batch validation (--all flag)
- JSON output for CI/CD integration
- Auto-suggest filename corrections
- Detailed error reporting with line numbers
- Markdown syntax validation
- Helpful correction suggestions

**Required Format:**

Filename: `YYYY-MM-DD-topic.md`
- Date must be valid YYYY-MM-DD format
- Topic must be lowercase with hyphens only
- Example: `2024-12-09-performance-improvement.md`

Required Sections:
- ## Issue/Improvement (minimum 50 words)
- ## Impact
- ## Suggested Solution
- ## Example (optional but recommended)

Must Include:
- Impact Level: Critical | High | Medium | Low
- Valid markdown syntax

**Usage:**
```bash
# Validate single feedback file
python validate_feedback.py feedback/2024-12-09-performance.md

# Validate with JSON output
python validate_feedback.py feedback/2024-12-09-ux-fix.md --json

# Validate all files in submitted/ directory
python validate_feedback.py --all

# Validate all with JSON output for CI/CD
python validate_feedback.py --all --json
```

**Example Feedback File:**
```markdown
## Issue/Improvement

The current validation scripts are slow when processing large files.
This impacts the development workflow as developers have to wait
3-5 minutes for validation to complete. The performance issue is
particularly noticeable when validating duplicate URLs across multiple
files. This compounds when running the full validation suite.

## Impact

Impact Level: High

Slow validation scripts delay the development pipeline. Currently a
developer must wait 3-5 minutes for CSV validation on large datasets.

## Suggested Solution

Optimize duplicate URL detection using set-based approach. Implement
parallel processing using Python's concurrent.futures module.

## Example

Current: 300 rows = 4 minutes
Expected: 300 rows = 15-20 seconds
```

**Exit Codes:**
- 0: All validations passed
- 1: One or more validation errors found

---

## Common Features

All scripts include:

1. **Help Documentation**
   ```bash
   python validate_*.py --help
   ```

2. **JSON Output Mode** (for CI/CD integration)
   ```bash
   python validate_*.py <file> --json
   ```

3. **Proper Error Handling**
   - Meaningful error messages
   - Helpful suggestions for corrections
   - Exit codes for automation

4. **Comprehensive Docstrings**
   - Function-level documentation
   - Usage examples
   - Parameter descriptions

5. **Unicode Safe Output**
   - Works on Windows (cp1252 encoding)
   - ASCII-safe output format
   - No unicode decode errors

## Installation & Setup

1. Ensure Python 3.7+ is installed
2. No external dependencies required
3. Scripts are self-contained standard library only
4. Place scripts in your project's scripts/ directory

## CI/CD Integration

Use JSON output mode for automated validation in CI/CD pipelines:

```bash
# Run validation and capture JSON output
python validate_csv_data.py --all --json > validation_report.json

# Check exit code
if [ $? -eq 0 ]; then
    echo "All validations passed"
else
    echo "Validation failed"
    cat validation_report.json
fi
```

## JSON Output Format

All scripts support JSON output with consistent format:

```json
{
  "validation_type": "csv_data|phase_json|feedback",
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

## Exit Codes

All scripts follow standard exit code conventions:

- **Exit 0:** Validation passed (no errors)
- **Exit 1:** Validation failed (errors detected)

Use exit codes in shell scripts for automation:

```bash
python validate_csv_data.py data.csv
if [ $? -eq 0 ]; then
    # Proceed with next step
    git commit ...
else
    # Handle validation failure
    echo "Please fix validation errors"
    exit 1
fi
```

## Testing

Sample test files are included in test_data/ directory:

- `test_site_structure.csv` - Valid CSV
- `test_invalid_data.csv` - Invalid CSV with multiple errors
- `phase1_example.json` - Valid Phase 1 JSON
- `phase2_example.json` - Valid Phase 2 JSON
- `phase3_example.json` - Valid Phase 3 JSON
- `2024-12-09-performance-improvement.md` - Valid feedback file

Run tests:
```bash
cd test_data
python ../scripts/validate_csv_data.py test_site_structure.csv
python ../scripts/validate_csv_data.py test_invalid_data.csv
python ../scripts/validate_phase_json.py phase1_example.json --phase 1
python ../scripts/validate_feedback.py 2024-12-09-performance-improvement.md
```

## Development Notes

Scripts are designed with:
- Clear separation of concerns
- Modular validation methods
- Comprehensive error handling
- Extensibility for future requirements
- Standard Python best practices
- Type hints for clarity
- Dataclass usage for structured data

## Support & Troubleshooting

If you encounter issues:

1. Ensure Python 3.7+ is installed
2. Check file encoding is UTF-8
3. Verify file paths are correct
4. Run with --help to see available options
5. Check exit code: `echo $?` (Linux/Mac) or `echo %ERRORLEVEL%` (Windows)

## License & Usage

These scripts are part of the topendsports-content-briefs project and should be used to maintain data quality standards across the project.
