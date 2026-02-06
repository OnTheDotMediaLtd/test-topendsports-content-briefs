#!/usr/bin/env python3
"""CSV configuration validation with tiered system."""

import sys
import csv
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


class CSVConfigValidator(TieredValidator):
    """Validates CSV configuration files."""

    def __init__(self, csv_path: str, strict_mode: bool = False):
        super().__init__(strict_mode)
        self.csv_path = csv_path
        self.rows = []
        self.headers = []

    def validate_format(self) -> bool:
        """BLOCKING: CSV format is valid."""
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames or []
                self.rows = list(reader)

            self.add_result(
                ValidationLevel.BLOCKING,
                "csv_format",
                True,
                f"CSV format valid ({len(self.rows)} rows, {len(self.headers)} columns)",
                details="File can be parsed as CSV"
            )
            return True
        except Exception as e:
            self.add_result(
                ValidationLevel.BLOCKING,
                "csv_format",
                False,
                f"CSV format invalid: {str(e)}",
                details="File cannot be parsed as CSV"
            )
            return False

    def validate_required_columns(self) -> bool:
        """BLOCKING: Required columns present."""
        # Detect CSV type based on filename or headers
        filename = Path(self.csv_path).name.lower()

        if 'site-structure' in filename:
            # Allow flexible column names for site structure CSVs
            has_url = any(col in self.headers for col in ['url', 'URL', 'Full URL'])
            has_keyword = any(col in self.headers for col in ['primary_keyword', 'Target Keywords', 'keyword'])

            missing = []
            if not has_url:
                missing.append('URL column')
            if not has_keyword:
                missing.append('Keyword column')

            passed = len(missing) == 0

            self.add_result(
                ValidationLevel.BLOCKING,
                "required_columns",
                passed,
                "All required columns present" if passed else f"Missing: {', '.join(missing)}",
                details="Site structure CSVs need URL and keyword columns"
            )
            return passed
        elif 'keyword' in filename:
            required = ['keyword', 'volume']
        elif 'state' in filename:
            has_state = any(col in self.headers for col in ['state', 'State'])
            has_url = any(col in self.headers for col in ['url', 'URL', 'Full URL'])

            missing = []
            if not has_state:
                missing.append('State column')
            if not has_url:
                missing.append('URL column')

            passed = len(missing) == 0

            self.add_result(
                ValidationLevel.BLOCKING,
                "required_columns",
                passed,
                "All required columns present" if passed else f"Missing: {', '.join(missing)}",
                details="State CSVs need State and URL columns"
            )
            return passed
        else:
            # Generic requirement - skip
            self.add_result(
                ValidationLevel.BLOCKING,
                "required_columns",
                True,
                "CSV type not detected, skipping column check",
                details="No specific column requirements for this CSV type"
            )
            return True

        # For keyword CSVs
        missing = [col for col in required if col not in self.headers]
        passed = len(missing) == 0

        self.add_result(
            ValidationLevel.BLOCKING,
            "required_columns",
            passed,
            "All required columns present" if passed else f"Missing columns: {', '.join(missing)}",
            details=f"Required: {', '.join(required)}"
        )
        return passed

    def validate_data_integrity(self) -> bool:
        """BLOCKING: No data corruption (empty required fields)."""
        if not self.rows:
            self.add_result(
                ValidationLevel.BLOCKING,
                "data_integrity",
                False,
                "CSV is empty",
                details="No data rows found"
            )
            return False

        # Check for rows with all empty values
        empty_rows = []
        for idx, row in enumerate(self.rows):
            if all(not str(v).strip() for v in row.values()):
                empty_rows.append(idx + 2)  # +2 for header row and 1-indexed

        passed = len(empty_rows) == 0

        self.add_result(
            ValidationLevel.BLOCKING,
            "data_integrity",
            passed,
            "No empty rows found" if passed else f"Found {len(empty_rows)} empty rows: {empty_rows[:5]}",
            details="All rows should have at least one non-empty field"
        )
        return passed

    def validate_data_completeness(self) -> bool:
        """ADVISORY: Data completeness."""
        if not self.rows:
            return True

        # Check for rows with some missing values
        incomplete_count = 0
        for row in self.rows:
            empty_fields = sum(1 for v in row.values() if not str(v).strip())
            if empty_fields > 0 and empty_fields < len(row):
                incomplete_count += 1

        passed = incomplete_count == 0

        self.add_result(
            ValidationLevel.ADVISORY,
            "data_completeness",
            passed,
            f"All {len(self.rows)} rows complete" if passed else f"{incomplete_count} rows have missing fields",
            details="Some fields are empty in otherwise valid rows"
        )
        return passed

    def validate_data_quality(self) -> bool:
        """INFO: Data quality suggestions."""
        if not self.rows:
            return True

        # Check for potential issues
        issues = []

        # Check for duplicate values in key columns
        for col in self.headers:
            if col in ['url', 'keyword', 'state']:
                values = [str(row.get(col, '')).strip() for row in self.rows]
                non_empty = [v for v in values if v]
                if len(non_empty) != len(set(non_empty)):
                    duplicates = len(non_empty) - len(set(non_empty))
                    issues.append(f"{duplicates} duplicate {col} values")

        passed = len(issues) == 0

        self.add_result(
            ValidationLevel.INFO,
            "data_quality",
            passed,
            "No quality issues found" if passed else f"Quality suggestions: {', '.join(issues)}",
            details="Duplicate values may indicate data issues"
        )
        return passed

    def validate_all(self):
        """Run all CSV validations."""
        if self.validate_format():
            self.validate_required_columns()
            self.validate_data_integrity()
            self.validate_data_completeness()
            self.validate_data_quality()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate CSV configuration file')
    parser.add_argument('csv_file', help='Path to CSV file')
    parser.add_argument('--strict', action='store_true', help='Strict mode - fail on any warning')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    # Check file exists
    if not Path(args.csv_file).exists():
        print(f"Error: File not found: {args.csv_file}")
        sys.exit(1)

    # Validate
    validator = CSVConfigValidator(args.csv_file, strict_mode=args.strict)
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
