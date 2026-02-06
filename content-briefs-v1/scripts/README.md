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

Last Updated: November 28, 2025
