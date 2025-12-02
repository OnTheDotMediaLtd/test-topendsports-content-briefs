# Scripts Documentation

## convert_to_docx.py

Converts markdown brief files to Microsoft Word (.docx) format for content writers.

### Features

- Preserves all formatting (headings, bold, italic, lists, tables, code blocks)
- Applies professional styling with green headings matching brand colors
- Handles complex markdown structures
- Batch converts all files in output folder

### Usage

**Convert all markdown files in output folder:**
```bash
python scripts/convert_to_docx.py --all
```

**Convert specific files:**
```bash
python scripts/convert_to_docx.py path/to/file1.md path/to/file2.md
```

### Requirements

```bash
pip install python-docx markdown
```

### What Gets Converted

The script converts these markdown elements to Word:

| Markdown | Word Output |
|----------|-------------|
| `# H1` | Heading 1 (24pt, green, bold) |
| `## H2` | Heading 2 (16pt, green, bold) |
| `### H3` | Heading 3 (14pt, dark gray, bold) |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `` `code` `` | Courier New, 10pt |
| `- bullet` | Bulleted list |
| `1. numbered` | Numbered list |
| Tables | Word tables with Light Grid style |
| Code blocks | Courier New, indented, gray background |

### Output Location

Word files are saved in the same location as the markdown files with `.docx` extension:
- `output/nfl-betting-sites-writer-brief.md` → `output/nfl-betting-sites-writer-brief.docx`

### Automated Workflow

After Claude completes all 3 phases of brief generation, it automatically runs:
```bash
python scripts/convert_to_docx.py --all
```

This ensures writers always receive Word documents, not markdown files.

### Troubleshooting

**Error: "python-docx not found"**
- Run: `pip install python-docx markdown`

**Error: "File not found"**
- Check that markdown files exist in `output/` folder
- Verify file paths are correct

**Formatting issues:**
- Script preserves most markdown formatting
- Complex HTML/CSS in markdown may not convert perfectly
- Tables with merged cells may need manual adjustment

### Manual Conversion Alternative

If the script doesn't work, you can also:
1. Open the `.md` file in Microsoft Word (File → Open → Select "All Files")
2. Word will automatically convert markdown
3. Save As → `.docx`

---

## validate_feedback.py

Validates submitted feedback files for completeness and readiness for review.

### Features

- Checks all required fields are filled out
- Identifies incomplete sections
- Highlights Priority 1 (critical) items
- Provides readiness summary for weekly review

### Usage

**Validate all submitted feedback:**
```bash
python scripts/validate_feedback.py
```

### What Gets Checked

The script validates:

| Check | Description |
|-------|-------------|
| Required fields | Brief ID, dates, reviewer name/role |
| Overall rating | At least one rating selected |
| What worked well | At least one item listed |
| What needs improvement | At least one item listed |
| Priority 1 items | Flags critical issues requiring immediate attention |

### Output

```
Validating 3 feedback file(s)...

==================================================================
File: nfl-betting-sites-feedback-20251128.md
==================================================================

[OK] No issues found - ready for review

==================================================================
SUMMARY
==================================================================
Total files: 3
Ready for review: 3
Need attention: 0

[OK] All files ready for review
```

### When to Use

- **Before weekly review**: Check which feedback is complete
- **After submission**: Validate your own feedback before submitting
- **Quality control**: Ensure all required information is present

### Exit Codes

- `0` - All files valid
- `1` - Some files have issues

---

Last Updated: November 28, 2025
