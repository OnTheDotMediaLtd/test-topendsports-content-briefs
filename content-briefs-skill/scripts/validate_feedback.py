#!/usr/bin/env python3
"""
Feedback Validation Helper

Checks submitted feedback files for completeness and common issues.
Helps reviewers quickly identify which feedback is ready for validation.
"""

import sys
from pathlib import Path
import re


def validate_feedback_file(file_path):
    """
    Validate a single feedback file and return issues found.
    """
    issues = []
    warnings = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check required fields are filled
    required_patterns = {
        'Brief ID': r'\*\*Brief ID\*\*:\s*\[?([^\]]+)\]?',
        'Date Generated': r'\*\*Date Generated\*\*:\s*\[?([^\]]+)\]?',
        'Date Reviewed': r'\*\*Date Reviewed\*\*:\s*\[?([^\]]+)\]?',
        'Reviewer Name': r'\*\*Reviewer Name\*\*:\s*\[?([^\]]+)\]?',
        'Reviewer Role': r'\*\*Reviewer Role\*\*:\s*\[?([^\]]+)\]?',
    }

    # Placeholders without brackets (regex extracts content inside brackets)
    placeholder_values = [
        '',
        'Your name',
        'e.g., nfl-betting-sites',
        'YYYY-MM-DD',
        'Writer / SEO Manager / Editor / Other',
    ]

    for field_name, pattern in required_patterns.items():
        match = re.search(pattern, content)
        if not match:
            issues.append(f"Missing required field: {field_name}")
        elif match.group(1).strip() in placeholder_values:
            issues.append(f"Field not filled out: {field_name}")

    # Check overall rating
    if not re.search(r'\[X\].*?(?:1|2|3|4|5)\s*-\s*(?:Poor|Needs Work|Good|Very Good|Excellent)', content, re.IGNORECASE):
        warnings.append("Overall rating not selected (no [X] found)")

    # Check if at least one "What Worked Well" item is filled
    what_worked_section = re.search(r'## What Worked Well\s*(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if what_worked_section:
        worked_items = re.findall(r'^\d+\.\s*(.+)$', what_worked_section.group(1), re.MULTILINE)
        filled_items = [item for item in worked_items if item.strip() and item.strip() != '']
        if len(filled_items) == 0:
            warnings.append("No items listed in 'What Worked Well'")

    # Check if at least one improvement is listed
    improvement_section = re.search(r'## What Needs Improvement\s*(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if improvement_section:
        improvement_items = re.findall(r'^\d+\.\s*(.+)$', improvement_section.group(1), re.MULTILINE)
        filled_improvements = [item for item in improvement_items if item.strip() and item.strip() != '']
        if len(filled_improvements) == 0:
            warnings.append("No items listed in 'What Needs Improvement'")

    # Check if actionable changes are specified
    if 'Priority 1 (Critical)' in content:
        # Use .*? (zero or more) instead of .+? to handle empty Priority 1 sections
        priority1_section = re.search(r'\*\*Priority 1 \(Critical\)\*\*:\s*(.*?)(?=\*\*Priority 2|\Z)', content, re.DOTALL)
        if priority1_section:
            priority1_items = re.findall(r'^\d+\.\s*(.+)$', priority1_section.group(1), re.MULTILINE)
            filled_priority1 = [item for item in priority1_items if item.strip() and item.strip() != '']
            if len(filled_priority1) > 0:
                warnings.append(f"Priority 1 items found: {len(filled_priority1)} (requires immediate attention)")

    # Check if status is still SUBMITTED
    if 'Status**: SUBMITTED' in content or 'Status: SUBMITTED' in content:
        # This is expected for new submissions
        pass

    return issues, warnings


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    submitted_dir = project_root / 'feedback' / 'submitted'

    if not submitted_dir.exists():
        print("[ERROR] Submitted feedback folder not found")
        print(f"Expected: {submitted_dir}")
        sys.exit(1)

    # Get all markdown files in submitted folder
    feedback_files = list(submitted_dir.glob('*.md'))

    if not feedback_files:
        print("[OK] No feedback files to validate")
        sys.exit(0)

    print(f"Validating {len(feedback_files)} feedback file(s)...\n")

    has_issues = False

    for feedback_file in feedback_files:
        print(f"{'='*70}")
        print(f"File: {feedback_file.name}")
        print(f"{'='*70}")

        issues, warnings = validate_feedback_file(feedback_file)

        if issues:
            has_issues = True
            print("\n[ERROR] Issues found:")
            for issue in issues:
                print(f"  - {issue}")

        if warnings:
            print("\n[WARNING] Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if not issues and not warnings:
            print("\n[OK] No issues found - ready for review")

        print()

    # Summary
    print(f"{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")

    files_with_issues = sum(1 for f in feedback_files if validate_feedback_file(f)[0])
    files_ready = len(feedback_files) - files_with_issues

    print(f"Total files: {len(feedback_files)}")
    print(f"Ready for review: {files_ready}")
    print(f"Need attention: {files_with_issues}")

    if has_issues:
        print("\n[ACTION REQUIRED] Some files have issues that need to be fixed")
        sys.exit(1)
    else:
        print("\n[OK] All files ready for review")
        sys.exit(0)


if __name__ == '__main__':
    main()
