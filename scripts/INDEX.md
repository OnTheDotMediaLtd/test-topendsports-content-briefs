# Validation Scripts - Complete Index

## Overview

Three production-ready validation scripts for the topendsports-content-briefs project.

**Total Lines of Code:** 1,441 lines
**Status:** Complete and tested
**Location:** C:\temp\content-briefs-temp\scripts\

---

## Scripts

### 1. validate_csv_data.py
**File:** `validate_csv_data.py`
**Lines:** 322
**Purpose:** Validate site structure CSV files for data quality

#### Key Features:
- Duplicate URL detection with line numbers
- Required column validation
- Writer name validation (Lewis, Tom, Gustavo Cantella)
- Priority value validation (High, Medium, Low)
- URL format checking (/sport/*)
- Empty field detection
- Single file or batch validation (--all)
- JSON output mode (--json)

#### Quick Usage:
```bash
python validate_csv_data.py site-structure-english.csv
python validate_csv_data.py --all --json
```

#### Validation Rules:
```
- Duplicate URLs: Checked with line number reporting
- Required Columns: URL, Keyword, Writer, Priority
- Valid Writers: Lewis, Tom, Gustavo Cantella
- Valid Priorities: High, Medium, Low
- URL Format: Must start with /sport/
- Empty Fields: Not allowed in required columns
```

---

### 2. validate_phase_json.py
**File:** `validate_phase_json.py`
**Lines:** 606
**Purpose:** Validate Phase 1, 2, and 3 JSON outputs

#### Phase 1 Checks:
- Primary keyword presence
- Secondary keywords: 8-15 count
- Volume data for all keywords
- Competitor analysis: minimum 3
- Brand selection: FanDuel #1, BetMGM #2, research #3-10
- Writer assignment validation

#### Phase 2 Checks:
- Content outline presence
- H2 sections mapped to high-volume keywords (1000+)
- H3 sections mapped to medium-volume keywords (100+)
- FAQ questions: 5-7 for articles/reviews
- FAQ keyword mapping
- Source requirements (TIER 1 preferred)

#### Phase 3 Checks:
- HTML content presence
- Schema markup (Article, FAQ, Breadcrumb)
- Terms & Conditions for all brands
- Interactive elements
- Responsible gambling section

#### Quick Usage:
```bash
python validate_phase_json.py phase1-output.json --phase 1
python validate_phase_json.py phase2-output.json --phase 2
python validate_phase_json.py phase3-output.json --phase 3
python validate_phase_json.py --all --json
```

#### Auto-Detection:
The script can auto-detect phase from JSON structure. If it can't detect:
```bash
python validate_phase_json.py phase1-output.json --phase 1
```

---

### 3. validate_feedback.py
**File:** `validate_feedback.py`
**Lines:** 513
**Purpose:** Validate feedback submission format and content

#### Validation Checks:
- Filename format: YYYY-MM-DD-topic.md
- Valid date in filename
- Topic format (lowercase, hyphens only)
- Required sections:
  - `## Issue/Improvement` (50+ words)
  - `## Impact`
  - `## Suggested Solution`
  - `## Example` (optional)
- Impact level specification
- Markdown syntax validation

### Filename Rules:
```
Format: YYYY-MM-DD-topic.md
Date: Must be valid calendar date
Topic: Lowercase letters, numbers, hyphens only
Example: 2024-12-09-performance-improvement.md
```

### Required Content:
```
## Issue/Improvement
[Minimum 50 words describing the issue]

## Impact
Impact Level: Critical|High|Medium|Low
[Description of impact]

## Suggested Solution
[Clear action items]

## Example (optional)
[Concrete example]
```

#### Quick Usage:
```bash
python validate_feedback.py feedback/2024-12-09-improvement.md
python validate_feedback.py --all
python validate_feedback.py --all --json
```

---

## Documentation Files

### README.md
**Purpose:** Comprehensive reference guide
**Contents:**
- Detailed script descriptions
- All validation rules
- Usage examples
- CI/CD integration
- JSON output format
- Exit codes
- Testing section
- Troubleshooting

### QUICK_START.md
**Purpose:** Fast start guide for users
**Contents:**
- Installation instructions
- Basic usage for each script
- What each script checks
- Common issues and solutions
- Test data information
- Summary table

### IMPLEMENTATION_SUMMARY.md
**Purpose:** Technical implementation details
**Contents:**
- Design patterns used
- Data validation approach
- Error reporting strategy
- Performance considerations
- Compatibility notes
- Validation coverage matrix

### VALIDATION_SCRIPTS_REPORT.txt
**Purpose:** Detailed delivery and testing report
**Contents:**
- Deliverables summary
- All requirements verification
- Testing results
- Code quality metrics
- Deployment checklist
- Compatibility verification

### INDEX.md
**Purpose:** This file - complete overview

---

## Test Data

Sample files are located in `test_data/` directory:

### CSV Test Files:
- `test_site_structure.csv` - Valid CSV with correct data
- `test_invalid_data.csv` - CSV with multiple validation errors

### Phase JSON Files:
- `phase1_example.json` - Valid Phase 1 JSON
- `phase2_example.json` - Valid Phase 2 JSON
- `phase3_example.json` - Valid Phase 3 JSON

### Feedback File:
- `2024-12-09-performance-improvement.md` - Valid feedback file

### Test Results:
All test files have been validated successfully.

---

## Features Summary

### All Scripts Include:

#### Command-line Interface
```bash
python validate_*.py --help                 # View options
python validate_*.py <file>                 # Validate file
python validate_*.py --all                  # Batch validation
python validate_*.py <file> --json          # JSON output
```

#### Exit Codes
```
Exit 0: Validation passed
Exit 1: Validation failed
```

#### JSON Output Format
```json
{
  "validation_type": "csv_data|phase_json|feedback",
  "timestamp": "ISO 8601 timestamp",
  "all_valid": true/false,
  "total_files": number,
  "reports": [
    {
      "file": "filename",
      "valid": true/false,
      "error_count": number,
      "warning_count": number,
      "errors": [...],
      "warnings": [...]
    }
  ]
}
```

#### Error Reporting
- Detailed error messages
- Line number reporting (where applicable)
- Helpful suggestions for fixes
- Context-specific messages

#### Compatibility
- Python 3.7+
- Windows, Linux, Mac
- UTF-8 encoding support
- No external dependencies

---

## Quick Command Reference

### CSV Validation
```bash
# Single file
python validate_csv_data.py site-structure-english.csv

# All CSV files
python validate_csv_data.py --all

# JSON output for CI/CD
python validate_csv_data.py --all --json

# Check help
python validate_csv_data.py --help
```

### Phase JSON Validation
```bash
# Phase 1
python validate_phase_json.py phase1.json --phase 1

# Phase 2
python validate_phase_json.py phase2.json --phase 2

# Phase 3
python validate_phase_json.py phase3.json --phase 3

# All phases
python validate_phase_json.py --all

# JSON output
python validate_phase_json.py --all --json
```

### Feedback Validation
```bash
# Single file
python validate_feedback.py feedback/2024-12-09-topic.md

# All feedback
python validate_feedback.py --all

# JSON output
python validate_feedback.py --all --json

# Help
python validate_feedback.py --help
```

---

## Code Statistics

| Script | Lines | Purpose |
|--------|-------|---------|
| validate_csv_data.py | 322 | CSV validation |
| validate_phase_json.py | 606 | Phase JSON validation |
| validate_feedback.py | 513 | Feedback validation |
| **Total** | **1,441** | **Complete suite** |

All scripts exceed their minimum line requirements.

---

## Deployment Checklist

- [x] Scripts implemented and tested
- [x] All requirements verified
- [x] Error handling implemented
- [x] JSON output working
- [x] Exit codes functional
- [x] Documentation complete
- [x] Test data included
- [x] Code quality verified
- [x] Platform compatibility checked
- [x] Ready for production

---

## Support

### Documentation
1. Start with QUICK_START.md for basic usage
2. Refer to README.md for complete reference
3. Check IMPLEMENTATION_SUMMARY.md for technical details

### Common Issues
See QUICK_START.md for troubleshooting section.

### Testing
Use files in test_data/ directory to verify scripts work.

---

## Files Included

```
scripts/
├── validate_csv_data.py (322 lines)
├── validate_phase_json.py (606 lines)
├── validate_feedback.py (513 lines)
├── README.md
├── QUICK_START.md
├── IMPLEMENTATION_SUMMARY.md
├── VALIDATION_SCRIPTS_REPORT.txt
├── INDEX.md
└── test_data/
    ├── test_site_structure.csv
    ├── test_invalid_data.csv
    ├── phase1_example.json
    ├── phase2_example.json
    ├── phase3_example.json
    └── 2024-12-09-performance-improvement.md
```

---

## Next Steps

1. Copy scripts to project repository
2. Add to version control
3. Configure pre-commit hooks (optional)
4. Integrate into CI/CD pipeline
5. Train team on usage
6. Monitor validation reports

---

**Status:** Production Ready
**Version:** 1.0
**Date:** 2025-12-09

All scripts are fully tested, documented, and ready for deployment.
