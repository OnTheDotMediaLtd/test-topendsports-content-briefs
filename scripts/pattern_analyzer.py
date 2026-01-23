#!/usr/bin/env python3
"""
TES Article Formatting - Pattern Analyzer

Analyzes validation reports to detect recurring issues and generate auto-feedback
for the self-learning system.

Adapted from tes-internal-linking pattern analyzer.

Usage:
    python scripts/pattern_analyzer.py analyze
    python scripts/pattern_analyzer.py alerts
    python scripts/pattern_analyzer.py auto-feedback
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional


class PatternAnalyzer:
    """Analyzes validation reports for recurring failure patterns."""

    # Pattern detection thresholds
    RECURRENCE_THRESHOLD = 2  # Patterns appearing > 2 times in 7 days
    LOOKBACK_DAYS = 7

    # Failure type categorization (adapted for article formatting)
    FAILURE_CATEGORIES = {
        'word_count': ['word count', 'minimum 800 words', 'word_count < 800'],
        'attribution': ['attribution', 'generic attribution', 'Research shows', 'Studies indicate'],
        'structure': ['Citation Library', '#container', 'library placement', 'structure'],
        'links': ['placeholder link', 'href="#"', 'broken link', 'skip link'],
        'components': ['component', 'module', 'FAQ', 'expert quote'],
        'validation': ['validation', 'failed check', 'test failed'],
        'encoding': ['encoding', 'UTF-8', 'character'],
        'schema': ['schema', 'meta tag', 'tracking code']
    }

    def __init__(self, output_dir: str = 'output'):
        self.output_dir = Path(output_dir)
        self.validation_files = list(self.output_dir.glob('*.validation.json'))
        self.patterns = defaultdict(list)
        self.recurring_patterns = []
        self.alerts = []
        self.cutoff_date = datetime.now() - timedelta(days=self.LOOKBACK_DAYS)

    def load_validation_reports(self) -> List[Dict]:
        """Load all validation reports within lookback period."""
        reports = []

        for vf in self.validation_files:
            try:
                # Check file modification time
                file_time = datetime.fromtimestamp(vf.stat().st_mtime)
                if file_time < self.cutoff_date:
                    continue

                with open(vf, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['file_path'] = str(vf)
                    data['timestamp'] = file_time.isoformat()
                    reports.append(data)
            except Exception as e:
                print(f"[WARN] Failed to load {vf}: {e}")
                continue

        return reports

    def categorize_failure(self, error_msg: str) -> str:
        """Categorize a failure message by type."""
        error_lower = error_msg.lower()

        for category, keywords in self.FAILURE_CATEGORIES.items():
            if any(keyword.lower() in error_lower for keyword in keywords):
                return category

        return 'other'

    def detect_word_count_patterns(self, reports: List[Dict]) -> List[Dict]:
        """Detect recurring word count violations."""
        word_count_failures = []

        for report in reports:
            if report.get('status') == 'FAIL':
                for error in report.get('checks', {}).get('errors', []):
                    if 'word count' in error.lower() or 'word_count < 800' in error:
                        # Extract word count if present
                        count_match = re.search(r'(\d+)\s*words?', error)
                        word_count = int(count_match.group(1)) if count_match else None

                        word_count_failures.append({
                            'file': report.get('file', 'unknown'),
                            'timestamp': report['timestamp'],
                            'error': error,
                            'word_count': word_count,
                            'category': 'word_count'
                        })

        return word_count_failures

    def detect_attribution_patterns(self, reports: List[Dict]) -> List[Dict]:
        """Detect recurring attribution quality issues."""
        attribution_failures = []

        for report in reports:
            if report.get('status') == 'FAIL':
                for error in report.get('checks', {}).get('errors', []):
                    if 'attribution' in error.lower() or 'research shows' in error.lower():
                        # Extract generic phrase if present
                        phrase_match = re.search(r'"([^"]+)"', error)
                        generic_phrase = phrase_match.group(1) if phrase_match else None

                        attribution_failures.append({
                            'file': report.get('file', 'unknown'),
                            'timestamp': report['timestamp'],
                            'error': error,
                            'generic_phrase': generic_phrase,
                            'category': 'attribution'
                        })

        return attribution_failures

    def detect_structure_patterns(self, reports: List[Dict]) -> List[Dict]:
        """Detect recurring structure/library placement issues."""
        structure_failures = []

        for report in reports:
            if report.get('status') == 'FAIL':
                for error in report.get('checks', {}).get('errors', []):
                    if 'citation library' in error.lower() or 'library placement' in error.lower() or '#container' in error:
                        structure_failures.append({
                            'file': report.get('file', 'unknown'),
                            'timestamp': report['timestamp'],
                            'error': error,
                            'category': 'structure'
                        })

        return structure_failures

    def detect_link_patterns(self, reports: List[Dict]) -> List[Dict]:
        """Detect recurring link quality issues."""
        link_failures = []

        for report in reports:
            # Check both errors and warnings
            all_issues = report.get('checks', {}).get('errors', []) + report.get('checks', {}).get('warnings', [])

            for issue in all_issues:
                if 'placeholder link' in issue.lower() or 'href="#"' in issue or 'skip link' in issue.lower():
                    link_failures.append({
                        'file': report.get('file', 'unknown'),
                        'timestamp': report['timestamp'],
                        'error': issue,
                        'category': 'links'
                    })

        return link_failures

    def analyze_all_patterns(self) -> Dict:
        """Run all pattern detection and identify recurring issues."""
        print(f"\n{'='*60}")
        print("TES Article Formatting - Pattern Analyzer")
        print(f"{'='*60}\n")
        print(f"Analyzing validation reports from last {self.LOOKBACK_DAYS} days...")
        print(f"Found {len(self.validation_files)} validation files\n")

        # Load reports
        reports = self.load_validation_reports()
        print(f"Loaded {len(reports)} reports within timeframe\n")

        if not reports:
            print("[WARN] No recent validation reports found")
            return {
                'total_reports': 0,
                'total_failures': 0,
                'patterns': {},
                'recurring_patterns': []
            }

        # Detect patterns by category
        self.patterns['word_count'] = self.detect_word_count_patterns(reports)
        self.patterns['attribution'] = self.detect_attribution_patterns(reports)
        self.patterns['structure'] = self.detect_structure_patterns(reports)
        self.patterns['links'] = self.detect_link_patterns(reports)

        # Identify recurring patterns (>2 occurrences)
        for category, failures in self.patterns.items():
            if len(failures) > self.RECURRENCE_THRESHOLD:
                self.recurring_patterns.append({
                    'category': category,
                    'count': len(failures),
                    'failures': failures,
                    'severity': self._calculate_severity(category, len(failures), len(reports))
                })

        return {
            'total_reports': len(reports),
            'total_failures': sum(len(f) for f in self.patterns.values()),
            'patterns': {k: len(v) for k, v in self.patterns.items()},
            'recurring_patterns': self.recurring_patterns
        }

    def _calculate_severity(self, category: str, count: int, total_reports: int) -> str:
        """Calculate severity based on occurrence frequency."""
        occurrence_rate = count / total_reports if total_reports > 0 else 0

        # Critical categories for article formatting
        if category in ['word_count', 'structure', 'attribution']:
            if occurrence_rate > 0.5:
                return 'critical'
            elif occurrence_rate > 0.3:
                return 'high'
            else:
                return 'medium'
        else:
            if occurrence_rate > 0.6:
                return 'high'
            else:
                return 'medium'

    def generate_alerts(self) -> List[Dict]:
        """Generate alerts for recurring patterns."""
        alerts = []

        for pattern in self.recurring_patterns:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'category': pattern['category'],
                'severity': pattern['severity'],
                'count': pattern['count'],
                'message': self._format_alert_message(pattern),
                'recommendation': self._get_recommendation(pattern)
            }
            alerts.append(alert)

        self.alerts = alerts
        return alerts

    def _format_alert_message(self, pattern: Dict) -> str:
        """Format human-readable alert message."""
        category = pattern['category']
        count = pattern['count']

        messages = {
            'word_count': f"[ALERT] Word Count Violations: {count} instances of articles below 800 words",
            'attribution': f"[ALERT] Attribution Issues: {count} instances of generic/missing attributions",
            'structure': f"[ALERT] Structure Issues: {count} instances of incorrect library placement",
            'links': f"[WARN] Link Issues: {count} instances of placeholder or broken links"
        }

        return messages.get(category, f"[WARN] {category.title()} Issues: {count} instances")

    def _get_recommendation(self, pattern: Dict) -> str:
        """Get recommendation for addressing the pattern."""
        category = pattern['category']

        recommendations = {
            'word_count': "Review word count calculation. Ensure minimum 800 words before formatting. Add content if needed or flag for editorial review.",
            'attribution': "Review attribution guidelines. Replace generic phrases ('Research shows', 'Studies indicate') with specific sources or remove. Use expert quotes with proper attribution.",
            'structure': "Review library placement rules. Citation Library MUST be OUTSIDE #container. Verify 7 libraries are in correct order.",
            'links': "Remove placeholder links (href='#'). Either complete the link or delete it entirely. Preserve all working links."
        }

        return recommendations.get(category, "Review documentation and add validation checks.")

    def suggest_doc_updates(self) -> List[Dict]:
        """Suggest documentation updates based on recurring patterns."""
        suggestions = []

        for pattern in self.recurring_patterns:
            category = pattern['category']

            # Map to target documentation
            doc_mapping = {
                'word_count': 'references/phase1-content-analysis.md',
                'attribution': 'references/attribution-guidelines.md',
                'structure': 'references/library-placement-guide.md',
                'links': 'CLAUDE.md'
            }

            target_doc = doc_mapping.get(category, 'references/LESSONS-LEARNED.md')

            suggestion = {
                'target_document': target_doc,
                'category': category,
                'severity': pattern['severity'],
                'suggested_update': self._generate_doc_update(pattern),
                'rationale': f"Recurring pattern detected: {pattern['count']} occurrences in {self.LOOKBACK_DAYS} days"
            }

            suggestions.append(suggestion)

        return suggestions

    def _generate_doc_update(self, pattern: Dict) -> str:
        """Generate suggested documentation update text."""
        category = pattern['category']

        updates = {
            'word_count': """
## [!] COMMON MISTAKE: Word Count Violations

**Issue:** Articles submitted with less than 800 words.

**Prevention:**
- ALWAYS calculate word count in Phase 1 BEFORE formatting
- Add validation check: `if word_count < 800: flag_for_review`
- Review content guidelines before each article
- Use this checklist: "Is word count >= 800?"

**Example Anti-Pattern:**
[X] Formatting 650-word article without flagging
[OK] Flagging short content for editorial expansion
""",
            'attribution': """
## [!] COMMON MISTAKE: Generic Attribution Issues

**Issue:** Using generic phrases like "Research shows" or "Studies indicate".

**Prevention:**
- NEVER use: "Research shows", "Studies indicate", "Experts say"
- Always attribute to specific source or person
- Use expert quotes with proper names and credentials
- Remove attribution if no specific source available

**Example Anti-Pattern:**
[X] "Research shows that hydration improves performance" (generic)
[X] "Studies indicate that training helps" (generic)
[OK] "Dr. Smith (2024) found that hydration improves performance by 15%" (specific)
[OK] Removed unsourced claims entirely
""",
            'structure': """
## [!] COMMON MISTAKE: Library Placement Errors

**Issue:** Citation Library placed inside #container instead of outside.

**Prevention:**
- Citation Library MUST be OUTSIDE #container (after closing </div>)
- Verify 7 libraries in exact order before delivery
- Use visual structure check
- Test in browser to verify layout

**Example Anti-Pattern:**
[X] Citation Library inside #container (layout breaks)
[OK] Citation Library after container closing tag
"""
        }

        return updates.get(category, f"Document common issues for {category}")

    def create_auto_feedback(self) -> List[str]:
        """Generate automatic feedback submissions from validation failures."""
        feedback_files = []
        feedback_dir = Path('feedback/submitted')
        feedback_dir.mkdir(parents=True, exist_ok=True)

        for pattern in self.recurring_patterns:
            # Only create auto-feedback for high/critical severity
            if pattern['severity'] in ['high', 'critical']:
                feedback_id = f"auto-{pattern['category']}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

                feedback_data = {
                    'feedback_id': feedback_id,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'pattern_analyzer',
                    'category': pattern['category'],
                    'severity': pattern['severity'],
                    'title': f"Recurring {pattern['category'].title()} Violations",
                    'description': self._format_alert_message(pattern),
                    'root_cause': f"Detected {pattern['count']} occurrences in last {self.LOOKBACK_DAYS} days",
                    'solution': self._get_recommendation(pattern),
                    'prevention': self._generate_doc_update(pattern),
                    'examples': [
                        {'file': f['file'], 'error': f['error']}
                        for f in pattern['failures'][:3]  # First 3 examples
                    ],
                    'rationale': 'Auto-generated from recurring validation failures'
                }

                feedback_file = feedback_dir / f"{feedback_id}.json"
                with open(feedback_file, 'w', encoding='utf-8') as f:
                    json.dump(feedback_data, f, indent=2)

                feedback_files.append(str(feedback_file))
                print(f"[OK] Created auto-feedback: {feedback_file.name}")

        return feedback_files

    def integrate_with_ingest(self, feedback_files: List[str]) -> List[Dict]:
        """Pass auto-feedback to feedback processor."""
        results = []

        # Import FeedbackProcessor if available
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'feedback'))
            from ingest_feedback import FeedbackProcessor

            for feedback_file in feedback_files:
                try:
                    processor = FeedbackProcessor(feedback_file)
                    result = processor.process()
                    results.append(result)
                except Exception as e:
                    print(f"[WARN] Failed to process {feedback_file}: {e}")
                    results.append({
                        'status': 'failed',
                        'file': feedback_file,
                        'error': str(e)
                    })
        except ImportError as e:
            print(f"[WARN] Could not import FeedbackProcessor: {e}")
            print("Auto-feedback created but not processed automatically.")
            results.append({
                'status': 'skipped',
                'reason': 'import_error'
            })

        return results

    def print_analysis_report(self, analysis: Dict):
        """Print comprehensive pattern analysis report."""
        print(f"\n{'='*60}")
        print("PATTERN ANALYSIS REPORT")
        print(f"{'='*60}\n")

        print(f"[SUMMARY]:")
        print(f"   Total Reports Analyzed: {analysis['total_reports']}")
        print(f"   Total Failures Detected: {analysis['total_failures']}")
        print(f"   Recurring Patterns: {len(analysis['recurring_patterns'])}\n")

        if analysis['patterns']:
            print("[DISTRIBUTION] Failure Distribution:")
            for category, count in analysis['patterns'].items():
                if count > 0:
                    print(f"   {category.title()}: {count} instances")
            print()

        if self.recurring_patterns:
            print("[ALERT] Recurring Patterns (>2 occurrences):\n")
            for pattern in self.recurring_patterns:
                severity_prefix = {
                    'critical': '[CRITICAL]',
                    'high': '[HIGH]',
                    'medium': '[MEDIUM]'
                }

                prefix = severity_prefix.get(pattern['severity'], '[LOW]')
                print(f"{prefix} {pattern['category'].upper()}")
                print(f"   Count: {pattern['count']}")
                print(f"   Severity: {pattern['severity'].upper()}")
                print(f"   Message: {self._format_alert_message(pattern)}")
                print(f"   Recommendation: {self._get_recommendation(pattern)[:80]}...")
                print()
        else:
            print("[PASS] No recurring patterns detected - quality is consistent!\n")

        print(f"{'='*60}\n")

    def print_alerts_report(self):
        """Print alerts report."""
        if not self.alerts:
            print("[WARN] No alerts generated. Run 'analyze' first.")
            return

        print(f"\n{'='*60}")
        print("ALERTS REPORT")
        print(f"{'='*60}\n")

        for alert in self.alerts:
            severity_labels = {
                'critical': '[CRITICAL] CRITICAL',
                'high': '[HIGH] HIGH',
                'medium': '[MEDIUM] MEDIUM'
            }

            print(f"{severity_labels.get(alert['severity'], '[LOW] LOW')}")
            print(f"Category: {alert['category'].upper()}")
            print(f"Message: {alert['message']}")
            print(f"Count: {alert['count']} occurrences")
            print(f"Recommendation: {alert['recommendation']}")
            print(f"{'-'*60}\n")

        print(f"{'='*60}\n")

    def save_analysis_report(self, analysis: Dict):
        """Save analysis report to JSON."""
        report = {
            'generated_at': datetime.now().isoformat(),
            'lookback_days': self.LOOKBACK_DAYS,
            'analysis': analysis,
            'recurring_patterns': self.recurring_patterns,
            'alerts': self.alerts,
            'doc_suggestions': self.suggest_doc_updates()
        }

        report_file = Path('insights/pattern-analysis.json')
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"[OK] Analysis saved: {report_file}\n")


def main():
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python scripts/pattern_analyzer.py analyze      # Analyze validation reports")
        print("  python scripts/pattern_analyzer.py alerts       # Generate alerts")
        print("  python scripts/pattern_analyzer.py auto-feedback # Create auto-feedback\n")
        sys.exit(1)

    command = sys.argv[1]

    analyzer = PatternAnalyzer()

    if command == 'analyze':
        analysis = analyzer.analyze_all_patterns()
        analyzer.print_analysis_report(analysis)
        analyzer.save_analysis_report(analysis)

    elif command == 'alerts':
        # Run analysis first if not done
        if not analyzer.recurring_patterns:
            analyzer.analyze_all_patterns()

        alerts = analyzer.generate_alerts()
        analyzer.print_alerts_report()

        # Save alerts
        alerts_file = Path('insights/alerts.json')
        alerts_file.parent.mkdir(parents=True, exist_ok=True)
        with open(alerts_file, 'w', encoding='utf-8') as f:
            json.dump(alerts, f, indent=2)
        print(f"[OK] Alerts saved: {alerts_file}\n")

    elif command == 'auto-feedback':
        # Run analysis first if not done
        if not analyzer.recurring_patterns:
            analysis = analyzer.analyze_all_patterns()
            print()

        print("Creating auto-feedback from recurring patterns...\n")
        feedback_files = analyzer.create_auto_feedback()

        if feedback_files:
            print(f"\n[OK] Created {len(feedback_files)} auto-feedback submissions")
            print("\nProcessing feedback through ingest system...\n")

            results = analyzer.integrate_with_ingest(feedback_files)

            success_count = sum(1 for r in results if r.get('status') == 'success')
            print(f"\n[OK] Processed {success_count}/{len(results)} feedback submissions successfully")
        else:
            print("[OK] No high/critical severity patterns detected - no auto-feedback needed")

    else:
        print(f"[FAIL] Unknown command: {command}")
        print("\nAvailable commands: analyze, alerts, auto-feedback")
        sys.exit(1)


if __name__ == '__main__':
    main()
