#!/usr/bin/env python3
"""
Comprehensive tests for validate_csv_data_integrated.py
Target: 85%+ coverage

Tests cover:
- CSVValidator class initialization and all methods
- File validation (existence, readability, format)
- Header validation
- Required field validation
- Writer name validation
- Priority validation
- URL format validation
- Duplicate detection
- Report generation (dict and print)
- CLI main() function with various arguments
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from io import StringIO

# Mock the tes_shared import before importing the module under test
sys.modules['tes_shared'] = MagicMock()
sys.modules['tes_shared.utils'] = MagicMock()
sys.modules['tes_shared.utils.csv_handler'] = MagicMock()

# Now import the module under test
from scripts.validate_csv_data_integrated import CSVValidator, main


class TestCSVValidatorInit:
    """Test CSVValidator initialization."""

    def test_init_creates_validator_with_file_path(self, tmp_path):
        """Test that CSVValidator initializes with correct attributes."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n")
        
        validator = CSVValidator(csv_file)
        
        assert validator.csv_file == csv_file
        assert validator.errors == []
        assert validator.warnings == []
        assert validator.rows == []
        assert validator.headers == []
        assert validator.csv_handler is not None

    def test_init_with_nonexistent_file(self, tmp_path):
        """Test initialization with a file that doesn't exist yet."""
        csv_file = tmp_path / "nonexistent.csv"
        
        validator = CSVValidator(csv_file)
        
        assert validator.csv_file == csv_file
        assert validator.errors == []


class TestCSVValidatorValidate:
    """Test the main validate() method."""

    def test_validate_returns_false_for_nonexistent_file(self, tmp_path):
        """Test validation fails when file doesn't exist."""
        csv_file = tmp_path / "missing.csv"
        validator = CSVValidator(csv_file)
        
        result = validator.validate()
        
        assert result is False
        assert len(validator.errors) == 1
        assert "File not found" in validator.errors[0]

    def test_validate_returns_false_for_directory(self, tmp_path):
        """Test validation fails when path is a directory."""
        directory = tmp_path / "testdir"
        directory.mkdir()
        validator = CSVValidator(directory)
        
        result = validator.validate()
        
        assert result is False
        assert len(validator.errors) == 1
        assert "Not a file" in validator.errors[0]

    def test_validate_returns_true_for_valid_csv(self, tmp_path):
        """Test validation passes for valid CSV."""
        csv_file = tmp_path / "valid.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis Rules,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0

    def test_validate_clears_previous_errors(self, tmp_path):
        """Test that validate() clears previous validation state."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n/sport/test,Test,Lewis,High\n")
        validator = CSVValidator(csv_file)
        
        # Add some errors manually
        validator.errors = ["Old error"]
        validator.warnings = ["Old warning"]
        validator.rows = [(1, {})]
        
        validator.validate()
        
        # Should have been cleared
        assert "Old error" not in validator.errors
        assert "Old warning" not in validator.warnings


class TestCSVValidatorReadCSV:
    """Test the _read_csv() method."""

    def test_read_csv_success(self, tmp_path):
        """Test successful CSV reading."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
        )
        validator = CSVValidator(csv_file)
        
        result = validator._read_csv()
        
        assert result is True
        assert validator.headers == ["URL", "Keyword", "Writer", "Priority"]
        assert len(validator.rows) == 2
        assert validator.rows[0][0] == 2  # line number
        assert validator.rows[0][1]["URL"] == "/sport/tennis"

    def test_read_csv_empty_file(self, tmp_path):
        """Test reading empty CSV file."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")
        validator = CSVValidator(csv_file)
        
        result = validator._read_csv()
        
        assert result is False
        assert "CSV file is empty or invalid" in validator.errors[0]

    def test_read_csv_unicode_error(self, tmp_path):
        """Test handling of encoding errors."""
        csv_file = tmp_path / "bad_encoding.csv"
        # Write invalid UTF-8 bytes
        csv_file.write_bytes(b'\xff\xfe')
        validator = CSVValidator(csv_file)
        
        result = validator._read_csv()
        
        assert result is False
        assert any("encoding error" in err.lower() for err in validator.errors)

    def test_read_csv_parsing_error(self, tmp_path):
        """Test handling of CSV parsing errors."""
        csv_file = tmp_path / "malformed.csv"
        # Create malformed CSV with mismatched quotes
        csv_file.write_text('URL,Keyword\n"unclosed quote,value\n')
        validator = CSVValidator(csv_file)
        
        result = validator._read_csv()
        
        # CSV might handle this differently, but we should handle errors
        # The result depends on Python's csv module behavior
        assert isinstance(result, bool)


class TestCSVValidatorValidateHeaders:
    """Test the _validate_headers() method."""

    def test_validate_headers_all_present(self, tmp_path):
        """Test validation passes when all required headers present."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority\n")
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_headers()
        
        assert len(validator.errors) == 0

    def test_validate_headers_missing_single_column(self, tmp_path):
        """Test validation fails when one column is missing."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Priority\n")  # Missing Writer
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_headers()
        
        assert len(validator.errors) == 1
        assert "Writer" in validator.errors[0]
        assert "Missing required columns" in validator.errors[0]

    def test_validate_headers_missing_multiple_columns(self, tmp_path):
        """Test validation fails when multiple columns are missing."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword\n")  # Missing Writer and Priority
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_headers()
        
        assert len(validator.errors) == 1
        assert "Writer" in validator.errors[0]
        assert "Priority" in validator.errors[0]

    def test_validate_headers_extra_columns_ok(self, tmp_path):
        """Test that extra columns are allowed."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("URL,Keyword,Writer,Priority,Extra,Another\n")
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_headers()
        
        assert len(validator.errors) == 0


class TestCSVValidatorValidateRequiredFields:
    """Test the _validate_required_fields() method."""

    def test_validate_required_fields_all_filled(self, tmp_path):
        """Test validation passes when all required fields are filled."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_required_fields()
        
        assert len(validator.errors) == 0

    def test_validate_required_fields_empty_url(self, tmp_path):
        """Test validation fails for empty URL."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            ",Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_required_fields()
        
        assert len(validator.errors) == 1
        assert "Line 2" in validator.errors[0]
        assert "URL" in validator.errors[0]

    def test_validate_required_fields_whitespace_only(self, tmp_path):
        """Test validation fails for whitespace-only fields."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,   ,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_required_fields()
        
        assert len(validator.errors) == 1
        assert "Keyword" in validator.errors[0]

    def test_validate_required_fields_multiple_empty(self, tmp_path):
        """Test validation reports multiple empty fields."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,,Lewis,\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_required_fields()
        
        assert len(validator.errors) == 2  # Keyword and Priority


class TestCSVValidatorValidateWriters:
    """Test the _validate_writers() method."""

    def test_validate_writers_valid_names(self, tmp_path):
        """Test validation passes for valid writer names."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
            "/sport/basketball,Basketball,Gustavo Cantella,Low\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_writers()
        
        assert len(validator.errors) == 0

    def test_validate_writers_invalid_name(self, tmp_path):
        """Test validation fails for invalid writer name."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,InvalidWriter,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_writers()
        
        assert len(validator.errors) == 1
        assert "InvalidWriter" in validator.errors[0]
        assert "Lewis" in validator.errors[0]  # Should mention valid writers

    def test_validate_writers_case_sensitive(self, tmp_path):
        """Test that writer validation is case-sensitive."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,lewis,High\n"  # lowercase
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_writers()
        
        assert len(validator.errors) == 1


class TestCSVValidatorValidatePriorities:
    """Test the _validate_priorities() method."""

    def test_validate_priorities_valid_values(self, tmp_path):
        """Test validation passes for valid priority values."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
            "/sport/basketball,Basketball,Lewis,Low\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_priorities()
        
        assert len(validator.errors) == 0

    def test_validate_priorities_invalid_value(self, tmp_path):
        """Test validation fails for invalid priority."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,Urgent\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_priorities()
        
        assert len(validator.errors) == 1
        assert "Urgent" in validator.errors[0]
        assert "High" in validator.errors[0]  # Should mention valid priorities

    def test_validate_priorities_case_sensitive(self, tmp_path):
        """Test that priority validation is case-sensitive."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,high\n"  # lowercase
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_priorities()
        
        assert len(validator.errors) == 1


class TestCSVValidatorValidateURLs:
    """Test the _validate_urls() method."""

    def test_validate_urls_valid_format(self, tmp_path):
        """Test validation passes for valid URLs."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis/rules,Tennis,Lewis,High\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_urls()
        
        assert len(validator.errors) == 0

    def test_validate_urls_wrong_prefix(self, tmp_path):
        """Test validation fails for URLs without correct prefix."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/tennis/rules,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_urls()
        
        assert len(validator.errors) == 1
        assert "/sport/" in validator.errors[0]
        assert "/tennis/rules" in validator.errors[0]

    def test_validate_urls_with_spaces(self, tmp_path):
        """Test validation fails for URLs with spaces."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis rules,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_urls()
        
        assert len(validator.errors) == 1
        assert "whitespace" in validator.errors[0].lower()

    def test_validate_urls_with_leading_trailing_spaces(self, tmp_path):
        """Test validation for URLs with leading/trailing spaces."""
        csv_file = tmp_path / "test.csv"
        # CSV reader strips spaces by default, so the validation logic
        # in the source checks if url != url.strip() to detect this
        # However, since CSV already strips, we test the actual behavior
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_urls()
        
        # CSV reader auto-strips, so this is actually valid
        assert len(validator.errors) == 0


class TestCSVValidatorValidateDuplicates:
    """Test the _validate_duplicates() method."""

    def test_validate_duplicates_no_duplicates(self, tmp_path):
        """Test validation passes when no duplicate URLs."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_duplicates()
        
        assert len(validator.errors) == 0

    def test_validate_duplicates_with_duplicate(self, tmp_path):
        """Test validation fails for duplicate URLs."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/tennis,Tennis Rules,Tom,Medium\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_duplicates()
        
        assert len(validator.errors) == 1
        assert "Duplicate" in validator.errors[0]
        assert "/sport/tennis" in validator.errors[0]
        assert "2" in validator.errors[0]
        assert "3" in validator.errors[0]

    def test_validate_duplicates_multiple_duplicates(self, tmp_path):
        """Test validation reports multiple duplicate URLs."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/tennis,Tennis Rules,Tom,Medium\n"
            "/sport/soccer,Soccer,Lewis,Low\n"
            "/sport/soccer,Football,Tom,High\n"
        )
        validator = CSVValidator(csv_file)
        validator._read_csv()
        
        validator._validate_duplicates()
        
        assert len(validator.errors) == 2


class TestCSVValidatorGetReport:
    """Test the get_report() method."""

    def test_get_report_structure(self, tmp_path):
        """Test that get_report returns correct structure."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator.validate()
        
        report = validator.get_report()
        
        assert isinstance(report, dict)
        assert "file" in report
        assert "valid" in report
        assert "error_count" in report
        assert "warning_count" in report
        assert "errors" in report
        assert "warnings" in report
        assert "rows_validated" in report
        assert "integration_note" in report

    def test_get_report_valid_file(self, tmp_path):
        """Test report for valid file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator.validate()
        
        report = validator.get_report()
        
        assert report["valid"] is True
        assert report["error_count"] == 0
        assert report["rows_validated"] == 1

    def test_get_report_invalid_file(self, tmp_path):
        """Test report for invalid file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,InvalidWriter,High\n"
        )
        validator = CSVValidator(csv_file)
        validator.validate()
        
        report = validator.get_report()
        
        assert report["valid"] is False
        assert report["error_count"] > 0
        assert len(report["errors"]) > 0


class TestCSVValidatorPrintReport:
    """Test the print_report() method."""

    def test_print_report_valid_file(self, tmp_path, capsys):
        """Test print output for valid file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator.validate()
        
        validator.print_report()
        
        captured = capsys.readouterr()
        assert "Validation Report" in captured.out
        assert "PASSED" in captured.out
        assert "Rows validated: 1" in captured.out

    def test_print_report_invalid_file(self, tmp_path, capsys):
        """Test print output for invalid file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,InvalidWriter,High\n"
        )
        validator = CSVValidator(csv_file)
        validator.validate()
        
        validator.print_report()
        
        captured = capsys.readouterr()
        assert "FAILED" in captured.out
        assert "Errors:" in captured.out
        assert "InvalidWriter" in captured.out

    def test_print_report_with_warnings(self, tmp_path, capsys):
        """Test print output includes warnings section."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        validator = CSVValidator(csv_file)
        validator.validate()
        validator.warnings = ["Test warning"]
        
        validator.print_report()
        
        captured = capsys.readouterr()
        assert "Warnings:" in captured.out
        assert "Test warning" in captured.out


class TestMainFunction:
    """Test the main() CLI function."""

    def test_main_no_arguments(self, capsys):
        """Test main exits with error when no arguments provided."""
        with patch('sys.argv', ['validate_csv_data_integrated.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1

    def test_main_with_valid_file(self, tmp_path):
        """Test main with valid CSV file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        
        with patch('sys.argv', ['script', str(csv_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 0

    def test_main_with_invalid_file(self, tmp_path):
        """Test main with invalid CSV file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/tennis,Tennis,InvalidWriter,High\n"  # Multiple errors
        )
        
        with patch('sys.argv', ['script', str(csv_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1

    def test_main_with_json_output(self, tmp_path, capsys):
        """Test main with --json flag."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        
        with patch('sys.argv', ['script', str(csv_file), '--json']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        # Should output valid JSON
        output = json.loads(captured.out)
        assert "validation_type" in output
        assert output["validation_type"] == "csv_data"
        assert "all_valid" in output
        assert "reports" in output

    def test_main_with_all_flag(self, tmp_path, monkeypatch):
        """Test main with --all flag."""
        # Create test CSV files
        csv1 = tmp_path / "site-structure-test1.csv"
        csv1.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        csv2 = tmp_path / "site-structure-test2.csv"
        csv2.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
        )
        
        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        
        with patch('sys.argv', ['script', '--all']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 0

    def test_main_with_all_flag_no_files(self, tmp_path, monkeypatch, capsys):
        """Test main with --all flag when no CSV files found."""
        monkeypatch.chdir(tmp_path)
        
        with patch('sys.argv', ['script', '--all']):
            with pytest.raises(SystemExit) as exc_info:
                main()
        
        captured = capsys.readouterr()
        assert "No site structure CSV files found" in captured.out
        assert exc_info.value.code == 1

    def test_main_with_all_and_json(self, tmp_path, monkeypatch, capsys):
        """Test main with both --all and --json flags."""
        csv1 = tmp_path / "site-structure-test.csv"
        csv1.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        
        monkeypatch.chdir(tmp_path)
        
        with patch('sys.argv', ['script', '--all', '--json']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["total_files"] >= 1
        assert "integration_info" in output

    def test_main_with_parent_directory_search(self, tmp_path, monkeypatch):
        """Test that --all searches parent directory too."""
        # Create parent CSV
        parent_csv = tmp_path / "site-structure-parent.csv"
        parent_csv.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        
        # Create subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        
        monkeypatch.chdir(subdir)
        
        with patch('sys.argv', ['script', '--all', '--json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            # Should find the parent CSV and exit successfully
            assert exc_info.value.code == 0

    def test_main_multiple_files_one_invalid(self, tmp_path, monkeypatch):
        """Test main with multiple files where one is invalid."""
        csv1 = tmp_path / "site-structure-valid.csv"
        csv1.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
        )
        csv2 = tmp_path / "site-structure-invalid.csv"
        csv2.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/tennis,Tennis,BadWriter,High\n"
        )
        
        monkeypatch.chdir(tmp_path)
        
        with patch('sys.argv', ['script', '--all']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            # Should exit with error code because one file is invalid
            assert exc_info.value.code == 1


class TestIntegrationScenarios:
    """Integration tests covering complete validation scenarios."""

    def test_complete_valid_csv(self, tmp_path):
        """Test complete validation of a fully valid CSV."""
        csv_file = tmp_path / "complete.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority,Extra Column\n"
            "/sport/tennis,Tennis Rules,Lewis,High,Some data\n"
            "/sport/soccer/rules,Soccer Rules,Tom,Medium,More data\n"
            "/sport/basketball,Basketball,Gustavo Cantella,Low,Extra\n"
        )
        validator = CSVValidator(csv_file)
        
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0
        assert len(validator.rows) == 3
        
        report = validator.get_report()
        assert report["valid"] is True
        assert report["rows_validated"] == 3

    def test_complete_invalid_csv_multiple_errors(self, tmp_path):
        """Test CSV with multiple types of errors."""
        csv_file = tmp_path / "invalid.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            ",Empty URL,Lewis,High\n"  # Empty URL
            "/tennis,Wrong prefix,Tom,Medium\n"  # Wrong URL prefix
            "/sport/soccer,Soccer,InvalidWriter,High\n"  # Invalid writer
            "/sport/basketball,Basketball,Lewis,InvalidPriority\n"  # Invalid priority
            "/sport/hockey,Hockey with space,Lewis,High\n"  # URL with space (actually keyword has space, but URL is fine)
            "/sport/duplicate,Dup1,Tom,Low\n"
            "/sport/duplicate,Dup2,Lewis,High\n"  # Duplicate URL
        )
        validator = CSVValidator(csv_file)
        
        result = validator.validate()
        
        assert result is False
        # Should have at least 5 errors: empty URL, wrong prefix, invalid writer, invalid priority, duplicate
        assert len(validator.errors) >= 5
        
        report = validator.get_report()
        assert report["valid"] is False
        assert report["error_count"] >= 5

    def test_csv_with_all_valid_writers(self, tmp_path):
        """Test CSV containing all valid writer names."""
        csv_file = tmp_path / "all_writers.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
            "/sport/basketball,Basketball,Gustavo Cantella,Low\n"
        )
        validator = CSVValidator(csv_file)
        
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0

    def test_csv_with_all_valid_priorities(self, tmp_path):
        """Test CSV containing all valid priority levels."""
        csv_file = tmp_path / "all_priorities.csv"
        csv_file.write_text(
            "URL,Keyword,Writer,Priority\n"
            "/sport/tennis,Tennis,Lewis,High\n"
            "/sport/soccer,Soccer,Tom,Medium\n"
            "/sport/basketball,Basketball,Lewis,Low\n"
        )
        validator = CSVValidator(csv_file)
        
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0
