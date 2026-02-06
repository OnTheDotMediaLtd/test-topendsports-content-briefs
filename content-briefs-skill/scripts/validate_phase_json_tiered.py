#!/usr/bin/env python3
"""Phase JSON validation with tiered system."""

import sys
import json
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


class PhaseJSONValidator(TieredValidator):
    """Validates phase JSON files."""

    def __init__(self, json_path: str, strict_mode: bool = False):
        super().__init__(strict_mode)
        self.json_path = json_path
        self.data = None
        self.phase = self._detect_phase()

    def _detect_phase(self) -> int:
        """Detect phase number from filename."""
        filename = Path(self.json_path).name
        if 'phase1' in filename:
            return 1
        elif 'phase2' in filename:
            return 2
        else:
            return 0  # Unknown

    def validate_json_syntax(self) -> bool:
        """BLOCKING: Valid JSON syntax."""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

            self.add_result(
                ValidationLevel.BLOCKING,
                "json_syntax",
                True,
                "JSON syntax valid",
                details="File can be parsed as JSON"
            )
            return True
        except json.JSONDecodeError as e:
            self.add_result(
                ValidationLevel.BLOCKING,
                "json_syntax",
                False,
                f"JSON syntax invalid: {str(e)}",
                details="File cannot be parsed as JSON"
            )
            return False
        except Exception as e:
            self.add_result(
                ValidationLevel.BLOCKING,
                "json_syntax",
                False,
                f"Error reading file: {str(e)}"
            )
            return False

    def validate_required_fields(self) -> bool:
        """BLOCKING: Required fields present."""
        if self.data is None:
            return False

        # Common required fields
        required = ['pageName', 'url', 'primaryKeyword']

        # Phase-specific required fields
        if self.phase == 1:
            required.extend(['secondaryKeywords', 'writer', 'priority'])
        elif self.phase == 2:
            required.extend(['contentStructure', 'faqs'])

        missing = [field for field in required if field not in self.data]
        passed = len(missing) == 0

        self.add_result(
            ValidationLevel.BLOCKING,
            "required_fields",
            passed,
            "All required fields present" if passed else f"Missing fields: {', '.join(missing)}",
            details=f"Phase {self.phase} requires: {', '.join(required)}"
        )
        return passed

    def validate_schema_compliance(self) -> bool:
        """BLOCKING: Schema compliance."""
        if self.data is None:
            return False

        issues = []

        # Validate primaryKeyword structure
        if 'primaryKeyword' in self.data:
            pk = self.data['primaryKeyword']
            if isinstance(pk, dict):
                if 'keyword' not in pk or 'volume' not in pk:
                    issues.append("primaryKeyword missing 'keyword' or 'volume'")
            else:
                issues.append("primaryKeyword should be an object")

        # Validate secondaryKeywords structure (Phase 1)
        if self.phase == 1 and 'secondaryKeywords' in self.data:
            sk = self.data['secondaryKeywords']
            if isinstance(sk, list):
                if len(sk) < 5:
                    issues.append(f"secondaryKeywords has only {len(sk)} items (recommend 8+)")
                for idx, kw in enumerate(sk):
                    if not isinstance(kw, dict) or 'keyword' not in kw or 'volume' not in kw:
                        issues.append(f"secondaryKeywords[{idx}] invalid structure")
                        break
            else:
                issues.append("secondaryKeywords should be an array")

        # Validate FAQs structure (Phase 2)
        if self.phase == 2 and 'faqs' in self.data:
            faqs = self.data['faqs']
            if isinstance(faqs, list):
                if len(faqs) < 5:
                    issues.append(f"faqs has only {len(faqs)} items (recommend 7+)")
                for idx, faq in enumerate(faqs):
                    if not isinstance(faq, dict) or 'question' not in faq or 'answer' not in faq:
                        issues.append(f"faqs[{idx}] missing 'question' or 'answer'")
                        break
            else:
                issues.append("faqs should be an array")

        passed = len(issues) == 0

        self.add_result(
            ValidationLevel.BLOCKING,
            "schema_compliance",
            passed,
            "Schema compliance verified" if passed else f"Schema issues: {', '.join(issues)}",
            details="Data structure matches expected format"
        )
        return passed

    def validate_best_practices(self) -> bool:
        """ADVISORY: Best practices followed."""
        if self.data is None:
            return False

        suggestions = []

        # Check secondary keyword count (Phase 1)
        if self.phase == 1 and 'secondaryKeywords' in self.data:
            count = len(self.data['secondaryKeywords'])
            if count < 8:
                suggestions.append(f"Only {count} secondary keywords (recommend 8-15)")

        # Check FAQ count (Phase 2)
        if self.phase == 2 and 'faqs' in self.data:
            count = len(self.data['faqs'])
            if count < 7:
                suggestions.append(f"Only {count} FAQs (recommend 7+)")

        # Check word count targets (Phase 2)
        if self.phase == 2 and 'contentStructure' in self.data:
            cs = self.data['contentStructure']
            if isinstance(cs, dict) and 'sections' in cs:
                sections_without_wordcount = sum(
                    1 for s in cs['sections']
                    if isinstance(s, dict) and 'wordCount' not in s
                )
                if sections_without_wordcount > 0:
                    suggestions.append(f"{sections_without_wordcount} sections missing wordCount")

        passed = len(suggestions) == 0

        self.add_result(
            ValidationLevel.ADVISORY,
            "best_practices",
            passed,
            "Best practices followed" if passed else f"Suggestions: {', '.join(suggestions)}",
            details="Following best practices improves brief quality"
        )
        return passed

    def validate_optimization_opportunities(self) -> bool:
        """INFO: Optimization opportunities."""
        if self.data is None:
            return False

        opportunities = []

        # Check for keyword placement details (Phase 1)
        if self.phase == 1 and 'secondaryKeywords' in self.data:
            sk = self.data['secondaryKeywords']
            if isinstance(sk, list):
                without_placement = sum(1 for kw in sk if isinstance(kw, dict) and 'placement' not in kw)
                if without_placement > 0:
                    opportunities.append(f"{without_placement} keywords missing 'placement' field")

        # Check for internal linking (Phase 2)
        if self.phase == 2 and 'internalLinks' in self.data:
            links = self.data.get('internalLinks', [])
            if isinstance(links, list) and len(links) < 12:
                opportunities.append(f"Only {len(links)} internal links (recommend 12+)")

        # Check for competitor analysis
        if 'competitors' in self.data:
            competitors = self.data['competitors']
            if isinstance(competitors, list) and len(competitors) < 3:
                opportunities.append(f"Only {len(competitors)} competitors analyzed (recommend 3+)")

        passed = len(opportunities) == 0

        self.add_result(
            ValidationLevel.INFO,
            "optimization_opportunities",
            passed,
            "Fully optimized" if passed else f"Opportunities: {', '.join(opportunities)}",
            details="Additional optimizations could enhance the brief"
        )
        return passed

    def validate_all(self):
        """Run all phase JSON validations."""
        if self.validate_json_syntax():
            self.validate_required_fields()
            self.validate_schema_compliance()
            self.validate_best_practices()
            self.validate_optimization_opportunities()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate phase JSON file')
    parser.add_argument('json_file', help='Path to phase JSON file')
    parser.add_argument('--strict', action='store_true', help='Strict mode - fail on any warning')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    # Check file exists
    if not Path(args.json_file).exists():
        print(f"Error: File not found: {args.json_file}")
        sys.exit(1)

    # Validate
    validator = PhaseJSONValidator(args.json_file, strict_mode=args.strict)
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
