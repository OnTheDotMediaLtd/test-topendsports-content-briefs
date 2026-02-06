"""
TopEndSports Content Validation Package

This package provides comprehensive quality validation for sports betting content,
ensuring compliance with E-E-A-T guidelines, responsible gambling requirements,
brand accuracy, SEO best practices, and content authenticity.

Main Components:
- ContentQualityGate: Main validation orchestrator
- Multiple specialized validators from shared infrastructure
- Comprehensive testing and reporting capabilities

Usage:
    from validation.quality_gate import ContentQualityGate, validate_content_brief
    
    # Basic usage
    result = validate_content_brief(html_content)
    
    # Advanced usage with custom configuration
    gate = ContentQualityGate(
        strict_mode=True,
        target_keywords=['sports betting', 'sportsbook'],
        target_states=['NV', 'NJ', 'PA']
    )
    result = gate.validate(html_content)
    
    if result.passed:
        print("✅ Content passed quality gate!")
    else:
        print("❌ Content failed quality gate")
        print(result.summary)
"""

from .quality_gate import (
    ContentQualityGate,
    QualityGateResult,
    QualityGateStatus,
    ValidatorType,
    ValidatorResult,
    validate_content_brief
)

__version__ = "1.0.0"
__author__ = "TopEndSports"

__all__ = [
    "ContentQualityGate",
    "QualityGateResult", 
    "QualityGateStatus",
    "ValidatorType",
    "ValidatorResult",
    "validate_content_brief"
]