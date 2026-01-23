#!/usr/bin/env python3
"""
Feedback Validation Script

This script validates feedback submissions for correct format and content.

Required Format:
- Filename: YYYY-MM-DD-topic.md
- Date in filename must be valid
- Must contain specific markdown sections:
  - ## Issue/Improvement
  - ## Impact
  - ## Suggested Solution
  - ## Example (if applicable)
- Impact level specified: Critical, High, Medium, or Low
- Minimum 50 words in Issue section
- Valid markdown format

Usage:
    python validate_feedback.py <feedback_file> [--json]
    python validate_feedback.py --all [--json]

Exit codes:
    0: Validation passed
    1: Validation failed
"""

import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a single validation error."""
    line_number: Optional[int]
    message: str
    suggestion: Optional[str] = None


class FeedbackValidator:
    """Validator for feedback submission files."""

    # Required markdown sections
    REQUIRED_SECTIONS = {
        "Issue/Improvement",
        "Impact",
        "Suggested Solution"
    }

    OPTIONAL_SECTIONS = {"Example"}

    # Valid impact levels
    VALID_IMPACT_LEVELS = {"Critical", "High", "Medium", "Low"}

    # Minimum word count for Issue section
    MIN_ISSUE_WORDS = 50

    def __init__(self, feedback_file: Path):
        """
        Initialize the feedback validator.

        Args:
            feedback_file: Path to the feedback markdown file
        """
        self.feedback_file = feedback_file
        self.errors = []
        self.warnings = []
        self.content = ""
        self.lines = []

    def validate(self) -> bool:
        """
        Perform all validation checks on the feedback file.

        Returns:
            True if validation passed, False otherwise
        """
        self.errors = []
        self.warnings = []
        self.content = ""
        self.lines = []

        # Check file exists
        if not self.feedback_file.exists():
            self.errors.append(ValidationError(
                None,
                f"File not found: {self.feedback_file}"
            ))
            return False

        # Check file is readable
        if not self.feedback_file.is_file():
            self.errors.append(ValidationError(
                None,
                f"Not a file: {self.feedback_file}"
            ))
            return False

        # Validate filename format
        if not self._validate_filename():
            return False

        # Read file content
        if not self._read_file():
            return False

        # Perform validation checks
        self._validate_markdown_format()
        self._validate_required_sections()
        self._validate_impact_level()
        self._validate_issue_length()
        self._validate_markdown_syntax()

        return len(self.errors) == 0

    def _validate_filename(self) -> bool:
        """
        Validate filename format: YYYY-MM-DD-topic.md

        Returns:
            True if valid, False otherwise
        """
        filename = self.feedback_file.name
        pattern = r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$"
        match = re.match(pattern, filename)

        if not match:
            self.errors.append(ValidationError(
                None,
                f"Invalid filename format: '{filename}'. Expected: YYYY-MM-DD-topic.md",
                "Example: 2024-12-09-performance-improvement.md"
            ))
            return False

        # Validate date
        year, month, day, topic = match.groups()
        try:
            date_obj = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

            # Warn if date is in the future
            if date_obj > datetime.now():
                self.warnings.append(ValidationError(
                    None,
                    f"Filename date is in the future: {year}-{month}-{day}"
                ))
        except ValueError:
            self.errors.append(ValidationError(
                None,
                f"Invalid date in filename: {year}-{month}-{day}",
                "Date must be valid YYYY-MM-DD format"
            ))
            return False

        # Validate topic
        if not topic or not re.match(r"^[a-z0-9\-]+$", topic):
            self.errors.append(ValidationError(
                None,
                f"Invalid topic in filename: '{topic}'. Topic must contain only lowercase letters, numbers, and hyphens"
            ))
            return False

        return True

    def _read_file(self) -> bool:
        """
        Read file content.

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
            return True
        except UnicodeDecodeError:
            self.errors.append(ValidationError(
                None,
                "File encoding error: must be UTF-8"
            ))
            return False
        except Exception as e:
            self.errors.append(ValidationError(
                None,
                f"Error reading file: {str(e)}"
            ))
            return False

    def _validate_markdown_format(self) -> None:
        """Validate basic markdown format."""
        if not self.content.strip():
            self.errors.append(ValidationError(
                None,
                "File is empty"
            ))

    def _validate_required_sections(self) -> None:
        """Validate that all required sections are present."""
        found_sections = set()

        for line_num, line in enumerate(self.lines, start=1):
            # Look for ## section headers
            match = re.match(r"^##\s+(.+?)(?:\s*#*)?$", line.strip())
            if match:
                section_name = match.group(1).strip()
                found_sections.add(section_name)

        # Check for each required section
        for required in self.REQUIRED_SECTIONS:
            found = any(required.lower() in section.lower() for section in found_sections)

            if not found:
                self.errors.append(ValidationError(
                    None,
                    f"Missing required section: '## {required}'",
                    f"Add a section like: ## {required}"
                ))

    def _validate_impact_level(self) -> None:
        """Validate that impact level is specified correctly."""
        impact_pattern = r"^Impact Level:\s*(.+?)(?:\s*$|[;\.])"
        found_impact = False

        for line_num, line in enumerate(self.lines, start=1):
            match = re.search(impact_pattern, line, re.IGNORECASE)
            if match:
                impact_level = match.group(1).strip()
                found_impact = True

                if impact_level not in self.VALID_IMPACT_LEVELS:
                    self.errors.append(ValidationError(
                        line_num,
                        f"Invalid impact level: '{impact_level}'. Must be one of: {', '.join(self.VALID_IMPACT_LEVELS)}",
                        f"Change to: Impact Level: {self.VALID_IMPACT_LEVELS.pop()}"
                    ))

        if not found_impact:
            # Check if it's in the content but not formatted correctly
            if any(word in self.content.lower() for word in ["critical", "high", "medium", "low"]):
                self.warnings.append(ValidationError(
                    None,
                    "Impact level detected in content but not in standard format",
                    "Add 'Impact Level: [Level]' explicitly"
                ))
            else:
                self.errors.append(ValidationError(
                    None,
                    "Impact level not specified",
                    "Add 'Impact Level: Critical|High|Medium|Low' to your feedback"
                ))

    def _validate_issue_length(self) -> None:
        """Validate that Issue/Improvement section has minimum word count."""
        issue_content = self._extract_section("Issue/Improvement")

        if issue_content:
            words = issue_content.split()
            word_count = len(words)

            if word_count < self.MIN_ISSUE_WORDS:
                self.errors.append(ValidationError(
                    None,
                    f"Issue/Improvement section too short: {word_count} words. Minimum: {self.MIN_ISSUE_WORDS}",
                    f"Add {self.MIN_ISSUE_WORDS - word_count} more words to the Issue/Improvement section"
                ))

    def _validate_markdown_syntax(self) -> None:
        """Validate markdown syntax."""
        # Check for balanced code blocks
        backtick_count = self.content.count("```")
        if backtick_count % 2 != 0:
            self.warnings.append(ValidationError(
                None,
                "Unbalanced code blocks (```) detected"
            ))

        # Check for balanced bold/italic markers
        asterisk_pairs = len(re.findall(r"\*\*", self.content))
        if asterisk_pairs % 2 != 0:
            self.warnings.append(ValidationError(
                None,
                "Unbalanced bold markers (**) detected"
            ))

        # Check for balanced links
        link_pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
        links = re.findall(link_pattern, self.content)
        if links:
            for text, url in links:
                if not url.startswith(("http://", "https://", "/")):
                    self.warnings.append(ValidationError(
                        None,
                        f"Link may be invalid: [{text}]({url})",
                        "Link URLs should start with http://, https://, or /"
                    ))

    def _extract_section(self, section_name: str) -> str:
        """
        Extract content from a markdown section.

        Args:
            section_name: Name of the section to extract

        Returns:
            Content of the section, excluding the header
        """
        content = []
        in_section = False
        section_pattern = re.compile(r"^##\s+" + re.escape(section_name), re.IGNORECASE)

        for line in self.lines:
            if section_pattern.match(line.strip()):
                in_section = True
                continue

            if in_section:
                # Stop if we hit another section
                if re.match(r"^##\s+", line.strip()):
                    break

                content.append(line)

        return ' '.join(content).strip()

    def get_report(self) -> Dict:
        """
        Get validation report as a dictionary.

        Returns:
            Dictionary containing validation results
        """
        return {
            "file": str(self.feedback_file),
            "filename": self.feedback_file.name,
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": [
                {
                    "line": error.line_number,
                    "message": error.message,
                    "suggestion": error.suggestion
                }
                for error in self.errors
            ],
            "warnings": [
                {
                    "line": warning.line_number,
                    "message": warning.message,
                    "suggestion": warning.suggestion
                }
                for warning in self.warnings
            ]
        }

    def print_report(self) -> None:
        """Print human-readable validation report."""
        report = self.get_report()

        print(f"\nFeedback Validation Report: {report['filename']}")
        print("=" * 80)
        print(f"Status: {'PASSED' if report['valid'] else 'FAILED'}")
        print(f"Errors: {report['error_count']}")
        print(f"Warnings: {report['warning_count']}")

        if report['errors']:
            print("\nErrors:")
            print("-" * 80)
            for error in report['errors']:
                line_info = f" (line {error['line']})" if error['line'] else ""
                print(f"  - {error['message']}{line_info}")
                if error['suggestion']:
                    print(f"    Suggestion: {error['suggestion']}")

        if report['warnings']:
            print("\nWarnings:")
            print("-" * 80)
            for warning in report['warnings']:
                line_info = f" (line {warning['line']})" if warning['line'] else ""
                print(f"  - {warning['message']}{line_info}")
                if warning['suggestion']:
                    print(f"    Suggestion: {warning['suggestion']}")

        print("=" * 80)

    @staticmethod
    def auto_suggest_corrections(feedback_file: Path) -> Dict[str, str]:
        """
        Auto-suggest corrections for a feedback file.

        Args:
            feedback_file: Path to the feedback file

        Returns:
            Dictionary with suggested corrections
        """
        suggestions = {}

        # Suggest filename corrections
        filename = feedback_file.name
        pattern = r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$"

        if not re.match(pattern, filename):
            today = datetime.now().strftime("%Y-%m-%d")
            topic = re.sub(r"[^\w\-]", "-", filename.replace(".md", "")).lower()
            suggestions['filename'] = f"{today}-{topic}.md"

        return suggestions


def main():
    """Main entry point for the validation script."""
    parser = argparse.ArgumentParser(
        description="Validate feedback submission files for correct format and content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s feedback/2024-12-09-performance.md
  %(prog)s feedback/2024-12-09-ux-improvement.md --json
  %(prog)s --all
  %(prog)s --all --json
        """
    )

    parser.add_argument(
        "feedback_file",
        nargs="?",
        help="Path to feedback markdown file to validate"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all feedback files in 'submitted/' directory"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (useful for CI/CD integration)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.feedback_file and not args.all:
        parser.print_help()
        sys.exit(1)

    feedback_files = []

    if args.all:
        # Find all markdown files in submitted directory
        submitted_dir = Path.cwd() / "submitted"
        if submitted_dir.exists():
            feedback_files.extend(submitted_dir.glob("*.md"))
        else:
            # Fall back to finding all .md files
            feedback_files.extend(Path.cwd().glob("*.md"))

        if not feedback_files:
            print("No feedback files found")
            sys.exit(1)
    else:
        feedback_files = [Path(args.feedback_file)]

    # Validate all files
    all_reports = []
    all_valid = True

    for feedback_file in sorted(feedback_files):
        validator = FeedbackValidator(feedback_file)
        is_valid = validator.validate()
        all_valid = all_valid and is_valid

        report = validator.get_report()
        all_reports.append(report)

        if not args.json:
            validator.print_report()

            # Print auto-suggestions if there are errors
            if report['error_count'] > 0:
                suggestions = FeedbackValidator.auto_suggest_corrections(feedback_file)
                if suggestions:
                    print("\nAuto-Suggestions:")
                    print("-" * 80)
                    for field, suggestion in suggestions.items():
                        print(f"  {field}: {suggestion}")

    # Output JSON if requested
    if args.json:
        output = {
            "validation_type": "feedback",
            "timestamp": datetime.now().isoformat(),
            "all_valid": all_valid,
            "total_files": len(all_reports),
            "reports": all_reports
        }
        print(json.dumps(output, indent=2))

    # Exit with appropriate code
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
