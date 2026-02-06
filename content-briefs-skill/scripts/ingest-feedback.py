#!/usr/bin/env python3
"""
Feedback Ingestion Script for TopEndSports Content Briefs

Reads validated feedback files and extracts actionable lessons.
Outputs summary report and can update lessons-learned.md.

Usage:
    python3 ingest-feedback.py                    # Generate report only
    python3 ingest-feedback.py --update-lessons   # Update lessons-learned.md
    python3 ingest-feedback.py --verbose          # Show detailed output
    python3 ingest-feedback.py --dry-run           # Show what would be done

Examples:
    # Generate report and show details
    python3 ingest-feedback.py -v

    # Update lessons-learned.md with new findings
    python3 ingest-feedback.py --update-lessons

    # Preview changes without modifying files
    python3 ingest-feedback.py --update-lessons --dry-run
"""

import os
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json


# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
FEEDBACK_DIR = PROJECT_ROOT / "feedback" / "validated"
LESSONS_FILE = PROJECT_ROOT / "references" / "lessons-learned.md"


class FeedbackParser:
    """Parse feedback markdown files and extract structured data."""

    def __init__(self, verbose=False):
        """Initialize parser with optional verbose logging."""
        self.verbose = verbose

    def log(self, message):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[DEBUG] {message}")

    def parse_file(self, filepath):
        """
        Parse a single feedback markdown file.

        Returns dict with extracted feedback data or None if parsing fails.
        """
        self.log(f"Parsing {filepath.name}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[ERROR] Could not read {filepath.name}: {e}")
            return None

        if not content.strip():
            self.log(f"  → File is empty, skipping")
            return None

        feedback_data = {
            'file': filepath.name,
            'filepath': str(filepath),
            'timestamp': self._extract_date(content),
            'brief_id': self._extract_field(content, 'Brief ID'),
            'reviewer': self._extract_field(content, 'Reviewer Name'),
            'role': self._extract_field(content, 'Reviewer Role'),
            'overall_rating': self._extract_overall_rating(content),
            'what_worked': self._extract_list_section(content, 'What Worked Well'),
            'needs_improvement': self._extract_list_section(content, 'What Needs Improvement'),
            'priority_1': self._extract_list_section(content, 'Priority 1 (Critical)'),
            'priority_2': self._extract_list_section(content, 'Priority 2 (Important)'),
            'priority_3': self._extract_list_section(content, 'Priority 3 (Nice to Have)'),
            'keyword_issues': self._extract_keyword_issues(content),
            'technical_issues': self._extract_technical_issues(content),
            'system_improvement': self._extract_system_improvement(content),
            'raw_content': content
        }

        # Determine category based on content
        feedback_data['categories'] = self._determine_categories(feedback_data)

        self.log(f"  → Parsed successfully: {feedback_data['brief_id']}")
        return feedback_data

    def _extract_field(self, content, field_name):
        """Extract a field value from the feedback file."""
        pattern = rf'\*\*{field_name}\*\*:\s*\[?([^\[\]\n]+)\]?'
        match = re.search(pattern, content)
        if match:
            value = match.group(1).strip()
            # Filter out placeholder values
            if value and value not in ['', 'Your name', 'e.g., nfl-betting-sites', 'YYYY-MM-DD',
                                      'Writer / SEO Manager / Editor / Other', 'N/A']:
                return value
        return None

    def _extract_date(self, content):
        """Extract the review date from content."""
        # Try "Date Reviewed" first
        pattern = r'\*\*Date Reviewed\*\*:\s*(\d{4}-\d{2}-\d{2})'
        match = re.search(pattern, content)
        if match:
            return match.group(1)

        # Try "Date" at the end
        pattern = r'\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})'
        match = re.search(pattern, content)
        if match:
            return match.group(1)

        # Use current date as fallback
        return datetime.now().strftime('%Y-%m-%d')

    def _extract_overall_rating(self, content):
        """Extract the overall quality rating."""
        pattern = r'\[X\].*?(\d)\s*-\s*(?:Poor|Needs Work|Good|Very Good|Excellent)'
        match = re.search(pattern, content)
        if match:
            return int(match.group(1))
        return None

    def _extract_list_section(self, content, section_name):
        """Extract a numbered list from a section."""
        # Find section
        pattern = rf'##\s*{re.escape(section_name)}\s*(.+?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if not match:
            return []

        section_content = match.group(1)

        # Extract numbered items
        items = re.findall(r'^\s*\d+\.\s*(.+?)$', section_content, re.MULTILINE)

        # Filter out empty items and template placeholders
        filtered_items = [item.strip() for item in items
                         if item.strip() and item.strip() not in ['', '-']]

        return filtered_items

    def _extract_keyword_issues(self, content):
        """Extract keyword-related issues from feedback."""
        issues = {
            'cannibalization': [],
            'missing': [],
            'unnecessary': []
        }

        # Extract cannibalization concerns
        pattern = r'\*\*Cannibalization Concerns?\*\*:?\s*-\s*\[X\]\s*Potential cannibalization with:\s*(.+?)(?=\n\n|\n\*\*|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            urls = re.findall(r'([/\w\-\.]+)', match.group(1))
            issues['cannibalization'] = urls

        # Extract missing keywords
        pattern = r'Missing Keywords\*\*:?\s*(.+?)(?=\n\n\*\*Unnecessary|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            keyword_lines = re.findall(r'-\s*Keyword:\s*(.+?)(?:\n|$)', match.group(1))
            issues['missing'] = keyword_lines

        # Extract unnecessary keywords
        pattern = r'Unnecessary Keywords\*\*:?\s*(.+?)(?=\n\n|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            keyword_lines = re.findall(r'-\s*Keyword:\s*(.+?)(?:\n|$)', match.group(1))
            issues['unnecessary'] = keyword_lines

        return issues

    def _extract_technical_issues(self, content):
        """Extract technical issues from feedback."""
        issues = {
            'html': [],
            'schema': [],
            'interactive': []
        }

        # Extract HTML issues
        if '[X]' in content and 'HTML/Code Problems' in content:
            pattern = r'HTML/Code Problems.*?\[X\]\s*Issues found:\s*(.+?)(?=\n\n|\*\*Schema|\Z)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                html_issues = re.findall(r'-\s*(.+?)(?:\n|$)', match.group(1))
                issues['html'] = [item.strip() for item in html_issues if item.strip()]

        # Extract schema issues
        if '[X]' in content and 'Schema Markup' in content:
            pattern = r'Schema Markup.*?\[X\]\s*Issues found:\s*(.+?)(?=\n\n|\*\*Interactive|\Z)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                schema_issues = re.findall(r'-\s*(.+?)(?:\n|$)', match.group(1))
                issues['schema'] = [item.strip() for item in schema_issues if item.strip()]

        # Extract interactive element issues
        if '[X]' in content and 'Interactive Elements' in content:
            pattern = r'Interactive Elements.*?\[X\]\s*Issues found:\s*(.+?)(?=\n\n|\Z)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                interactive_issues = re.findall(r'-\s*(.+?)(?:\n|$)', match.group(1))
                issues['interactive'] = [item.strip() for item in interactive_issues if item.strip()]

        return issues

    def _extract_system_improvement(self, content):
        """Extract system improvement suggestions."""
        improvements = {
            'update_lessons': False,
            'update_checklist': False,
            'update_phase_instructions': False,
            'update_templates': False,
            'specific_docs': []
        }

        # Check what should be updated
        if re.search(r'\[X\].*?Yes.*?lessons-learned\.md', content, re.IGNORECASE | re.DOTALL):
            improvements['update_lessons'] = True

        if re.search(r'\[X\].*?Yes.*?quality-checklist\.md', content, re.IGNORECASE | re.DOTALL):
            improvements['update_checklist'] = True

        if re.search(r'\[X\].*?Yes.*?phase instructions', content, re.IGNORECASE | re.DOTALL):
            improvements['update_phase_instructions'] = True

        if re.search(r'\[X\].*?Yes.*?templates', content, re.IGNORECASE | re.DOTALL):
            improvements['update_templates'] = True

        # Extract specific documentation to update
        pattern = r'Specific Documentation to Update.*?(?:---|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            doc_section = match.group(0)
            # Extract file: section: proposed change triples
            doc_entries = re.findall(
                r'-\s*File:\s*(.+?)\s*-\s*Section:\s*(.+?)\s*-\s*Proposed change:\s*(.+?)(?=\n-\s*File:|$)',
                doc_section,
                re.DOTALL
            )
            improvements['specific_docs'] = [
                {
                    'file': entry[0].strip(),
                    'section': entry[1].strip(),
                    'change': entry[2].strip()
                }
                for entry in doc_entries
            ]

        return improvements

    def _determine_categories(self, feedback_data):
        """Determine feedback categories based on content."""
        categories = set()

        # Check keyword issues
        if (feedback_data['keyword_issues']['cannibalization'] or
            feedback_data['keyword_issues']['missing'] or
            feedback_data['keyword_issues']['unnecessary']):
            categories.add('Keyword Research')

        # Check if structure/outline issues mentioned
        if feedback_data['needs_improvement']:
            content_lower = '\n'.join(feedback_data['needs_improvement']).lower()
            if any(word in content_lower for word in ['structure', 'outline', 'h2', 'h3', 'section', 'word count']):
                categories.add('Content Structure')

        # Check technical issues
        if (feedback_data['technical_issues']['html'] or
            feedback_data['technical_issues']['schema'] or
            feedback_data['technical_issues']['interactive']):
            categories.add('Technical')

        # Check brand-related issues
        if feedback_data['needs_improvement']:
            content_lower = '\n'.join(feedback_data['needs_improvement']).lower()
            if any(word in content_lower for word in ['brand', 'bonus', 'feature', 'sportsbook']):
                categories.add('Brand Selection')

        # Check writer experience
        if feedback_data['needs_improvement']:
            content_lower = '\n'.join(feedback_data['needs_improvement']).lower()
            if any(word in content_lower for word in ['unclear', 'confusing', 'instruction', 'time']):
                categories.add('Writer Experience')

        # Default if no categories found
        if not categories:
            categories.add('General')

        return list(categories)


class LessonExtractor:
    """Extract actionable lessons from feedback data."""

    def __init__(self, verbose=False):
        """Initialize extractor."""
        self.verbose = verbose

    def log(self, message):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[DEBUG] {message}")

    def extract_lessons(self, feedback_data_list):
        """
        Extract actionable lessons from multiple feedback files.

        Returns dict organized by category.
        """
        lessons_by_category = defaultdict(list)
        all_lessons = []

        for feedback in feedback_data_list:
            lessons = self._extract_from_feedback(feedback)

            for lesson in lessons:
                # Add to category
                for category in lesson.get('categories', ['General']):
                    lessons_by_category[category].append(lesson)

                all_lessons.append(lesson)

        # Remove duplicates while preserving order
        unique_lessons_by_category = {}
        for category, lessons in lessons_by_category.items():
            seen = set()
            unique = []
            for lesson in lessons:
                lesson_key = lesson.get('lesson', '')
                if lesson_key not in seen:
                    seen.add(lesson_key)
                    unique.append(lesson)
            unique_lessons_by_category[category] = unique

        return unique_lessons_by_category

    def _extract_from_feedback(self, feedback):
        """Extract lessons from a single feedback file."""
        lessons = []
        brief_id = feedback.get('brief_id', 'unknown')
        source_file = feedback.get('file')
        categories = feedback.get('categories', [])

        # Extract from Priority 1 items
        for item in feedback.get('priority_1', []):
            lesson = self._convert_to_lesson(item, brief_id, source_file, categories)
            if lesson:
                lesson['priority'] = 1
                lessons.append(lesson)

        # Extract from Priority 2 items
        for item in feedback.get('priority_2', []):
            lesson = self._convert_to_lesson(item, brief_id, source_file, categories)
            if lesson:
                lesson['priority'] = 2
                lessons.append(lesson)

        # Extract from Priority 3 items
        for item in feedback.get('priority_3', []):
            lesson = self._convert_to_lesson(item, brief_id, source_file, categories)
            if lesson:
                lesson['priority'] = 3
                lessons.append(lesson)

        # Extract from needs improvement
        for item in feedback.get('needs_improvement', []):
            lesson = self._convert_to_lesson(item, brief_id, source_file, categories)
            if lesson:
                lesson['priority'] = 2  # Default to medium priority
                lessons.append(lesson)

        # Extract from keyword issues
        for keyword in feedback.get('keyword_issues', {}).get('missing', []):
            lesson = {
                'lesson': f"Add missing keyword: {keyword}",
                'action': f"Research and include keyword: {keyword}",
                'reason': "Competitors rank for this keyword; missing it creates content gap",
                'source': source_file,
                'brief_id': brief_id,
                'categories': ['Keyword Research'],
                'priority': 1
            }
            lessons.append(lesson)

        for keyword in feedback.get('keyword_issues', {}).get('cannibalization', []):
            lesson = {
                'lesson': f"Check for keyword cannibalization",
                'action': f"Verify keyword doesn't conflict with existing page: {keyword}",
                'reason': "Keyword cannibalization dilutes ranking power across multiple pages",
                'source': source_file,
                'brief_id': brief_id,
                'categories': ['Keyword Research'],
                'priority': 1
            }
            lessons.append(lesson)

        # Extract from technical issues
        for html_issue in feedback.get('technical_issues', {}).get('html', []):
            lesson = {
                'lesson': f"Fix HTML issue: {html_issue[:50]}...",
                'action': f"Review and fix: {html_issue}",
                'reason': "Malformed HTML can affect rendering and SEO",
                'source': source_file,
                'brief_id': brief_id,
                'categories': ['Technical'],
                'priority': 1
            }
            lessons.append(lesson)

        for schema_issue in feedback.get('technical_issues', {}).get('schema', []):
            lesson = {
                'lesson': f"Validate schema markup: {schema_issue[:50]}",
                'action': f"Fix schema syntax: {schema_issue}",
                'reason': "Schema markup validation is essential for search appearance",
                'source': source_file,
                'brief_id': brief_id,
                'categories': ['Technical'],
                'priority': 1
            }
            lessons.append(lesson)

        # Extract from system improvements
        system_improve = feedback.get('system_improvement', {})
        for doc_update in system_improve.get('specific_docs', []):
            lesson = {
                'lesson': f"Update {doc_update['file']}: {doc_update['section']}",
                'action': f"Modify {doc_update['file']} in {doc_update['section']} section",
                'reason': f"Proposed: {doc_update['change'][:80]}...",
                'source': source_file,
                'brief_id': brief_id,
                'categories': ['Process Improvement'],
                'priority': 2
            }
            lessons.append(lesson)

        return lessons

    def _convert_to_lesson(self, item, brief_id, source_file, categories):
        """Convert a feedback item to a lesson format."""
        if not item or len(item) < 5:  # Skip very short items
            return None

        # Try to format as "When X, do Y because Z"
        # For now, just structure the item
        return {
            'lesson': item,
            'source': source_file,
            'brief_id': brief_id,
            'categories': categories,
            'action': None,
            'reason': None,
            'priority': 2
        }


class ReportGenerator:
    """Generate summary reports from feedback data."""

    def __init__(self, verbose=False):
        """Initialize report generator."""
        self.verbose = verbose

    def log(self, message):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[DEBUG] {message}")

    def generate_report(self, feedback_data_list, lessons_by_category):
        """Generate a comprehensive summary report."""
        report = []

        # Header
        report.append("=" * 80)
        report.append("FEEDBACK INGESTION REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Files processed: {len(feedback_data_list)}")

        # Statistics
        total_priority_1 = sum(
            len(fb.get('priority_1', []))
            for fb in feedback_data_list
        )
        total_priority_2 = sum(
            len(fb.get('priority_2', []))
            for fb in feedback_data_list
        )
        total_lessons = sum(
            len(lessons)
            for lessons in lessons_by_category.values()
        )

        report.append(f"Total lessons extracted: {total_lessons}")
        report.append(f"Priority 1 items: {total_priority_1}")
        report.append(f"Priority 2 items: {total_priority_2}")

        # Brief summary
        if feedback_data_list:
            avg_rating = sum(
                fb.get('overall_rating', 3) or 3
                for fb in feedback_data_list
            ) / len(feedback_data_list)
            report.append(f"Average quality rating: {avg_rating:.1f}/5")

        # Lessons by category
        report.append("\n" + "=" * 80)
        report.append("LESSONS BY CATEGORY")
        report.append("=" * 80)

        for category in sorted(lessons_by_category.keys()):
            lessons = lessons_by_category[category]
            report.append(f"\n### {category.upper()} ({len(lessons)} lessons)")
            report.append("-" * 80)

            for i, lesson in enumerate(lessons[:5], 1):  # Show top 5 per category
                priority_label = {1: "CRITICAL", 2: "IMPORTANT", 3: "NICE-TO-HAVE"}.get(
                    lesson.get('priority', 2), "MEDIUM"
                )

                report.append(f"\n{i}. [{priority_label}] {lesson.get('lesson', 'N/A')}")
                if lesson.get('reason'):
                    report.append(f"   Why: {lesson['reason']}")
                report.append(f"   Source: {lesson.get('brief_id', 'unknown')} ({lesson.get('source', 'unknown')})")

            if len(lessons) > 5:
                report.append(f"\n   ... and {len(lessons) - 5} more lessons in this category")

        # Feedback file summary
        report.append("\n" + "=" * 80)
        report.append("FEEDBACK FILES PROCESSED")
        report.append("=" * 80)

        for fb in feedback_data_list:
            rating = fb.get('overall_rating')
            rating_str = f"{rating}/5" if rating else "N/A"

            report.append(
                f"\n- {fb.get('brief_id', 'unknown')}: {rating_str} "
                f"({fb.get('reviewer', 'unknown')} - {fb.get('role', 'unknown')})"
            )
            report.append(f"  File: {fb.get('file')}")
            report.append(f"  Date: {fb.get('timestamp')}")
            report.append(
                f"  Categories: {', '.join(fb.get('categories', ['General']))}"
            )

        # Recommendations
        report.append("\n" + "=" * 80)
        report.append("RECOMMENDATIONS")
        report.append("=" * 80)

        # Check for system improvement docs
        docs_to_update = set()
        for fb in feedback_data_list:
            for doc in fb.get('system_improvement', {}).get('specific_docs', []):
                docs_to_update.add(doc['file'])

        if docs_to_update:
            report.append(f"\nDocumentation files that need updating:")
            for doc in sorted(docs_to_update):
                report.append(f"  - {doc}")
            report.append("\nUse --update-lessons flag to apply changes automatically.")

        # High-priority issues
        if total_priority_1 > 0:
            report.append(f"\nATTENTION: {total_priority_1} Priority 1 (Critical) items identified")
            report.append("These require immediate attention before next brief generation.")

        report.append("\n" + "=" * 80)

        return "\n".join(report)

    def print_report(self, report):
        """Print the report to stdout."""
        print(report)


class LessonsFileUpdater:
    """Update lessons-learned.md with new lessons."""

    def __init__(self, verbose=False):
        """Initialize updater."""
        self.verbose = verbose

    def log(self, message):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[DEBUG] {message}")

    def update_lessons_file(self, lessons_by_category, dry_run=False):
        """
        Update lessons-learned.md with new lessons.

        Returns (success: bool, message: str)
        """
        if not LESSONS_FILE.exists():
            return False, f"File not found: {LESSONS_FILE}"

        self.log(f"Reading {LESSONS_FILE}")

        try:
            with open(LESSONS_FILE, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            return False, f"Could not read lessons file: {e}"

        # Prepare new sections
        new_sections = []

        # Add a dated section for new lessons
        date_str = datetime.now().strftime('%Y-%m-%d')
        new_sections.append(f"\n## New Lessons ({date_str})\n")
        new_sections.append("*Extracted from validated user feedback*\n")

        for category in sorted(lessons_by_category.keys()):
            lessons = lessons_by_category[category]
            if not lessons:
                continue

            new_sections.append(f"\n### {category}\n")

            for lesson in lessons[:3]:  # Limit to top 3 per category
                priority = {1: "CRITICAL", 2: "IMPORTANT", 3: "NOTE"}.get(
                    lesson.get('priority', 2), "NOTE"
                )

                lesson_text = lesson.get('lesson', 'N/A')
                reason = lesson.get('reason', '')
                brief_id = lesson.get('brief_id', 'multiple')

                new_sections.append(f"**[{priority}]** {lesson_text}")
                if reason:
                    new_sections.append(f"> {reason}")
                new_sections.append(f"*Source: {brief_id}*\n")

        new_content = original_content + "\n".join(new_sections)

        if dry_run:
            self.log("DRY RUN - Would add the following to lessons-learned.md:")
            print("\n" + "=" * 80)
            print("PROPOSED CHANGES TO lessons-learned.md")
            print("=" * 80)
            print("".join(new_sections))
            print("=" * 80)
            return True, "Dry run complete - no changes made"

        # Write updated content
        try:
            with open(LESSONS_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.log(f"Updated {LESSONS_FILE}")
            return True, f"Successfully updated {LESSONS_FILE}"

        except Exception as e:
            return False, f"Could not write to lessons file: {e}"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Ingest validated feedback files and extract lessons',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ingest-feedback.py                    # Generate report only
  python3 ingest-feedback.py --verbose          # Show debug output
  python3 ingest-feedback.py --update-lessons   # Update lessons-learned.md
  python3 ingest-feedback.py --update-lessons --dry-run  # Preview changes
        """
    )

    parser.add_argument(
        '--update-lessons',
        action='store_true',
        help='Update lessons-learned.md with new lessons'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output for debugging'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )

    args = parser.parse_args()

    # Check if feedback directory exists
    if not FEEDBACK_DIR.exists():
        print(f"[NOTICE] Feedback directory not found: {FEEDBACK_DIR}")
        print("Creating directory structure...")
        FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created {FEEDBACK_DIR}")
        print("\nNo validated feedback files to process.")
        return 0

    # Find feedback files
    feedback_files = sorted(FEEDBACK_DIR.glob('*.md'))

    if not feedback_files:
        print(f"[NOTICE] No feedback files found in {FEEDBACK_DIR}")
        print("Place validated feedback files there and run again.")
        return 0

    print(f"[INFO] Found {len(feedback_files)} feedback file(s)")

    # Parse feedback files
    parser_obj = FeedbackParser(verbose=args.verbose)
    feedback_data_list = []

    for feedback_file in feedback_files:
        feedback = parser_obj.parse_file(feedback_file)
        if feedback:
            feedback_data_list.append(feedback)

    if not feedback_data_list:
        print("[ERROR] No valid feedback files could be parsed")
        return 1

    print(f"[OK] Successfully parsed {len(feedback_data_list)} file(s)")

    # Extract lessons
    extractor = LessonExtractor(verbose=args.verbose)
    lessons_by_category = extractor.extract_lessons(feedback_data_list)

    print(f"[OK] Extracted {sum(len(l) for l in lessons_by_category.values())} lessons")

    # Generate and display report
    report_gen = ReportGenerator(verbose=args.verbose)
    report = report_gen.generate_report(feedback_data_list, lessons_by_category)
    report_gen.print_report(report)

    # Update lessons file if requested
    if args.update_lessons:
        print("\n[INFO] Updating lessons-learned.md...")
        updater = LessonsFileUpdater(verbose=args.verbose)
        success, message = updater.update_lessons_file(
            lessons_by_category,
            dry_run=args.dry_run
        )

        if success:
            print(f"[OK] {message}")
            return 0
        else:
            print(f"[ERROR] {message}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
