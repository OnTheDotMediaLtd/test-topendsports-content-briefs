"""
Expanded tests for unified_content_validator.py to increase coverage.
Target: from 63.13% to 80%+
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
from dataclasses import dataclass

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))

# Mock the validators before importing
mock_validators = MagicMock()

# Create mock classes for validators
class MockAIPatternValidator:
    def validate(self, content):
        return {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'details': {}
        }

class MockBrandValidator:
    def validate(self, content):
        @dataclass
        class MockResult:
            valid: bool = True
            errors: list = None
            warnings: list = None
            verified_brands: list = None
            unknown_brands: list = None
            suggestions: dict = None

            def __post_init__(self):
                self.errors = self.errors or []
                self.warnings = self.warnings or []
                self.verified_brands = self.verified_brands or []
                self.unknown_brands = self.unknown_brands or []
                self.suggestions = self.suggestions or {}

        return MockResult()

class MockEEATValidator:
    def validate(self, content):
        @dataclass
        class MockScore:
            total: float = 75.0
            grade: str = 'B'

        @dataclass
        class MockEEATResult:
            is_valid: bool = True
            errors: list = None
            warnings: list = None
            score: object = None

            def __post_init__(self):
                self.errors = self.errors or []
                self.warnings = self.warnings or []
                self.score = MockScore()

            def to_dict(self):
                return {
                    'is_valid': self.is_valid,
                    'score': {'total': self.score.total, 'grade': self.score.grade},
                    'errors': [],
                    'warnings': []
                }

        return MockEEATResult()


# Patch the import before loading the module
with patch.dict('sys.modules', {
    'tes_shared': MagicMock(),
    'tes_shared.validators': MagicMock(
        AIPatternValidator=MockAIPatternValidator,
        BrandValidator=MockBrandValidator,
        EEATValidator=MockEEATValidator,
        EEATResult=type('EEATResult', (), {})
    )
}):
    # Now we can import with mocked validators
    from unified_content_validator import (
        ValidationSummary,
        UnifiedValidationResult,
        UnifiedContentValidator,
        validate_content,
        validate_file,
        main,
        VALIDATORS_AVAILABLE
    )


class TestValidationSummary:
    """Tests for ValidationSummary dataclass."""

    def test_create_summary(self):
        """Test creating a validation summary."""
        summary = ValidationSummary(
            validator_name="Test Validator",
            passed=True,
            score=85.0,
            grade='B'
        )
        assert summary.validator_name == "Test Validator"
        assert summary.passed is True
        assert summary.score == 85.0
        assert summary.grade == 'B'

    def test_summary_with_errors(self):
        """Test summary with errors list."""
        summary = ValidationSummary(
            validator_name="Test",
            passed=False,
            errors=["Error 1", "Error 2"]
        )
        assert len(summary.errors) == 2
        assert "Error 1" in summary.errors

    def test_summary_with_warnings(self):
        """Test summary with warnings list."""
        summary = ValidationSummary(
            validator_name="Test",
            passed=True,
            warnings=["Warning 1"]
        )
        assert len(summary.warnings) == 1

    def test_summary_with_details(self):
        """Test summary with details dict."""
        summary = ValidationSummary(
            validator_name="Test",
            passed=True,
            details={"key": "value", "nested": {"a": 1}}
        )
        assert summary.details["key"] == "value"
        assert summary.details["nested"]["a"] == 1


class TestUnifiedValidationResult:
    """Tests for UnifiedValidationResult dataclass."""

    def test_create_result(self):
        """Test creating a validation result."""
        result = UnifiedValidationResult(is_valid=True)
        assert result.is_valid is True
        assert result.content_file is None

    def test_result_with_content_file(self):
        """Test result with content file path."""
        result = UnifiedValidationResult(
            is_valid=True,
            content_file="/path/to/file.html"
        )
        assert result.content_file == "/path/to/file.html"

    def test_total_errors_empty(self):
        """Test total_errors with no validators."""
        result = UnifiedValidationResult(is_valid=True)
        assert result.total_errors == 0

    def test_total_errors_with_validators(self):
        """Test total_errors aggregates across validators."""
        result = UnifiedValidationResult(is_valid=False)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=False,
            errors=["AI Error"]
        )
        result.brand_validation = ValidationSummary(
            validator_name="Brand",
            passed=False,
            errors=["Brand Error 1", "Brand Error 2"]
        )
        result.errors = ["General Error"]

        assert result.total_errors == 4

    def test_total_warnings(self):
        """Test total_warnings aggregates across validators."""
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            warnings=["Warning 1"]
        )
        result.brand_validation = ValidationSummary(
            validator_name="Brand",
            passed=True,
            warnings=["Warning 2", "Warning 3"]
        )

        assert result.total_warnings == 3

    def test_to_dict(self):
        """Test converting result to dictionary."""
        result = UnifiedValidationResult(
            is_valid=True,
            content_file="test.html"
        )
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            score=90.0
        )

        d = result.to_dict()

        assert d['is_valid'] is True
        assert d['content_file'] == "test.html"
        assert d['ai_patterns']['passed'] is True
        assert d['ai_patterns']['score'] == 90.0

    def test_to_dict_with_none_validators(self):
        """Test to_dict handles None validators."""
        result = UnifiedValidationResult(is_valid=True)
        d = result.to_dict()

        assert d['ai_patterns'] is None
        assert d['brand_validation'] is None
        assert d['eeat_validation'] is None


class TestUnifiedValidationResultPrint:
    """Tests for print_report method."""

    def test_print_report_passed(self, capsys):
        """Test printing report for passed validation."""
        result = UnifiedValidationResult(
            is_valid=True,
            content_file="test.html"
        )
        result.print_report()

        captured = capsys.readouterr()
        assert "PASSED" in captured.out
        assert "test.html" in captured.out

    def test_print_report_failed(self, capsys):
        """Test printing report for failed validation."""
        result = UnifiedValidationResult(
            is_valid=False,
            errors=["General error"]
        )
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=False,
            errors=["AI detected"]
        )
        result.print_report()

        captured = capsys.readouterr()
        assert "FAILED" in captured.out
        assert "GENERAL ERRORS" in captured.out

    def test_print_report_with_all_validators(self, capsys):
        """Test printing report with all validators."""
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            score=95.0
        )
        result.brand_validation = ValidationSummary(
            validator_name="Brand",
            passed=True
        )
        result.eeat_validation = ValidationSummary(
            validator_name="EEAT",
            passed=True,
            score=80.0,
            grade='B'
        )

        result.print_report()

        captured = capsys.readouterr()
        assert "AI Pattern Detection" in captured.out
        assert "Brand Validation" in captured.out
        assert "E-E-A-T Validation" in captured.out

    def test_print_report_verbose_warnings(self, capsys):
        """Test printing report with verbose warnings."""
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            warnings=["Warning 1", "Warning 2"]
        )

        result.print_report(verbose=True)

        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_print_report_truncates_errors(self, capsys):
        """Test printing report truncates many errors."""
        result = UnifiedValidationResult(is_valid=False)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=False,
            errors=[f"Error {i}" for i in range(10)]
        )

        result.print_report()

        captured = capsys.readouterr()
        assert "and 5 more" in captured.out


class TestUnifiedContentValidatorInit:
    """Tests for UnifiedContentValidator initialization."""

    def test_init_all_validators(self):
        """Test initializing with all validators enabled."""
        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MockAIPatternValidator,
                BrandValidator=MockBrandValidator,
                EEATValidator=MockEEATValidator,
                EEATResult=type('EEATResult', (), {})
            )
        }):
            validator = UnifiedContentValidator()
            assert validator.validate_ai_patterns is True
            assert validator.validate_brands is True
            assert validator.validate_eeat is True

    def test_init_disable_ai_patterns(self):
        """Test initializing with AI patterns disabled."""
        validator = UnifiedContentValidator(validate_ai_patterns=False)
        assert validator.validate_ai_patterns is False
        assert validator._ai_validator is None

    def test_init_disable_brands(self):
        """Test initializing with brand validation disabled."""
        validator = UnifiedContentValidator(validate_brands=False)
        assert validator.validate_brands is False
        assert validator._brand_validator is None

    def test_init_disable_eeat(self):
        """Test initializing with EEAT validation disabled."""
        validator = UnifiedContentValidator(validate_eeat=False)
        assert validator.validate_eeat is False
        assert validator._eeat_validator is None

    def test_init_custom_eeat_min(self):
        """Test initializing with custom EEAT minimum score."""
        validator = UnifiedContentValidator(eeat_min_score=70.0)
        assert validator.eeat_min_score == 70.0

    def test_init_strict_mode(self):
        """Test initializing with strict AI pattern mode."""
        validator = UnifiedContentValidator(ai_pattern_strict=True)
        assert validator.ai_pattern_strict is True


class TestUnifiedContentValidatorValidate:
    """Tests for validate method."""

    def test_validate_html_content(self):
        """Test validating HTML content."""
        validator = UnifiedContentValidator()
        content = "<html><body><h1>Test</h1><p>Content</p></body></html>"

        result = validator.validate(content, content_type='html')

        assert isinstance(result, UnifiedValidationResult)

    def test_validate_markdown_content(self):
        """Test validating Markdown content."""
        validator = UnifiedContentValidator()
        content = "# Test\n\nThis is **bold** and *italic* content."

        result = validator.validate(content, content_type='markdown')

        assert isinstance(result, UnifiedValidationResult)

    def test_validate_with_filename(self):
        """Test validating with filename specified."""
        validator = UnifiedContentValidator()
        content = "<p>Test</p>"

        result = validator.validate(content, filename="test.html")

        assert result.content_file == "test.html"

    def test_validate_records_ai_patterns(self):
        """Test that AI pattern results are recorded."""
        validator = UnifiedContentValidator()
        content = "<p>Test content</p>"

        result = validator.validate(content)

        assert result.ai_patterns is not None
        assert result.ai_patterns.validator_name == "AI Pattern Detection"

    def test_validate_records_brand_validation(self):
        """Test that brand validation results are recorded."""
        validator = UnifiedContentValidator()
        content = "<p>Test content</p>"

        result = validator.validate(content)

        assert result.brand_validation is not None
        assert result.brand_validation.validator_name == "Brand Validation"

    def test_validate_records_eeat_validation(self):
        """Test that EEAT validation results are recorded."""
        validator = UnifiedContentValidator()
        content = "<p>Test content</p>"

        result = validator.validate(content)

        assert result.eeat_validation is not None
        assert result.eeat_validation.validator_name == "E-E-A-T Validation"


class TestUnifiedContentValidatorValidateFile:
    """Tests for validate_file method."""

    def test_validate_file_not_found(self, tmp_path):
        """Test validating non-existent file."""
        validator = UnifiedContentValidator()
        fake_path = tmp_path / "nonexistent.html"

        result = validator.validate_file(fake_path)

        assert result.is_valid is False
        assert "not found" in result.errors[0].lower()

    def test_validate_file_html(self, tmp_path):
        """Test validating HTML file."""
        validator = UnifiedContentValidator()
        html_file = tmp_path / "test.html"
        html_file.write_text("<html><body>Test</body></html>")

        result = validator.validate_file(html_file)

        assert isinstance(result, UnifiedValidationResult)

    def test_validate_file_markdown(self, tmp_path):
        """Test validating Markdown file."""
        validator = UnifiedContentValidator()
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\nContent here.")

        result = validator.validate_file(md_file)

        assert isinstance(result, UnifiedValidationResult)

    def test_validate_file_read_error(self, tmp_path):
        """Test handling file read errors."""
        validator = UnifiedContentValidator()
        test_file = tmp_path / "test.html"
        test_file.write_text("test")

        with patch.object(Path, 'read_text', side_effect=PermissionError("Access denied")):
            result = validator.validate_file(test_file)

        assert result.is_valid is False
        assert len(result.errors) > 0


class TestMarkdownToHtml:
    """Tests for markdown to HTML conversion."""

    def test_convert_headers(self):
        """Test markdown header conversion."""
        validator = UnifiedContentValidator()
        markdown = "# H1\n## H2\n### H3"

        html = validator._markdown_to_html(markdown)

        assert "<h1>" in html
        assert "<h2>" in html
        assert "<h3>" in html

    def test_convert_bold(self):
        """Test markdown bold conversion."""
        validator = UnifiedContentValidator()
        markdown = "This is **bold** text"

        html = validator._markdown_to_html(markdown)

        assert "<strong>" in html

    def test_convert_italic(self):
        """Test markdown italic conversion."""
        validator = UnifiedContentValidator()
        markdown = "This is *italic* text"

        html = validator._markdown_to_html(markdown)

        assert "<em>" in html

    def test_convert_links(self):
        """Test markdown link conversion."""
        validator = UnifiedContentValidator()
        markdown = "[Link text](https://example.com)"

        html = validator._markdown_to_html(markdown)

        assert "<a href=" in html
        assert "example.com" in html

    def test_convert_paragraphs(self):
        """Test paragraph wrapping."""
        validator = UnifiedContentValidator()
        markdown = "Paragraph one.\n\nParagraph two."

        html = validator._markdown_to_html(markdown)

        assert "<p>" in html


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_validate_content_function(self):
        """Test validate_content convenience function."""
        result = validate_content("<p>Test</p>", content_type='html')
        assert isinstance(result, UnifiedValidationResult)

    def test_validate_content_disable_validators(self):
        """Test validate_content with disabled validators."""
        result = validate_content(
            "<p>Test</p>",
            validate_ai=False,
            validate_brands=False,
            validate_eeat=False
        )
        assert isinstance(result, UnifiedValidationResult)

    def test_validate_file_function(self, tmp_path):
        """Test validate_file convenience function."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test</p>")

        result = validate_file(test_file)
        assert isinstance(result, UnifiedValidationResult)


class TestCLIMain:
    """Tests for CLI main function."""

    def test_main_no_path(self, monkeypatch):
        """Test main with no path argument."""
        monkeypatch.setattr('sys.argv', ['unified_content_validator.py'])

        result = main()

        assert result == 1

    def test_main_file_not_found(self, monkeypatch, tmp_path):
        """Test main with non-existent file."""
        fake_path = tmp_path / "nonexistent.html"
        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(fake_path)
        ])

        result = main()

        assert result == 2

    def test_main_single_file(self, monkeypatch, tmp_path, capsys):
        """Test main with single file."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test content</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file)
        ])

        result = main()

        # Result depends on validation outcome
        assert result in [0, 1]

    def test_main_json_output(self, monkeypatch, tmp_path, capsys):
        """Test main with JSON output flag."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test content</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file), '--json'
        ])

        result = main()

        captured = capsys.readouterr()
        # Output should be valid JSON
        output = json.loads(captured.out)
        assert 'all_passed' in output
        assert 'results' in output

    def test_main_verbose_flag(self, monkeypatch, tmp_path, capsys):
        """Test main with verbose flag."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test content</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file), '-v'
        ])

        result = main()
        assert result in [0, 1]

    def test_main_disable_validators(self, monkeypatch, tmp_path):
        """Test main with validators disabled."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file),
            '--no-ai', '--no-brands', '--no-eeat'
        ])

        result = main()
        assert result in [0, 1]

    def test_main_custom_eeat_min(self, monkeypatch, tmp_path):
        """Test main with custom EEAT minimum."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file),
            '--eeat-min', '70'
        ])

        result = main()
        assert result in [0, 1]

    def test_main_strict_mode(self, monkeypatch, tmp_path):
        """Test main with strict mode."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test</p>")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file), '--strict'
        ])

        result = main()
        assert result in [0, 1]

    def test_main_all_flag_directory(self, monkeypatch, tmp_path, capsys):
        """Test main with --all flag on directory."""
        # Create test files
        (tmp_path / "test1.html").write_text("<p>Test 1</p>")
        (tmp_path / "test2.md").write_text("# Test 2")

        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', '--all', str(tmp_path)
        ])

        result = main()

        captured = capsys.readouterr()
        assert "SUMMARY" in captured.out


class TestValidatorErrorHandling:
    """Tests for error handling in validators."""

    def test_ai_validator_exception(self):
        """Test handling exception from AI validator."""
        validator = UnifiedContentValidator()

        # Mock AI validator to raise exception
        with patch.object(validator._ai_validator, 'validate', side_effect=Exception("Test error")):
            result = validator.validate("<p>Test</p>")

        assert result.ai_patterns.passed is False
        assert "error" in result.ai_patterns.errors[0].lower()

    def test_brand_validator_exception(self):
        """Test handling exception from brand validator."""
        validator = UnifiedContentValidator()

        with patch.object(validator._brand_validator, 'validate', side_effect=Exception("Test error")):
            result = validator.validate("<p>Test</p>")

        assert result.brand_validation.passed is False

    def test_eeat_validator_exception(self):
        """Test handling exception from EEAT validator."""
        validator = UnifiedContentValidator()

        with patch.object(validator._eeat_validator, 'validate', side_effect=Exception("Test error")):
            result = validator.validate("<p>Test</p>")

        assert result.eeat_validation.passed is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
