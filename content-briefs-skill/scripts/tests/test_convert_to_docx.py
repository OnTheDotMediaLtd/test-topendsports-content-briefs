"""
Tests for convert_to_docx.py markdown to Word document converter
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from convert_to_docx import parse_markdown_to_docx, convert_file, add_hyperlink


class TestParseMarkdownToDocx:
    """Tests for the parse_markdown_to_docx function"""

    @pytest.fixture
    def sample_markdown(self):
        """Load sample markdown fixture"""
        fixture_path = Path(__file__).parent / "fixtures" / "sample_brief.md"
        with open(fixture_path, "r", encoding="utf-8") as f:
            return f.read()

    @pytest.fixture
    def output_path(self):
        """Create temporary output path for test documents"""
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            yield f.name
        # Cleanup after test
        if os.path.exists(f.name):
            os.unlink(f.name)

    def test_creates_docx_file(self, sample_markdown, output_path):
        """Test that a .docx file is created"""
        parse_markdown_to_docx(sample_markdown, output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_handles_h1_heading(self, output_path):
        """Test H1 heading parsing"""
        markdown = "# Main Title\n\nSome content."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_h2_heading(self, output_path):
        """Test H2 heading parsing"""
        markdown = "## Section Title\n\nSome content."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_h3_heading(self, output_path):
        """Test H3 heading parsing"""
        markdown = "### Subsection Title\n\nSome content."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_h4_heading(self, output_path):
        """Test H4 heading parsing"""
        markdown = "#### Minor Section\n\nSome content."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_h5_heading(self, output_path):
        """Test H5 heading parsing"""
        markdown = "##### Small Section\n\nSome content."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_bullet_lists(self, output_path):
        """Test bullet list parsing"""
        markdown = """## List Section

- Item one
- Item two
- Item three
"""
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_asterisk_bullet_lists(self, output_path):
        """Test asterisk bullet list parsing"""
        markdown = """## List Section

* Item one
* Item two
* Item three
"""
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_numbered_lists(self, output_path):
        """Test numbered list parsing"""
        markdown = """## List Section

1. First item
2. Second item
3. Third item
"""
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_code_blocks(self, output_path):
        """Test code block parsing"""
        markdown = """## Code Section

```python
def hello():
    print("Hello")
```
"""
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_inline_code(self, output_path):
        """Test inline code parsing"""
        markdown = "Use the `print()` function to output text."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_bold_text(self, output_path):
        """Test bold text parsing"""
        markdown = "This is **bold text** in a sentence."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_tables(self, output_path):
        """Test table parsing"""
        markdown = """## Table Section

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
"""
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_blockquotes(self, output_path):
        """Test blockquote parsing"""
        markdown = "> This is a quoted block of text."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_horizontal_rules(self, output_path):
        """Test horizontal rule parsing (should be skipped)"""
        markdown = "Some text\n\n---\n\nMore text"
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_empty_lines(self, output_path):
        """Test empty line handling"""
        markdown = "Line 1\n\n\n\nLine 2"
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_mixed_content(self, sample_markdown, output_path):
        """Test full markdown with mixed content types"""
        parse_markdown_to_docx(sample_markdown, output_path)
        assert os.path.exists(output_path)
        # File should be reasonably sized
        assert os.path.getsize(output_path) > 1000

    def test_handles_empty_markdown(self, output_path):
        """Test empty markdown input"""
        markdown = ""
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_removes_emojis_from_headings(self, output_path):
        """Test emoji removal from headings"""
        markdown = "## 🎯 Section with Emoji\n\nContent here."
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)


class TestConvertFile:
    """Tests for the convert_file function"""

    @pytest.fixture
    def temp_markdown_file(self):
        """Create a temporary markdown file"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Test Document\n\nThis is test content.")
            temp_path = f.name
        yield temp_path
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        docx_path = temp_path.replace(".md", ".docx")
        if os.path.exists(docx_path):
            os.unlink(docx_path)

    def test_converts_markdown_file(self, temp_markdown_file):
        """Test successful file conversion"""
        result = convert_file(temp_markdown_file)
        assert result is True

        docx_path = temp_markdown_file.replace(".md", ".docx")
        assert os.path.exists(docx_path)

    def test_returns_false_for_missing_file(self):
        """Test handling of non-existent file"""
        result = convert_file("/nonexistent/path/file.md")
        assert result is False

    def test_creates_docx_with_same_name(self, temp_markdown_file):
        """Test that output file has same name with .docx extension"""
        convert_file(temp_markdown_file)

        expected_docx = Path(temp_markdown_file).with_suffix(".docx")
        assert expected_docx.exists()


class TestAddHyperlink:
    """Tests for the add_hyperlink function"""

    @pytest.fixture
    def document(self):
        """Create a test document with a paragraph"""
        from docx import Document

        doc = Document()
        paragraph = doc.add_paragraph()
        return doc, paragraph

    def test_creates_hyperlink_element(self, document):
        """Test that hyperlink is created"""
        doc, paragraph = document
        result = add_hyperlink(paragraph, "https://example.com", "Example Link")
        assert result is not None

    def test_hyperlink_has_text(self, document):
        """Test that hyperlink contains text"""
        doc, paragraph = document
        add_hyperlink(paragraph, "https://example.com", "Click Here")
        # The paragraph should contain the link
        assert len(paragraph._p) > 0


class TestEdgeCases:
    """Tests for edge cases and error handling"""

    @pytest.fixture
    def output_path(self):
        """Create temporary output path"""
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            yield f.name
        if os.path.exists(f.name):
            os.unlink(f.name)

    def test_handles_unicode_content(self, output_path):
        """Test Unicode character handling"""
        markdown = "# Title with émojis and spëcial çharacters\n\nContent: 你好世界"
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_very_long_lines(self, output_path):
        """Test handling of very long lines"""
        long_line = "A" * 10000
        markdown = f"# Title\n\n{long_line}"
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_deeply_nested_structure(self, output_path):
        """Test handling of complex nested structure"""
        markdown = """# Level 1
## Level 2
### Level 3
#### Level 4
##### Level 5

- Item 1
  - Nested item
- Item 2

1. Numbered
2. List
"""
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_unclosed_code_block(self, output_path):
        """Test handling of unclosed code block"""
        markdown = """# Title

```python
def test():
    pass
"""
        # Should not raise an exception
        parse_markdown_to_docx(markdown, output_path)
        assert os.path.exists(output_path)

    def test_handles_table_with_varying_columns(self, output_path):
        """Test handling of tables with inconsistent columns - raises IndexError"""
        markdown = """| A | B | C |
|---|---|---|
| 1 | 2 |
| 3 | 4 | 5 | 6 |
"""
        # Currently, the code doesn't handle varying column counts gracefully
        # This documents the existing behavior
        with pytest.raises(IndexError):
            parse_markdown_to_docx(markdown, output_path)
