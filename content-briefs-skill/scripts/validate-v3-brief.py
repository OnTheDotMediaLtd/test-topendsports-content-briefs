#!/usr/bin/env python3
"""
V3 Brief Validation Script

Validates writer briefs against V3 quality standards.
Run after generating a brief to check compliance.

Usage:
    python3 validate-v3-brief.py [brief-file.md]
    python3 validate-v3-brief.py --all  # Validate all briefs in output/
    python3 validate-v3-brief.py --verbose [brief-file.md]

Exit codes:
    0 - All checks passed
    1 - Some checks failed
    2 - Error reading file
"""

import os
import sys
import re
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_name: str
    passed: bool
    message: str
    severity: str  # 'error', 'warning', 'info'


class V3BriefValidator:
    """Validates briefs against V3 quality standards."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[ValidationResult] = []

    def validate_file(self, filepath: Path) -> List[ValidationResult]:
        """Validate a single brief file."""
        self.results = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.results.append(ValidationResult(
                "File Read",
                False,
                f"Could not read file: {e}",
                "error"
            ))
            return self.results

        # Determine page type from content
        page_type = self._detect_page_type(content)

        # Run all V3 checks
        self._check_word_count_table(content)
        self._check_keyword_volume_total(content)
        self._check_unmapped_keywords(content)
        self._check_competitor_urls(content)
        self._check_writer_must_cover(content)
        self._check_internal_link_placement(content)
        self._check_eeat_requirements(content)
        self._check_mobile_section_limits(content, page_type)
        self._check_no_affiliate_disclosure(content)
        self._check_no_dated_language(content)

        return self.results

    def _detect_page_type(self, content: str) -> str:
        """Detect page type from content."""
        content_lower = content.lower()

        if 'hub page strategy' in content_lower or 'this is a hub page' in content_lower:
            return 'hub'
        elif 'template type' in content_lower:
            if 'template 1' in content_lower or 'review' in content_lower:
                return 'review'
            elif 'template 2' in content_lower or 'comparison' in content_lower:
                return 'comparison'
        return 'unknown'

    def _check_word_count_table(self, content: str):
        """Check for Word Count by Section table."""
        patterns = [
            r'word count targets by section',
            r'\|\s*section\s*\|\s*target words',
            r'\|\s*section\s*\|\s*words',
        ]

        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)

        self.results.append(ValidationResult(
            "Word Count Table",
            found,
            "Word Count by Section table found" if found else "Missing Word Count by Section table",
            "error" if not found else "info"
        ))

    def _check_keyword_volume_total(self, content: str):
        """Check for total secondary keyword volume."""
        patterns = [
            r'total secondary( keyword)? volume[:\s]+[\d,]+',
            r'secondary volume[:\s]+[\d,]+',
            r'total cluster volume[:\s]+[\d,]+',
        ]

        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)

        self.results.append(ValidationResult(
            "Keyword Volume Total",
            found,
            "Keyword volume total found" if found else "Missing total secondary keyword volume calculation",
            "error" if not found else "info"
        ))

    def _check_unmapped_keywords(self, content: str):
        """Check for 'Unmapped Keywords: NONE' statement."""
        patterns = [
            r'unmapped keywords[:\s]+none',
            r'unmapped[:\s]+none',
            r'\*\*unmapped keywords\*\*[:\s]+none',
        ]

        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)

        self.results.append(ValidationResult(
            "Unmapped Keywords Check",
            found,
            "'Unmapped Keywords: NONE' verification found" if found else "Missing 'Unmapped Keywords: NONE' verification",
            "error" if not found else "info"
        ))

    def _check_competitor_urls(self, content: str):
        """Check for competitor reference URLs."""
        patterns = [
            r'competitor references',
            r'competitor\s*\|\s*url',
            r'use these pages as benchmarks',
        ]

        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)

        # Also check for actual URLs
        url_pattern = r'https?://[^\s\|\)]+\.(com|net|org|ie|uk|ca)'
        urls_found = len(re.findall(url_pattern, content, re.IGNORECASE)) >= 2

        self.results.append(ValidationResult(
            "Competitor URLs",
            found and urls_found,
            "Competitor reference URLs section found" if (found and urls_found) else "Missing competitor reference URLs (need 2-3)",
            "error" if not (found and urls_found) else "info"
        ))

    def _check_writer_must_cover(self, content: str):
        """Check for 'Writer must cover' bullets."""
        pattern = r'writer must (cover|include)'
        matches = re.findall(pattern, content, re.IGNORECASE)

        # Should have multiple instances (at least 5 for a proper brief)
        count = len(matches)
        passed = count >= 5

        self.results.append(ValidationResult(
            "Writer Must Cover Bullets",
            passed,
            f"Found {count} 'Writer must cover/include' sections" if passed else f"Only {count} 'Writer must cover' sections (need 5+)",
            "error" if not passed else "info"
        ))

    def _check_internal_link_placement(self, content: str):
        """Check that internal links are mapped to specific sections."""
        # Look for internal links table with placement column
        patterns = [
            r'\|\s*#\s*\|\s*anchor\s*.*\|\s*.*placement',
            r'\|\s*anchor text\s*\|\s*target url\s*\|\s*.*section',
            r'exact placement section',
        ]

        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)

        # Check for vague "within 500 words" without specific section
        vague_pattern = r'within\s+(\d+)\s+words'
        specific_pattern = r'(introduction|quick answer|brand section|h2|paragraph)'

        has_vague = bool(re.search(vague_pattern, content, re.IGNORECASE))
        has_specific = bool(re.search(specific_pattern, content, re.IGNORECASE))

        passed = found or (has_specific and not has_vague)

        self.results.append(ValidationResult(
            "Internal Link Placement",
            passed,
            "Internal links mapped to specific sections" if passed else "Internal links need specific section placement (not just 'within X words')",
            "warning" if not passed else "info"
        ))

    def _check_eeat_requirements(self, content: str):
        """Check for E-E-A-T author requirements."""
        patterns = [
            r'e-e-a-t',
            r'author (name|credentials|bio)',
            r'author information',
        ]

        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)

        self.results.append(ValidationResult(
            "E-E-A-T Requirements",
            found,
            "E-E-A-T author requirements found" if found else "Missing E-E-A-T author requirements (author name, credentials, bio link)",
            "error" if not found else "info"
        ))

    def _check_mobile_section_limits(self, content: str, page_type: str):
        """Check mobile section word limits based on page type."""
        # Extract mobile section word counts
        mobile_pattern = r'mobile\s+experience.*?(\d+)-?(\d+)?\s*words'
        matches = re.findall(mobile_pattern, content, re.IGNORECASE)

        if not matches:
            self.results.append(ValidationResult(
                "Mobile Section Limits",
                True,
                "No mobile section word counts detected (manual check needed)",
                "warning"
            ))
            return

        # Check limits based on page type
        max_words = 100 if page_type == 'hub' else 150 if page_type == 'comparison' else 200

        issues = []
        for match in matches:
            upper_limit = int(match[1]) if match[1] else int(match[0])
            if upper_limit > max_words:
                issues.append(f"{upper_limit} words exceeds {max_words} limit for {page_type} pages")

        passed = len(issues) == 0

        self.results.append(ValidationResult(
            "Mobile Section Limits",
            passed,
            f"Mobile sections within {max_words}w limit for {page_type}" if passed else f"Mobile sections exceed limit: {'; '.join(issues)}",
            "error" if not passed else "info"
        ))

    def _check_no_affiliate_disclosure(self, content: str):
        """Check that affiliate disclosure is NOT in content."""
        patterns = [
            r'affiliate\s+disclosure',
            r'we\s+may\s+(earn|receive)\s+(a\s+)?commission',
            r'advertising\s+disclosure',
        ]

        # Should NOT find these (it's in sidebar)
        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)

        # Exception: "NO affiliate disclosure" is fine
        exception = re.search(r'no\s+affiliate\s+disclosure', content, re.IGNORECASE)

        passed = not found or exception

        self.results.append(ValidationResult(
            "No Affiliate Disclosure",
            passed,
            "No affiliate disclosure in content (correct - it's in sidebar)" if passed else "Remove affiliate disclosure from content (it's in website sidebar)",
            "error" if not passed else "info"
        ))

    def _check_no_dated_language(self, content: str):
        """Check for dated language in H1/titles."""
        # Look for year references in H1 context
        h1_pattern = r'#\s+[^\n]+\s+(2024|2025|january|february|march|april|may|june|july|august|september|october|november|december)'

        found = bool(re.search(h1_pattern, content, re.IGNORECASE))

        # Exception: "Last Updated" is fine
        exception = re.search(r'last\s+updated', content, re.IGNORECASE)

        passed = not found or exception

        self.results.append(ValidationResult(
            "No Dated Language",
            passed,
            "No dated language in H1/titles" if passed else "Remove dates from H1/titles (use Last Updated badge instead)",
            "warning" if not passed else "info"
        ))

    def print_results(self, filepath: Path):
        """Print validation results."""
        print(f"\n{'=' * 60}")
        print(f"V3 VALIDATION REPORT: {filepath.name}")
        print(f"{'=' * 60}\n")

        errors = [r for r in self.results if not r.passed and r.severity == 'error']
        warnings = [r for r in self.results if not r.passed and r.severity == 'warning']
        passed = [r for r in self.results if r.passed]

        if errors:
            print("ERRORS (must fix):")
            for r in errors:
                print(f"  [{r.check_name}] {r.message}")
            print()

        if warnings:
            print("WARNINGS (should fix):")
            for r in warnings:
                print(f"  [{r.check_name}] {r.message}")
            print()

        if self.verbose and passed:
            print("PASSED:")
            for r in passed:
                print(f"  [{r.check_name}] {r.message}")
            print()

        # Summary
        total = len(self.results)
        passed_count = len(passed)
        error_count = len(errors)
        warning_count = len(warnings)

        print(f"{'=' * 60}")
        print(f"SUMMARY: {passed_count}/{total} checks passed")
        if error_count > 0:
            print(f"         {error_count} errors, {warning_count} warnings")
        print(f"{'=' * 60}")

        return error_count == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate writer briefs against V3 standards',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'file',
        nargs='?',
        help='Brief file to validate (or --all for all briefs)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all writer briefs in output/'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show all checks including passed ones'
    )

    args = parser.parse_args()

    # Find the output directory
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / 'output'

    if args.all:
        # Validate all writer briefs
        brief_files = list(output_dir.glob('*-writer-brief.md'))

        if not brief_files:
            print(f"No writer briefs found in {output_dir}")
            return 1

        print(f"Validating {len(brief_files)} writer briefs...")

        all_passed = True
        failed_files = []

        for filepath in sorted(brief_files):
            validator = V3BriefValidator(verbose=args.verbose)
            validator.validate_file(filepath)

            errors = [r for r in validator.results if not r.passed and r.severity == 'error']

            if errors:
                failed_files.append(filepath.name)
                all_passed = False
                if args.verbose:
                    validator.print_results(filepath)
            else:
                print(f"  [PASS] {filepath.name}")

        print(f"\n{'=' * 60}")
        print(f"BATCH SUMMARY: {len(brief_files) - len(failed_files)}/{len(brief_files)} briefs passed")

        if failed_files:
            print(f"\nFailed briefs ({len(failed_files)}):")
            for f in failed_files:
                print(f"  - {f}")
            print(f"\nRun with --verbose to see detailed errors")

        print(f"{'=' * 60}")

        return 0 if all_passed else 1

    elif args.file:
        # Validate single file
        filepath = Path(args.file)

        if not filepath.exists():
            # Try relative to output dir
            filepath = output_dir / args.file

        if not filepath.exists():
            print(f"File not found: {args.file}")
            return 2

        validator = V3BriefValidator(verbose=args.verbose)
        validator.validate_file(filepath)
        passed = validator.print_results(filepath)

        return 0 if passed else 1

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
