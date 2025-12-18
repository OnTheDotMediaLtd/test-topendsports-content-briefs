#!/usr/bin/env python3
"""
TES Article Formatting - Run Pattern Analysis

Wrapper script to run pattern analysis and auto-generate feedback.
This script is designed to be run manually or via CI/CD.

Usage:
    python scripts/run_pattern_analysis.py
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pattern_analyzer import PatternAnalyzer


def main():
    """Run pattern analysis and auto-generate feedback."""
    print("Starting pattern analysis for TES Article Formatting...\n")

    # Initialize analyzer
    analyzer = PatternAnalyzer()

    # Run analysis
    print("Phase 1: Analyzing validation reports...")
    analysis = analyzer.analyze_all_patterns()
    analyzer.print_analysis_report(analysis)
    analyzer.save_analysis_report(analysis)

    # Check for recurring patterns
    if analyzer.recurring_patterns:
        print("\nPhase 2: Generating alerts...")
        alerts = analyzer.generate_alerts()
        analyzer.print_alerts_report()

        # Save alerts
        alerts_file = Path('insights/alerts.json')
        alerts_file.parent.mkdir(parents=True, exist_ok=True)

        import json
        with open(alerts_file, 'w', encoding='utf-8') as f:
            json.dump(alerts, f, indent=2)
        print(f"[OK] Alerts saved: {alerts_file}\n")

        # Generate auto-feedback for high/critical severity
        high_severity = [p for p in analyzer.recurring_patterns if p['severity'] in ['high', 'critical']]
        if high_severity:
            print("\nPhase 3: Creating auto-feedback...")
            feedback_files = analyzer.create_auto_feedback()

            if feedback_files:
                print(f"\n[OK] Created {len(feedback_files)} auto-feedback submissions")
                print("Review feedback in: feedback/submitted/\n")
            else:
                print("[OK] No auto-feedback needed\n")
        else:
            print("\n[OK] No high/critical severity patterns - no auto-feedback needed\n")
    else:
        print("\n[OK] No recurring patterns detected - quality is consistent!\n")

    print("="*60)
    print("Pattern analysis complete!")
    print("="*60)


if __name__ == '__main__':
    main()
