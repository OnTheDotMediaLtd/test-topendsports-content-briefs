# Feedback Ingestion Script

## Overview

The `ingest-feedback.py` script automates the process of reading validated feedback files and extracting actionable lessons for continuous improvement of the TopEndSports content brief system.

**Location**: `/content-briefs-skill/scripts/ingest-feedback.py`

## Purpose

This script:
1. **Reads** validated feedback files from `feedback/validated/` directory
2. **Parses** structured feedback markdown files
3. **Extracts** actionable lessons from feedback data
4. **Generates** comprehensive summary reports
5. **Updates** `lessons-learned.md` with new insights (optional)

## Quick Start

### Basic Usage

```bash
# Generate report from all feedback files
python3 content-briefs-skill/scripts/ingest-feedback.py

# Show detailed debug output
python3 content-briefs-skill/scripts/ingest-feedback.py --verbose

# Preview changes to lessons-learned.md
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons --dry-run

# Apply changes to lessons-learned.md
python3 content-briefs-skill/scripts/ingest-feedback.py --update-lessons
```

### Command-Line Options

```
--update-lessons    Update lessons-learned.md with new lessons
--verbose, -v       Show verbose output for debugging
--dry-run           Show what would be changed without making changes
--help, -h          Show help message
```

## Workflow

### Step 1: Feedback Submission
Reviewers place completed feedback files in `feedback/validated/` directory:
```
feedback/validated/[page-name]-feedback-[YYYYMMDD].md
```

### Step 2: Run Ingestion Script
```bash
python3 ingest-feedback.py --verbose
```

The script will:
- Find all `.md` files in `feedback/validated/`
- Parse each file and extract structured data
- Generate a comprehensive report
- Exit with status 0 on success

### Step 3: Review Report
Output shows:
- Number of files processed
- Lessons extracted by category
- Priority 1 (Critical) items
- Average quality rating
- Recommendations for documentation updates

### Step 4: Update Documentation (Optional)
```bash
python3 ingest-feedback.py --update-lessons --dry-run
```

Review proposed changes, then apply:
```bash
python3 ingest-feedback.py --update-lessons
```

## Input Format

### Feedback File Structure

Feedback files should follow the template in `feedback/FEEDBACK-TEMPLATE.md`:

```markdown
# Brief Feedback Form

## Brief Information
- **Brief ID**: [page-name]
- **Date Generated**: [YYYY-MM-DD]
- **Date Reviewed**: [YYYY-MM-DD]
- **Reviewer Name**: [Name]
- **Reviewer Role**: [Writer / SEO Manager / Editor / Other]

## Overall Rating
**Overall Quality**: [X] 3 - Good

## Category Ratings
[Table with ratings 1-5 for each category]

## What Worked Well
[Numbered list of 3-5 items]

## What Needs Improvement
[Numbered list of issues]

## Keyword Issues
[Cannibalization concerns, missing keywords, unnecessary keywords]

## Technical Issues
[HTML/Code problems, schema markup issues, interactive element issues]

## Actionable Changes Recommended
**Priority 1 (Critical)**: [Critical items]
**Priority 2 (Important)**: [Important items]
**Priority 3 (Nice to Have)**: [Nice-to-have items]

## For System Improvement
[Documentation updates needed]

## Follow-Up Required?
[Follow-up actions if any]
```

## Output Report

The script generates a formatted report with:

### 1. Summary Statistics
- Files processed
- Lessons extracted
- Priority breakdown
- Average quality rating

### 2. Lessons by Category
Organized categories include:
- **Keyword Research**: Keyword gaps, cannibalization issues
- **Content Structure**: Outline, word count, organization
- **Brand Selection**: Brand positioning, feature coverage
- **Technical**: HTML, schema, interactive elements
- **Writer Experience**: Clarity, sources, missing information
- **Process Improvement**: System documentation updates

### 3. Feedback File Summary
Lists each feedback file with:
- Brief ID
- Quality rating
- Reviewer name and role
- Feedback categories
- Date reviewed

### 4. Recommendations
- Documentation files needing updates
- High-priority issues requiring attention
- Next steps

## Lesson Extraction

The script extracts lessons from multiple feedback sources:

### From Priority Items
**Priority 1 (Critical)**: Immediate action required
- Marked as CRITICAL in output

**Priority 2 (Important)**: Should be addressed soon
- Marked as IMPORTANT in output

**Priority 3 (Nice to Have)**: Enhancement opportunities
- Marked as NOTE in output

### From Keyword Issues
- **Cannibalization**: Flags potential keyword conflicts
- **Missing Keywords**: Identifies content gaps
- **Unnecessary Keywords**: Highlights out-of-scope keywords

### From Technical Issues
- **HTML Problems**: Code structure issues
- **Schema Markup**: Structured data problems
- **Interactive Elements**: Feature implementation issues

### From System Improvements
- Extracts specific documentation updates needed
- Maps to affected sections and files

## Lessons File Update

When using `--update-lessons`, the script:

1. **Creates a dated section** in `lessons-learned.md`:
   ```markdown
   ## New Lessons (YYYY-MM-DD)
   *Extracted from validated user feedback*
   ```

2. **Organizes by category**:
   ```markdown
   ### Category Name
   **[PRIORITY]** Lesson text
   > Reason or explanation
   *Source: brief-id*
   ```

3. **Preserves existing content** - all new lessons are appended

4. **Prevents duplicates** - checks existing content before adding

### Example Output

```markdown
## New Lessons (2025-12-08)
*Extracted from validated user feedback*

### Keyword Research

**[CRITICAL]** Always check for keyword cannibalization by searching site-structure CSV before finalizing secondary keywords
> Keyword cannibalization dilutes ranking power across multiple pages
*Source: nfl-betting-sites*

**[IMPORTANT]** Narrow word count guidance to 100-word range
> Broad ranges (2,500-3,500) make content unpredictable
*Source: nfl-betting-sites*

### Technical

**[CRITICAL]** Validate schema markup before publishing
> Schema markup validation is essential for search appearance
*Source: nfl-betting-sites*
```

## Error Handling

The script handles various error conditions gracefully:

### Missing Feedback Directory
If `feedback/validated/` doesn't exist:
```
[NOTICE] Feedback directory not found: ...
Creating directory structure...
[OK] Created ...
```

### Empty Feedback Directory
If no feedback files found:
```
[NOTICE] No feedback files found in ...
Place validated feedback files there and run again.
```

### Malformed Feedback Files
Skips files that can't be parsed and continues with others:
```
[ERROR] Could not read [filename]: [reason]
```

### Invalid Lessons File
If `lessons-learned.md` doesn't exist or can't be written:
```
[ERROR] File not found: ...
[ERROR] Could not write to lessons file: ...
```

## Features

### 1. Flexible Parsing
- Parses feedback files with varying completeness
- Extracts data from standard feedback form sections
- Handles missing or empty fields gracefully
- Skips placeholder template values

### 2. Intelligent Categorization
Automatically categorizes feedback by type:
- **Keyword Research**: Cannibalization, gaps, volume
- **Content Structure**: Word count, outline, H2/H3
- **Brand Selection**: Features, positioning, comparisons
- **Technical**: Code, schema, interactivity
- **Writer Experience**: Instructions, sources, clarity
- **Process Improvement**: System documentation

### 3. Priority Awareness
Distinguishes between:
- **CRITICAL (P1)**: Must fix before next brief
- **IMPORTANT (P2)**: Should address in next cycle
- **NICE-TO-HAVE (P3)**: Enhancement opportunities
- **NOTE**: General observations

### 4. Source Tracking
Every extracted lesson tracks:
- Original feedback file name
- Brief ID that generated the feedback
- Reviewer name and role
- Date reviewed

### 5. Dry-Run Mode
Preview changes to lessons-learned.md without modifying files:
```bash
python3 ingest-feedback.py --update-lessons --dry-run
```

### 6. Verbose Debugging
Get detailed parsing information:
```bash
python3 ingest-feedback.py --verbose
```

Output includes:
- Files being parsed
- Fields extracted
- Lessons identified
- Processing steps

## Integration with Feedback System

This script is part of the larger feedback system:

```
[Reviewer submits feedback]
        ↓
[Manual review in feedback/submitted/]
        ↓
[Move to feedback/validated/]
        ↓
[ingest-feedback.py extracts lessons]
        ↓
[Review report and proposed changes]
        ↓
[Optional: Update lessons-learned.md]
        ↓
[Next brief uses improved instructions]
```

See `feedback/FEEDBACK-PROCESS.md` for complete workflow.

## Common Use Cases

### Use Case 1: Weekly Ingestion
Run weekly to capture new feedback:
```bash
# Every Monday morning
python3 ingest-feedback.py > /tmp/weekly-feedback-report.txt
```

### Use Case 2: Before Brief Generation
Check latest feedback before generating new briefs:
```bash
# Shows what we learned from recent briefs
python3 ingest-feedback.py --verbose
```

### Use Case 3: Documentation Updates
Apply cumulative lessons to reference docs:
```bash
# Review what changed
python3 ingest-feedback.py --update-lessons --dry-run

# Apply changes
python3 ingest-feedback.py --update-lessons
```

### Use Case 4: Feedback Validation
Verify feedback files are complete:
```bash
# Check for parsing errors
python3 ingest-feedback.py --verbose 2>&1 | grep ERROR
```

## Performance

The script is optimized for typical feedback volumes:
- **1-10 files**: < 1 second
- **11-50 files**: 1-2 seconds
- **50+ files**: 2-5 seconds

Memory usage is minimal as files are processed sequentially.

## Troubleshooting

### No feedback files found
**Problem**: Script says "No feedback files found"
**Solution**:
1. Check directory exists: `ls feedback/validated/`
2. Verify files have `.md` extension
3. Ensure files are readable: `chmod 644 feedback/validated/*.md`

### Parsing errors for valid files
**Problem**: Script skips a file that looks valid
**Solution**:
1. Run with `--verbose` to see details: `python3 ingest-feedback.py --verbose`
2. Check required fields are filled (not template placeholders)
3. Verify file encoding is UTF-8: `file feedback/validated/*.md`

### Can't update lessons file
**Problem**: "Could not write to lessons file" error
**Solution**:
1. Check file exists: `ls content-briefs-skill/references/lessons-learned.md`
2. Verify write permissions: `chmod 644 content-briefs-skill/references/lessons-learned.md`
3. Ensure parent directory is writable: `ls -ld content-briefs-skill/references/`

### Dry-run shows but update fails
**Problem**: `--dry-run` works but actual update fails
**Solution**:
1. Check disk space: `df -h`
2. Verify no other process is editing the file
3. Try again: `python3 ingest-feedback.py --update-lessons`

## Technical Details

### Dependencies
- Python 3.11+
- Standard library only (no external packages required)
- Works on Linux, macOS, Windows

### Architecture

The script is organized into classes:

1. **FeedbackParser**: Parses markdown feedback files
   - `parse_file()`: Parse single file
   - `_extract_field()`: Extract field values
   - `_extract_list_section()`: Extract numbered lists
   - `_determine_categories()`: Categorize feedback

2. **LessonExtractor**: Converts feedback to lessons
   - `extract_lessons()`: Process all feedback
   - `_extract_from_feedback()`: Extract from single feedback
   - `_convert_to_lesson()`: Format as lesson

3. **ReportGenerator**: Creates summary reports
   - `generate_report()`: Build complete report
   - `print_report()`: Output to console

4. **LessonsFileUpdater**: Updates lessons-learned.md
   - `update_lessons_file()`: Apply changes to file

### Exit Codes
- `0`: Success
- `1`: Error (file not readable, write failed, etc.)

## Files Modified

When using `--update-lessons`, this script modifies:
- `content-briefs-skill/references/lessons-learned.md` (appends new section)

No files are modified when running in default or `--dry-run` modes.

## Contributing

To improve this script:
1. Test with various feedback file formats
2. Add new category detection patterns if needed
3. Update lesson formatting based on feedback
4. Report issues or enhancement requests

See `feedback/README.md` for feedback system guidelines.

## Related Documentation

- `feedback/FEEDBACK-TEMPLATE.md` - Template for feedback submission
- `feedback/FEEDBACK-PROCESS.md` - Complete feedback workflow
- `feedback/EXAMPLE-FEEDBACK.md` - Example completed feedback
- `references/lessons-learned.md` - Generated lessons output
- `GUARDRAILS.md` - Anti-patterns the script helps prevent
