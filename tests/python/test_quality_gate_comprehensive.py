#!/usr/bin/env python3
"""
Comprehensive tests for Quality Gate validation system.

Tests cover:
- ContentQualityGate initialization
- Validator type handling
- Score calculation
- Status determination
- Recommendations generation
- Edge cases and error handling
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
from dataclasses import dataclass
from typing import List, Optional
import sys

# Add src to path
SRC_DIR = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_DIR))

from validation.quality_gate import (
    ContentQualityGate, 
    QualityGateResult, 
    ValidatorResult, 
    ValidatorType, 
    QualityGateStatus,
    MockValidator,
    validate_content_brief
)


class TestValidatorTypeEnum:
    """Tests for ValidatorType enum."""

    def test_validator_types_defined(self):
        """Test all validator types are defined."""
        assert ValidatorType.EEAT.value == "eeat"
        assert ValidatorType.BRAND.value == "brand"
        assert ValidatorType.RESPONSIBLE_GAMBLING.value == "responsible_gambling"
        assert ValidatorType.SEO_META.value == "seo_meta"
        assert ValidatorType.AI_PATTERN.value == "ai_pattern"

    def test_validator_type_count(self):
        """Test expected number of validator types."""
        assert len(ValidatorType) == 5


class TestQualityGateStatusEnum:
    """Tests for QualityGateStatus enum."""

    def test_status_values(self):
        """Test status enum values."""
        assert QualityGateStatus.PASSED.value == "passed"
        assert QualityGateStatus.FAILED.value == "failed"
        assert QualityGateStatus.WARNING.value == "warning"


class TestValidatorResult:
    """Tests for ValidatorResult dataclass."""

    def test_create_validator_result(self):
        """Test creating ValidatorResult."""
        result = ValidatorResult(
            validator_type=ValidatorType.EEAT,
            passed=True,
            score=85.0,
            errors=[],
            warnings=["Minor issue"],
            details={"test": "data"},
            execution_time=0.5
        )
        
        assert result.validator_type == ValidatorType.EEAT
        assert result.passed is True
        assert result.score == 85.0
        assert len(result.warnings) == 1
        assert result.execution_time == 0.5

    def test_validator_result_default_values(self):
        """Test ValidatorResult default values."""
        result = ValidatorResult(
            validator_type=ValidatorType.BRAND,
            passed=False,
            score=50.0
        )
        
        assert result.errors == []
        assert result.warnings == []
        assert result.details is None
        assert result.execution_time == 0.0


class TestQualityGateResult:
    """Tests for QualityGateResult dataclass."""

    def test_create_quality_gate_result(self):
        """Test creating QualityGateResult."""
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=80.0
            )
        }
        
        result = QualityGateResult(
            passed=True,
            status=QualityGateStatus.PASSED,
            total_score=80.0,
            validator_results=validator_results,
            critical_errors=[],
            warnings=["Test warning"],
            execution_time=1.0
        )
        
        assert result.passed is True
        assert result.status == QualityGateStatus.PASSED
        assert result.total_score == 80.0
        assert len(result.warnings) == 1

    def test_summary_property_passed(self):
        """Test summary property for passed result."""
        result = QualityGateResult(
            passed=True,
            status=QualityGateStatus.PASSED,
            total_score=85.5,
            validator_results={
                ValidatorType.EEAT: ValidatorResult(
                    validator_type=ValidatorType.EEAT,
                    passed=True,
                    score=90.0
                )
            }
        )
        
        summary = result.summary
        assert "✅" in summary
        assert "PASSED" in summary
        assert "85.5" in summary

    def test_summary_property_failed(self):
        """Test summary property for failed result."""
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=40.0,
            critical_errors=["Critical error 1", "Critical error 2"],
            validator_results={
                ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                    validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                    passed=False,
                    score=30.0
                )
            }
        )
        
        summary = result.summary
        assert "❌" in summary
        assert "FAILED" in summary
        assert "Critical Errors" in summary

    def test_summary_truncates_errors(self):
        """Test summary truncates long error lists."""
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=30.0,
            critical_errors=[f"Error {i}" for i in range(10)],
            validator_results={}
        )
        
        summary = result.summary
        # Should show max 5 errors plus "and X more"
        assert "... and" in summary

    def test_summary_with_warnings(self):
        """Test summary shows warnings."""
        result = QualityGateResult(
            passed=True,
            status=QualityGateStatus.WARNING,
            total_score=70.0,
            warnings=["Warning 1", "Warning 2"],
            validator_results={}
        )
        
        summary = result.summary
        assert "Warnings" in summary


class TestContentQualityGateInit:
    """Tests for ContentQualityGate initialization."""

    def test_default_initialization(self):
        """Test default initialization."""
        gate = ContentQualityGate()
        
        assert gate.strict_mode is True
        assert gate.target_keywords == []
        assert gate.brand_name == "TopEndSports"
        assert gate.target_states == []

    def test_custom_initialization(self):
        """Test custom initialization."""
        gate = ContentQualityGate(
            strict_mode=False,
            target_keywords=["betting", "sports"],
            brand_name="CustomBrand",
            target_states=["NJ", "PA"]
        )
        
        assert gate.strict_mode is False
        assert gate.target_keywords == ["betting", "sports"]
        assert gate.brand_name == "CustomBrand"
        assert gate.target_states == ["NJ", "PA"]

    def test_validators_initialized(self):
        """Test validators are initialized."""
        gate = ContentQualityGate()
        
        assert hasattr(gate, 'validators')
        assert len(gate.validators) == 5

    def test_validator_weights_sum_to_100(self):
        """Test validator weights sum to 100."""
        total_weight = sum(ContentQualityGate.VALIDATOR_WEIGHTS.values())
        assert total_weight == 100


class TestContentQualityGateValidate:
    """Tests for ContentQualityGate.validate method."""

    def test_validate_simple_content(self):
        """Test validating simple HTML content."""
        gate = ContentQualityGate()
        content = "<html><body><h1>Test Content</h1></body></html>"
        
        result = gate.validate(content)
        
        assert isinstance(result, QualityGateResult)
        assert hasattr(result, 'passed')
        assert hasattr(result, 'total_score')
        assert result.execution_time >= 0

    def test_validate_with_page_url(self):
        """Test validating with page URL."""
        gate = ContentQualityGate()
        content = "<html><body>Test</body></html>"
        
        result = gate.validate(content, page_url="https://example.com/test")
        
        assert isinstance(result, QualityGateResult)

    def test_validate_empty_content(self):
        """Test validating empty content."""
        gate = ContentQualityGate()
        
        result = gate.validate("")
        
        assert isinstance(result, QualityGateResult)
        # Empty content should likely fail
        assert result.total_score is not None

    def test_validate_returns_all_validator_results(self):
        """Test that validation includes all validator types."""
        gate = ContentQualityGate()
        content = "<html><body>Content</body></html>"
        
        result = gate.validate(content)
        
        # Should have results for all validator types
        assert len(result.validator_results) == 5

    def test_validate_with_good_content(self):
        """Test validating well-formed content."""
        gate = ContentQualityGate()
        content = """
        <html>
        <head>
            <title>Best Sports Betting Sites | TopEndSports</title>
            <meta name="description" content="Expert reviews of sports betting sites. 21+ only. Gamble responsibly.">
        </head>
        <body>
            <h1>Best Sports Betting Sites 2024</h1>
            <p>Our expert team tests sites since 2010.</p>
            <p>Please gamble responsibly. Call 1-800-GAMBLER for help.</p>
            <p>Featured: DraftKings, FanDuel, BetMGM</p>
        </body>
        </html>
        """
        
        result = gate.validate(content)
        
        assert isinstance(result, QualityGateResult)
        assert result.total_score >= 0


class TestScoreCalculation:
    """Tests for score calculation."""

    def test_calculate_total_score_all_perfect(self):
        """Test total score calculation with all perfect scores."""
        gate = ContentQualityGate()
        
        validator_results = {
            vtype: ValidatorResult(
                validator_type=vtype,
                passed=True,
                score=100.0
            )
            for vtype in ValidatorType
        }
        
        total = gate._calculate_total_score(validator_results)
        
        assert total == 100.0

    def test_calculate_total_score_all_zero(self):
        """Test total score calculation with all zero scores."""
        gate = ContentQualityGate()
        
        validator_results = {
            vtype: ValidatorResult(
                validator_type=vtype,
                passed=False,
                score=0.0
            )
            for vtype in ValidatorType
        }
        
        total = gate._calculate_total_score(validator_results)
        
        assert total == 0.0

    def test_calculate_total_score_mixed(self):
        """Test total score calculation with mixed scores."""
        gate = ContentQualityGate()
        
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=80.0  # Weight: 30
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=True,
                score=100.0  # Weight: 20
            ),
            ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                passed=True,
                score=60.0  # Weight: 25
            ),
            ValidatorType.SEO_META: ValidatorResult(
                validator_type=ValidatorType.SEO_META,
                passed=True,
                score=70.0  # Weight: 15
            ),
            ValidatorType.AI_PATTERN: ValidatorResult(
                validator_type=ValidatorType.AI_PATTERN,
                passed=True,
                score=90.0  # Weight: 10
            ),
        }
        
        total = gate._calculate_total_score(validator_results)
        
        # Expected: (80*30 + 100*20 + 60*25 + 70*15 + 90*10) / 100
        # = (2400 + 2000 + 1500 + 1050 + 900) / 100 = 7850 / 100 = 78.5
        assert total == 78.5

    def test_calculate_score_with_missing_validators(self):
        """Test score calculation with missing validators."""
        gate = ContentQualityGate()
        
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=100.0
            )
        }
        
        total = gate._calculate_total_score(validator_results)
        
        # Only EEAT score contributes (100 * 30 / 100 = 30)
        assert total == 30.0


class TestStatusDetermination:
    """Tests for pass/fail status determination."""

    def test_determine_status_all_passed_strict(self):
        """Test status when all validators pass in strict mode."""
        gate = ContentQualityGate(strict_mode=True)
        
        validator_results = {
            vtype: ValidatorResult(
                validator_type=vtype,
                passed=True,
                score=80.0
            )
            for vtype in ValidatorType
        }
        
        passed, status = gate._determine_status(validator_results, [])
        
        assert passed is True
        assert status == QualityGateStatus.PASSED

    def test_determine_status_critical_failure(self):
        """Test status when critical validator fails."""
        gate = ContentQualityGate()
        
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=False,  # Critical failure
                score=40.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=True,
                score=80.0
            ),
            ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                passed=True,
                score=90.0
            ),
            ValidatorType.SEO_META: ValidatorResult(
                validator_type=ValidatorType.SEO_META,
                passed=True,
                score=70.0
            ),
            ValidatorType.AI_PATTERN: ValidatorResult(
                validator_type=ValidatorType.AI_PATTERN,
                passed=True,
                score=85.0
            ),
        }
        
        passed, status = gate._determine_status(validator_results, [])
        
        assert passed is False
        assert status == QualityGateStatus.FAILED

    def test_determine_status_responsible_gambling_failure(self):
        """Test status when responsible gambling validator fails."""
        gate = ContentQualityGate()
        
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=80.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=True,
                score=80.0
            ),
            ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                passed=False,  # Critical failure
                score=40.0
            ),
            ValidatorType.SEO_META: ValidatorResult(
                validator_type=ValidatorType.SEO_META,
                passed=True,
                score=70.0
            ),
            ValidatorType.AI_PATTERN: ValidatorResult(
                validator_type=ValidatorType.AI_PATTERN,
                passed=True,
                score=85.0
            ),
        }
        
        passed, status = gate._determine_status(validator_results, [])
        
        assert passed is False
        assert status == QualityGateStatus.FAILED

    def test_determine_status_non_critical_failure_non_strict(self):
        """Test status when non-critical validator fails in non-strict mode."""
        gate = ContentQualityGate(strict_mode=False)
        
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=80.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=False,  # Non-critical failure
                score=50.0
            ),
            ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                passed=True,
                score=90.0
            ),
            ValidatorType.SEO_META: ValidatorResult(
                validator_type=ValidatorType.SEO_META,
                passed=True,
                score=70.0
            ),
            ValidatorType.AI_PATTERN: ValidatorResult(
                validator_type=ValidatorType.AI_PATTERN,
                passed=True,
                score=85.0
            ),
        }
        
        passed, status = gate._determine_status(validator_results, [])
        
        assert passed is True
        assert status == QualityGateStatus.WARNING


class TestRecommendations:
    """Tests for recommendations generation."""

    def test_recommendations_for_eeat_failure(self):
        """Test recommendations when EEAT fails."""
        gate = ContentQualityGate()
        
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=50.0,
            validator_results={
                ValidatorType.EEAT: ValidatorResult(
                    validator_type=ValidatorType.EEAT,
                    passed=False,
                    score=40.0
                )
            }
        )
        
        recommendations = gate.get_recommendations(result)
        
        assert len(recommendations) > 0
        assert any("E-E-A-T" in r for r in recommendations)

    def test_recommendations_for_brand_failure(self):
        """Test recommendations when brand validation fails."""
        gate = ContentQualityGate()
        
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=60.0,
            validator_results={
                ValidatorType.BRAND: ValidatorResult(
                    validator_type=ValidatorType.BRAND,
                    passed=False,
                    score=50.0
                )
            }
        )
        
        recommendations = gate.get_recommendations(result)
        
        assert len(recommendations) > 0
        assert any("brand" in r.lower() for r in recommendations)

    def test_recommendations_for_responsible_gambling_failure(self):
        """Test recommendations when responsible gambling fails."""
        gate = ContentQualityGate()
        
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=50.0,
            validator_results={
                ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                    validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                    passed=False,
                    score=30.0
                )
            }
        )
        
        recommendations = gate.get_recommendations(result)
        
        assert len(recommendations) > 0
        assert any("responsible gambling" in r.lower() for r in recommendations)

    def test_recommendations_for_multiple_failures(self):
        """Test recommendations for multiple validator failures."""
        gate = ContentQualityGate()
        
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=30.0,
            validator_results={
                ValidatorType.EEAT: ValidatorResult(
                    validator_type=ValidatorType.EEAT,
                    passed=False,
                    score=40.0
                ),
                ValidatorType.SEO_META: ValidatorResult(
                    validator_type=ValidatorType.SEO_META,
                    passed=False,
                    score=30.0
                ),
                ValidatorType.AI_PATTERN: ValidatorResult(
                    validator_type=ValidatorType.AI_PATTERN,
                    passed=False,
                    score=20.0
                )
            }
        )
        
        recommendations = gate.get_recommendations(result)
        
        assert len(recommendations) >= 3

    def test_no_recommendations_all_passed(self):
        """Test no recommendations when all validators pass."""
        gate = ContentQualityGate()
        
        result = QualityGateResult(
            passed=True,
            status=QualityGateStatus.PASSED,
            total_score=90.0,
            validator_results={
                vtype: ValidatorResult(
                    validator_type=vtype,
                    passed=True,
                    score=90.0
                )
                for vtype in ValidatorType
            }
        )
        
        recommendations = gate.get_recommendations(result)
        
        assert len(recommendations) == 0


class TestMockValidator:
    """Tests for MockValidator class."""

    def test_mock_validator_creation(self):
        """Test creating MockValidator."""
        mock = MockValidator("TestValidator")
        assert mock.name == "TestValidator"

    def test_mock_validator_validate_ai_pattern(self):
        """Test MockValidator validation for AI pattern type."""
        mock = MockValidator("AIPattern")
        result = mock.validate("test content")
        
        assert "total_score" in result
        assert "issues" in result
        assert "passed" in result

    def test_mock_validator_validate_other_types(self):
        """Test MockValidator validation for other types."""
        mock = MockValidator("EEAT")
        result = mock.validate("test content")
        
        assert hasattr(result, 'valid')
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'score')
        assert result.score.total == 75.0


class TestValidateContentBriefFunction:
    """Tests for convenience function validate_content_brief."""

    def test_validate_content_brief_basic(self):
        """Test basic usage of validate_content_brief."""
        content = "<html><body>Test</body></html>"
        result = validate_content_brief(content)
        
        assert isinstance(result, QualityGateResult)

    def test_validate_content_brief_with_kwargs(self):
        """Test validate_content_brief with additional arguments."""
        content = "<html><body>Test</body></html>"
        result = validate_content_brief(
            content,
            strict_mode=False,
            target_keywords=["test"],
            brand_name="CustomBrand"
        )
        
        assert isinstance(result, QualityGateResult)


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_validate_none_content(self):
        """Test validation handles None gracefully."""
        gate = ContentQualityGate()
        
        # Passing None might cause issues
        try:
            result = gate.validate(None)
            # If it doesn't crash, check result is valid
            assert isinstance(result, QualityGateResult)
        except (TypeError, AttributeError):
            # Expected if None is not handled
            pass

    def test_validate_very_long_content(self):
        """Test validation of very long content."""
        gate = ContentQualityGate()
        content = "<html><body>" + "Test content. " * 10000 + "</body></html>"
        
        result = gate.validate(content)
        
        assert isinstance(result, QualityGateResult)
        # Should complete without timeout

    def test_validate_unicode_content(self):
        """Test validation of Unicode content."""
        gate = ContentQualityGate()
        content = """
        <html><body>
        <h1>日本語テスト</h1>
        <p>测试中文内容</p>
        <p>Emoji: 🎰🏈⚽</p>
        </body></html>
        """
        
        result = gate.validate(content)
        
        assert isinstance(result, QualityGateResult)

    def test_validate_malformed_html(self):
        """Test validation of malformed HTML."""
        gate = ContentQualityGate()
        content = "<html><body><p>Unclosed paragraph<div>Mixed tags</body>"
        
        result = gate.validate(content)
        
        # Should not crash on malformed HTML
        assert isinstance(result, QualityGateResult)

    def test_validate_plain_text_not_html(self):
        """Test validation of plain text (not HTML)."""
        gate = ContentQualityGate()
        content = "This is plain text content without any HTML tags."
        
        result = gate.validate(content)
        
        assert isinstance(result, QualityGateResult)

    def test_validator_execution_time_tracked(self):
        """Test that execution time is tracked."""
        gate = ContentQualityGate()
        content = "<html><body>Test</body></html>"
        
        result = gate.validate(content)
        
        assert result.execution_time >= 0
        # Individual validators should also have execution time
        for vr in result.validator_results.values():
            assert vr.execution_time >= 0


class TestMinimumPassingScores:
    """Tests for minimum passing score configuration."""

    def test_minimum_scores_defined(self):
        """Test minimum passing scores are defined for all validators."""
        for vtype in ValidatorType:
            assert vtype in ContentQualityGate.MINIMUM_PASSING_SCORES

    def test_responsible_gambling_has_highest_threshold(self):
        """Test responsible gambling has highest minimum score."""
        scores = ContentQualityGate.MINIMUM_PASSING_SCORES
        rg_score = scores[ValidatorType.RESPONSIBLE_GAMBLING]
        
        # RG should be highest (80)
        for vtype, score in scores.items():
            if vtype != ValidatorType.RESPONSIBLE_GAMBLING:
                assert rg_score >= score


class TestValidatorWeights:
    """Tests for validator weight configuration."""

    def test_weights_defined_for_all_validators(self):
        """Test weights are defined for all validators."""
        for vtype in ValidatorType:
            assert vtype in ContentQualityGate.VALIDATOR_WEIGHTS

    def test_weights_are_positive(self):
        """Test all weights are positive."""
        for weight in ContentQualityGate.VALIDATOR_WEIGHTS.values():
            assert weight > 0

    def test_eeat_has_highest_weight(self):
        """Test E-E-A-T has highest weight (YMYL content)."""
        weights = ContentQualityGate.VALIDATOR_WEIGHTS
        eeat_weight = weights[ValidatorType.EEAT]
        
        assert eeat_weight == max(weights.values())
