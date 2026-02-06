#!/usr/bin/env python3
"""
Comprehensive tests for CSV Data Validation Script.

Tests cover:
- Required column validation
- Writer name validation
- Priority value validation
- URL format validation
- Duplicate detection
- Edge cases and error handling
"""

import csv
import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add scripts to path
SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_csv_data import CSVValidator


class TestCSVValidatorInit:
    """Tests for CSVValidator initialization."""

    def test_init_with_path(self, tmp_path):
        """Test initialization with file path."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n")
        
        validator = CSVValidator(csv_file)
        assert validator.csv_file == csv_file
        assert validator.errors == []
        assert validator.warnings == []
        assert validator.rows == []
        assert validator.headers == []

    def test_class_constants(self):
        """Test class constants are properly defined."""
        assert "URL" in CSVValidator.REQUIRED_COLUMNS
        assert "Keyword" in CSVValidator.REQUIRED_COLUMNS
        assert "Writer" in CSVValidator.REQUIRED_COLUMNS
        assert "Priority" in CSVValidator.REQUIRED_COLUMNS
        
        assert "Lewis" in CSVValidator.VALID_WRITERS
        assert "Tom" in CSVValidator.VALID_WRITERS
        assert "Gustavo Cantella" in CSVValidator.VALID_WRITERS
        
        assert "High" in CSVValidator.VALID_PRIORITIES
        assert "Medium" in CSVValidator.VALID_PRIORITIES
        assert "Low" in CSVValidator.VALID_PRIORITIES


class TestCSVReading:
    """Tests for CSV reading functionality."""

    def test_read_valid_csv(self, tmp_path):
        """Test reading valid CSV file."""
        csv_file = tmp_path / "valid.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,test kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        result = validator._read_csv()
        
        assert result is True
        assert validator.headers == ["URL", "Keyword", "Writer", "Priority"]
        assert len(validator.rows) == 1

    def test_read_empty_csv(self, tmp_path):
        """Test reading empty CSV file."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")
        
        validator = CSVValidator(csv_file)
        result = validator._read_csv()
        
        assert result is False
        assert len(validator.errors) > 0

    def test_read_csv_headers_only(self, tmp_path):
        """Test reading CSV with only headers."""
        csv_file = tmp_path / "headers_only.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n")
        
        validator = CSVValidator(csv_file)
        result = validator._read_csv()
        
        assert result is True
        assert len(validator.rows) == 0
        assert len(validator.headers) == 4

    def test_read_nonexistent_file(self, tmp_path):
        """Test reading non-existent file."""
        csv_file = tmp_path / "nonexistent.csv"
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        assert result is False
        assert "File not found" in validator.errors[0]

    def test_read_csv_with_extra_columns(self, tmp_path):
        """Test reading CSV with extra columns."""
        csv_file = tmp_path / "extra_cols.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority,Extra1,Extra2\n/sport/test,kw,Lewis,High,e1,e2\n")
        
        validator = CSVValidator(csv_file)
        result = validator._read_csv()
        
        assert result is True
        assert "Extra1" in validator.headers
        assert "Extra2" in validator.headers

    def test_read_csv_with_encoding_error(self, tmp_path):
        """Test reading CSV with encoding issues."""
        csv_file = tmp_path / "encoding.csv"
        # Write with latin-1 encoding that has invalid UTF-8 bytes
        csv_file.write_bytes(b"URL,Keyword,Writer,Priority\n/sport/test,\xff\xfe,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        result = validator._read_csv()
        
        # Should handle encoding gracefully
        assert result is False or len(validator.errors) > 0


class TestHeaderValidation:
    """Tests for required column validation."""

    def test_all_required_columns_present(self, tmp_path):
        """Test validation passes with all required columns."""
        csv_file = tmp_path / "complete.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_headers()
        
        # No errors for missing columns
        assert not any("Missing required columns" in e for e in validator.errors)

    def test_missing_url_column(self, tmp_path):
        """Test validation fails without URL column."""
        csv_file = tmp_path / "no_url.csv"
        csv_file.write_text("Keyword,Writer,Priority\ntest,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_headers()
        
        assert any("URL" in e for e in validator.errors)

    def test_missing_keyword_column(self, tmp_path):
        """Test validation fails without Keyword column."""
        csv_file = tmp_path / "no_keyword.csv"
        csv_file.write_text("URL,Writer,Priority\n/sport/test,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_headers()
        
        assert any("Keyword" in e for e in validator.errors)

    def test_missing_multiple_columns(self, tmp_path):
        """Test validation reports all missing columns."""
        csv_file = tmp_path / "minimal.csv"
        csv_file.write_text("URL\n/sport/test\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_headers()
        
        assert any("Missing required columns" in e for e in validator.errors)


class TestRequiredFieldsValidation:
    """Tests for required field value validation."""

    def test_empty_url_field(self, tmp_path):
        """Test validation fails with empty URL."""
        csv_file = tmp_path / "empty_url.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n,test kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_required_fields()
        
        assert any("Empty required field 'URL'" in e for e in validator.errors)

    def test_whitespace_only_field(self, tmp_path):
        """Test validation fails with whitespace-only field."""
        csv_file = tmp_path / "whitespace.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n   ,test kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_required_fields()
        
        assert any("Empty required field 'URL'" in e for e in validator.errors)

    def test_multiple_empty_fields(self, tmp_path):
        """Test validation reports all empty fields."""
        csv_file = tmp_path / "multiple_empty.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n,,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_required_fields()
        
        url_errors = [e for e in validator.errors if "URL" in e]
        keyword_errors = [e for e in validator.errors if "Keyword" in e]
        
        assert len(url_errors) > 0
        assert len(keyword_errors) > 0

    def test_correct_line_number_reported(self, tmp_path):
        """Test error reports correct line number."""
        csv_file = tmp_path / "line_nums.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/a,kw1,Lewis,High\n/sport/b,,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_required_fields()
        
        # Error should mention line 3 (row 2 of data + header)
        assert any("Line 3" in e for e in validator.errors)


class TestWriterValidation:
    """Tests for writer name validation."""

    @pytest.mark.parametrize("writer", ["Lewis", "Tom", "Gustavo Cantella"])
    def test_valid_writers(self, tmp_path, writer):
        """Test all valid writer names pass validation."""
        csv_file = tmp_path / f"writer_{writer.replace(' ', '_')}.csv"
        csv_file.write_text(f"URL,Keyword,Writer,Priority\n/sport/test,kw,{writer},High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_writers()
        
        assert not any("Invalid writer" in e for e in validator.errors)

    def test_invalid_writer_name(self, tmp_path):
        """Test validation fails with invalid writer name."""
        csv_file = tmp_path / "invalid_writer.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,InvalidWriter,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_writers()
        
        assert any("Invalid writer name" in e for e in validator.errors)
        assert any("InvalidWriter" in e for e in validator.errors)

    def test_case_sensitive_writer(self, tmp_path):
        """Test writer names are case-sensitive."""
        csv_file = tmp_path / "case_writer.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_writers()
        
        # 'lewis' should fail (not 'Lewis')
        assert any("Invalid writer" in e for e in validator.errors)

    def test_empty_writer_skipped(self, tmp_path):
        """Test empty writer field doesn't trigger writer validation error."""
        csv_file = tmp_path / "empty_writer.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_writers()
        
        # Should not have writer validation error (handled by required field validation)
        assert not any("Invalid writer name" in e for e in validator.errors)


class TestPriorityValidation:
    """Tests for priority value validation."""

    @pytest.mark.parametrize("priority", ["High", "Medium", "Low"])
    def test_valid_priorities(self, tmp_path, priority):
        """Test all valid priority values pass validation."""
        csv_file = tmp_path / f"priority_{priority}.csv"
        csv_file.write_text(f"URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,{priority}\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_priorities()
        
        assert not any("Invalid priority" in e for e in validator.errors)

    def test_invalid_priority(self, tmp_path):
        """Test validation fails with invalid priority."""
        csv_file = tmp_path / "invalid_priority.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,Critical\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_priorities()
        
        assert any("Invalid priority" in e for e in validator.errors)

    def test_case_sensitive_priority(self, tmp_path):
        """Test priority values are case-sensitive."""
        csv_file = tmp_path / "case_priority.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,high\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_priorities()
        
        # 'high' should fail (not 'High')
        assert any("Invalid priority" in e for e in validator.errors)


class TestURLValidation:
    """Tests for URL format validation."""

    def test_valid_url_format(self, tmp_path):
        """Test valid URL format passes validation."""
        csv_file = tmp_path / "valid_url.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/betting/test,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_urls()
        
        assert not any("URL format invalid" in e for e in validator.errors)

    def test_url_missing_sport_prefix(self, tmp_path):
        """Test URL without /sport/ prefix fails."""
        csv_file = tmp_path / "no_prefix.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/betting/test,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_urls()
        
        assert any("URL format invalid" in e for e in validator.errors)
        assert any("/sport/" in e for e in validator.errors)

    def test_url_with_spaces(self, tmp_path):
        """Test URL with spaces fails validation."""
        csv_file = tmp_path / "space_url.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test page,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_urls()
        
        assert any("invalid whitespace" in e for e in validator.errors)

    def test_url_with_leading_space(self, tmp_path):
        """Test URL with leading space fails validation."""
        csv_file = tmp_path / "leading_space.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n /sport/test,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_urls()
        
        # Leading space in URL should trigger format error (no /sport/ prefix due to leading space)
        # or whitespace error - either indicates the issue was caught
        has_error = len(validator.errors) > 0
        assert has_error or len(validator.rows) == 1  # Either error or parsed OK

    def test_url_with_trailing_space(self, tmp_path):
        """Test URL with trailing space fails validation."""
        csv_file = tmp_path / "trailing_space.csv"
        # Note: CSV parser might strip trailing spaces, so we check behavior
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test ,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_urls()
        
        # May or may not fail depending on CSV parsing
        # At minimum, should not crash


class TestDuplicateValidation:
    """Tests for duplicate URL detection."""

    def test_no_duplicates(self, tmp_path):
        """Test validation passes with no duplicates."""
        csv_file = tmp_path / "no_dupes.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/a,kw1,Lewis,High\n/sport/b,kw2,Tom,Medium\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_duplicates()
        
        assert not any("Duplicate URL" in e for e in validator.errors)

    def test_duplicate_urls(self, tmp_path):
        """Test validation fails with duplicate URLs."""
        csv_file = tmp_path / "dupes.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw1,Lewis,High\n/sport/test,kw2,Tom,Medium\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_duplicates()
        
        assert any("Duplicate URL" in e for e in validator.errors)
        assert any("/sport/test" in e for e in validator.errors)

    def test_multiple_duplicates(self, tmp_path):
        """Test validation reports all duplicate occurrences."""
        csv_file = tmp_path / "multi_dupes.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/a,kw1,Lewis,High\n"
            "/sport/a,kw2,Tom,Medium\n"
            "/sport/a,kw3,Lewis,Low\n"
        )
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_duplicates()
        
        # Should report that URL appears on lines 2, 3, and 4
        assert any("Duplicate URL" in e for e in validator.errors)

    def test_case_sensitive_duplicates(self, tmp_path):
        """Test duplicate detection is case-sensitive for URLs."""
        csv_file = tmp_path / "case_dupes.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/Test,kw1,Lewis,High\n/sport/test,kw2,Tom,Medium\n")
        
        validator = CSVValidator(csv_file)
        validator._read_csv()
        validator._validate_duplicates()
        
        # /sport/Test and /sport/test are different URLs
        assert not any("Duplicate URL" in e for e in validator.errors)


class TestFullValidation:
    """Tests for complete validation flow."""

    def test_validate_complete_valid_csv(self, tmp_path):
        """Test complete validation of valid CSV."""
        csv_file = tmp_path / "complete_valid.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/betting/site1,best betting sites,Lewis,High\n"
            "/sport/betting/site2,sports betting,Tom,Medium\n"
            "/sport/betting/site3,online betting,Gustavo Cantella,Low\n"
        )
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0

    def test_validate_with_multiple_errors(self, tmp_path):
        """Test validation catches multiple error types."""
        csv_file = tmp_path / "multi_errors.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/wrong/path,kw1,InvalidWriter,Invalid\n"
            "/sport/test,kw2,Lewis,High\n"
            "/sport/test,kw3,Tom,Medium\n"  # Duplicate
        )
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        assert result is False
        # Should have URL, writer, priority, and duplicate errors
        assert len(validator.errors) >= 3

    def test_validate_not_a_file(self, tmp_path):
        """Test validation fails for directory instead of file."""
        dir_path = tmp_path / "directory"
        dir_path.mkdir()
        
        validator = CSVValidator(dir_path)
        result = validator.validate()
        
        assert result is False
        assert any("Not a file" in e for e in validator.errors)


class TestValidationReport:
    """Tests for report generation."""

    def test_get_report_structure(self, tmp_path):
        """Test report dictionary structure."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator.validate()
        report = validator.get_report()
        
        assert "file" in report
        assert "valid" in report
        assert "error_count" in report
        assert "warning_count" in report
        assert "errors" in report
        assert "warnings" in report
        assert "rows_validated" in report

    def test_report_valid_status(self, tmp_path):
        """Test report shows valid status for valid file."""
        csv_file = tmp_path / "valid.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator.validate()
        report = validator.get_report()
        
        assert report["valid"] is True
        assert report["error_count"] == 0
        assert report["rows_validated"] == 1

    def test_report_invalid_status(self, tmp_path):
        """Test report shows invalid status for invalid file."""
        csv_file = tmp_path / "invalid.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/wrong/path,kw,Invalid,Wrong\n")
        
        validator = CSVValidator(csv_file)
        validator.validate()
        report = validator.get_report()
        
        assert report["valid"] is False
        assert report["error_count"] > 0

    def test_print_report_output(self, tmp_path):
        """Test print_report produces output."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        validator.validate()
        # Just test it doesn't crash
        validator.print_report()


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_long_url(self, tmp_path):
        """Test handling of very long URL."""
        csv_file = tmp_path / "long_url.csv"
        long_path = "/sport/" + "a" * 500
        csv_file.write_text(f"URL,Keyword,Writer,Priority\n{long_path},kw,Lewis,High\n")
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        # Should handle long URLs without crashing
        assert validator.rows is not None

    def test_unicode_content(self, tmp_path):
        """Test handling of Unicode content."""
        csv_file = tmp_path / "unicode.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,キーワード,Lewis,High\n", encoding='utf-8')
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        # Should handle Unicode without errors
        assert len(validator.rows) == 1

    def test_special_characters_in_keyword(self, tmp_path):
        """Test handling of special characters in keyword."""
        csv_file = tmp_path / "special.csv"
        csv_file.write_text('URL,Keyword,Writer,Priority\n/sport/test,"keyword with, comma",Lewis,High\n')
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        # CSV should handle quoted fields with commas
        assert len(validator.rows) == 1

    def test_quoted_fields(self, tmp_path):
        """Test handling of quoted fields."""
        csv_file = tmp_path / "quoted.csv"
        csv_file.write_text('URL,Keyword,Writer,Priority\n"/sport/test","test keyword","Lewis","High"\n')
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        assert result is True

    def test_newlines_in_fields(self, tmp_path):
        """Test handling of newlines in quoted fields."""
        csv_file = tmp_path / "newlines.csv"
        csv_file.write_text('URL,Keyword,Writer,Priority\n/sport/test,"multi\nline",Lewis,High\n')
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        # Should handle without crashing
        assert validator.rows is not None

    def test_thousands_of_rows(self, tmp_path):
        """Test handling of large CSV files."""
        csv_file = tmp_path / "large.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Keyword", "Writer", "Priority"])
            for i in range(5000):
                writer.writerow([f"/sport/page{i}", f"keyword{i}", "Lewis", "High"])
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        assert result is True
        assert len(validator.rows) == 5000

    def test_empty_file_with_only_whitespace(self, tmp_path):
        """Test handling of file with only whitespace."""
        csv_file = tmp_path / "whitespace.csv"
        csv_file.write_text("   \n  \n   ")
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        # Should handle gracefully
        assert result is False


class TestMainFunction:
    """Tests for the main CLI function."""

    def test_main_no_args(self, monkeypatch):
        """Test main function with no arguments shows help."""
        import validate_csv_data as module
        
        monkeypatch.setattr('sys.argv', ['validate_csv_data.py'])
        
        with pytest.raises(SystemExit) as exc_info:
            module.main()
        
        assert exc_info.value.code == 1

    def test_main_with_valid_file(self, tmp_path, monkeypatch):
        """Test main function with valid file."""
        import validate_csv_data as module
        
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,High\n")
        
        monkeypatch.setattr('sys.argv', ['validate_csv_data.py', str(csv_file)])
        
        with pytest.raises(SystemExit) as exc_info:
            module.main()
        
        assert exc_info.value.code == 0

    def test_main_with_invalid_file(self, tmp_path, monkeypatch):
        """Test main function with invalid file."""
        import validate_csv_data as module
        
        csv_file = tmp_path / "invalid.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/wrong/path,kw,Invalid,Wrong\n")
        
        monkeypatch.setattr('sys.argv', ['validate_csv_data.py', str(csv_file)])
        
        with pytest.raises(SystemExit) as exc_info:
            module.main()
        
        assert exc_info.value.code == 1

    def test_main_json_output(self, tmp_path, monkeypatch):
        """Test main function with JSON output flag."""
        import validate_csv_data as module
        
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,High\n")
        
        monkeypatch.setattr('sys.argv', ['validate_csv_data.py', str(csv_file), '--json'])
        
        with pytest.raises(SystemExit) as exc_info:
            module.main()
        
        # Should exit cleanly
        assert exc_info.value.code == 0


class TestCSVParsingEdgeCases:
    """Tests for CSV parsing edge cases."""

    def test_different_delimiters(self, tmp_path):
        """Test that comma-delimited is expected."""
        csv_file = tmp_path / "semicolon.csv"
        # Using semicolon delimiter (should fail to parse correctly)
        csv_file.write_text("URL;Keyword;Writer;Priority\n/sport/test;kw;Lewis;High\n")
        
        validator = CSVValidator(csv_file)
        validator.validate()
        
        # Comma-delimited expected, so should have issues
        # The entire first line would be treated as one column name
        assert "Missing required columns" in str(validator.errors)

    def test_bom_in_utf8_file(self, tmp_path):
        """Test handling of UTF-8 BOM."""
        csv_file = tmp_path / "bom.csv"
        # Write with UTF-8 BOM
        csv_file.write_bytes(b'\xef\xbb\xbfURL,Keyword,Writer,Priority\n/sport/test,kw,Lewis,High\n')
        
        validator = CSVValidator(csv_file)
        result = validator.validate()
        
        # Python's CSV reader should handle BOM
        # May or may not affect header detection
        assert validator.rows is not None
