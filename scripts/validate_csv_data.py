#!/usr/bin/env python3
"""
CSV Data Validation Script

This script validates site structure CSV files for data quality, checking for:
- Duplicate URLs
- Missing required columns
- Invalid writer names
- URL format consistency
- Empty required fields
- Invalid priority values

Usage:
    python validate_csv_data.py <csv_file> [--json]
    python validate_csv_data.py --all [--json]

Exit codes:
    0: Validation passed
    1: Validation failed
"""

import csv
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class CSVValidator:
    """Validator for site structure CSV files."""

    # Required columns that must be present
    REQUIRED_COLUMNS = {"URL", "Keyword", "Writer", "Priority"}

    # Valid writer names
    VALID_WRITERS = {"Lewis", "Tom", "Gustavo Cantella"}

    # Valid priority levels
    VALID_PRIORITIES = {"High", "Medium", "Low"}

    # Expected URL format pattern (starts with /sport/)
    EXPECTED_URL_PREFIX = "/sport/"

    def __init__(self, csv_file: Path):
        """
        Initialize the CSV validator.

        Args:
            csv_file: Path to the CSV file to validate
        """
        self.csv_file = csv_file
        self.errors = []
        self.warnings = []
        self.rows = []
        self.headers = []

    def validate(self) -> bool:
        """
        Perform all validation checks on the CSV file.

        Returns:
            True if validation passed, False otherwise
        """
        self.errors = []
        self.warnings = []
        self.rows = []

        # Check file exists
        if not self.csv_file.exists():
            self.errors.append(f"File not found: {self.csv_file}")
            return False

        # Check file is readable
        if not self.csv_file.is_file():
            self.errors.append(f"Not a file: {self.csv_file}")
            return False

        # Read and parse CSV
        if not self._read_csv():
            return False

        # Perform validation checks
        self._validate_headers()
        self._validate_required_fields()
        self._validate_writers()
        self._validate_priorities()
        self._validate_urls()
        self._validate_duplicates()

        return len(self.errors) == 0

    def _read_csv(self) -> bool:
        """
        Read CSV file and parse contents.

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                if reader.fieldnames is None:
                    self.errors.append("CSV file is empty or invalid")
                    return False

                self.headers = list(reader.fieldnames)

                for row_num, row in enumerate(reader, start=2):  # start at 2 to account for header
                    self.rows.append((row_num, row))

            return True
        except UnicodeDecodeError:
            self.errors.append("File encoding error: must be UTF-8")
            return False
        except csv.Error as e:
            self.errors.append(f"CSV parsing error: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            return False

    def _validate_headers(self) -> None:
        """Validate that all required columns are present."""
        header_set = set(self.headers)
        missing_columns = self.REQUIRED_COLUMNS - header_set

        if missing_columns:
            self.errors.append(
                f"Missing required columns: {', '.join(sorted(missing_columns))}"
            )

    def _validate_required_fields(self) -> None:
        """Validate that required fields are not empty."""
        for line_num, row in self.rows:
            for column in self.REQUIRED_COLUMNS:
                if column not in row or not row[column] or not row[column].strip():
                    self.errors.append(
                        f"Line {line_num}: Empty required field '{column}'"
                    )

    def _validate_writers(self) -> None:
        """Validate that writer names are in the allowed list."""
        for line_num, row in self.rows:
            writer = row.get("Writer", "").strip()
            if writer and writer not in self.VALID_WRITERS:
                self.errors.append(
                    f"Line {line_num}: Invalid writer name '{writer}'. "
                    f"Must be one of: {', '.join(sorted(self.VALID_WRITERS))}"
                )

    def _validate_priorities(self) -> None:
        """Validate that priority values are correct."""
        for line_num, row in self.rows:
            priority = row.get("Priority", "").strip()
            if priority and priority not in self.VALID_PRIORITIES:
                self.errors.append(
                    f"Line {line_num}: Invalid priority '{priority}'. "
                    f"Must be one of: {', '.join(sorted(self.VALID_PRIORITIES))}"
                )

    def _validate_urls(self) -> None:
        """Validate URL format consistency."""
        for line_num, row in self.rows:
            url = row.get("URL", "").strip()
            if url:
                if not url.startswith(self.EXPECTED_URL_PREFIX):
                    self.errors.append(
                        f"Line {line_num}: URL format invalid '{url}'. "
                        f"URLs must start with '{self.EXPECTED_URL_PREFIX}'"
                    )

                # Check for spaces or other invalid characters
                if ' ' in url or url != url.strip():
                    self.errors.append(
                        f"Line {line_num}: URL contains invalid whitespace: '{url}'"
                    )

    def _validate_duplicates(self) -> None:
        """Validate that there are no duplicate URLs."""
        urls_seen = defaultdict(list)

        for line_num, row in self.rows:
            url = row.get("URL", "").strip()
            if url:
                urls_seen[url].append(line_num)

        for url, lines in urls_seen.items():
            if len(lines) > 1:
                self.errors.append(
                    f"Duplicate URL '{url}' found on lines: {', '.join(map(str, lines))}"
                )

    def get_report(self) -> Dict:
        """
        Get validation report as a dictionary.

        Returns:
            Dictionary containing validation results
        """
        return {
            "file": str(self.csv_file),
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "rows_validated": len(self.rows)
        }

    def print_report(self) -> None:
        """Print human-readable validation report."""
        report = self.get_report()

        print(f"\nValidation Report: {self.csv_file.name}")
        print("=" * 70)
        print(f"Status: {'PASSED' if report['valid'] else 'FAILED'}")
        print(f"Rows validated: {report['rows_validated']}")
        print(f"Errors: {report['error_count']}")
        print(f"Warnings: {report['warning_count']}")

        if report['errors']:
            print("\nErrors:")
            print("-" * 70)
            for error in report['errors']:
                print(f"  - {error}")

        if report['warnings']:
            print("\nWarnings:")
            print("-" * 70)
            for warning in report['warnings']:
                print(f"  - {warning}")

        print("=" * 70)


def main():
    """Main entry point for the validation script."""
    parser = argparse.ArgumentParser(
        description="Validate site structure CSV files for data quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s site-structure-english.csv
  %(prog)s site-structure-english.csv --json
  %(prog)s --all --json
        """
    )

    parser.add_argument(
        "csv_file",
        nargs="?",
        help="Path to CSV file to validate"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all CSV files in current and parent directories"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (useful for CI/CD integration)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.csv_file and not args.all:
        parser.print_help()
        sys.exit(1)

    csv_files = []

    if args.all:
        # Find all CSV files with "site-structure" in the name
        current_dir = Path.cwd()
        csv_files.extend(current_dir.glob("*site-structure*.csv"))
        csv_files.extend(current_dir.parent.glob("*site-structure*.csv"))

        if not csv_files:
            print("No site structure CSV files found")
            sys.exit(1)
    else:
        csv_files = [Path(args.csv_file)]

    # Validate all files
    all_reports = []
    all_valid = True

    for csv_file in sorted(csv_files):
        validator = CSVValidator(csv_file)
        is_valid = validator.validate()
        all_valid = all_valid and is_valid

        report = validator.get_report()
        all_reports.append(report)

        if not args.json:
            validator.print_report()

    # Output JSON if requested
    if args.json:
        output = {
            "validation_type": "csv_data",
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
