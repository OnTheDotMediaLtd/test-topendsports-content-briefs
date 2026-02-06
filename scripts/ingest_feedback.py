#!/usr/bin/env python3
"""
Feedback Ingestion System - TopEndSports Content Briefs v1.0

Processes submitted feedback and routes it to appropriate documentation updates.
Part of the self-learning system for continuous protocol improvement.

Usage:
    python scripts/ingest_feedback.py
    python scripts/ingest_feedback.py --category keyword
    python scripts/ingest_feedback.py --validate-only
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class FeedbackIngestor:
    """Ingests and processes feedback for protocol improvements"""

    CATEGORIES = {
        'keyword': {
            'doc': 'references/keyword-research-protocol.md',
            'section': 'Keyword Discovery',
            'priority': 'high'
        },
        'writer': {
            'doc': 'references/writer-brief-protocol.md',
            'section': 'Writer Brief Generation',
            'priority': 'medium'
        },
        'technical': {
            'doc': 'references/technical-implementation.md',
            'section': 'Technical Implementation',
            'priority': 'medium'
        },
        'compliance': {
            'doc': 'references/lessons-learned.md',
            'section': 'Legal Compliance',
            'priority': 'critical'
        },
        'workflow': {
            'doc': 'CLAUDE.md',
            'section': 'Workflow Execution',
            'priority': 'high'
        },
        'seo': {
            'doc': 'references/seo-optimization.md',
            'section': 'SEO Best Practices',
            'priority': 'medium'
        },
        'edge-case': {
            'doc': 'references/lessons-learned.md',
            'section': 'Edge Cases and Solutions',
            'priority': 'low'
        }
    }

    def __init__(self, base_path: str = '.'):
        self.base_path = Path(base_path)
        self.feedback_dir = self.base_path / 'feedback'
        self.submitted_dir = self.feedback_dir / 'submitted'
        self.validated_dir = self.feedback_dir / 'validated'
        self.applied_dir = self.feedback_dir / 'applied'

        # Ensure directories exist
        for directory in [self.submitted_dir, self.validated_dir, self.applied_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def scan_submitted_feedback(self, category: Optional[str] = None) -> List[Dict]:
        """Scan submitted feedback directory for new feedback"""
        feedback_items = []

        for feedback_file in self.submitted_dir.glob('*.json'):
            try:
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Filter by category if specified
                if category and data.get('category') != category:
                    continue

                data['filename'] = feedback_file.name
                data['filepath'] = str(feedback_file)
                feedback_items.append(data)

            except Exception as e:
                print(f"Warning: Error reading {feedback_file.name}: {e}")

        return feedback_items

    def validate_feedback(self, feedback: Dict) -> tuple:
        """Validate feedback structure and content"""
        errors = []

        # Required fields
        required_fields = ['category', 'issue', 'context', 'timestamp']
        for field in required_fields:
            if field not in feedback:
                errors.append(f"Missing required field: {field}")

        # Validate category
        if 'category' in feedback and feedback['category'] not in self.CATEGORIES:
            errors.append(f"Invalid category: {feedback['category']}")
            errors.append(f"Valid categories: {', '.join(self.CATEGORIES.keys())}")

        # Validate issue description
        if 'issue' in feedback:
            if len(feedback['issue']) < 10:
                errors.append("Issue description too short (min 10 characters)")
            if len(feedback['issue']) > 1000:
                errors.append("Issue description too long (max 1000 characters)")

        # Validate context
        if 'context' in feedback:
            if len(feedback['context']) < 20:
                errors.append("Context too short (min 20 characters)")

        return (len(errors) == 0, errors)

    def categorize_feedback(self, feedback: Dict) -> Dict:
        """Add routing information to feedback"""
        category = feedback.get('category', 'edge-case')
        category_info = self.CATEGORIES.get(category, self.CATEGORIES['edge-case'])

        feedback['routing'] = {
            'target_doc': category_info['doc'],
            'target_section': category_info['section'],
            'priority': category_info['priority'],
            'processed_at': datetime.now().isoformat()
        }

        return feedback

    def move_to_validated(self, feedback: Dict) -> Path:
        """Move feedback from submitted to validated"""
        source_path = Path(feedback['filepath'])
        dest_path = self.validated_dir / source_path.name

        # Save updated feedback with routing info
        with open(dest_path, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, indent=2)

        # Remove from submitted
        source_path.unlink()

        return dest_path

    def generate_report(self, feedback_items: List[Dict]) -> str:
        """Generate human-readable feedback report"""
        if not feedback_items:
            return "No feedback items to process."

        report = []
        report.append("=" * 70)
        report.append(f"FEEDBACK INGESTION REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)
        report.append("")

        # Group by category
        by_category = {}
        for item in feedback_items:
            cat = item.get('category', 'unknown')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)

        # Summary
        report.append(f"Total Feedback Items: {len(feedback_items)}")
        report.append("")
        report.append("By Category:")
        for cat, items in sorted(by_category.items()):
            priority = self.CATEGORIES.get(cat, {}).get('priority', 'unknown')
            report.append(f"  - {cat}: {len(items)} items (priority: {priority})")
        report.append("")
        report.append("-" * 70)
        report.append("")

        # Detailed items
        for category, items in sorted(by_category.items()):
            report.append(f"\n## {category.upper()} ({len(items)} items)")
            report.append("")

            for idx, item in enumerate(items, 1):
                report.append(f"### {idx}. {item.get('filename', 'unknown')}")
                report.append(f"**Issue:** {item.get('issue', 'No description')}")
                report.append(f"**Context:** {item.get('context', 'No context')[:200]}...")

                if 'routing' in item:
                    routing = item['routing']
                    report.append(f"**Target Doc:** {routing['target_doc']}")
                    report.append(f"**Target Section:** {routing['target_section']}")

                if 'suggested_fix' in item:
                    report.append(f"**Suggested Fix:** {item['suggested_fix'][:150]}...")

                report.append("")

        report.append("-" * 70)
        report.append("")
        report.append("Next Steps:")
        report.append("1. Review validated feedback in: feedback/validated/")
        report.append("2. Update appropriate documentation files")
        report.append("3. Review and commit protocol updates")
        report.append("")

        return "\n".join(report)

    def process_all(self, category: Optional[str] = None, validate_only: bool = False):
        """Process all submitted feedback"""
        print("Scanning for submitted feedback...")

        feedback_items = self.scan_submitted_feedback(category)

        if not feedback_items:
            print("No feedback to process.")
            return

        print(f"Found {len(feedback_items)} feedback item(s)")
        print("")

        validated_items = []
        failed_items = []

        for feedback in feedback_items:
            filename = feedback.get('filename', 'unknown')
            print(f"Processing: {filename}")

            # Validate
            is_valid, errors = self.validate_feedback(feedback)

            if not is_valid:
                print(f"  Validation failed:")
                for error in errors:
                    print(f"     - {error}")
                failed_items.append(feedback)
                continue

            print(f"  Valid")

            if validate_only:
                validated_items.append(feedback)
                continue

            # Categorize and route
            feedback = self.categorize_feedback(feedback)
            print(f"  Category: {feedback['category']}")
            print(f"  Priority: {feedback['routing']['priority']}")
            print(f"  Target: {feedback['routing']['target_doc']}")

            # Move to validated
            dest_path = self.move_to_validated(feedback)
            print(f"  Moved to: {dest_path.relative_to(self.base_path)}")

            validated_items.append(feedback)
            print("")

        # Generate report
        report = self.generate_report(validated_items)
        print("")
        print(report)

        # Save report
        report_path = self.feedback_dir / f"ingestion-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to: {report_path.relative_to(self.base_path)}")

        if failed_items:
            print(f"\n{len(failed_items)} item(s) failed validation - left in submitted/")

        if validated_items and not validate_only:
            print(f"\n{len(validated_items)} item(s) validated and ready for processing")


def main():
    parser = argparse.ArgumentParser(
        description='Ingest and process feedback for protocol improvements'
    )
    parser.add_argument(
        '--category',
        choices=list(FeedbackIngestor.CATEGORIES.keys()),
        help='Process only feedback in this category'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Validate feedback without moving files'
    )
    parser.add_argument(
        '--base-path',
        default='.',
        help='Base path to repository (default: current directory)'
    )

    args = parser.parse_args()

    ingestor = FeedbackIngestor(args.base_path)
    ingestor.process_all(category=args.category, validate_only=args.validate_only)


if __name__ == '__main__':
    main()
