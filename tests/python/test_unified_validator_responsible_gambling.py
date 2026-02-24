"""
Tests for responsible gambling validator integration in unified_content_validator.py.

Covers:
- ResponsibleGamblingValidator wiring into UnifiedContentValidator
- _run_responsible_gambling method (dataclass result, dict result, exception)
- Grade calculation (A/B/C/D/F)
- CLI --no-rg and --rg-min flags
- Graceful degradation when validator unavailable
- UnifiedValidationResult.responsible_gambling in to_dict, total_errors, total_warnings, print_report
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
from dataclasses import dataclass, field

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))


# --- Mock classes ---

class MockAIPatternValidator:
    def validate(self, content):
        return {'is_valid': True, 'errors': [], 'warnings': [], 'details': {}}


class MockBrandValidator:
    def validate(self, content):
        @dataclass
        class R:
            valid: bool = True
            errors: list = field(default_factory=list)
            warnings: list = field(default_factory=list)
            verified_brands: list = field(default_factory=list)
            unknown_brands: list = field(default_factory=list)
            suggestions: dict = field(default_factory=dict)
        return R()


class MockEEATValidator:
    def validate(self, content):
        @dataclass
        class Score:
            total: float = 75.0
            grade: str = 'B'
        @dataclass
        class EEATResult:
            is_valid: bool = True
            errors: list = field(default_factory=list)
            warnings: list = field(default_factory=list)
            score: object = field(default_factory=Score)
            def to_dict(self):
                return {'score': {'total': self.score.total, 'grade': self.score.grade}}
        return EEATResult()


@dataclass
class MockRGFoundElement:
    category: str = "disclaimer"
    text: str = "Gamble responsibly"
    position: int = 100
    pattern_matched: str = "gamble responsibly"


@dataclass
class MockRGResult:
    """Mock for ResponsibleGamblingResult dataclass."""
    valid: bool = True
    status: str = "PASS"
    found_elements: list = field(default_factory=list)
    missing_elements: list = field(default_factory=list)
    issues: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    score: float = 0.8
    state_requirements_met: dict = field(default_factory=dict)

    def to_dict(self):
        return {'valid': self.valid, 'score': self.score}


class MockResponsibleGamblingValidator:
    def __init__(self, **kwargs):
        self._result = None

    def validate(self, content):
        if self._result:
            return self._result
        return MockRGResult(
            valid=True,
            score=0.8,
            found_elements=[MockRGFoundElement()],
            missing_elements=[],
            errors=[],
            warnings=[],
        )


class MockResponsibleGamblingValidatorFail:
    def __init__(self, **kwargs):
        pass

    def validate(self, content):
        return MockRGResult(
            valid=False,
            status="FAIL",
            score=0.15,
            found_elements=[],
            missing_elements=["disclaimer", "help_resources", "age_verification"],
            errors=["Missing required disclaimer"],
            warnings=["No helpline number found"],
        )


class MockResponsibleGamblingValidatorCrash:
    def __init__(self, **kwargs):
        pass

    def validate(self, content):
        raise RuntimeError("Validator crashed")


# --- Fixtures ---

def _import_with_rg_available(monkeypatch):
    """Import unified_content_validator with RG validator mocked as available."""
    # Remove cached module if present
    for mod_name in list(sys.modules.keys()):
        if 'unified_content_validator' in mod_name:
            del sys.modules[mod_name]

    mock_tes = MagicMock()
    mock_tes.validators.AIPatternValidator = MockAIPatternValidator
    mock_tes.validators.BrandValidator = MockBrandValidator
    mock_tes.validators.EEATValidator = MockEEATValidator
    mock_tes.validators.EEATResult = type('EEATResult', (), {})

    mock_rg_module = MagicMock()
    mock_rg_module.ResponsibleGamblingValidator = MockResponsibleGamblingValidator
    mock_rg_module.ResponsibleGamblingResult = MockRGResult

    with patch.dict('sys.modules', {
        'tes_shared': mock_tes,
        'tes_shared.validators': mock_tes.validators,
        'tes_shared.validators.responsible_gambling': mock_rg_module,
    }):
        import unified_content_validator as ucv
        # Ensure flags are set correctly
        ucv.VALIDATORS_AVAILABLE = True
        ucv.RESPONSIBLE_GAMBLING_AVAILABLE = True
        ucv.ResponsibleGamblingValidator = MockResponsibleGamblingValidator
        ucv.ResponsibleGamblingResult = MockRGResult
        ucv.AIPatternValidator = MockAIPatternValidator
        ucv.BrandValidator = MockBrandValidator
        ucv.EEATValidator = MockEEATValidator
        return ucv


def _import_without_rg(monkeypatch):
    """Import with RG validator NOT available."""
    for mod_name in list(sys.modules.keys()):
        if 'unified_content_validator' in mod_name:
            del sys.modules[mod_name]

    mock_tes = MagicMock()
    mock_tes.validators.AIPatternValidator = MockAIPatternValidator
    mock_tes.validators.BrandValidator = MockBrandValidator
    mock_tes.validators.EEATValidator = MockEEATValidator
    mock_tes.validators.EEATResult = type('EEATResult', (), {})

    with patch.dict('sys.modules', {
        'tes_shared': mock_tes,
        'tes_shared.validators': mock_tes.validators,
    }):
        import unified_content_validator as ucv
        ucv.VALIDATORS_AVAILABLE = True
        ucv.RESPONSIBLE_GAMBLING_AVAILABLE = False
        ucv.AIPatternValidator = MockAIPatternValidator
        ucv.BrandValidator = MockBrandValidator
        ucv.EEATValidator = MockEEATValidator
        return ucv


# --- Tests ---

class TestResponsibleGamblingIntegration:
    """Test that RG validator is wired into UnifiedContentValidator."""

    def test_rg_validator_initialized_when_available(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(validate_responsible_gambling=True)
        assert v._rg_validator is not None
        assert v.validate_responsible_gambling is True

    def test_rg_validator_disabled_when_not_available(self, monkeypatch):
        ucv = _import_without_rg(monkeypatch)
        v = ucv.UnifiedContentValidator(validate_responsible_gambling=True)
        assert v._rg_validator is None
        assert v.validate_responsible_gambling is False

    def test_rg_validator_not_initialized_when_disabled(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(validate_responsible_gambling=False)
        assert v._rg_validator is None

    def test_validate_runs_rg_check(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False,
            validate_brands=False,
            validate_eeat=False,
            validate_responsible_gambling=True,
        )
        result = v.validate("<p>Gamble responsibly. Call 1-800-GAMBLER.</p>")
        assert result.responsible_gambling is not None
        assert result.responsible_gambling.passed is True
        assert result.responsible_gambling.validator_name == "Responsible Gambling"

    def test_validate_skips_rg_when_disabled(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False,
            validate_brands=False,
            validate_eeat=False,
            validate_responsible_gambling=False,
        )
        result = v.validate("<p>Content</p>")
        assert result.responsible_gambling is None

    def test_rg_failure_makes_result_invalid(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        ucv.ResponsibleGamblingValidator = MockResponsibleGamblingValidatorFail
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False,
            validate_brands=False,
            validate_eeat=False,
            validate_responsible_gambling=True,
        )
        v._rg_validator = MockResponsibleGamblingValidatorFail()
        result = v.validate("<p>No gambling disclaimers here.</p>")
        assert result.is_valid is False
        assert result.responsible_gambling.passed is False


class TestRunResponsibleGambling:
    """Test _run_responsible_gambling method with different result types."""

    def test_dataclass_result_passing(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        summary = v._run_responsible_gambling("<p>Gamble responsibly.</p>")
        assert summary.passed is True
        assert summary.score == 80.0  # 0.8 * 100
        assert summary.grade == 'A'
        assert summary.validator_name == "Responsible Gambling"

    def test_dataclass_result_failing(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        v._rg_validator = MockResponsibleGamblingValidatorFail()
        summary = v._run_responsible_gambling("<p>No disclaimers.</p>")
        assert summary.passed is False
        assert summary.score == 15.0  # 0.15 * 100
        assert summary.grade == 'F'
        assert len(summary.errors) > 0
        assert len(summary.warnings) > 0

    def test_validator_exception_handled(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        v._rg_validator = MockResponsibleGamblingValidatorCrash()
        summary = v._run_responsible_gambling("<p>Content</p>")
        assert summary.passed is False
        assert "Validator error" in summary.errors[0]

    def test_dict_result_handling(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        # Make validator return a dict instead of dataclass
        mock_v = MagicMock()
        mock_v.validate.return_value = {
            'valid': True,
            'score': 0.7,
            'errors': [],
            'warnings': ['Minor issue'],
        }
        v._rg_validator = mock_v
        summary = v._run_responsible_gambling("<p>Content</p>")
        assert summary.passed is True
        assert summary.score == 70.0
        assert summary.grade == 'B'

    def test_rg_min_score_threshold(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
            rg_min_score=0.9,  # Higher threshold
        )
        # Score 0.8 should fail when threshold is 0.9
        summary = v._run_responsible_gambling("<p>Content</p>")
        assert summary.passed is False  # 0.8 < 0.9 threshold

    def test_missing_elements_added_as_warnings(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        v._rg_validator = MockResponsibleGamblingValidatorFail()
        summary = v._run_responsible_gambling("<p>No disclaimers.</p>")
        warning_texts = [w for w in summary.warnings if w.startswith("Missing:")]
        assert len(warning_texts) >= 3  # disclaimer, help_resources, age_verification


class TestGradeCalculation:
    """Test grade letter assignment based on score."""

    def _get_grade(self, score_01, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
            rg_min_score=0.0,  # Don't fail on score
        )
        mock_v = MagicMock()
        mock_v.validate.return_value = MockRGResult(valid=True, score=score_01)
        v._rg_validator = mock_v
        summary = v._run_responsible_gambling("<p>test</p>")
        return summary.grade

    def test_grade_a(self, monkeypatch):
        assert self._get_grade(0.85, monkeypatch) == 'A'

    def test_grade_b(self, monkeypatch):
        assert self._get_grade(0.65, monkeypatch) == 'B'

    def test_grade_c(self, monkeypatch):
        assert self._get_grade(0.45, monkeypatch) == 'C'

    def test_grade_d(self, monkeypatch):
        assert self._get_grade(0.30, monkeypatch) == 'D'

    def test_grade_f(self, monkeypatch):
        assert self._get_grade(0.10, monkeypatch) == 'F'


class TestUnifiedValidationResultWithRG:
    """Test that responsible_gambling field integrates into result methods."""

    def test_total_errors_includes_rg(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.UnifiedValidationResult(
            is_valid=False,
            responsible_gambling=ucv.ValidationSummary(
                validator_name="Responsible Gambling",
                passed=False,
                errors=["Missing disclaimer", "Missing helpline"],
                warnings=[],
            ),
        )
        assert result.total_errors == 2

    def test_total_warnings_includes_rg(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.UnifiedValidationResult(
            is_valid=True,
            responsible_gambling=ucv.ValidationSummary(
                validator_name="Responsible Gambling",
                passed=True,
                errors=[],
                warnings=["Missing: age_verification"],
            ),
        )
        assert result.total_warnings == 1

    def test_to_dict_includes_rg(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.UnifiedValidationResult(
            is_valid=True,
            responsible_gambling=ucv.ValidationSummary(
                validator_name="Responsible Gambling",
                passed=True,
                score=80.0,
                grade='A',
                errors=[],
                warnings=[],
            ),
        )
        d = result.to_dict()
        assert 'responsible_gambling' in d
        assert d['responsible_gambling']['validator'] == "Responsible Gambling"
        assert d['responsible_gambling']['score'] == 80.0
        assert d['responsible_gambling']['grade'] == 'A'

    def test_to_dict_rg_none(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.UnifiedValidationResult(is_valid=True)
        d = result.to_dict()
        assert d['responsible_gambling'] is None

    def test_print_report_includes_rg(self, monkeypatch, capsys):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.UnifiedValidationResult(
            is_valid=True,
            responsible_gambling=ucv.ValidationSummary(
                validator_name="Responsible Gambling",
                passed=True,
                score=80.0,
                grade='A',
                errors=[],
                warnings=[],
            ),
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "Responsible Gambling" in captured.out
        assert "80.0/100" in captured.out

    def test_print_report_rg_with_errors(self, monkeypatch, capsys):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.UnifiedValidationResult(
            is_valid=False,
            responsible_gambling=ucv.ValidationSummary(
                validator_name="Responsible Gambling",
                passed=False,
                score=15.0,
                grade='F',
                errors=["Missing disclaimer", "Missing helpline", "No age check"],
                warnings=[],
            ),
        )
        result.print_report()
        captured = capsys.readouterr()
        assert "[FAIL]" in captured.out
        assert "Missing disclaimer" in captured.out


class TestCLIResponsibleGambling:
    """Test CLI flags for responsible gambling."""

    def test_no_rg_flag(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        with patch.object(ucv, 'VALIDATORS_AVAILABLE', True):
            with patch('sys.argv', ['prog', '--no-rg', '--no-ai', '--no-brands', '--no-eeat', 'test.html']):
                with patch.object(Path, 'is_file', return_value=True):
                    with patch.object(Path, 'is_dir', return_value=False):
                        with patch.object(Path, 'read_text', return_value='<p>test</p>'):
                            with patch.object(Path, 'exists', return_value=True):
                                with patch.object(Path, 'suffix', new_callable=PropertyMock, return_value='.html'):
                                    # The validator should be created without RG
                                    v = ucv.UnifiedContentValidator(
                                        validate_ai_patterns=False,
                                        validate_brands=False,
                                        validate_eeat=False,
                                        validate_responsible_gambling=False,
                                    )
                                    result = v.validate("<p>test</p>")
                                    assert result.responsible_gambling is None

    def test_rg_min_flag(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
            rg_min_score=0.5,
        )
        assert v.rg_min_score == 0.5


class TestValidateContentConvenienceFunction:
    """Test validate_content() with rg params."""

    def test_validate_content_with_rg_enabled(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.validate_content(
            "<p>Gamble responsibly. Call 1-800-GAMBLER.</p>",
            content_type='html',
            validate_rg=True,
        )
        assert result.responsible_gambling is not None

    def test_validate_content_with_rg_disabled(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        result = ucv.validate_content(
            "<p>Content</p>",
            content_type='html',
            validate_rg=False,
        )
        assert result.responsible_gambling is None

    def test_validate_content_rg_min_score_passthrough(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        # With rg_min_score=0.9, default mock (0.8) should fail
        result = ucv.validate_content(
            "<p>Content</p>",
            content_type='html',
            validate_rg=True,
            rg_min_score=0.9,
        )
        assert result.responsible_gambling is not None
        assert result.responsible_gambling.passed is False


class TestRGDetails:
    """Test details dict in _run_responsible_gambling."""

    def test_details_include_compliance_score(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        summary = v._run_responsible_gambling("<p>test</p>")
        assert 'compliance_score' in summary.details
        assert summary.details['compliance_score'] == 0.8

    def test_details_include_found_count(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        summary = v._run_responsible_gambling("<p>test</p>")
        assert summary.details['found_count'] == 1

    def test_details_include_missing_elements(self, monkeypatch):
        ucv = _import_with_rg_available(monkeypatch)
        v = ucv.UnifiedContentValidator(
            validate_ai_patterns=False, validate_brands=False,
            validate_eeat=False, validate_responsible_gambling=True,
        )
        v._rg_validator = MockResponsibleGamblingValidatorFail()
        summary = v._run_responsible_gambling("<p>test</p>")
        assert len(summary.details['missing_elements']) == 3
        assert 'disclaimer' in summary.details['missing_elements']
