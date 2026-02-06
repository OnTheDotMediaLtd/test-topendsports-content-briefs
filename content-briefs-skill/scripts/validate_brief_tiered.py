#!/usr/bin/env python3
"""Content brief validation with tiered system."""

import sys
import re
from pathlib import Path

# Import shared framework
try:
    sys.path.insert(0, str(Path.cwd().parent.parent / 'tes-shared-infrastructure' / 'src'))
    from tes_shared.validation.tiered_validator import (
        TieredValidator, ValidationLevel
    )
    SHARED_AVAILABLE = True
except ImportError:
    SHARED_AVAILABLE = False
    # Fallback implementation
    from enum import Enum
    from dataclasses import dataclass
    from typing import List, Optional

    class ValidationLevel(Enum):
        BLOCKING = "blocking"
        ADVISORY = "advisory"
        INFO = "info"

    @dataclass
    class ValidationResult:
        level: ValidationLevel
        check_name: str
        passed: bool
        message: str
        details: Optional[str] = None

        def __str__(self):
            icon = "[PASS]" if self.passed else "[FAIL]"
            level_icon = {
                ValidationLevel.BLOCKING: "[BLOCK]",
                ValidationLevel.ADVISORY: "[WARN] ",
                ValidationLevel.INFO: "[INFO] "
            }
            return f"{icon} {level_icon[self.level]} [{self.level.value.upper()}] {self.check_name}: {self.message}"

        def to_dict(self):
            return {
                'level': self.level.value,
                'check_name': self.check_name,
                'passed': self.passed,
                'message': self.message,
                'details': self.details
            }

    class TieredValidator:
        def __init__(self, strict_mode: bool = False):
            self.strict_mode = strict_mode
            self.results: List[ValidationResult] = []

        def add_result(self, level: ValidationLevel, check_name: str,
                       passed: bool, message: str, details: str = None):
            result = ValidationResult(level, check_name, passed, message, details)
            self.results.append(result)
            return result

        def should_fail_ci(self) -> bool:
            if self.strict_mode:
                return any(not r.passed for r in self.results)
            return any(not r.passed for r in self.results if r.level == ValidationLevel.BLOCKING)

        def print_report(self):
            print("\n" + "="*70)
            print("VALIDATION REPORT")
            print("="*70 + "\n")

            for level in [ValidationLevel.BLOCKING, ValidationLevel.ADVISORY, ValidationLevel.INFO]:
                level_results = [r for r in self.results if r.level == level]
                if level_results:
                    print(f"\n{level.value.upper()} CHECKS ({len(level_results)}):")
                    print("-" * 70)
                    for result in level_results:
                        print(f"  {result}")
                        if result.details:
                            print(f"    → {result.details}")

            print("\n" + "="*70)
            blocking_failed = sum(1 for r in self.results if r.level == ValidationLevel.BLOCKING and not r.passed)
            advisory_failed = sum(1 for r in self.results if r.level == ValidationLevel.ADVISORY and not r.passed)
            info_failed = sum(1 for r in self.results if r.level == ValidationLevel.INFO and not r.passed)

            print(f"SUMMARY: {blocking_failed} blocking failures, {advisory_failed} advisory warnings, {info_failed} info notices")
            if self.should_fail_ci():
                print("STATUS: FAILED - CI should fail")
            else:
                print("STATUS: PASSED - CI should succeed")
            print("="*70 + "\n")


class ContentBriefValidator(TieredValidator):
    """Validates content brief structure and completeness."""

    def __init__(self, brief_content: str, brief_path: str = "", strict_mode: bool = False):
        super().__init__(strict_mode)
        self.content = brief_content
        self.brief_path = brief_path
        # Detect brief type from filename
        self.is_control_sheet = 'control-sheet' in brief_path.lower()
        self.is_writer_brief = 'writer-brief' in brief_path.lower()
        self.is_ai_enhancement = 'ai-enhancement' in brief_path.lower()

    def validate_required_sections(self) -> bool:
        """BLOCKING: Brief has all required sections."""
        # Check for flexible section names
        has_keyword = any(term in self.content for term in ["Primary Keyword", "Target Keyword", "PAGE BASICS"])
        has_content_structure = any(term in self.content for term in ["Content Structure", "CONTENT OUTLINE", "## H1:", "## H2:"])
        has_url = any(term in self.content for term in ["Target URL", "URL", "**URL**"])

        missing = []
        if not has_keyword:
            missing.append("Keyword information")

        # Only require content structure for writer briefs and AI enhancement
        if not self.is_control_sheet:
            if not has_content_structure:
                missing.append("Content structure/outline")

        if not has_url:
            missing.append("Target URL")

        passed = len(missing) == 0

        brief_type = "control sheet" if self.is_control_sheet else ("writer brief" if self.is_writer_brief else "content brief")

        self.add_result(
            ValidationLevel.BLOCKING,
            "required_sections",
            passed,
            f"All required sections present for {brief_type}" if passed else f"Missing sections: {', '.join(missing)}",
            details="These sections are essential for content creation"
        )
        return passed

    def validate_keyword_data(self) -> bool:
        """BLOCKING: Keyword data is complete."""
        # Check for keyword metrics
        has_volume = re.search(r'(search volume|volume):\s*[\d,]+', self.content, re.IGNORECASE)
        has_difficulty = re.search(r'(difficulty|KD):\s*\d+', self.content, re.IGNORECASE)
        has_keywords = "Primary Keyword" in self.content or "Target Keyword" in self.content

        passed = bool(has_volume or has_difficulty or has_keywords)

        self.add_result(
            ValidationLevel.BLOCKING,
            "keyword_data",
            passed,
            "Keyword data present" if passed else "Missing keyword data",
            details="Volume, difficulty, or keyword list required"
        )
        return passed

    def validate_csv_reference(self) -> bool:
        """BLOCKING: CSV file referenced and exists (if applicable)."""
        csv_match = re.search(r'data/([^\s]+\.csv)', self.content)

        if not csv_match:
            # CSV reference is optional - not all briefs need them
            self.add_result(
                ValidationLevel.BLOCKING,
                "csv_reference",
                True,
                "No CSV file referenced (optional)",
                details="CSV data files are optional for content briefs"
            )
            return True

        # If CSV is referenced, verify it exists
        if self.brief_path:
            brief_dir = Path(self.brief_path).parent.parent
            csv_path = brief_dir / csv_match.group(1)
        else:
            csv_path = Path.cwd() / csv_match.group(1)

        csv_exists = csv_path.exists()

        self.add_result(
            ValidationLevel.BLOCKING,
            "csv_reference",
            csv_exists,
            f"CSV file exists: {csv_match.group(1)}" if csv_exists else f"CSV file not found: {csv_match.group(1)}"
        )
        return csv_exists

    def validate_seo_recommendations(self) -> bool:
        """ADVISORY: SEO recommendations included."""
        has_seo = any(term in self.content.lower() for term in [
            "seo recommendation",
            "optimization",
            "meta description",
            "title tag"
        ])

        self.add_result(
            ValidationLevel.ADVISORY,
            "seo_recommendations",
            has_seo,
            "SEO recommendations present" if has_seo else "Consider adding SEO recommendations",
            details="SEO guidance improves content quality"
        )
        return has_seo

    def validate_competitor_analysis(self) -> bool:
        """ADVISORY: Competitor analysis included."""
        has_competitors = "competitor" in self.content.lower() or "competition" in self.content.lower()

        self.add_result(
            ValidationLevel.ADVISORY,
            "competitor_analysis",
            has_competitors,
            "Competitor analysis present" if has_competitors else "Consider adding competitor analysis",
            details="Understanding competition improves content strategy"
        )
        return has_competitors

    def validate_analysis_depth(self) -> bool:
        """INFO: Analysis depth and detail."""
        word_count = len(self.content.split())
        detailed = word_count > 500

        self.add_result(
            ValidationLevel.INFO,
            "analysis_depth",
            detailed,
            f"Brief is detailed ({word_count} words)" if detailed else f"Brief is concise ({word_count} words)",
            details="500+ words indicates thorough analysis"
        )
        return detailed

    def validate_all(self):
        """Run all content brief validations."""
        self.validate_required_sections()
        self.validate_keyword_data()
        self.validate_csv_reference()
        self.validate_seo_recommendations()
        self.validate_competitor_analysis()
        self.validate_analysis_depth()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate content brief')
    parser.add_argument('brief_file', help='Path to content brief markdown file')
    parser.add_argument('--strict', action='store_true', help='Strict mode - fail on any warning')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    # Read file
    try:
        with open(args.brief_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.brief_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Validate
    validator = ContentBriefValidator(content, brief_path=args.brief_file, strict_mode=args.strict)
    validator.validate_all()

    # Output
    if args.output_format == 'text':
        validator.print_report()
    elif args.output_format == 'json':
        import json
        results = [r.to_dict() for r in validator.results]
        print(json.dumps({'results': results, 'should_fail_ci': validator.should_fail_ci()}, indent=2))

    sys.exit(0 if not validator.should_fail_ci() else 1)


if __name__ == '__main__':
    main()
