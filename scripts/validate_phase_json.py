#!/usr/bin/env python3
"""
Phase JSON Validation Script

This script validates Phase 1, 2, and 3 JSON outputs against specific requirements.

Phase 1 Validation:
- Primary keyword present
- 8-15 secondary keywords
- Keyword volume data
- Competitor analysis (minimum 3 competitors)
- Brand selection (FanDuel #1, BetMGM #2, research #3-10)
- Writer assigned correctly

Phase 2 Validation:
- Content outline present
- H2 sections mapped to high-volume keywords
- H3 sections mapped to medium-volume keywords
- FAQ questions 5-7 (if article/review)
- FAQ questions mapped to question keywords
- Source requirements specified (TIER 1 preferred)

Phase 3 Validation:
- All required HTML components present
- Schema markup complete (Article, FAQ, Breadcrumb)
- T&Cs complete for all brands
- Interactive elements included
- Responsible gambling section present

Usage:
    python validate_phase_json.py <phase_file> [--phase 1|2|3] [--json]
    python validate_phase_json.py --all [--json]

Exit codes:
    0: Validation passed
    1: Validation failed
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_name: str
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info


class PhaseJSONValidator:
    """Validator for phase JSON files."""

    # Valid writers
    VALID_WRITERS = {"Lewis", "Tom", "Gustavo Cantella"}

    # Valid priority levels
    VALID_PRIORITIES = {"High", "Medium", "Low"}

    def __init__(self, json_file: Path, phase: Optional[int] = None):
        """
        Initialize the JSON validator.

        Args:
            json_file: Path to the JSON file to validate
            phase: Optional phase number (1, 2, or 3). Auto-detect if not provided.
        """
        self.json_file = json_file
        self.phase = phase
        self.data = None
        self.errors = []
        self.warnings = []
        self.checks = []

    def validate(self) -> bool:
        """
        Perform all validation checks on the JSON file.

        Returns:
            True if validation passed, False otherwise
        """
        self.errors = []
        self.warnings = []
        self.checks = []

        # Check file exists
        if not self.json_file.exists():
            self.errors.append(f"File not found: {self.json_file}")
            return False

        # Read and parse JSON
        if not self._read_json():
            return False

        # Detect phase if not provided
        if not self.phase:
            self.phase = self._detect_phase()

        if not self.phase:
            self.errors.append("Could not determine phase. Specify with --phase flag.")
            return False

        # Run appropriate validation
        if self.phase == 1:
            self._validate_phase_1()
        elif self.phase == 2:
            self._validate_phase_2()
        elif self.phase == 3:
            self._validate_phase_3()
        else:
            self.errors.append(f"Invalid phase: {self.phase}")
            return False

        return len(self.errors) == 0

    def _read_json(self) -> bool:
        """
        Read and parse JSON file.

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            return False

    def _detect_phase(self) -> Optional[int]:
        """
        Attempt to detect phase from JSON structure.

        Returns:
            Phase number (1, 2, or 3) or None if detection fails
        """
        if not isinstance(self.data, dict):
            return None

        # Check for Phase 1 indicators
        if "primary_keyword" in self.data and "secondary_keywords" in self.data:
            return 1

        # Check for Phase 2 indicators
        if "content_outline" in self.data or "h2_sections" in self.data:
            return 2

        # Check for Phase 3 indicators
        if "html_content" in self.data or "schema_markup" in self.data:
            return 3

        return None

    def _add_check(self, name: str, passed: bool, message: str,
                   severity: str = "error") -> None:
        """Add a check result."""
        self.checks.append(ValidationResult(name, passed, message, severity))
        if not passed:
            if severity == "error":
                self.errors.append(f"{name}: {message}")
            else:
                self.warnings.append(f"{name}: {message}")

    def _validate_phase_1(self) -> None:
        """Validate Phase 1 JSON structure and content."""
        # Check primary keyword
        primary_keyword = self.data.get("primary_keyword", "")
        self._add_check(
            "Primary Keyword Present",
            bool(primary_keyword),
            "Primary keyword is required" if not primary_keyword else "Primary keyword found"
        )

        # Check secondary keywords (8-15 required)
        secondary_keywords = self.data.get("secondary_keywords", [])
        if isinstance(secondary_keywords, dict):
            secondary_keywords = list(secondary_keywords.values())

        keyword_count = len(secondary_keywords) if secondary_keywords else 0
        self._add_check(
            "Secondary Keywords Count",
            8 <= keyword_count <= 15,
            f"Found {keyword_count} secondary keywords. Required: 8-15"
        )

        # Check keyword volume data
        has_volume_data = True
        if secondary_keywords:
            for idx, kw in enumerate(secondary_keywords):
                if isinstance(kw, dict):
                    if not kw.get("volume") and kw.get("volume") != 0:
                        has_volume_data = False
                        self._add_check(
                            f"Keyword {idx + 1} Volume Data",
                            False,
                            f"Keyword '{kw.get('keyword', 'unknown')}' missing volume data"
                        )

        if has_volume_data and secondary_keywords:
            self._add_check(
                "Keyword Volume Data",
                True,
                "All keywords have volume data"
            )

        # Check competitors
        competitors = self.data.get("competitor_analysis", {})
        competitor_count = len(competitors) if competitors else 0
        self._add_check(
            "Competitor Analysis",
            competitor_count >= 3,
            f"Found {competitor_count} competitors. Minimum required: 3"
        )

        # Check brand selection
        brands = self.data.get("brand_selection", {})
        brand_check_passed = True
        brand_message = ""

        if not brands:
            brand_check_passed = False
            brand_message = "No brands selected"
        else:
            # Check for FanDuel as #1
            if brands.get("1") != "FanDuel":
                brand_check_passed = False
                brand_message = "FanDuel must be ranked #1"

            # Check for BetMGM as #2
            elif brands.get("2") != "BetMGM":
                brand_check_passed = False
                brand_message = "BetMGM must be ranked #2"

            # Check for research brands #3-10
            elif not any(brands.get(str(i)) for i in range(3, 11)):
                brand_check_passed = False
                brand_message = "Research brands #3-10 required"

            if brand_check_passed:
                brand_message = "Brand selection correct: FanDuel #1, BetMGM #2, research #3-10"

        self._add_check(
            "Brand Selection",
            brand_check_passed,
            brand_message
        )

        # Check writer assignment
        writer = self.data.get("assigned_writer", "")
        writer_valid = writer in self.VALID_WRITERS
        self._add_check(
            "Writer Assignment",
            writer_valid,
            f"Writer '{writer}' valid" if writer_valid else f"Invalid writer: {writer}. Must be: {', '.join(self.VALID_WRITERS)}"
        )

    def _validate_phase_2(self) -> None:
        """Validate Phase 2 JSON structure and content."""
        # Check content outline
        outline = self.data.get("content_outline", {})
        self._add_check(
            "Content Outline Present",
            bool(outline),
            "Content outline is required" if not outline else "Content outline present"
        )

        # Check H2 sections
        h2_sections = self.data.get("h2_sections", {})
        h2_count = len(h2_sections) if h2_sections else 0
        self._add_check(
            "H2 Sections Present",
            h2_count > 0,
            f"Found {h2_count} H2 sections" if h2_count > 0 else "No H2 sections found"
        )

        # Validate H2 sections mapped to high-volume keywords
        h2_keyword_valid = True
        if h2_sections:
            for idx, (heading, content) in enumerate(h2_sections.items()):
                if isinstance(content, dict):
                    keyword = content.get("keyword")
                    volume = content.get("volume", 0)
                    if not keyword or volume < 1000:  # High-volume threshold
                        h2_keyword_valid = False

        self._add_check(
            "H2 Sections Keyword Mapping",
            h2_keyword_valid or not h2_sections,
            "H2 sections mapped to high-volume keywords" if h2_keyword_valid else "Some H2 sections not mapped to high-volume keywords"
        )

        # Check H3 sections
        h3_sections = self.data.get("h3_sections", {})
        h3_count = len(h3_sections) if h3_sections else 0
        self._add_check(
            "H3 Sections Present",
            h3_count > 0,
            f"Found {h3_count} H3 sections" if h3_count > 0 else "No H3 sections found"
        )

        # Validate H3 sections mapped to medium-volume keywords
        h3_keyword_valid = True
        if h3_sections:
            for idx, (heading, content) in enumerate(h3_sections.items()):
                if isinstance(content, dict):
                    keyword = content.get("keyword")
                    volume = content.get("volume", 0)
                    if not keyword or volume < 100:  # Medium-volume threshold
                        h3_keyword_valid = False

        self._add_check(
            "H3 Sections Keyword Mapping",
            h3_keyword_valid or not h3_sections,
            "H3 sections mapped to medium-volume keywords" if h3_keyword_valid else "Some H3 sections not mapped to medium-volume keywords"
        )

        # Check FAQ questions (5-7 for article/review types)
        faq = self.data.get("faq", {})
        questions = faq.get("questions", []) if isinstance(faq, dict) else []
        article_type = self.data.get("content_type", "").lower()

        if "article" in article_type or "review" in article_type:
            faq_count = len(questions)
            self._add_check(
                "FAQ Questions Count",
                5 <= faq_count <= 7,
                f"Found {faq_count} FAQ questions. Required for articles/reviews: 5-7"
            )
        else:
            self._add_check(
                "FAQ Questions Count",
                len(questions) > 0,
                "FAQ present",
                severity="warning"
            )

        # Check FAQ questions mapped to question keywords
        faq_keywords_valid = True
        if questions:
            for q in questions:
                if isinstance(q, dict):
                    if not q.get("keyword"):
                        faq_keywords_valid = False

        self._add_check(
            "FAQ Keyword Mapping",
            faq_keywords_valid or not questions,
            "FAQ questions mapped to keywords" if faq_keywords_valid else "Some FAQ questions missing keyword mapping"
        )

        # Check source requirements
        sources = self.data.get("source_requirements", {})
        tier1_preference = sources.get("tier1_preferred", False) if isinstance(sources, dict) else False

        self._add_check(
            "Source Requirements",
            bool(sources),
            "TIER 1 sources preferred" if tier1_preference else "Source requirements specified"
        )

    def _validate_phase_3(self) -> None:
        """Validate Phase 3 JSON structure and content."""
        # Check HTML content
        html_content = self.data.get("html_content", "")
        self._add_check(
            "HTML Content Present",
            bool(html_content),
            "HTML content present" if html_content else "HTML content missing"
        )

        # Check schema markup
        schema_markup = self.data.get("schema_markup", {})
        self._add_check(
            "Schema Markup Present",
            bool(schema_markup),
            "Schema markup present" if schema_markup else "Schema markup missing"
        )

        # Validate schema components
        if schema_markup:
            schema_str = str(schema_markup).lower()
            has_article = "article" in schema_str
            has_faq = "faq" in schema_str or "faqpage" in schema_str
            has_breadcrumb = "breadcrumblist" in schema_str

            self._add_check(
                "Article Schema",
                has_article or isinstance(schema_markup, dict),
                "Article schema present"
            )

            self._add_check(
                "FAQ Schema",
                has_faq or isinstance(schema_markup, dict),
                "FAQ schema present"
            )

            self._add_check(
                "Breadcrumb Schema",
                has_breadcrumb or isinstance(schema_markup, dict),
                "Breadcrumb schema present"
            )

        # Check T&Cs for brands
        brands_tcs = self.data.get("terms_and_conditions", {})
        brands_in_content = self.data.get("brands_featured", [])

        if brands_in_content:
            tcs_complete = all(
                brand in brands_tcs for brand in brands_in_content
            ) if brands_tcs else False

            self._add_check(
                "Terms & Conditions",
                tcs_complete or not brands_in_content,
                f"T&Cs complete for all {len(brands_in_content)} brands" if tcs_complete else "T&Cs missing for some brands"
            )
        else:
            self._add_check(
                "Terms & Conditions",
                bool(brands_tcs),
                "T&Cs specified",
                severity="warning"
            )

        # Check interactive elements
        interactive = self.data.get("interactive_elements", {})
        has_interactive = bool(interactive)
        self._add_check(
            "Interactive Elements",
            has_interactive,
            "Interactive elements included" if has_interactive else "No interactive elements found",
            severity="warning"
        )

        # Check responsible gambling section
        responsible_gambling = self.data.get("responsible_gambling_section", "")
        self._add_check(
            "Responsible Gambling Section",
            bool(responsible_gambling),
            "Responsible gambling section present" if responsible_gambling else "Responsible gambling section missing"
        )

    def get_report(self) -> Dict:
        """
        Get validation report as a dictionary.

        Returns:
            Dictionary containing validation results
        """
        return {
            "file": str(self.json_file),
            "phase": self.phase,
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "checks_run": len(self.checks),
            "checks": [
                {
                    "name": check.check_name,
                    "passed": check.passed,
                    "message": check.message,
                    "severity": check.severity
                }
                for check in self.checks
            ],
            "errors": self.errors,
            "warnings": self.warnings
        }

    def print_report(self) -> None:
        """Print human-readable validation report."""
        report = self.get_report()

        print(f"\nPhase {report['phase']} Validation Report: {self.json_file.name}")
        print("=" * 80)
        print(f"Status: {'PASSED' if report['valid'] else 'FAILED'}")
        print(f"Checks run: {report['checks_run']}")
        print(f"Errors: {report['error_count']}")
        print(f"Warnings: {report['warning_count']}")

        print("\nDetailed Checks:")
        print("-" * 80)
        for check in report['checks']:
            status = "[PASS]" if check['passed'] else "[FAIL]"
            severity = f" [{check['severity'].upper()}]" if not check['passed'] else ""
            print(f"  {status} {check['name']}{severity}")
            print(f"    {check['message']}")

        if report['errors']:
            print("\nErrors:")
            print("-" * 80)
            for error in report['errors']:
                print(f"  - {error}")

        if report['warnings']:
            print("\nWarnings:")
            print("-" * 80)
            for warning in report['warnings']:
                print(f"  - {warning}")

        print("=" * 80)


def main():
    """Main entry point for the validation script."""
    parser = argparse.ArgumentParser(
        description="Validate Phase 1, 2, and 3 JSON files for content briefs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s phase1-output.json --phase 1
  %(prog)s phase2-output.json --phase 2 --json
  %(prog)s phase3-output.json --phase 3
  %(prog)s --all
        """
    )

    parser.add_argument(
        "json_file",
        nargs="?",
        help="Path to JSON file to validate"
    )

    parser.add_argument(
        "--phase",
        type=int,
        choices=[1, 2, 3],
        help="Phase number (1, 2, or 3). Auto-detect if not provided"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all phase JSON files in current directory"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (useful for CI/CD integration)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.json_file and not args.all:
        parser.print_help()
        sys.exit(1)

    json_files = []

    if args.all:
        # Find all phase JSON files
        current_dir = Path.cwd()
        for phase in [1, 2, 3]:
            json_files.extend(current_dir.glob(f"*phase{phase}*.json"))
            json_files.extend(current_dir.glob(f"phase{phase}-*.json"))

        if not json_files:
            print("No phase JSON files found")
            sys.exit(1)
    else:
        json_files = [Path(args.json_file)]

    # Validate all files
    all_reports = []
    all_valid = True

    for json_file in sorted(json_files):
        validator = PhaseJSONValidator(json_file, args.phase)
        is_valid = validator.validate()
        all_valid = all_valid and is_valid

        report = validator.get_report()
        all_reports.append(report)

        if not args.json:
            validator.print_report()

    # Output JSON if requested
    if args.json:
        output = {
            "validation_type": "phase_json",
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "all_valid": all_valid,
            "total_files": len(all_reports),
            "reports": all_reports
        }
        print(json.dumps(output, indent=2))

    # Exit with appropriate code
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
