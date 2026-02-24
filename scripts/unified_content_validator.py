#!/usr/bin/env python3
"""
Unified Content Validator for TopEndSports Content Briefs

Integrates validators from tes-shared-infrastructure:
- AI Pattern Validator: Detects AI-generated content patterns
- Brand Validator: Verifies sportsbook brand names are real
- E-E-A-T Validator: Checks Experience, Expertise, Authority, Trust signals

Usage:
    # CLI Usage
    python3 scripts/unified_content_validator.py path/to/content.html
    python3 scripts/unified_content_validator.py path/to/content.md --format markdown
    python3 scripts/unified_content_validator.py --all output/
    
    # Programmatic Usage
    from scripts.unified_content_validator import UnifiedContentValidator, validate_content
    
    validator = UnifiedContentValidator()
    result = validator.validate(html_content)
    
    # Or use the convenience function
    result = validate_content(content, content_type='html')

Exit codes:
    0 - All validations passed
    1 - One or more validations failed
    2 - Error reading file or importing validators

Requirements:
    - tes-shared-infrastructure must be installed or on PYTHONPATH
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Try to import from installed package or local path
try:
    from tes_shared.validators import (
        AIPatternValidator,
        BrandValidator,
        EEATValidator,
        EEATResult,
    )
    VALIDATORS_AVAILABLE = True
except ImportError:
    # Try relative import from repo
    import os
    shared_infra_path = Path(__file__).parent.parent.parent / "TEST-tes-shared-infrastructure" / "src"
    if shared_infra_path.exists():
        sys.path.insert(0, str(shared_infra_path))
        try:
            from tes_shared.validators import (
                AIPatternValidator,
                BrandValidator,
                EEATValidator,
                EEATResult,
            )
            VALIDATORS_AVAILABLE = True
        except ImportError:
            VALIDATORS_AVAILABLE = False
    else:
        VALIDATORS_AVAILABLE = False


@dataclass
class ValidationSummary:
    """Summary of validation results."""
    validator_name: str
    passed: bool
    score: Optional[float] = None
    grade: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnifiedValidationResult:
    """Complete validation result from all validators."""
    is_valid: bool
    content_file: Optional[str] = None
    ai_patterns: Optional[ValidationSummary] = None
    brand_validation: Optional[ValidationSummary] = None
    eeat_validation: Optional[ValidationSummary] = None
    errors: List[str] = field(default_factory=list)
    
    @property
    def total_errors(self) -> int:
        """Total error count across all validators."""
        count = len(self.errors)
        if self.ai_patterns:
            count += len(self.ai_patterns.errors)
        if self.brand_validation:
            count += len(self.brand_validation.errors)
        if self.eeat_validation:
            count += len(self.eeat_validation.errors)
        return count
    
    @property
    def total_warnings(self) -> int:
        """Total warning count across all validators."""
        count = 0
        if self.ai_patterns:
            count += len(self.ai_patterns.warnings)
        if self.brand_validation:
            count += len(self.brand_validation.warnings)
        if self.eeat_validation:
            count += len(self.eeat_validation.warnings)
        return count
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'is_valid': self.is_valid,
            'content_file': self.content_file,
            'total_errors': self.total_errors,
            'total_warnings': self.total_warnings,
            'ai_patterns': self._summary_to_dict(self.ai_patterns) if self.ai_patterns else None,
            'brand_validation': self._summary_to_dict(self.brand_validation) if self.brand_validation else None,
            'eeat_validation': self._summary_to_dict(self.eeat_validation) if self.eeat_validation else None,
            'errors': self.errors,
        }
    
    def _summary_to_dict(self, summary: ValidationSummary) -> Dict:
        return {
            'validator': summary.validator_name,
            'passed': summary.passed,
            'score': summary.score,
            'grade': summary.grade,
            'errors': summary.errors,
            'warnings': summary.warnings,
            'details': summary.details,
        }
    
    def print_report(self, verbose: bool = False) -> None:
        """Print human-readable validation report."""
        print("=" * 70)
        print("UNIFIED CONTENT VALIDATION REPORT")
        print("=" * 70)
        
        if self.content_file:
            print(f"File: {self.content_file}")
        
        status = "[PASS] PASSED" if self.is_valid else "[FAIL] FAILED"
        print(f"Overall Status: {status}")
        print(f"Total Errors: {self.total_errors}")
        print(f"Total Warnings: {self.total_warnings}")
        print("-" * 70)
        
        # AI Patterns
        if self.ai_patterns:
            self._print_validator_section("AI Pattern Detection", self.ai_patterns, verbose)
        
        # Brand Validation
        if self.brand_validation:
            self._print_validator_section("Brand Validation", self.brand_validation, verbose)
        
        # E-E-A-T Validation
        if self.eeat_validation:
            self._print_validator_section("E-E-A-T Validation", self.eeat_validation, verbose)
        
        # General errors
        if self.errors:
            print("\n[WARN] GENERAL ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        print("=" * 70)
    
    def _print_validator_section(self, title: str, summary: ValidationSummary, verbose: bool) -> None:
        """Print a single validator section."""
        status = "[PASS]" if summary.passed else "[FAIL]"
        print(f"\n{status} {title}")
        
        if summary.score is not None:
            grade = f" ({summary.grade})" if summary.grade else ""
            print(f"   Score: {summary.score}/100{grade}")
        
        if summary.errors:
            print(f"   Errors ({len(summary.errors)}):")
            for error in summary.errors[:5]:  # Show first 5
                print(f"     - {error}")
            if len(summary.errors) > 5:
                print(f"     ... and {len(summary.errors) - 5} more")
        
        if verbose and summary.warnings:
            print(f"   Warnings ({len(summary.warnings)}):")
            for warning in summary.warnings[:5]:
                print(f"     - {warning}")
            if len(summary.warnings) > 5:
                print(f"     ... and {len(summary.warnings) - 5} more")


class UnifiedContentValidator:
    """
    Unified content validator that runs all TES shared validators.
    
    Validates content against:
    1. AI Pattern Detection - Avoids AI-detectable writing patterns
    2. Brand Validation - Ensures only real sportsbook brands are mentioned
    3. E-E-A-T Requirements - Google quality guidelines compliance
    """
    
    def __init__(
        self,
        validate_ai_patterns: bool = True,
        validate_brands: bool = True,
        validate_eeat: bool = True,
        ai_pattern_strict: bool = False,
        eeat_min_score: float = 50.0,
    ):
        """
        Initialize the unified validator.
        
        Args:
            validate_ai_patterns: Enable AI pattern detection
            validate_brands: Enable brand name validation
            validate_eeat: Enable E-E-A-T validation
            ai_pattern_strict: Fail on any AI pattern warnings (not just errors)
            eeat_min_score: Minimum E-E-A-T score to pass (0-100)
        """
        if not VALIDATORS_AVAILABLE:
            raise ImportError(
                "TES shared validators not available. "
                "Install tes-shared-infrastructure or add it to PYTHONPATH."
            )
        
        self.validate_ai_patterns = validate_ai_patterns
        self.validate_brands = validate_brands
        self.validate_eeat = validate_eeat
        self.ai_pattern_strict = ai_pattern_strict
        self.eeat_min_score = eeat_min_score
        
        # Initialize validators
        self._ai_validator = AIPatternValidator() if validate_ai_patterns else None
        self._brand_validator = BrandValidator() if validate_brands else None
        self._eeat_validator = EEATValidator() if validate_eeat else None
    
    def validate(
        self, 
        content: str, 
        content_type: str = 'html',
        filename: Optional[str] = None
    ) -> UnifiedValidationResult:
        """
        Run all enabled validators on content.
        
        Args:
            content: The content to validate (HTML or markdown)
            content_type: Type of content ('html' or 'markdown')
            filename: Optional filename for reporting
            
        Returns:
            UnifiedValidationResult with all validation results
        """
        result = UnifiedValidationResult(
            is_valid=True,
            content_file=filename,
        )
        
        # Convert markdown to simple HTML if needed for validation
        if content_type == 'markdown':
            content = self._markdown_to_html(content)
        
        # Run AI Pattern validation
        if self.validate_ai_patterns and self._ai_validator:
            ai_result = self._run_ai_patterns(content)
            result.ai_patterns = ai_result
            if not ai_result.passed:
                result.is_valid = False
        
        # Run Brand validation
        if self.validate_brands and self._brand_validator:
            brand_result = self._run_brand_validation(content)
            result.brand_validation = brand_result
            if not brand_result.passed:
                result.is_valid = False
        
        # Run E-E-A-T validation
        if self.validate_eeat and self._eeat_validator:
            eeat_result = self._run_eeat_validation(content)
            result.eeat_validation = eeat_result
            if not eeat_result.passed:
                result.is_valid = False
        
        return result
    
    def validate_file(self, filepath: Union[str, Path]) -> UnifiedValidationResult:
        """
        Validate a file.
        
        Args:
            filepath: Path to file to validate
            
        Returns:
            UnifiedValidationResult
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            return UnifiedValidationResult(
                is_valid=False,
                content_file=str(filepath),
                errors=[f"File not found: {filepath}"]
            )
        
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            return UnifiedValidationResult(
                is_valid=False,
                content_file=str(filepath),
                errors=[f"Error reading file: {e}"]
            )
        
        # Determine content type from extension
        content_type = 'markdown' if filepath.suffix.lower() in ['.md', '.markdown'] else 'html'
        
        return self.validate(content, content_type=content_type, filename=str(filepath))
    
    def _run_ai_patterns(self, content: str) -> ValidationSummary:
        """Run AI pattern detection."""
        try:
            result = self._ai_validator.validate(content)
            
            # AI Pattern validator returns a dictionary
            if isinstance(result, dict):
                errors = result.get('errors', [])
                warnings = result.get('warnings', [])
                details = result.get('details', {})
                is_valid = result.get('is_valid', True)
                
                # Calculate AI score if method is available
                score = None
                if hasattr(self._ai_validator, 'calculate_score'):
                    score = 100 - self._ai_validator.calculate_score()  # Invert: higher = better
            else:
                # Handle object-based result
                errors = getattr(result, 'errors', [])
                warnings = getattr(result, 'warnings', [])
                details = getattr(result, 'details', {})
                is_valid = getattr(result, 'is_valid', True)
                score = getattr(result, 'score', None)
            
            # Determine pass/fail
            if self.ai_pattern_strict:
                passed = len(errors) == 0 and len(warnings) == 0
            else:
                passed = is_valid and len(errors) == 0
            
            return ValidationSummary(
                validator_name="AI Pattern Detection",
                passed=passed,
                score=score,
                errors=errors if isinstance(errors, list) else [errors],
                warnings=warnings if isinstance(warnings, list) else [warnings],
                details=details,
            )
        except Exception as e:
            return ValidationSummary(
                validator_name="AI Pattern Detection",
                passed=False,
                errors=[f"Validator error: {str(e)}"],
            )
    
    def _run_brand_validation(self, content: str) -> ValidationSummary:
        """Run brand name validation."""
        try:
            result = self._brand_validator.validate(content)
            
            # Handle ValidationResult dataclass
            if hasattr(result, 'valid'):
                passed = result.valid
                errors = result.errors if hasattr(result, 'errors') else []
                warnings = result.warnings if hasattr(result, 'warnings') else []
                details = {
                    'verified_brands': result.verified_brands if hasattr(result, 'verified_brands') else [],
                    'unknown_brands': result.unknown_brands if hasattr(result, 'unknown_brands') else [],
                    'suggestions': result.suggestions if hasattr(result, 'suggestions') else {},
                }
            else:
                # Dict result
                passed = result.get('valid', True)
                errors = result.get('errors', [])
                warnings = result.get('warnings', [])
                details = result
            
            return ValidationSummary(
                validator_name="Brand Validation",
                passed=passed,
                errors=errors,
                warnings=warnings,
                details=details,
            )
        except Exception as e:
            return ValidationSummary(
                validator_name="Brand Validation",
                passed=False,
                errors=[f"Validator error: {str(e)}"],
            )
    
    def _run_eeat_validation(self, content: str) -> ValidationSummary:
        """Run E-E-A-T validation."""
        try:
            result = self._eeat_validator.validate(content)
            
            # Handle EEATResult dataclass
            if isinstance(result, EEATResult):
                score = result.score.total if result.score else 0
                grade = result.score.grade if result.score else 'F'
                passed = result.is_valid and score >= self.eeat_min_score
                errors = [f"{i.category.value}: {i.message}" for i in result.errors]
                warnings = [f"{i.category.value}: {i.message}" for i in result.warnings]
                details = result.to_dict()
            else:
                # Dict result
                score = result.get('score', {}).get('total', 0)
                grade = result.get('score', {}).get('grade', 'F')
                passed = result.get('is_valid', False) and score >= self.eeat_min_score
                errors = result.get('errors', [])
                warnings = result.get('warnings', [])
                details = result
            
            return ValidationSummary(
                validator_name="E-E-A-T Validation",
                passed=passed,
                score=score,
                grade=grade,
                errors=errors,
                warnings=warnings,
                details=details,
            )
        except Exception as e:
            return ValidationSummary(
                validator_name="E-E-A-T Validation",
                passed=False,
                errors=[f"Validator error: {str(e)}"],
            )
    
    def _markdown_to_html(self, markdown: str) -> str:
        """
        Convert markdown to basic HTML for validation.
        
        This is a simple conversion for validation purposes.
        """
        html = markdown
        
        # Convert headers
        for i in range(6, 0, -1):
            pattern = r'^' + '#' * i + r'\s+(.+)$'
            html = __import__('re').sub(pattern, f'<h{i}>\\1</h{i}>', html, flags=__import__('re').MULTILINE)
        
        # Convert bold
        html = __import__('re').sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = __import__('re').sub(r'__(.+?)__', r'<strong>\1</strong>', html)
        
        # Convert italic
        html = __import__('re').sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = __import__('re').sub(r'_(.+?)_', r'<em>\1</em>', html)
        
        # Convert links
        html = __import__('re').sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        
        # Wrap paragraphs
        paragraphs = html.split('\n\n')
        wrapped = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<'):
                wrapped.append(f'<p>{p}</p>')
            else:
                wrapped.append(p)
        
        return '\n'.join(wrapped)


def validate_content(
    content: str,
    content_type: str = 'html',
    validate_ai: bool = True,
    validate_brands: bool = True,
    validate_eeat: bool = True,
    eeat_min_score: float = 50.0,
) -> UnifiedValidationResult:
    """
    Convenience function to validate content with default settings.
    
    Args:
        content: Content to validate
        content_type: 'html' or 'markdown'
        validate_ai: Enable AI pattern detection
        validate_brands: Enable brand validation
        validate_eeat: Enable E-E-A-T validation
        eeat_min_score: Minimum E-E-A-T score to pass
        
    Returns:
        UnifiedValidationResult
    """
    validator = UnifiedContentValidator(
        validate_ai_patterns=validate_ai,
        validate_brands=validate_brands,
        validate_eeat=validate_eeat,
        eeat_min_score=eeat_min_score,
    )
    return validator.validate(content, content_type)


def validate_file(
    filepath: Union[str, Path],
    **kwargs
) -> UnifiedValidationResult:
    """
    Convenience function to validate a file.
    
    Args:
        filepath: Path to file to validate
        **kwargs: Additional arguments passed to UnifiedContentValidator
        
    Returns:
        UnifiedValidationResult
    """
    validator = UnifiedContentValidator(**kwargs)
    return validator.validate_file(filepath)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Unified content validator for TopEndSports briefs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate a single file
    python3 unified_content_validator.py output/example-ai-enhancement.md

    # Validate all files in a directory
    python3 unified_content_validator.py --all output/

    # Validate with specific options
    python3 unified_content_validator.py --no-brands --eeat-min 60 output/example.html

    # Output JSON report
    python3 unified_content_validator.py --json output/example.html
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        help='File or directory to validate'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all HTML/MD files in directory'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['html', 'markdown'],
        default=None,
        help='Override content type detection'
    )
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI pattern detection'
    )
    parser.add_argument(
        '--no-brands',
        action='store_true',
        help='Disable brand validation'
    )
    parser.add_argument(
        '--no-eeat',
        action='store_true',
        help='Disable E-E-A-T validation'
    )
    parser.add_argument(
        '--eeat-min',
        type=float,
        default=50.0,
        help='Minimum E-E-A-T score to pass (default: 50.0)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Strict mode: fail on warnings too'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if not args.path:
        parser.print_help()
        return 1
    
    if not VALIDATORS_AVAILABLE:
        print("ERROR: TES shared validators not available.", file=sys.stderr)
        print("Install tes-shared-infrastructure or add it to PYTHONPATH.", file=sys.stderr)
        return 2
    
    path = Path(args.path)
    
    try:
        validator = UnifiedContentValidator(
            validate_ai_patterns=not args.no_ai,
            validate_brands=not args.no_brands,
            validate_eeat=not args.no_eeat,
            ai_pattern_strict=args.strict,
            eeat_min_score=args.eeat_min,
        )
    except ImportError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    
    results = []
    
    if args.all and path.is_dir():
        # Validate all files in directory
        files = list(path.glob('*.html')) + list(path.glob('*.md'))
        for file in files:
            result = validator.validate_file(file)
            results.append(result)
    elif path.is_file():
        result = validator.validate_file(path)
        results.append(result)
    else:
        print(f"ERROR: Path not found: {path}", file=sys.stderr)
        return 2
    
    # Output results
    all_passed = all(r.is_valid for r in results)
    
    if args.json:
        output = {
            'all_passed': all_passed,
            'total_files': len(results),
            'results': [r.to_dict() for r in results]
        }
        print(json.dumps(output, indent=2))
    else:
        for result in results:
            result.print_report(verbose=args.verbose)
        
        if len(results) > 1:
            print(f"\n{'='*70}")
            print(f"SUMMARY: {sum(1 for r in results if r.is_valid)}/{len(results)} files passed")
            print(f"{'='*70}")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
