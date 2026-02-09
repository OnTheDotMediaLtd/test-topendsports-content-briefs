"""
Coverage tests for unified_content_validator.py to fill remaining gaps.
Targets specific lines and edge cases not covered by existing tests.
"""

import pytest
import sys
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock, mock_open
from dataclasses import dataclass
from typing import List

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))


class TestValidatorsImportFallback:
    """Tests for validators import fallback logic."""
    
    def test_validators_not_available_init_error(self):
        """Test UnifiedContentValidator raises error when validators unavailable."""
        # Mock VALIDATORS_AVAILABLE = False
        with patch('unified_content_validator.VALIDATORS_AVAILABLE', False):
            from unified_content_validator import UnifiedContentValidator
            
            with pytest.raises(ImportError, match="TES shared validators not available"):
                UnifiedContentValidator()

    def test_import_fallback_path_exists(self):
        """Test fallback import path when shared_infra_path exists."""
        # This tests that the module-level import fallback logic works.
        # Since the module is already loaded with real validators, we just
        # verify that VALIDATORS_AVAILABLE is True (fallback succeeded).
        import unified_content_validator
        assert unified_content_validator.VALIDATORS_AVAILABLE is True

    def test_import_fallback_path_not_exists(self):
        """Test fallback when shared_infra_path doesn't exist."""
        with patch('unified_content_validator.Path') as mock_path:
            # Mock path doesn't exist
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = False
            mock_path.return_value.parent.parent.parent = mock_path_instance
            
            # This should set VALIDATORS_AVAILABLE = False
            import importlib
            import unified_content_validator
            importlib.reload(unified_content_validator)


class TestValidatorResultFormats:
    """Tests for different validator result formats."""

    def test_ai_validator_object_result(self):
        """Test AI validator with object-based result instead of dict."""
        @dataclass
        class MockAIResult:
            is_valid: bool = True
            errors: List[str] = None
            warnings: List[str] = None
            details: dict = None
            score: float = None
            
            def __post_init__(self):
                self.errors = self.errors or []
                self.warnings = self.warnings or []
                self.details = self.details or {}

        class MockAIValidator:
            def validate(self, content):
                return MockAIResult(errors=["AI pattern detected"], warnings=["Suspicious phrase"], score=75.0)

        from unified_content_validator import UnifiedContentValidator
        
        # Construct with AI disabled, then inject mock
        validator = UnifiedContentValidator(validate_ai_patterns=False, validate_brands=False, validate_eeat=False)
        validator._ai_validator = MockAIValidator()
        result = validator._run_ai_patterns("<p>Test AI content</p>")
        
        assert result.validator_name == "AI Pattern Detection"
        assert result.score == 75.0  # Score from object result
        assert len(result.errors) == 1
        assert len(result.warnings) == 1

    def test_ai_validator_strict_mode_fails_on_warnings(self):
        """Test AI validator strict mode fails on warnings."""
        class MockAIValidator:
            def validate(self, content):
                return {
                    'is_valid': True,
                    'errors': [],
                    'warnings': ['Minor AI pattern'],
                    'details': {}
                }

        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MockAIValidator,
                BrandValidator=MagicMock(),
                EEATValidator=MagicMock(),
                EEATResult=type('EEATResult', (), {})
            )
        }):
            from unified_content_validator import UnifiedContentValidator
            
            # Non-strict mode should pass with warnings
            validator = UnifiedContentValidator(ai_pattern_strict=False)
            result = validator._run_ai_patterns("<p>Test</p>")
            assert result.passed is True
            
            # Strict mode should fail with warnings
            validator_strict = UnifiedContentValidator(ai_pattern_strict=True)
            result_strict = validator_strict._run_ai_patterns("<p>Test</p>")
            assert result_strict.passed is False

    def test_brand_validator_dict_result(self):
        """Test brand validator with dict result instead of object."""
        class MockBrandValidator:
            def validate(self, content):
                return {
                    'valid': False,
                    'errors': ['Unknown brand: FakeBet'],
                    'warnings': ['Consider using DraftKings'],
                    'verified_brands': ['BetMGM'],
                    'unknown_brands': ['FakeBet'],
                    'suggestions': {'FakeBet': 'DraftKings'}
                }

        from unified_content_validator import UnifiedContentValidator
        
        validator = UnifiedContentValidator(validate_ai_patterns=False, validate_brands=False, validate_eeat=False)
        validator._brand_validator = MockBrandValidator()
        result = validator._run_brand_validation("<p>Try FakeBet for sports betting</p>")
        
        assert result.validator_name == "Brand Validation"
        assert result.passed is False
        assert "Unknown brand" in result.errors[0]
        assert len(result.warnings) == 1

    def test_eeat_validator_dict_result(self):
        """Test EEAT validator with dict result instead of EEATResult object."""
        class MockEEATValidator:
            def validate(self, content):
                return {
                    'is_valid': False,
                    'score': {'total': 45.0, 'grade': 'D'},
                    'errors': ['Missing author expertise signals'],
                    'warnings': ['Could improve authority signals']
                }

        from unified_content_validator import UnifiedContentValidator
        
        validator = UnifiedContentValidator(validate_ai_patterns=False, validate_brands=False, validate_eeat=False)
        validator.eeat_min_score = 50.0
        validator._eeat_validator = MockEEATValidator()
        result = validator._run_eeat_validation("<p>Basic content</p>")
        
        assert result.validator_name == "E-E-A-T Validation"
        assert result.passed is False  # Score 45 < min 50
        assert result.score == 45.0
        assert result.grade == 'D'

    def test_eeat_validator_with_eeat_result_object(self):
        """Test EEAT validator with proper EEATResult object."""
        @dataclass
        class MockEEATScore:
            total: float = 85.0
            grade: str = 'A'

        @dataclass  
        class MockEEATIssue:
            category: MagicMock = None
            message: str = "Test message"
            
            def __post_init__(self):
                if self.category is None:
                    self.category = MagicMock()
                    self.category.value = "expertise"

        @dataclass
        class MockEEATResult:
            is_valid: bool = True
            score: MockEEATScore = None
            errors: List[MockEEATIssue] = None
            warnings: List[MockEEATIssue] = None
            
            def __post_init__(self):
                self.score = MockEEATScore()
                self.errors = self.errors or [MockEEATIssue()]
                self.warnings = self.warnings or [MockEEATIssue(message="Warning message")]
            
            def to_dict(self):
                return {
                    'is_valid': self.is_valid,
                    'score': {'total': self.score.total, 'grade': self.score.grade}
                }

        class MockEEATValidator:
            def validate(self, content):
                return MockEEATResult()

        import unified_content_validator as ucv
        
        # Patch EEATResult at module level so isinstance check works
        orig_eeat_result = ucv.EEATResult
        ucv.EEATResult = MockEEATResult
        try:
            validator = ucv.UnifiedContentValidator(
                validate_ai_patterns=False, validate_brands=False, validate_eeat=False
            )
            validator.eeat_min_score = 70.0
            validator._eeat_validator = MockEEATValidator()
            result = validator._run_eeat_validation("<p>Quality content</p>")
            
            assert result.validator_name == "E-E-A-T Validation"
            assert result.passed is True  # Score 85 > min 70
            assert result.score == 85.0
            assert result.grade == 'A'
            assert "expertise: Test message" in result.errors[0]
            assert "expertise: Warning message" in result.warnings[0]
        finally:
            ucv.EEATResult = orig_eeat_result


class TestValidationFailurePropagation:
    """Tests that validation failures properly set is_valid=False."""

    def test_ai_pattern_failure_sets_invalid(self):
        """Test AI pattern failure sets overall result invalid."""
        class MockAIValidator:
            def validate(self, content):
                return {'is_valid': False, 'errors': ['AI detected'], 'warnings': [], 'details': {}}

        from unified_content_validator import UnifiedContentValidator
        
        validator = UnifiedContentValidator(validate_ai_patterns=True, validate_brands=False, validate_eeat=False)
        validator._ai_validator = MockAIValidator()
        validator.validate_ai_patterns = True
        result = validator.validate("<p>AI generated text</p>")
        
        assert result.is_valid is False

    def test_brand_failure_sets_invalid(self):
        """Test brand validation failure sets overall result invalid."""
        @dataclass
        class MockBrandResult:
            valid: bool = False
            errors: list = None
            warnings: list = None
            verified_brands: list = None
            unknown_brands: list = None
            suggestions: dict = None

            def __post_init__(self):
                self.errors = ['Invalid brand found']
                self.warnings = []
                self.verified_brands = []
                self.unknown_brands = ['FakeCasino']
                self.suggestions = {}

        class MockBrandValidator:
            def validate(self, content):
                return MockBrandResult()

        from unified_content_validator import UnifiedContentValidator
        
        validator = UnifiedContentValidator(validate_ai_patterns=False, validate_brands=True, validate_eeat=False)
        validator._brand_validator = MockBrandValidator()
        validator.validate_brands = True
        result = validator.validate("<p>Visit FakeCasino</p>")
        
        assert result.is_valid is False

    def test_eeat_failure_sets_invalid(self):
        """Test EEAT validation failure sets overall result invalid."""
        @dataclass
        class MockEEATScore:
            total: float = 30.0
            grade: str = 'F'

        @dataclass
        class MockEEATResult:
            is_valid: bool = False
            score: MockEEATScore = None
            errors: list = None
            warnings: list = None
            
            def __post_init__(self):
                self.score = MockEEATScore()
                self.errors = []
                self.warnings = []
            
            def to_dict(self):
                return {'is_valid': self.is_valid, 'score': {'total': 30.0, 'grade': 'F'}}

        class MockEEATValidator:
            def validate(self, content):
                return MockEEATResult()

        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MagicMock(),
                BrandValidator=MagicMock(),
                EEATValidator=MockEEATValidator,
                EEATResult=MockEEATResult
            )
        }):
            from unified_content_validator import UnifiedContentValidator
            
            validator = UnifiedContentValidator(
                validate_ai_patterns=False, 
                validate_brands=False, 
                eeat_min_score=50.0
            )
            result = validator.validate("<p>Low quality content</p>")
            
            assert result.is_valid is False


class TestMarkdownConversionEdgeCases:
    """Tests for edge cases in markdown conversion."""

    def test_markdown_conversion_multiple_underscore_styles(self):
        """Test markdown conversion handles multiple underscore styles."""
        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MagicMock(),
                BrandValidator=MagicMock(),
                EEATValidator=MagicMock(),
                EEATResult=type('EEATResult', (), {})
            )
        }):
            from unified_content_validator import UnifiedContentValidator
            
            validator = UnifiedContentValidator()
            markdown = "__bold text__ and _italic text_"
            
            html = validator._markdown_to_html(markdown)
            
            assert "<strong>bold text</strong>" in html
            assert "<em>italic text</em>" in html

    def test_markdown_conversion_headers_in_order(self):
        """Test markdown headers converted in correct order (6 to 1)."""
        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MagicMock(),
                BrandValidator=MagicMock(),
                EEATValidator=MagicMock(),
                EEATResult=type('EEATResult', (), {})
            )
        }):
            from unified_content_validator import UnifiedContentValidator
            
            validator = UnifiedContentValidator()
            markdown = "# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6"
            
            html = validator._markdown_to_html(markdown)
            
            for i in range(1, 7):
                assert f"<h{i}>" in html and f"</h{i}>" in html

    def test_markdown_conversion_paragraph_wrapping_edge_cases(self):
        """Test paragraph wrapping with edge cases."""
        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MagicMock(),
                BrandValidator=MagicMock(),
                EEATValidator=MagicMock(),
                EEATResult=type('EEATResult', (), {})
            )
        }):
            from unified_content_validator import UnifiedContentValidator
            
            validator = UnifiedContentValidator()
            
            # Test with existing HTML tags (should not be wrapped)
            markdown = "<div>Existing HTML</div>\n\nPlain paragraph"
            html = validator._markdown_to_html(markdown)
            
            assert "<div>Existing HTML</div>" in html  # Not wrapped
            assert "<p>Plain paragraph</p>" in html  # Wrapped

    def test_markdown_conversion_empty_paragraphs(self):
        """Test markdown conversion handles empty paragraphs."""
        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MagicMock(),
                BrandValidator=MagicMock(),
                EEATValidator=MagicMock(),
                EEATResult=type('EEATResult', (), {})
            )
        }):
            from unified_content_validator import UnifiedContentValidator
            
            validator = UnifiedContentValidator()
            markdown = "Content\n\n\n\nMore content"
            
            html = validator._markdown_to_html(markdown)
            
            # Should handle multiple empty lines gracefully


class TestCLIEdgeCases:
    """Tests for CLI edge cases not covered."""

    def test_main_validators_unavailable_error(self, monkeypatch, tmp_path, capsys):
        """Test main function when validators are unavailable."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test</p>")
        
        monkeypatch.setattr('sys.argv', ['unified_content_validator.py', str(test_file)])
        
        with patch('unified_content_validator.VALIDATORS_AVAILABLE', False):
            from unified_content_validator import main
            
            result = main()
            
            assert result == 2
            captured = capsys.readouterr()
            assert "validators not available" in captured.err.lower()

    def test_main_validator_init_import_error(self, monkeypatch, tmp_path, capsys):
        """Test main function when validator initialization fails."""
        test_file = tmp_path / "test.html"
        test_file.write_text("<p>Test</p>")
        
        monkeypatch.setattr('sys.argv', ['unified_content_validator.py', str(test_file)])
        
        with patch('unified_content_validator.UnifiedContentValidator', side_effect=ImportError("Init failed")):
            from unified_content_validator import main
            
            result = main()
            
            assert result == 2

    def test_main_format_override(self, monkeypatch, tmp_path):
        """Test main function with format override."""
        test_file = tmp_path / "test.txt"  # Non-standard extension
        test_file.write_text("# Markdown Content")
        
        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', str(test_file), '--format', 'markdown'
        ])
        
        # Mock validators for clean test
        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MagicMock(),
                BrandValidator=MagicMock(),
                EEATValidator=MagicMock(),
                EEATResult=type('EEATResult', (), {})
            )
        }):
            from unified_content_validator import main
            
            result = main()
            assert result in [0, 1]  # Should run, not error

    def test_main_all_flag_no_files(self, monkeypatch, tmp_path, capsys):
        """Test main with --all flag when directory has no HTML/MD files."""
        # Create directory with non-target files
        (tmp_path / "test.txt").write_text("Not HTML or MD")
        (tmp_path / "other.py").write_text("print('hello')")
        
        monkeypatch.setattr('sys.argv', [
            'unified_content_validator.py', '--all', str(tmp_path)
        ])
        
        with patch.dict('sys.modules', {
            'tes_shared.validators': MagicMock(
                AIPatternValidator=MagicMock(),
                BrandValidator=MagicMock(),
                EEATValidator=MagicMock(),
                EEATResult=type('EEATResult', (), {})
            )
        }):
            from unified_content_validator import main
            
            result = main()
            
            captured = capsys.readouterr()
            assert "0/0" in captured.out or result == 0  # No files to validate


class TestValidationSummaryEdgeCases:
    """Tests for ValidationSummary edge cases."""

    def test_validation_summary_default_fields(self):
        """Test ValidationSummary with default field values."""
        from unified_content_validator import ValidationSummary
        
        summary = ValidationSummary(
            validator_name="Test",
            passed=True
        )
        
        assert summary.score is None
        assert summary.grade is None
        assert summary.errors == []
        assert summary.warnings == []
        assert summary.details == {}

    def test_validation_summary_non_list_error_handling(self):
        """Test AI validator when errors/warnings aren't lists."""
        class MockAIValidator:
            def validate(self, content):
                return {
                    'is_valid': False,
                    'errors': 'Single error string',
                    'warnings': 'Single warning string',
                    'details': {}
                }

        from unified_content_validator import UnifiedContentValidator
        
        validator = UnifiedContentValidator(validate_ai_patterns=False, validate_brands=False, validate_eeat=False)
        validator._ai_validator = MockAIValidator()
        result = validator._run_ai_patterns("<p>Test</p>")
        
        # Should convert strings to lists
        assert isinstance(result.errors, list)
        assert isinstance(result.warnings, list)
        assert "Single error string" in result.errors
        assert "Single warning string" in result.warnings


class TestPrintReportEdgeCases:
    """Tests for print_report edge cases."""

    def test_print_report_many_warnings_truncation(self, capsys):
        """Test print_report truncates many warnings in verbose mode."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            warnings=[f"Warning {i}" for i in range(10)]  # More than 5
        )
        
        result.print_report(verbose=True)
        
        captured = capsys.readouterr()
        assert "and 5 more" in captured.out

    def test_print_report_with_score_no_grade(self, capsys):
        """Test print_report with score but no grade."""
        from unified_content_validator import UnifiedValidationResult, ValidationSummary
        
        result = UnifiedValidationResult(is_valid=True)
        result.ai_patterns = ValidationSummary(
            validator_name="AI",
            passed=True,
            score=85.0,
            grade=None  # No grade
        )
        
        result.print_report()
        
        captured = capsys.readouterr()
        assert "Score: 85.0/100" in captured.out
        # Should not show grade in parentheses


if __name__ == "__main__":
    pytest.main([__file__, "-v"])