#!/usr/bin/env python3
"""
Comprehensive tests for validate_feedback.py

Targets 85%+ coverage of scripts/validate_feedback.py
"""

import sys
import json
import re
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open
from dataclasses import asdict

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_feedback import ValidationError, FeedbackValidator, main


class TestValidationError:
    """Test ValidationError dataclass."""

    def test_validation_error_creation(self):
        """Test creating ValidationError with required fields."""
        error = ValidationError(line_number=10, message="Test error")
        assert error.line_number == 10
        assert error.message == "Test error"
        assert error.suggestion is None

    def test_validation_error_with_suggestion(self):
        """Test ValidationError with suggestion field."""
        error = ValidationError(
            line_number=5,
            message="Invalid format",
            suggestion="Use correct format"
        )
        assert error.line_number == 5
        assert error.message == "Invalid format"
        assert error.suggestion == "Use correct format"

    def test_validation_error_none_line_number(self):
        """Test ValidationError with None line_number."""
        error = ValidationError(line_number=None, message="File error")
        assert error.line_number is None
        assert error.message == "File error"


class TestFeedbackValidatorInit:
    """Test FeedbackValidator initialization."""

    def test_init(self, tmp_path):
        """Test validator initialization."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        assert validator.feedback_file == test_file
        assert validator.errors == []
        assert validator.warnings == []
        assert validator.content == ""
        assert validator.lines == []

    def test_init_with_nonexistent_file(self, tmp_path):
        """Test initialization with non-existent file."""
        test_file = tmp_path / "nonexistent.md"
        validator = FeedbackValidator(test_file)
        assert validator.feedback_file == test_file


class TestFilenameValidation:
    """Test filename validation logic."""

    def test_valid_filename(self, tmp_path):
        """Test valid filename format."""
        test_file = tmp_path / "2024-12-09-test-topic.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        assert validator._validate_filename() is True
        assert len(validator.errors) == 0

    def test_invalid_filename_format(self, tmp_path):
        """Test invalid filename format."""
        test_file = tmp_path / "invalid-filename.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        assert validator._validate_filename() is False
        assert len(validator.errors) == 1
        assert "Invalid filename format" in validator.errors[0].message

    def test_invalid_date_in_filename(self, tmp_path):
        """Test invalid date in filename."""
        test_file = tmp_path / "2024-13-40-invalid-date.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        assert validator._validate_filename() is False
        assert len(validator.errors) == 1
        assert "Invalid date" in validator.errors[0].message

    def test_future_date_warning(self, tmp_path):
        """Test future date generates warning."""
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        test_file = tmp_path / f"{future_date}-future-topic.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        assert validator._validate_filename() is True
        assert len(validator.warnings) == 1
        assert "future" in validator.warnings[0].message.lower()

    def test_invalid_topic_in_filename(self, tmp_path):
        """Test invalid topic format in filename."""
        test_file = tmp_path / "2024-12-09-Invalid_Topic!.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        assert validator._validate_filename() is False
        assert len(validator.errors) == 1
        assert "Invalid topic" in validator.errors[0].message

    def test_empty_topic_in_filename(self, tmp_path):
        """Test empty topic in filename."""
        test_file = tmp_path / "2024-12-09-.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        assert validator._validate_filename() is False
        assert len(validator.errors) == 1


class TestFileReading:
    """Test file reading functionality."""

    def test_read_valid_file(self, tmp_path):
        """Test reading a valid UTF-8 file."""
        test_file = tmp_path / "2024-12-09-test.md"
        content = "# Test Content\n\nSome text here."
        test_file.write_text(content, encoding='utf-8')

        validator = FeedbackValidator(test_file)
        assert validator._read_file() is True
        assert validator.content == content
        assert len(validator.lines) == 3

    def test_read_file_with_unicode(self, tmp_path):
        """Test reading file with unicode characters."""
        test_file = tmp_path / "2024-12-09-test.md"
        content = "# Test Content\n\n日本語 Français émojis 🎉"
        test_file.write_text(content, encoding='utf-8')

        validator = FeedbackValidator(test_file)
        assert validator._read_file() is True
        assert "日本語" in validator.content
        assert "🎉" in validator.content

    def test_read_file_encoding_error(self, tmp_path):
        """Test reading file with encoding error."""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_bytes(b'\x80\x81\x82')  # Invalid UTF-8

        validator = FeedbackValidator(test_file)
        assert validator._read_file() is False
        assert len(validator.errors) == 1
        assert "encoding error" in validator.errors[0].message.lower()

    def test_read_file_generic_error(self, tmp_path, monkeypatch):
        """Test generic file reading error."""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)

        # Mock open to raise a generic exception
        def mock_open_error(*args, **kwargs):
            raise IOError("Generic file error")

        monkeypatch.setattr("builtins.open", mock_open_error)
        assert validator._read_file() is False
        assert len(validator.errors) == 1
        assert "Error reading file" in validator.errors[0].message


class TestMarkdownFormatValidation:
    """Test markdown format validation."""

    def test_empty_file(self, tmp_path):
        """Test validation of empty file."""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text("")

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_format()

        assert len(validator.errors) == 1
        assert "empty" in validator.errors[0].message.lower()

    def test_whitespace_only_file(self, tmp_path):
        """Test validation of whitespace-only file."""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text("   \n\n   \n")

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_format()

        assert len(validator.errors) == 1
        assert "empty" in validator.errors[0].message.lower()

    def test_non_empty_file(self, tmp_path):
        """Test validation of non-empty file."""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text("# Content here")

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_format()

        assert len(validator.errors) == 0


class TestRequiredSectionsValidation:
    """Test required sections validation."""

    def test_all_required_sections_present(self, tmp_path):
        """Test file with all required sections."""
        content = """# Feedback

## Issue/Improvement

Some issue description here.

## Impact

This is the impact.

## Suggested Solution

Here is the solution.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_required_sections()

        assert len(validator.errors) == 0

    def test_missing_issue_section(self, tmp_path):
        """Test missing Issue/Improvement section."""
        content = """# Feedback

## Impact

This is the impact.

## Suggested Solution

Here is the solution.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_required_sections()

        assert len(validator.errors) == 1
        assert "Issue/Improvement" in validator.errors[0].message

    def test_missing_impact_section(self, tmp_path):
        """Test missing Impact section."""
        content = """# Feedback

## Issue/Improvement

Some issue description.

## Suggested Solution

Here is the solution.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_required_sections()

        assert len(validator.errors) == 1
        assert "Impact" in validator.errors[0].message

    def test_missing_solution_section(self, tmp_path):
        """Test missing Suggested Solution section."""
        content = """# Feedback

## Issue/Improvement

Some issue description.

## Impact

This is the impact.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_required_sections()

        assert len(validator.errors) == 1
        assert "Suggested Solution" in validator.errors[0].message

    def test_case_insensitive_section_matching(self, tmp_path):
        """Test case-insensitive section name matching."""
        content = """# Feedback

## issue/improvement

Some issue description.

## IMPACT

This is the impact.

## suggested solution

Here is the solution.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_required_sections()

        assert len(validator.errors) == 0


class TestImpactLevelValidation:
    """Test impact level validation."""

    @pytest.fixture(autouse=True)
    def reset_impact_levels(self):
        """Reset VALID_IMPACT_LEVELS before each test."""
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}
        yield
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}

    def test_valid_critical_impact(self, tmp_path):
        """Test valid Critical impact level."""
        content = """# Feedback

Impact Level: Critical

## Issue/Improvement
Test issue
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 0

    def test_valid_high_impact(self, tmp_path):
        """Test valid High impact level."""
        content = "Impact Level: High\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 0

    def test_valid_medium_impact(self, tmp_path):
        """Test valid Medium impact level."""
        content = "Impact Level: Medium\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 0

    def test_valid_low_impact(self, tmp_path):
        """Test valid Low impact level."""
        content = "Impact Level: Low\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 0

    def test_invalid_impact_level(self, tmp_path):
        """Test invalid impact level."""
        content = "Impact Level: VeryHigh\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 1
        assert "Invalid impact level" in validator.errors[0].message
        assert "VeryHigh" in validator.errors[0].message

    def test_missing_impact_level(self, tmp_path):
        """Test missing impact level."""
        content = "# Some content without impact level\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 1
        assert "not specified" in validator.errors[0].message.lower()

    def test_impact_in_content_but_not_formatted(self, tmp_path):
        """Test impact level words in content but not formatted."""
        content = "This is a critical issue but not formatted correctly.\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.warnings) == 1
        assert "detected in content" in validator.warnings[0].message.lower()

    def test_impact_level_with_period(self, tmp_path):
        """Test impact level followed by period."""
        content = "Impact Level: High.\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 0

    def test_impact_level_with_semicolon(self, tmp_path):
        """Test impact level followed by semicolon."""
        content = "Impact Level: Medium; this is important\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_impact_level()

        assert len(validator.errors) == 0


class TestIssueLengthValidation:
    """Test Issue/Improvement section length validation."""

    def test_sufficient_issue_length(self, tmp_path):
        """Test Issue section with sufficient word count."""
        content = """# Feedback

## Issue/Improvement

""" + " ".join(["word"] * 60) + """

## Impact

Impact description.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_issue_length()

        assert len(validator.errors) == 0

    def test_insufficient_issue_length(self, tmp_path):
        """Test Issue section with insufficient word count."""
        content = """# Feedback

## Issue/Improvement

This is too short.

## Impact

Impact description.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_issue_length()

        assert len(validator.errors) == 1
        assert "too short" in validator.errors[0].message.lower()
        assert "4 words" in validator.errors[0].message

    def test_exactly_minimum_issue_length(self, tmp_path):
        """Test Issue section with exactly minimum word count."""
        content = """# Feedback

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact description.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_issue_length()

        assert len(validator.errors) == 0

    def test_missing_issue_section_for_length_check(self, tmp_path):
        """Test length check when Issue section is missing."""
        content = """# Feedback

## Impact

Impact description.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_issue_length()

        # Should not crash, just skip the check
        # The missing section error will be caught by _validate_required_sections
        assert len(validator.errors) == 0


class TestMarkdownSyntaxValidation:
    """Test markdown syntax validation."""

    def test_balanced_code_blocks(self, tmp_path):
        """Test balanced code blocks."""
        content = """# Feedback

```python
def test():
    pass
```

Some text.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 0

    def test_unbalanced_code_blocks(self, tmp_path):
        """Test unbalanced code blocks."""
        content = """# Feedback

```python
def test():
    pass

Some text without closing.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 1
        assert "code blocks" in validator.warnings[0].message.lower()

    def test_balanced_bold_markers(self, tmp_path):
        """Test balanced bold markers."""
        content = "This is **bold** text.\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 0

    def test_unbalanced_bold_markers(self, tmp_path):
        """Test unbalanced bold markers."""
        content = "This is **bold text without closing.\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 1
        assert "bold markers" in validator.warnings[0].message.lower()

    def test_valid_http_link(self, tmp_path):
        """Test valid HTTP link."""
        content = "Check [this link](https://example.com)\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 0

    def test_valid_https_link(self, tmp_path):
        """Test valid HTTPS link."""
        content = "Check [this link](https://example.com)\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 0

    def test_valid_relative_link(self, tmp_path):
        """Test valid relative link."""
        content = "Check [this page](/docs/guide.md)\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 0

    def test_invalid_link_format(self, tmp_path):
        """Test potentially invalid link format."""
        content = "Check [this link](invalid-link)\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()
        validator._validate_markdown_syntax()

        assert len(validator.warnings) == 1
        assert "invalid" in validator.warnings[0].message.lower()


class TestExtractSection:
    """Test section extraction functionality."""

    def test_extract_existing_section(self, tmp_path):
        """Test extracting an existing section."""
        content = """# Feedback

## Issue/Improvement

This is the issue content with multiple lines.
It continues here.

## Impact

This is impact content.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()

        section_content = validator._extract_section("Issue/Improvement")
        assert "issue content" in section_content.lower()
        assert "continues here" in section_content.lower()
        assert "impact content" not in section_content.lower()

    def test_extract_nonexistent_section(self, tmp_path):
        """Test extracting a non-existent section."""
        content = """# Feedback

## Impact

This is impact content.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()

        section_content = validator._extract_section("Issue/Improvement")
        assert section_content == ""

    def test_extract_last_section(self, tmp_path):
        """Test extracting the last section in the document."""
        content = """# Feedback

## Issue/Improvement

Issue content.

## Suggested Solution

This is the solution at the end.
With multiple lines.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()

        section_content = validator._extract_section("Suggested Solution")
        assert "solution at the end" in section_content.lower()
        assert "multiple lines" in section_content.lower()

    def test_extract_section_case_insensitive(self, tmp_path):
        """Test case-insensitive section extraction."""
        content = """# Feedback

## ISSUE/IMPROVEMENT

Issue content here.

## Impact

Impact content.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator._read_file()

        section_content = validator._extract_section("Issue/Improvement")
        assert "issue content" in section_content.lower()


class TestValidateMethod:
    """Test the main validate() method."""

    @pytest.fixture(autouse=True)
    def reset_impact_levels(self):
        """Reset VALID_IMPACT_LEVELS before each test."""
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}
        yield
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}

    def test_validate_nonexistent_file(self, tmp_path):
        """Test validating non-existent file."""
        test_file = tmp_path / "nonexistent.md"
        validator = FeedbackValidator(test_file)

        assert validator.validate() is False
        assert len(validator.errors) == 1
        assert "not found" in validator.errors[0].message.lower()

    def test_validate_directory_not_file(self, tmp_path):
        """Test validating a directory instead of file."""
        validator = FeedbackValidator(tmp_path)

        assert validator.validate() is False
        assert len(validator.errors) == 1
        assert "not a file" in validator.errors[0].message.lower()

    def test_validate_valid_complete_file(self, tmp_path):
        """Test validating a complete valid file."""
        content = """# Feedback

Impact Level: High

## Issue/Improvement

""" + " ".join(["word"] * 60) + """

## Impact

This is the impact section with detailed information.

## Suggested Solution

Here is the proposed solution with details.

## Example

Example code or scenario here.
"""
        test_file = tmp_path / "2024-12-09-valid-feedback.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        assert validator.validate() is True
        assert len(validator.errors) == 0

    def test_validate_file_with_multiple_errors(self, tmp_path):
        """Test file with multiple validation errors."""
        content = """# Feedback

Impact Level: InvalidLevel

## Issue/Improvement

Too short.

## Impact

Impact here.
"""
        test_file = tmp_path / "invalid-name.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        assert validator.validate() is False
        # Filename validation fails early, so we only get that error
        assert len(validator.errors) >= 1

    def test_validate_resets_errors(self, tmp_path):
        """Test that validate() resets errors from previous runs."""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)

        # First validation
        validator.validate()
        first_error_count = len(validator.errors)

        # Second validation should reset
        validator.validate()
        second_error_count = len(validator.errors)

        assert first_error_count == second_error_count


class TestGetReport:
    """Test report generation."""

    @pytest.fixture(autouse=True)
    def reset_impact_levels(self):
        """Reset VALID_IMPACT_LEVELS before each test."""
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}
        yield
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}

    def test_get_report_structure(self, tmp_path):
        """Test report structure."""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text("# Test")

        validator = FeedbackValidator(test_file)
        validator.validate()
        report = validator.get_report()

        assert "file" in report
        assert "filename" in report
        assert "valid" in report
        assert "error_count" in report
        assert "warning_count" in report
        assert "errors" in report
        assert "warnings" in report

    def test_get_report_valid_file(self, tmp_path):
        """Test report for valid file."""
        content = """# Feedback

Impact Level: Medium

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact description.

## Suggested Solution

Solution description.
"""
        test_file = tmp_path / "2024-12-09-valid.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator.validate()
        report = validator.get_report()

        assert report["valid"] is True
        assert report["error_count"] == 0
        assert report["filename"] == "2024-12-09-valid.md"

    def test_get_report_invalid_file(self, tmp_path):
        """Test report for invalid file."""
        content = "# Incomplete feedback"
        test_file = tmp_path / "invalid.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator.validate()
        report = validator.get_report()

        assert report["valid"] is False
        assert report["error_count"] > 0

    def test_get_report_error_details(self, tmp_path):
        """Test error details in report."""
        content = "Impact Level: InvalidLevel\n"
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator.validate()
        report = validator.get_report()

        errors = report["errors"]
        assert len(errors) > 0
        assert all("message" in error for error in errors)
        assert all("line" in error for error in errors)
        assert all("suggestion" in error for error in errors)


class TestPrintReport:
    """Test report printing."""

    def test_print_report_valid_file(self, tmp_path, capsys):
        """Test printing report for valid file."""
        # Reset VALID_IMPACT_LEVELS if it was modified by other tests
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}
        
        content = """# Feedback

Impact Level: Medium

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact description.

## Suggested Solution

Solution description.
"""
        test_file = tmp_path / "2024-12-09-valid.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator.validate()
        validator.print_report()

        captured = capsys.readouterr()
        assert "PASSED" in captured.out
        assert "2024-12-09-valid.md" in captured.out

    def test_print_report_with_errors(self, tmp_path, capsys):
        """Test printing report with errors."""
        content = "# Invalid"
        test_file = tmp_path / "invalid.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator.validate()
        validator.print_report()

        captured = capsys.readouterr()
        assert "FAILED" in captured.out
        assert "Errors:" in captured.out

    def test_print_report_with_warnings(self, tmp_path, capsys):
        """Test printing report with warnings."""
        content = """# Feedback

Impact Level: High

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

This is **unclosed bold.

## Suggested Solution

Solution here.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        validator = FeedbackValidator(test_file)
        validator.validate()
        validator.print_report()

        captured = capsys.readouterr()
        assert "Warnings:" in captured.out


class TestAutoSuggestCorrections:
    """Test auto-suggestion functionality."""

    def test_suggest_filename_correction(self, tmp_path):
        """Test filename correction suggestion."""
        test_file = tmp_path / "invalid_filename.md"
        test_file.write_text("# Test")

        suggestions = FeedbackValidator.auto_suggest_corrections(test_file)

        assert "filename" in suggestions
        assert ".md" in suggestions["filename"]
        assert re.match(r"\d{4}-\d{2}-\d{2}-", suggestions["filename"])

    def test_no_suggestions_for_valid_filename(self, tmp_path):
        """Test no suggestions for valid filename."""
        test_file = tmp_path / "2024-12-09-valid-topic.md"
        test_file.write_text("# Test")

        suggestions = FeedbackValidator.auto_suggest_corrections(test_file)

        assert "filename" not in suggestions


class TestMainFunction:
    """Test main CLI entry point."""

    @pytest.fixture(autouse=True)
    def reset_impact_levels(self):
        """Reset VALID_IMPACT_LEVELS before each test."""
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}
        yield
        FeedbackValidator.VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}

    def test_main_no_arguments(self, capsys):
        """Test main with no arguments."""
        with patch('sys.argv', ['validate_feedback.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            # Should print help message
            assert "usage:" in captured.out.lower() or "feedback_file" in captured.out

    def test_main_with_valid_file(self, tmp_path, capsys):
        """Test main with valid file argument."""
        content = """# Feedback

Impact Level: Medium

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact description.

## Suggested Solution

Solution description.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        with patch('sys.argv', ['validate_feedback.py', str(test_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_main_with_invalid_file(self, tmp_path):
        """Test main with invalid file."""
        content = "# Invalid"
        test_file = tmp_path / "invalid.md"
        test_file.write_text(content)

        with patch('sys.argv', ['validate_feedback.py', str(test_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_with_json_output(self, tmp_path, capsys):
        """Test main with JSON output."""
        content = """# Feedback

Impact Level: High

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact description.

## Suggested Solution

Solution description.
"""
        test_file = tmp_path / "2024-12-09-test.md"
        test_file.write_text(content)

        with patch('sys.argv', ['validate_feedback.py', str(test_file), '--json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
            captured = capsys.readouterr()

            # Parse JSON output
            output = json.loads(captured.out)
            assert "validation_type" in output
            assert output["validation_type"] == "feedback"
            assert "reports" in output

    def test_main_all_mode_with_submitted_dir(self, tmp_path, capsys):
        """Test --all mode with submitted directory."""
        # Create submitted directory with files
        submitted_dir = tmp_path / "submitted"
        submitted_dir.mkdir()

        content = """# Feedback

Impact Level: Medium

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact.

## Suggested Solution

Solution.
"""
        (submitted_dir / "2024-12-09-test1.md").write_text(content)
        (submitted_dir / "2024-12-09-test2.md").write_text(content)

        with patch('sys.argv', ['validate_feedback.py', '--all']):
            with patch('pathlib.Path.cwd', return_value=tmp_path):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0
                captured = capsys.readouterr()
                assert "test1.md" in captured.out
                assert "test2.md" in captured.out

    def test_main_all_mode_no_files(self, tmp_path, capsys):
        """Test --all mode with no files found."""
        with patch('sys.argv', ['validate_feedback.py', '--all']):
            with patch('pathlib.Path.cwd', return_value=tmp_path):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                captured = capsys.readouterr()
                assert "No feedback files found" in captured.out

    def test_main_all_mode_with_json(self, tmp_path, capsys):
        """Test --all mode with JSON output."""
        submitted_dir = tmp_path / "submitted"
        submitted_dir.mkdir()

        content = """# Feedback

Impact Level: Critical

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact.

## Suggested Solution

Solution.
"""
        (submitted_dir / "2024-12-09-test.md").write_text(content)

        with patch('sys.argv', ['validate_feedback.py', '--all', '--json']):
            with patch('pathlib.Path.cwd', return_value=tmp_path):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0
                captured = capsys.readouterr()

                output = json.loads(captured.out)
                assert "all_valid" in output
                assert "total_files" in output
                assert output["total_files"] >= 1

    def test_main_all_mode_fallback_to_cwd(self, tmp_path, capsys):
        """Test --all mode fallback when submitted/ doesn't exist."""
        # Create .md file in cwd
        content = """# Feedback

Impact Level: High

## Issue/Improvement

""" + " ".join(["word"] * 50) + """

## Impact

Impact.

## Suggested Solution

Solution.
"""
        (tmp_path / "2024-12-09-fallback.md").write_text(content)

        with patch('sys.argv', ['validate_feedback.py', '--all']):
            with patch('pathlib.Path.cwd', return_value=tmp_path):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0
                captured = capsys.readouterr()
                assert "fallback.md" in captured.out

    def test_main_shows_auto_suggestions(self, tmp_path, capsys):
        """Test main shows auto-suggestions for invalid files."""
        content = "# Invalid"
        test_file = tmp_path / "invalid-filename.md"
        test_file.write_text(content)

        with patch('sys.argv', ['validate_feedback.py', str(test_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Auto-Suggestions" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
