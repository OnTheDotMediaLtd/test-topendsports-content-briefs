"""
Tests for validate_csv_data_integrated.py - Coverage expansion.

This module imports from tes-shared-infrastructure which is not installed,
so we mock the import and test the actual validator logic.
"""

import csv
import json
import sys
import os
import importlib
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helper: import the module with mocked tes_shared dependency
# ---------------------------------------------------------------------------

def _import_module():
    """Import validate_csv_data_integrated with mocked tes_shared."""
    mock_tes_shared = MagicMock()
    mock_tes_shared.utils.csv_handler.CSVHandler = MagicMock

    with patch.dict(sys.modules, {
        'tes_shared': mock_tes_shared,
        'tes_shared.utils': mock_tes_shared.utils,
        'tes_shared.utils.csv_handler': mock_tes_shared.utils.csv_handler,
    }):
        module_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'scripts', 'validate_csv_data_integrated.py'
        )
        spec = importlib.util.spec_from_file_location(
            'validate_csv_data_integrated', module_path
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return mod


MOD = _import_module()
CSVValidator = MOD.CSVValidator


# ---------------------------------------------------------------------------
# Helper to write CSV files
# ---------------------------------------------------------------------------

def _write_csv(path, headers, rows):
    """Write a CSV file with given headers and rows."""
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _make_valid_row(url="/sport/betting/test", keyword="test kw", writer="Lewis", priority="High"):
    return {"URL": url, "Keyword": keyword, "Writer": writer, "Priority": priority}


# ---------------------------------------------------------------------------
# CSVValidator - init
# ---------------------------------------------------------------------------

class TestCSVValidatorInit:
    def test_init(self, tmp_path):
        f = tmp_path / "test.csv"
        f.write_text("URL,Keyword\n", encoding="utf-8")
        v = CSVValidator(f)
        assert v.csv_file == f
        assert v.errors == []
        assert v.warnings == []
        assert v.rows == []
        assert v.headers == []

    def test_class_constants(self):
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


# ---------------------------------------------------------------------------
# File handling
# ---------------------------------------------------------------------------

class TestFileHandling:
    def test_file_not_found(self, tmp_path):
        f = tmp_path / "nonexistent.csv"
        v = CSVValidator(f)
        assert v.validate() is False
        assert any("File not found" in e for e in v.errors)

    def test_not_a_file(self, tmp_path):
        d = tmp_path / "subdir"
        d.mkdir()
        v = CSVValidator(d)
        assert v.validate() is False
        assert any("Not a file" in e for e in v.errors)

    def test_empty_csv(self, tmp_path):
        f = tmp_path / "empty.csv"
        f.write_text("", encoding="utf-8")
        v = CSVValidator(f)
        assert v.validate() is False
        assert any("empty or invalid" in e for e in v.errors)

    def test_encoding_error(self, tmp_path):
        f = tmp_path / "bad_enc.csv"
        f.write_bytes(b'\xff\xfe' + b'\x00' * 20)
        v = CSVValidator(f)
        # This may raise UnicodeDecodeError or parse weirdly
        v.validate()
        # Just verify it doesn't crash - may or may not have errors

    def test_general_read_error(self, tmp_path):
        f = tmp_path / "test.csv"
        f.write_text("URL,Keyword\n", encoding="utf-8")
        v = CSVValidator(f)
        with patch("builtins.open", side_effect=IOError("disk error")):
            result = v._read_csv()
        assert result is False
        assert any("Error reading file" in e for e in v.errors)


# ---------------------------------------------------------------------------
# Header validation
# ---------------------------------------------------------------------------

class TestHeaderValidation:
    def test_all_required_headers(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        v = CSVValidator(f)
        v.validate()
        assert not any("Missing required columns" in e for e in v.errors)

    def test_missing_headers(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword"]  # missing Writer, Priority
        _write_csv(f, headers, [{"URL": "/sport/test", "Keyword": "test"}])
        v = CSVValidator(f)
        v.validate()
        assert any("Missing required columns" in e for e in v.errors)

    def test_extra_headers_ok(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority", "Notes", "Extra"]
        _write_csv(f, headers, [
            {"URL": "/sport/test", "Keyword": "kw", "Writer": "Lewis",
             "Priority": "High", "Notes": "n/a", "Extra": "x"}
        ])
        v = CSVValidator(f)
        v.validate()
        assert not any("Missing required columns" in e for e in v.errors)


# ---------------------------------------------------------------------------
# Required fields validation
# ---------------------------------------------------------------------------

class TestRequiredFields:
    def test_empty_url(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [{"URL": "", "Keyword": "kw", "Writer": "Lewis", "Priority": "High"}])
        v = CSVValidator(f)
        v.validate()
        assert any("Empty required field 'URL'" in e for e in v.errors)

    def test_empty_keyword(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [{"URL": "/sport/test", "Keyword": "", "Writer": "Tom", "Priority": "Low"}])
        v = CSVValidator(f)
        v.validate()
        assert any("Empty required field 'Keyword'" in e for e in v.errors)

    def test_whitespace_only_field(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [{"URL": "/sport/test", "Keyword": "  ", "Writer": "Lewis", "Priority": "High"}])
        v = CSVValidator(f)
        v.validate()
        assert any("Empty required field 'Keyword'" in e for e in v.errors)

    def test_all_required_fields_present(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        v = CSVValidator(f)
        v.validate()
        assert not any("Empty required field" in e for e in v.errors)


# ---------------------------------------------------------------------------
# Writer validation
# ---------------------------------------------------------------------------

class TestWriterValidation:
    def test_valid_writer_lewis(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(writer="Lewis")])
        v = CSVValidator(f)
        v.validate()
        assert not any("Invalid writer" in e for e in v.errors)

    def test_valid_writer_tom(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(writer="Tom")])
        v = CSVValidator(f)
        v.validate()
        assert not any("Invalid writer" in e for e in v.errors)

    def test_valid_writer_gustavo(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(writer="Gustavo Cantella")])
        v = CSVValidator(f)
        v.validate()
        assert not any("Invalid writer" in e for e in v.errors)

    def test_invalid_writer(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(writer="Unknown Author")])
        v = CSVValidator(f)
        v.validate()
        assert any("Invalid writer name" in e for e in v.errors)


# ---------------------------------------------------------------------------
# Priority validation
# ---------------------------------------------------------------------------

class TestPriorityValidation:
    def test_valid_priority_high(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(priority="High")])
        v = CSVValidator(f)
        v.validate()
        assert not any("Invalid priority" in e for e in v.errors)

    def test_valid_priority_medium(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(priority="Medium")])
        v = CSVValidator(f)
        v.validate()
        assert not any("Invalid priority" in e for e in v.errors)

    def test_valid_priority_low(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(priority="Low")])
        v = CSVValidator(f)
        v.validate()
        assert not any("Invalid priority" in e for e in v.errors)

    def test_invalid_priority(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(priority="Urgent")])
        v = CSVValidator(f)
        v.validate()
        assert any("Invalid priority" in e for e in v.errors)


# ---------------------------------------------------------------------------
# URL validation
# ---------------------------------------------------------------------------

class TestURLValidation:
    def test_valid_url(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(url="/sport/betting/apps")])
        v = CSVValidator(f)
        v.validate()
        assert not any("URL format invalid" in e for e in v.errors)

    def test_invalid_url_prefix(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(url="/blog/some-post")])
        v = CSVValidator(f)
        v.validate()
        assert any("URL format invalid" in e for e in v.errors)

    def test_url_with_space(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(url="/sport/best apps")])
        v = CSVValidator(f)
        v.validate()
        assert any("invalid whitespace" in e for e in v.errors)


# ---------------------------------------------------------------------------
# Duplicate URL validation
# ---------------------------------------------------------------------------

class TestDuplicateValidation:
    def test_no_duplicates(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [
            _make_valid_row(url="/sport/page1"),
            _make_valid_row(url="/sport/page2"),
        ])
        v = CSVValidator(f)
        v.validate()
        assert not any("Duplicate URL" in e for e in v.errors)

    def test_duplicate_urls(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [
            _make_valid_row(url="/sport/same-page"),
            _make_valid_row(url="/sport/same-page"),
        ])
        v = CSVValidator(f)
        v.validate()
        assert any("Duplicate URL" in e for e in v.errors)


# ---------------------------------------------------------------------------
# get_report / print_report
# ---------------------------------------------------------------------------

class TestReporting:
    def test_get_report_valid(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        v = CSVValidator(f)
        v.validate()
        report = v.get_report()
        assert report["valid"] is True
        assert report["error_count"] == 0
        assert report["rows_validated"] == 1
        assert "integration_note" in report

    def test_get_report_invalid(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(writer="BadWriter")])
        v = CSVValidator(f)
        v.validate()
        report = v.get_report()
        assert report["valid"] is False
        assert report["error_count"] > 0

    def test_print_report_passed(self, tmp_path, capsys):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        v = CSVValidator(f)
        v.validate()
        v.print_report()
        out = capsys.readouterr().out
        assert "PASSED" in out

    def test_print_report_failed(self, tmp_path, capsys):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(writer="Invalid")])
        v = CSVValidator(f)
        v.validate()
        v.print_report()
        out = capsys.readouterr().out
        assert "FAILED" in out
        assert "Errors:" in out


# ---------------------------------------------------------------------------
# main() function
# ---------------------------------------------------------------------------

class TestMain:
    def test_main_no_args(self):
        with patch("sys.argv", ["prog"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 1

    def test_main_single_file_valid(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        with patch("sys.argv", ["prog", str(f)]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 0

    def test_main_single_file_invalid(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row(writer="Nobody")])
        with patch("sys.argv", ["prog", str(f)]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 1

    def test_main_json_output(self, tmp_path, capsys):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        with patch("sys.argv", ["prog", str(f), "--json"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 0
        out = capsys.readouterr().out
        output_data = json.loads(out)
        assert output_data["validation_type"] == "csv_data"
        assert "integration_info" in output_data

    def test_main_all_flag_no_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        with patch("sys.argv", ["prog", "--all"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 1

    def test_main_all_flag_with_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        f = tmp_path / "site-structure-english.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        with patch("sys.argv", ["prog", "--all"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 0

    def test_main_all_json_output(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        f = tmp_path / "site-structure-test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [_make_valid_row()])
        with patch("sys.argv", ["prog", "--all", "--json"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 0
        out = capsys.readouterr().out
        output_data = json.loads(out)
        assert output_data["all_valid"] is True
        assert output_data["total_files"] >= 1


# ---------------------------------------------------------------------------
# Multiple rows
# ---------------------------------------------------------------------------

class TestMultipleRows:
    def test_multiple_valid_rows(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [
            _make_valid_row(url="/sport/page1", writer="Lewis"),
            _make_valid_row(url="/sport/page2", writer="Tom"),
            _make_valid_row(url="/sport/page3", writer="Gustavo Cantella", priority="Low"),
        ])
        v = CSVValidator(f)
        assert v.validate() is True
        assert len(v.errors) == 0
        assert len(v.rows) == 3

    def test_mixed_valid_and_invalid(self, tmp_path):
        f = tmp_path / "test.csv"
        headers = ["URL", "Keyword", "Writer", "Priority"]
        _write_csv(f, headers, [
            _make_valid_row(url="/sport/page1"),
            _make_valid_row(url="/sport/page2", writer="InvalidWriter"),
            _make_valid_row(url="/sport/page3", priority="SuperHigh"),
        ])
        v = CSVValidator(f)
        assert v.validate() is False
        assert any("Invalid writer" in e for e in v.errors)
        assert any("Invalid priority" in e for e in v.errors)
