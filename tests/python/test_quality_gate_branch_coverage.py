#!/usr/bin/env python3
"""
Branch coverage tests for src/validation/quality_gate.py.

Targets remaining missed lines/branches:
  Lines 320-323: _run_validator SEO_META path
  Lines 343-347: _run_validator AI_PATTERN path (with issues)
  Line 360:      _run_validator else (unknown validator type) path
  Line 426->416: get_recommendations SEO_META and AI_PATTERN failure branches

Lines 31->34, 40-44: sys.path insertion + ImportError fallback (env-dependent, skip)
Lines 190-192:        except NameError fallback (env-dependent, skip)
"""

import sys
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from validation.quality_gate import (
    ContentQualityGate,
    QualityGateResult,
    QualityGateStatus,
    ValidatorResult,
    ValidatorType,
)


# ---------------------------------------------------------------------------
# Helpers: mock validators with the right result shape
# ---------------------------------------------------------------------------

def _make_seo_meta_validator(score=78.0, issues=None):
    """Build a mock that looks like SEOMetaValidator.validate() result."""
    if issues is None:
        issues = []
    result = MagicMock()
    result.score = score
    result.issues = issues
    validator = MagicMock()
    validator.validate.return_value = result
    return validator


def _make_ai_pattern_validator(total_score=72.0, issues=None):
    """Build a mock that returns the dict shape AIPatternValidator returns."""
    if issues is None:
        issues = {}
    validator = MagicMock()
    validator.validate.return_value = {
        'total_score': total_score,
        'issues': issues,
        'passed': total_score >= 60,
    }
    return validator


def _make_severity(value):
    """Create a mock severity object with a .value attribute."""
    sev = MagicMock()
    sev.value = value
    return sev


def _make_issue(message, severity_value):
    """Create a mock issue object."""
    issue = MagicMock()
    issue.message = message
    issue.severity = _make_severity(severity_value)
    return issue


# ---------------------------------------------------------------------------
# _run_validator: SEO_META path (lines 315-330)
# ---------------------------------------------------------------------------

class TestRunValidatorSEOMeta:
    """Cover lines 320-323: _run_validator for SEO_META validator type."""

    def test_seo_meta_passing_score(self):
        """SEO_META validator with score above threshold -> passed=True."""
        gate = ContentQualityGate()
        mock_validator = _make_seo_meta_validator(score=85.0, issues=[])

        result = gate._run_validator(
            ValidatorType.SEO_META,
            mock_validator,
            "Sample content with title and meta",
            page_url="https://example.com/page"
        )

        assert result.validator_type == ValidatorType.SEO_META
        assert result.passed is True
        assert result.score == 85.0
        assert result.errors == []
        assert result.warnings == []

    def test_seo_meta_failing_score(self):
        """SEO_META validator with score below threshold -> passed=False."""
        gate = ContentQualityGate()
        mock_validator = _make_seo_meta_validator(score=30.0, issues=[])

        result = gate._run_validator(
            ValidatorType.SEO_META,
            mock_validator,
            "Content with poor SEO",
            page_url=None
        )

        assert result.validator_type == ValidatorType.SEO_META
        assert result.passed is False
        assert result.score == 30.0

    def test_seo_meta_with_error_issues(self):
        """SEO_META with error-severity issues -> errors list populated."""
        gate = ContentQualityGate()
        err_issue = _make_issue("Title tag missing", "error")
        warn_issue = _make_issue("Meta description too short", "warning")
        mock_validator = _make_seo_meta_validator(
            score=45.0,
            issues=[err_issue, warn_issue]
        )

        result = gate._run_validator(
            ValidatorType.SEO_META,
            mock_validator,
            "Page without title",
            page_url="https://example.com"
        )

        assert result.validator_type == ValidatorType.SEO_META
        assert "Title tag missing" in result.errors
        assert "Meta description too short" in result.warnings

    def test_seo_meta_validator_called_with_page_url(self):
        """SEO_META _run_validator passes page_url to validator.validate()."""
        gate = ContentQualityGate()
        mock_validator = _make_seo_meta_validator(score=70.0, issues=[])

        gate._run_validator(
            ValidatorType.SEO_META,
            mock_validator,
            "Some content",
            page_url="https://test.com/article"
        )

        mock_validator.validate.assert_called_once_with(
            "Some content",
            page_url="https://test.com/article"
        )


# ---------------------------------------------------------------------------
# _run_validator: AI_PATTERN path (lines 332-356)
# ---------------------------------------------------------------------------

class TestRunValidatorAIPattern:
    """Cover lines 343-347: _run_validator for AI_PATTERN validator type."""

    def test_ai_pattern_passing_score_no_issues(self):
        """AI_PATTERN with good score and no issues -> passed=True, empty errors."""
        gate = ContentQualityGate()
        mock_validator = _make_ai_pattern_validator(total_score=80.0, issues={})

        result = gate._run_validator(
            ValidatorType.AI_PATTERN,
            mock_validator,
            "Well-written authentic content",
            page_url=None
        )

        assert result.validator_type == ValidatorType.AI_PATTERN
        assert result.passed is True
        assert result.score == 80.0
        assert result.errors == []
        assert result.warnings == []

    def test_ai_pattern_with_high_severity_issues(self):
        """AI_PATTERN with high-severity issues -> errors list populated."""
        gate = ContentQualityGate()
        issues = {
            'formulaic_phrases': [
                {'severity': 'high', 'message': 'Overused phrase: "It is worth noting"'},
                {'severity': 'high', 'message': 'Overused phrase: "In conclusion"'},
            ]
        }
        mock_validator = _make_ai_pattern_validator(total_score=35.0, issues=issues)

        result = gate._run_validator(
            ValidatorType.AI_PATTERN,
            mock_validator,
            "It is worth noting that in conclusion...",
            page_url=None
        )

        assert result.validator_type == ValidatorType.AI_PATTERN
        assert result.passed is False
        assert len(result.errors) == 2
        assert any('formulaic_phrases' in e for e in result.errors)
        assert any('It is worth noting' in e for e in result.errors)

    def test_ai_pattern_with_low_severity_issues(self):
        """AI_PATTERN with low-severity issues -> warnings list populated."""
        gate = ContentQualityGate()
        issues = {
            'colon_headings': [
                {'severity': 'low', 'message': 'Heading uses colon pattern'},
            ]
        }
        mock_validator = _make_ai_pattern_validator(total_score=65.0, issues=issues)

        result = gate._run_validator(
            ValidatorType.AI_PATTERN,
            mock_validator,
            "Content with minor AI patterns",
            page_url=None
        )

        assert result.validator_type == ValidatorType.AI_PATTERN
        assert result.passed is True  # 65 >= minimum
        assert len(result.warnings) == 1
        assert 'colon_headings' in result.warnings[0]
        assert result.errors == []

    def test_ai_pattern_mixed_severities(self):
        """AI_PATTERN with mixed high/low issues -> both errors and warnings."""
        gate = ContentQualityGate()
        issues = {
            'formulaic': [
                {'severity': 'high', 'message': 'Critical AI pattern'},
            ],
            'style': [
                {'severity': 'medium', 'message': 'Style issue'},
            ]
        }
        mock_validator = _make_ai_pattern_validator(total_score=40.0, issues=issues)

        result = gate._run_validator(
            ValidatorType.AI_PATTERN,
            mock_validator,
            "Content with many AI patterns",
            page_url=None
        )

        assert len(result.errors) == 1  # high severity
        assert len(result.warnings) == 1  # non-high severity


# ---------------------------------------------------------------------------
# _run_validator: else path (line 358-365)
# ---------------------------------------------------------------------------

class TestRunValidatorElsePath:
    """Cover line 360: _run_validator else branch for unknown validator type."""

    def test_else_branch_with_unknown_type(self):
        """When validator_type is not one of the known types, else branch fires.

        We create a fake ValidatorType-like value and inject it into
        _run_validator directly to trigger the else: branch.
        """
        gate = ContentQualityGate()
        mock_validator = MagicMock()

        # Create a fake enum-like object that won't match any elif
        class FakeType:
            value = "fake_type"

        fake_type = FakeType()

        result = gate._run_validator(
            fake_type,
            mock_validator,
            "Any content",
            page_url=None
        )

        # else branch: returns mock result with score 75 and a warning
        assert result.passed is True
        assert result.score == 75.0
        assert result.errors == []
        assert len(result.warnings) == 1
        assert "Mock" in result.warnings[0]
        assert "fake_type" in result.warnings[0]


# ---------------------------------------------------------------------------
# get_recommendations: SEO_META and AI_PATTERN failure branches (line 426->416)
# ---------------------------------------------------------------------------

class TestRecommendationsSEOMetaAndAIPattern:
    """Cover line 426->416: SEO_META and AI_PATTERN recommendation branches."""

    def test_recommendations_for_seo_meta_failure_only(self):
        """get_recommendations with only SEO_META failing -> SEO recommendation returned."""
        gate = ContentQualityGate()

        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=55.0,
            validator_results={
                ValidatorType.SEO_META: ValidatorResult(
                    validator_type=ValidatorType.SEO_META,
                    passed=False,
                    score=40.0
                )
            }
        )

        recommendations = gate.get_recommendations(result)

        assert len(recommendations) == 1
        assert "title tag" in recommendations[0].lower() or "Optimize" in recommendations[0]
        assert "50-60" in recommendations[0]

    def test_recommendations_for_ai_pattern_failure_only(self):
        """get_recommendations with only AI_PATTERN failing -> AI recommendation returned."""
        gate = ContentQualityGate()

        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=60.0,
            validator_results={
                ValidatorType.AI_PATTERN: ValidatorResult(
                    validator_type=ValidatorType.AI_PATTERN,
                    passed=False,
                    score=35.0
                )
            }
        )

        recommendations = gate.get_recommendations(result)

        assert len(recommendations) == 1
        assert "formulaic" in recommendations[0].lower() or "AI" in recommendations[0] or "authentic" in recommendations[0]

    def test_recommendations_for_seo_meta_and_ai_pattern_both_failing(self):
        """Both SEO_META and AI_PATTERN failing -> both recommendations returned."""
        gate = ContentQualityGate()

        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=35.0,
            validator_results={
                ValidatorType.SEO_META: ValidatorResult(
                    validator_type=ValidatorType.SEO_META,
                    passed=False,
                    score=30.0
                ),
                ValidatorType.AI_PATTERN: ValidatorResult(
                    validator_type=ValidatorType.AI_PATTERN,
                    passed=False,
                    score=25.0
                )
            }
        )

        recommendations = gate.get_recommendations(result)

        assert len(recommendations) == 2

    def test_recommendations_all_five_validator_types_failing(self):
        """All 5 validators failing -> all 5 recommendations returned."""
        gate = ContentQualityGate()

        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=20.0,
            validator_results={
                ValidatorType.EEAT: ValidatorResult(
                    validator_type=ValidatorType.EEAT,
                    passed=False,
                    score=20.0
                ),
                ValidatorType.BRAND: ValidatorResult(
                    validator_type=ValidatorType.BRAND,
                    passed=False,
                    score=20.0
                ),
                ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                    validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                    passed=False,
                    score=20.0
                ),
                ValidatorType.SEO_META: ValidatorResult(
                    validator_type=ValidatorType.SEO_META,
                    passed=False,
                    score=20.0
                ),
                ValidatorType.AI_PATTERN: ValidatorResult(
                    validator_type=ValidatorType.AI_PATTERN,
                    passed=False,
                    score=20.0
                )
            }
        )

        recommendations = gate.get_recommendations(result)

        assert len(recommendations) == 5
        texts = ' '.join(recommendations).lower()
        assert 'e-e-a-t' in texts
        assert 'brand' in texts
        assert 'responsible gambling' in texts
        assert 'title tag' in texts or 'meta' in texts or 'optimize' in texts
        assert 'formulaic' in texts or 'authentic' in texts


class TestRecommendationsUnknownValidatorType:
    """Cover branch 426->416: unknown validator type falls through all elif conditions."""

    def test_recommendations_no_match_on_unknown_type(self):
        """A validator_result with an unknown type and passed=False hits the
        elif AI_PATTERN False branch and falls through without appending.

        Branch 426->416: elif ValidatorType.AI_PATTERN is False at line 426,
        flow falls through to end of if-block and loops back to for at line 416.
        """
        gate = ContentQualityGate()

        # Create a fake ValidatorType-like value
        class FakeValidatorType:
            value = "unknown_type"
            name = "UNKNOWN"

        fake_type = FakeValidatorType()

        # We need a ValidatorResult-like object with passed=False
        # but with a validator_type that doesn't match any known enum value
        fake_result = MagicMock()
        fake_result.passed = False
        fake_result.validator_type = fake_type

        # Build the validator_results dict with our fake type
        fake_gate_result = MagicMock()
        fake_gate_result.validator_results = {fake_type: fake_result}

        recommendations = gate.get_recommendations(fake_gate_result)

        # No matching elif -> no recommendation appended
        assert recommendations == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
