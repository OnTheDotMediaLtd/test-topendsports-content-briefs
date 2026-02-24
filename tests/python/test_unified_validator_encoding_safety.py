"""
Tests for unified_content_validator.py encoding safety and print_report coverage.

Validates that print_report uses ASCII-safe output (no emoji that crash cp1252),
and covers remaining untested branches in print_report and main().
"""

import pytest
import sys
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))


class TestPrintReportEncodingSafety:
    """Verify print_report output is ASCII-safe (no emoji)."""

    def test_passed_status_uses_ascii(self, capsys):
        """print_report should use [PASS] not emoji checkmark."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(is_valid=True)
        result.print_report()
        captured = capsys.readouterr()
        assert "[PASS] PASSED" in captured.out
        # Must NOT contain emoji
        assert "\u2705" not in captured.out  # checkmark emoji
        assert "\u274c" not in captured.out  # cross emoji

    def test_failed_status_uses_ascii(self, capsys):
        """print_report should use [FAIL] not emoji cross."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(is_valid=False)
        result.print_report()
        captured = capsys.readouterr()
        assert "[FAIL] FAILED" in captured.out
        assert "\u2705" not in captured.out
        assert "\u274c" not in captured.out

    def test_validator_section_pass_uses_ascii(self, capsys):
        """_print_validator_section should use [PASS] not emoji."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI Pattern Detection",
            passed=True,
            score=95.0,
            grade="A",
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "[PASS] AI Pattern Detection" in captured.out
        assert "\u2705" not in captured.out

    def test_validator_section_fail_uses_ascii(self, capsys):
        """_print_validator_section should use [FAIL] not emoji."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=False)
        result.brand_validation = ValidationSummary(
            validator_name="Brand Validation",
            passed=False,
            errors=["Unknown brand: FakeBet"],
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "[FAIL] Brand Validation" in captured.out
        assert "\u274c" not in captured.out

    def test_general_errors_uses_ascii(self, capsys):
        """General errors section should use [WARN] not emoji."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(
            is_valid=False,
            errors=["File not found: test.html"],
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "[WARN] GENERAL ERRORS:" in captured.out
        # Must not contain warning emoji
        assert "\u26a0" not in captured.out

    def test_output_encodable_as_cp1252(self, capsys):
        """Entire print_report output must be encodable as cp1252 (Windows default)."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(
            is_valid=False,
            content_file="test.html",
            errors=["General error"],
        )
        result.ai_patterns = ValidationSummary(
            validator_name="AI", passed=True, score=90.0, grade="A",
            warnings=["Minor pattern found"],
        )
        result.brand_validation = ValidationSummary(
            validator_name="Brand", passed=False,
            errors=["Unknown brand: TestBrand"],
        )
        result.eeat_validation = ValidationSummary(
            validator_name="EEAT", passed=True, score=75.0, grade="C",
        )
        result.print_report(verbose=True)
        captured = capsys.readouterr()
        # This should NOT raise UnicodeEncodeError
        captured.out.encode("cp1252")


class TestPrintReportBranches:
    """Cover remaining branches in print_report and _print_validator_section."""

    def test_print_report_with_content_file(self, capsys):
        """print_report shows filename when content_file is set."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(is_valid=True, content_file="output/brief.html")
        result.print_report()
        captured = capsys.readouterr()
        assert "File: output/brief.html" in captured.out

    def test_print_report_without_content_file(self, capsys):
        """print_report omits filename when content_file is None."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(is_valid=True, content_file=None)
        result.print_report()
        captured = capsys.readouterr()
        assert "File:" not in captured.out

    def test_print_report_error_truncation(self, capsys):
        """_print_validator_section truncates errors beyond 5."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=False)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=False,
            errors=[f"Error {i}" for i in range(8)],
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "Error 0" in captured.out
        assert "Error 4" in captured.out
        assert "and 3 more" in captured.out
        # Error 5, 6, 7 should not appear directly
        assert "Error 5" not in captured.out

    def test_print_report_errors_exactly_5(self, capsys):
        """5 errors shown without truncation message."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=False)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=False,
            errors=[f"Error {i}" for i in range(5)],
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "Error 4" in captured.out
        assert "more" not in captured.out

    def test_print_report_score_with_grade(self, capsys):
        """Score line includes grade in parentheses."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.eeat_validation = ValidationSummary(
            validator_name="EEAT",
            passed=True,
            score=85.0,
            grade="B",
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "Score: 85.0/100 (B)" in captured.out

    def test_print_report_score_without_grade(self, capsys):
        """Score line omits grade when grade is None."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.eeat_validation = ValidationSummary(
            validator_name="EEAT",
            passed=True,
            score=85.0,
            grade=None,
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "Score: 85.0/100" in captured.out
        assert "()" not in captured.out

    def test_print_report_no_score(self, capsys):
        """No score line when score is None."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            score=None,
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "Score:" not in captured.out

    def test_print_report_all_three_validators(self, capsys):
        """All three validator sections shown when present."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(validator_name="AI", passed=True)
        result.brand_validation = ValidationSummary(validator_name="Brand", passed=True)
        result.eeat_validation = ValidationSummary(validator_name="EEAT", passed=True)
        result.print_report()
        captured = capsys.readouterr()
        assert "AI Pattern Detection" in captured.out
        assert "Brand Validation" in captured.out
        assert "E-E-A-T Validation" in captured.out

    def test_print_report_verbose_warnings_truncation(self, capsys):
        """Verbose mode shows warnings with truncation beyond 5."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            warnings=[f"Warn {i}" for i in range(7)],
        )
        result.print_report(verbose=True)
        captured = capsys.readouterr()
        assert "Warn 0" in captured.out
        assert "Warn 4" in captured.out
        assert "and 2 more" in captured.out

    def test_print_report_non_verbose_hides_warnings(self, capsys):
        """Non-verbose mode does not show warnings."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            warnings=["Should not appear"],
        )
        result.print_report(verbose=False)
        captured = capsys.readouterr()
        assert "Should not appear" not in captured.out


class TestMainCLI:
    """Cover main() CLI entry point branches."""

    def test_main_no_path_shows_help(self, monkeypatch, capsys):
        """main() with no path argument prints help and returns 1."""
        monkeypatch.setattr('sys.argv', ['unified_content_validator.py'])
        from unified_content_validator import main
        exit_code = main()
        assert exit_code == 1

    def test_main_path_not_found_returns_2(self, monkeypatch, capsys):
        """main() with nonexistent path returns 2."""
        monkeypatch.setattr('sys.argv', ['unified_content_validator.py', '/nonexistent/file.html'])
        with patch('unified_content_validator.VALIDATORS_AVAILABLE', True):
            with patch('unified_content_validator.UnifiedContentValidator'):
                from unified_content_validator import main
                exit_code = main()
        captured = capsys.readouterr()
        assert exit_code == 2

    def test_main_json_output(self, monkeypatch, tmp_path, capsys):
        """main() with --json outputs JSON format."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test content</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file), '--json'
        ])

        from unified_content_validator import UnifiedValidationResult
        mock_result = UnifiedValidationResult(is_valid=True, content_file=str(test_file))

        with patch('unified_content_validator.VALIDATORS_AVAILABLE', True):
            mock_validator = MagicMock()
            mock_validator.validate_file.return_value = mock_result
            with patch('unified_content_validator.UnifiedContentValidator', return_value=mock_validator):
                from unified_content_validator import main
                exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        data = json.loads(captured.out)
        assert data["all_passed"] is True
        assert data["total_files"] == 1

    def test_main_all_directory(self, monkeypatch, tmp_path, capsys):
        """main() with --all scans directory."""
        (tmp_path / "a.html").write_text("<p>A</p>")
        (tmp_path / "b.md").write_text("# B")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(tmp_path), '--all'
        ])

        from unified_content_validator import UnifiedValidationResult
        mock_result = UnifiedValidationResult(is_valid=True)

        with patch('unified_content_validator.VALIDATORS_AVAILABLE', True):
            mock_validator = MagicMock()
            mock_validator.validate_file.return_value = mock_result
            with patch('unified_content_validator.UnifiedContentValidator', return_value=mock_validator):
                from unified_content_validator import main
                exit_code = main()

        assert exit_code == 0

    def test_main_failed_validation_returns_1(self, monkeypatch, tmp_path, capsys):
        """main() returns 1 when validation fails."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Bad content</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file)
        ])

        from unified_content_validator import UnifiedValidationResult
        mock_result = UnifiedValidationResult(is_valid=False, content_file=str(test_file))

        with patch('unified_content_validator.VALIDATORS_AVAILABLE', True):
            mock_validator = MagicMock()
            mock_validator.validate_file.return_value = mock_result
            with patch('unified_content_validator.UnifiedContentValidator', return_value=mock_validator):
                from unified_content_validator import main
                exit_code = main()

        assert exit_code == 1

    def test_main_multiple_files_summary(self, monkeypatch, tmp_path, capsys):
        """main() with multiple files shows summary."""
        (tmp_path / "a.html").write_text("<p>A</p>")
        (tmp_path / "b.html").write_text("<p>B</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(tmp_path), '--all'
        ])

        from unified_content_validator import UnifiedValidationResult
        result_a = UnifiedValidationResult(is_valid=True)
        result_b = UnifiedValidationResult(is_valid=False)

        with patch('unified_content_validator.VALIDATORS_AVAILABLE', True):
            mock_validator = MagicMock()
            mock_validator.validate_file.side_effect = [result_a, result_b]
            with patch('unified_content_validator.UnifiedContentValidator', return_value=mock_validator):
                from unified_content_validator import main
                exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 1  # one file failed
        assert "SUMMARY:" in captured.out
        assert "1/2 files passed" in captured.out

    def test_main_strict_and_eeat_min_flags(self, monkeypatch, tmp_path):
        """main() passes --strict and --eeat-min to validator constructor."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file),
            '--strict', '--eeat-min', '70', '--no-ai', '--no-brands'
        ])

        from unified_content_validator import UnifiedValidationResult
        mock_result = UnifiedValidationResult(is_valid=True)

        with patch('unified_content_validator.VALIDATORS_AVAILABLE', True):
            mock_cls = MagicMock()
            mock_instance = MagicMock()
            mock_instance.validate_file.return_value = mock_result
            mock_cls.return_value = mock_instance
            with patch('unified_content_validator.UnifiedContentValidator', mock_cls):
                from unified_content_validator import main
                exit_code = main()

        # Verify constructor was called with correct flags
        mock_cls.assert_called_once_with(
            validate_ai_patterns=False,
            validate_brands=False,
            validate_eeat=True,
            ai_pattern_strict=True,
            eeat_min_score=70.0,
        )
        assert exit_code == 0


class TestDataclassProperties:
    """Cover UnifiedValidationResult property branches."""

    def test_total_errors_with_all_validators(self):
        """total_errors sums across all validators + general errors."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(
            is_valid=False,
            errors=["general 1", "general 2"],
        )
        result.ai_patterns = ValidationSummary(
            validator_name="AI", passed=False, errors=["ai err"]
        )
        result.brand_validation = ValidationSummary(
            validator_name="Brand", passed=False, errors=["brand err 1", "brand err 2"]
        )
        result.eeat_validation = ValidationSummary(
            validator_name="EEAT", passed=False, errors=["eeat err"]
        )
        assert result.total_errors == 6  # 2 + 1 + 2 + 1

    def test_total_errors_no_validators(self):
        """total_errors with no validator results, only general."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(is_valid=False, errors=["err"])
        assert result.total_errors == 1

    def test_total_warnings_with_all_validators(self):
        """total_warnings sums across all validators."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI", passed=True, warnings=["w1", "w2"]
        )
        result.brand_validation = ValidationSummary(
            validator_name="Brand", passed=True, warnings=["w3"]
        )
        result.eeat_validation = ValidationSummary(
            validator_name="EEAT", passed=True, warnings=["w4", "w5", "w6"]
        )
        assert result.total_warnings == 6

    def test_total_warnings_no_validators(self):
        """total_warnings is 0 when no validators set."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(is_valid=True)
        assert result.total_warnings == 0

    def test_to_dict_full(self):
        """to_dict includes all validator summaries."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        result = UnifiedValidationResult(
            is_valid=True,
            content_file="test.html",
        )
        result.ai_patterns = ValidationSummary(
            validator_name="AI", passed=True, score=95.0, grade="A"
        )
        result.brand_validation = ValidationSummary(
            validator_name="Brand", passed=True
        )
        result.eeat_validation = ValidationSummary(
            validator_name="EEAT", passed=True, score=80.0, grade="B"
        )
        d = result.to_dict()
        assert d["is_valid"] is True
        assert d["content_file"] == "test.html"
        assert d["ai_patterns"]["validator"] == "AI"
        assert d["brand_validation"]["validator"] == "Brand"
        assert d["eeat_validation"]["validator"] == "EEAT"

    def test_to_dict_none_validators(self):
        """to_dict returns None for unset validators."""
        from unified_content_validator import UnifiedValidationResult
        result = UnifiedValidationResult(is_valid=True)
        d = result.to_dict()
        assert d["ai_patterns"] is None
        assert d["brand_validation"] is None
        assert d["eeat_validation"] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
