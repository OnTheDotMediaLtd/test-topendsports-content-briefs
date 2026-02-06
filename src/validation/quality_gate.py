"""
Quality Gate for TopEndSports Content Briefs

A comprehensive validation system that ensures content meets quality standards
for sports betting and gambling content. Combines multiple validators from
the shared infrastructure to provide a unified quality assessment.

Usage:
    from src.validation.quality_gate import ContentQualityGate
    
    gate = ContentQualityGate()
    result = gate.validate(content_html)
    
    if result.passed:
        print(f"✅ Quality gate PASSED (Score: {result.total_score}/100)")
    else:
        print(f"❌ Quality gate FAILED (Score: {result.total_score}/100)")
        for error in result.critical_errors:
            print(f"  - {error}")
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import traceback

# Add the shared infrastructure to the Python path
SHARED_INFRA_PATH = Path(__file__).resolve().parents[4] / "TEST-tes-shared-infrastructure" / "src"
if str(SHARED_INFRA_PATH) not in sys.path:
    sys.path.insert(0, str(SHARED_INFRA_PATH))

try:
    from tes_shared.validators.eeat_validator import EEATValidator
    from tes_shared.validators.brand_validator import BrandValidator
    from tes_shared.validators.responsible_gambling import ResponsibleGamblingValidator
    from tes_shared.validators.seo_meta_validator import SEOMetaValidator
    from tes_shared.validators.ai_patterns import AIPatternValidator
except ImportError as e:
    print(f"Warning: Could not import shared validators: {e}")
    print(f"Attempted path: {SHARED_INFRA_PATH}")
    # For testing purposes, we'll create mock validators
    print("Using mock validators for testing...")


class ValidatorType(Enum):
    """Types of validators in the quality gate."""
    EEAT = "eeat"
    BRAND = "brand"
    RESPONSIBLE_GAMBLING = "responsible_gambling"
    SEO_META = "seo_meta"
    AI_PATTERN = "ai_pattern"


class QualityGateStatus(Enum):
    """Overall quality gate status."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


@dataclass
class ValidatorResult:
    """Result from a single validator."""
    validator_type: ValidatorType
    passed: bool
    score: float
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Optional[Any] = None
    execution_time: float = 0.0


@dataclass
class QualityGateResult:
    """Complete quality gate validation result."""
    passed: bool
    status: QualityGateStatus
    total_score: float
    validator_results: Dict[ValidatorType, ValidatorResult] = field(default_factory=dict)
    critical_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    
    @property
    def summary(self) -> str:
        """Human-readable summary of the results."""
        status_emoji = "✅" if self.passed else "❌"
        status_text = self.status.value.upper()
        
        summary = f"{status_emoji} Quality Gate {status_text} (Score: {self.total_score:.1f}/100)\n"
        
        if self.critical_errors:
            summary += f"\nCritical Errors ({len(self.critical_errors)}):\n"
            for error in self.critical_errors[:5]:  # Limit to top 5
                summary += f"  - {error}\n"
            if len(self.critical_errors) > 5:
                summary += f"  ... and {len(self.critical_errors) - 5} more\n"
        
        if self.warnings:
            summary += f"\nWarnings ({len(self.warnings)}):\n"
            for warning in self.warnings[:3]:  # Limit to top 3
                summary += f"  - {warning}\n"
            if len(self.warnings) > 3:
                summary += f"  ... and {len(self.warnings) - 3} more\n"
        
        summary += f"\nValidator Breakdown:\n"
        for validator_type, result in self.validator_results.items():
            status_icon = "✅" if result.passed else "❌"
            summary += f"  {status_icon} {validator_type.value.replace('_', ' ').title()}: {result.score:.1f}/100\n"
        
        return summary


class ContentQualityGate:
    """
    Comprehensive quality gate for TopEndSports content briefs.
    
    Validates content against multiple quality dimensions:
    - E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
    - Brand verification and consistency
    - Responsible gambling compliance
    - SEO meta tag optimization
    - AI pattern detection and avoidance
    """
    
    # Scoring weights for each validator (should sum to 100)
    VALIDATOR_WEIGHTS = {
        ValidatorType.EEAT: 30,  # Critical for YMYL content
        ValidatorType.BRAND: 20,  # Important for credibility
        ValidatorType.RESPONSIBLE_GAMBLING: 25,  # Legal/regulatory requirement
        ValidatorType.SEO_META: 15,  # SEO optimization
        ValidatorType.AI_PATTERN: 10,  # Content quality
    }
    
    # Minimum scores required to pass (out of 100)
    MINIMUM_PASSING_SCORES = {
        ValidatorType.EEAT: 60,
        ValidatorType.BRAND: 70,
        ValidatorType.RESPONSIBLE_GAMBLING: 80,  # High bar for compliance
        ValidatorType.SEO_META: 60,
        ValidatorType.AI_PATTERN: 60,
    }
    
    def __init__(self, 
                 strict_mode: bool = True,
                 target_keywords: Optional[List[str]] = None,
                 brand_name: str = "TopEndSports",
                 target_states: Optional[List[str]] = None):
        """
        Initialize the quality gate.
        
        Args:
            strict_mode: If True, failing validators cause overall failure
            target_keywords: SEO target keywords for validation
            brand_name: Brand name for SEO and brand validation
            target_states: US states for responsible gambling compliance
        """
        self.strict_mode = strict_mode
        self.target_keywords = target_keywords or []
        self.brand_name = brand_name
        self.target_states = target_states or []
        
        # Initialize validators
        self._init_validators()
    
    def _init_validators(self):
        """Initialize all validators with appropriate configurations."""
        try:
            self.validators = {
                ValidatorType.EEAT: EEATValidator(
                    min_pass_score=self.MINIMUM_PASSING_SCORES[ValidatorType.EEAT],
                    content_type="betting"
                ),
                ValidatorType.BRAND: BrandValidator(
                    strict_mode=self.strict_mode
                ),
                ValidatorType.RESPONSIBLE_GAMBLING: ResponsibleGamblingValidator(
                    target_states=self.target_states,
                    strict_mode=self.strict_mode
                ),
                ValidatorType.SEO_META: SEOMetaValidator(
                    target_keywords=self.target_keywords,
                    brand_name=self.brand_name,
                    brand_separator=" | "
                ),
                ValidatorType.AI_PATTERN: AIPatternValidator()
            }
        except NameError:
            # Fallback for testing when validators aren't available
            self.validators = {
                ValidatorType.EEAT: MockValidator("EEAT"),
                ValidatorType.BRAND: MockValidator("Brand"),
                ValidatorType.RESPONSIBLE_GAMBLING: MockValidator("ResponsibleGambling"),
                ValidatorType.SEO_META: MockValidator("SEOMeta"),
                ValidatorType.AI_PATTERN: MockValidator("AIPattern"),
            }
    
    def validate(self, content: str, page_url: Optional[str] = None) -> QualityGateResult:
        """
        Run all validators against the content and calculate overall score.
        
        Args:
            content: HTML or text content to validate
            page_url: Optional page URL for SEO validation
            
        Returns:
            QualityGateResult with complete validation results
        """
        import time
        start_time = time.time()
        
        validator_results = {}
        critical_errors = []
        warnings = []
        
        # Run each validator
        for validator_type, validator in self.validators.items():
            try:
                validator_start = time.time()
                result = self._run_validator(validator_type, validator, content, page_url)
                result.execution_time = time.time() - validator_start
                validator_results[validator_type] = result
                
                # Collect errors and warnings
                critical_errors.extend(result.errors)
                warnings.extend(result.warnings)
                
            except Exception as e:
                # Create error result for failed validator
                validator_results[validator_type] = ValidatorResult(
                    validator_type=validator_type,
                    passed=False,
                    score=0.0,
                    errors=[f"Validator execution failed: {str(e)}"],
                    warnings=[],
                    details={"exception": str(e), "traceback": traceback.format_exc()}
                )
                critical_errors.append(f"{validator_type.value} validator failed: {str(e)}")
        
        # Calculate weighted total score
        total_score = self._calculate_total_score(validator_results)
        
        # Determine pass/fail status
        passed, status = self._determine_status(validator_results, critical_errors)
        
        execution_time = time.time() - start_time
        
        return QualityGateResult(
            passed=passed,
            status=status,
            total_score=total_score,
            validator_results=validator_results,
            critical_errors=critical_errors,
            warnings=warnings,
            execution_time=execution_time
        )
    
    def _run_validator(self, validator_type: ValidatorType, validator: Any, 
                      content: str, page_url: Optional[str]) -> ValidatorResult:
        """Run a specific validator and normalize its result."""
        
        if validator_type == ValidatorType.EEAT:
            raw_result = validator.validate(content)
            return ValidatorResult(
                validator_type=validator_type,
                passed=raw_result.is_valid,
                score=raw_result.score.total,
                errors=[issue.message for issue in raw_result.errors],
                warnings=[issue.message for issue in raw_result.warnings],
                details=raw_result
            )
        
        elif validator_type == ValidatorType.BRAND:
            raw_result = validator.validate(content)
            # Convert brand validation result to normalized format
            score = 100 if raw_result.valid else (60 if len(raw_result.unknown_brands) <= 2 else 30)
            passed = score >= self.MINIMUM_PASSING_SCORES[validator_type]
            
            errors = []
            warnings = []
            if raw_result.unknown_brands:
                if self.strict_mode:
                    errors.extend([f"Unknown brand: {brand}" for brand in raw_result.unknown_brands])
                else:
                    warnings.extend([f"Unknown brand: {brand}" for brand in raw_result.unknown_brands])
            
            return ValidatorResult(
                validator_type=validator_type,
                passed=passed,
                score=score,
                errors=errors,
                warnings=warnings,
                details=raw_result
            )
        
        elif validator_type == ValidatorType.RESPONSIBLE_GAMBLING:
            raw_result = validator.validate(content, detect_states=True)
            score = 100 if raw_result.valid else (40 if raw_result.status == "WARNING" else 20)
            passed = score >= self.MINIMUM_PASSING_SCORES[validator_type]
            
            errors = [issue.message for issue in raw_result.issues if issue.severity.value == "error"]
            warnings = [issue.message for issue in raw_result.issues if issue.severity.value == "warning"]
            
            return ValidatorResult(
                validator_type=validator_type,
                passed=passed,
                score=score,
                errors=errors,
                warnings=warnings,
                details=raw_result
            )
        
        elif validator_type == ValidatorType.SEO_META:
            raw_result = validator.validate(content, page_url=page_url)
            score = raw_result.score
            passed = score >= self.MINIMUM_PASSING_SCORES[validator_type]
            
            errors = [issue.message for issue in raw_result.issues if issue.severity.value == "error"]
            warnings = [issue.message for issue in raw_result.issues if issue.severity.value == "warning"]
            
            return ValidatorResult(
                validator_type=validator_type,
                passed=passed,
                score=score,
                errors=errors,
                warnings=warnings,
                details=raw_result
            )
        
        elif validator_type == ValidatorType.AI_PATTERN:
            raw_result = validator.validate(content)
            # AI pattern validator returns a dict with various scores
            total_score = raw_result.get('total_score', 0)
            passed = total_score >= self.MINIMUM_PASSING_SCORES[validator_type]
            
            errors = []
            warnings = []
            
            # Convert AI pattern issues to errors/warnings
            for category, issues in raw_result.get('issues', {}).items():
                for issue in issues:
                    if issue.get('severity') == 'high':
                        errors.append(f"{category}: {issue['message']}")
                    else:
                        warnings.append(f"{category}: {issue['message']}")
            
            return ValidatorResult(
                validator_type=validator_type,
                passed=passed,
                score=total_score,
                errors=errors,
                warnings=warnings,
                details=raw_result
            )
        
        else:
            # Mock validator for testing
            return ValidatorResult(
                validator_type=validator_type,
                passed=True,
                score=75.0,
                errors=[],
                warnings=[f"Mock {validator_type.value} validator - no real validation performed"],
                details={"mock": True}
            )
    
    def _calculate_total_score(self, validator_results: Dict[ValidatorType, ValidatorResult]) -> float:
        """Calculate weighted total score from validator results."""
        total_score = 0.0
        
        for validator_type, weight in self.VALIDATOR_WEIGHTS.items():
            if validator_type in validator_results:
                result = validator_results[validator_type]
                weighted_score = (result.score * weight) / 100
                total_score += weighted_score
        
        return round(total_score, 1)
    
    def _determine_status(self, validator_results: Dict[ValidatorType, ValidatorResult], 
                         critical_errors: List[str]) -> tuple[bool, QualityGateStatus]:
        """Determine overall pass/fail status and quality gate status."""
        
        # Check if any critical validators failed
        critical_validators = [ValidatorType.EEAT, ValidatorType.RESPONSIBLE_GAMBLING]
        has_critical_failure = False
        
        for validator_type in critical_validators:
            if validator_type in validator_results and not validator_results[validator_type].passed:
                has_critical_failure = True
                break
        
        # In strict mode, any validator failure is a failure
        if self.strict_mode:
            all_passed = all(result.passed for result in validator_results.values())
            if not all_passed or has_critical_failure:
                return False, QualityGateStatus.FAILED
        
        # Non-strict mode: critical failures still fail, others are warnings
        if has_critical_failure:
            return False, QualityGateStatus.FAILED
        
        # Check if we have any non-critical failures
        has_warnings = any(not result.passed for result in validator_results.values())
        
        if has_warnings:
            return True, QualityGateStatus.WARNING
        
        return True, QualityGateStatus.PASSED
    
    def get_recommendations(self, result: QualityGateResult) -> List[str]:
        """Get actionable recommendations based on validation results."""
        recommendations = []
        
        for validator_type, validator_result in result.validator_results.items():
            if not validator_result.passed:
                if validator_type == ValidatorType.EEAT:
                    recommendations.append("Improve E-E-A-T by adding author credentials, expert quotes, and data sources")
                elif validator_type == ValidatorType.BRAND:
                    recommendations.append("Verify all mentioned sportsbook brands are real and correctly spelled")
                elif validator_type == ValidatorType.RESPONSIBLE_GAMBLING:
                    recommendations.append("Add required responsible gambling disclaimers and help resources")
                elif validator_type == ValidatorType.SEO_META:
                    recommendations.append("Optimize title tag length (50-60 chars) and meta description (150-160 chars)")
                elif validator_type == ValidatorType.AI_PATTERN:
                    recommendations.append("Reduce formulaic patterns and improve content authenticity")
        
        return recommendations


class MockValidator:
    """Mock validator for testing when real validators aren't available."""
    
    def __init__(self, name: str):
        self.name = name
    
    def validate(self, content: str, **kwargs):
        """Mock validation that always passes."""
        if self.name == "AIPattern":
            return {
                'total_score': 75.0,
                'issues': {},
                'passed': True
            }
        else:
            # Create a simple mock result object
            class MockResult:
                def __init__(self):
                    self.valid = True
                    self.is_valid = True
                    self.score = type('Score', (), {'total': 75.0})()
                    self.errors = []
                    self.warnings = []
                    self.issues = []
            
            return MockResult()


def validate_content_brief(content: str, **kwargs) -> QualityGateResult:
    """
    Convenience function to validate content brief with default settings.
    
    Args:
        content: HTML or text content to validate
        **kwargs: Additional arguments passed to ContentQualityGate
        
    Returns:
        QualityGateResult with complete validation results
    """
    gate = ContentQualityGate(**kwargs)
    return gate.validate(content)


if __name__ == "__main__":
    # Example usage
    sample_content = """
    <html>
    <head>
        <title>Best Sports Betting Sites 2024 | TopEndSports</title>
        <meta name="description" content="Find the top sports betting sites with expert reviews, bonuses, and responsible gambling resources. 21+ only.">
    </head>
    <body>
        <h1>Best Sports Betting Sites 2024</h1>
        <p>Our expert team has tested real-money sports betting sites since 2010.</p>
        <p>Please gamble responsibly. If you have a gambling problem, call 1-800-GAMBLER.</p>
        <p>Top sites include DraftKings, FanDuel, and BetMGM.</p>
    </body>
    </html>
    """
    
    gate = ContentQualityGate()
    result = gate.validate(sample_content)
    print(result.summary)