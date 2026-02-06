#!/usr/bin/env python3
"""
Unified Automation Script for TopEndSports Content Briefs

Combines error tracking, feedback ingestion, and lesson generation
into a single workflow for CI/CD integration.

Usage:
    python3 scripts/automation.py run           # Run full automation cycle
    python3 scripts/automation.py test          # Run tests with error tracking
    python3 scripts/automation.py report        # Generate combined report
    python3 scripts/automation.py lessons       # Generate lessons from all sources

Features:
    - Integrates error tracker with feedback ingestion
    - Generates combined reports
    - Updates lessons-learned.md from multiple sources
    - CI/CD compatible with exit codes
"""

import argparse
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
FEEDBACK_SKILL_DIR = PROJECT_ROOT / "content-briefs-skill"
LESSONS_FILE = FEEDBACK_SKILL_DIR / "references" / "lessons-learned.md"
ERROR_LOG_DIR = PROJECT_ROOT / "logs" / "errors"


class AutomationRunner:
    """Main automation class that orchestrates all tasks."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {
            "tests": {"status": "skipped", "details": {}},
            "errors": {"status": "skipped", "details": {}},
            "feedback": {"status": "skipped", "details": {}},
            "lessons": {"status": "skipped", "details": {}},
        }

    def log(self, msg: str, level: str = "INFO"):
        """Print log message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "[INFO]", "OK": "[OK]", "WARN": "[WARN]", "ERROR": "[ERROR]"}.get(level, "[?]")
        try:
            print(f"[{timestamp}] {prefix} {msg}")
        except UnicodeEncodeError:
            print(f"[{timestamp}] {prefix} {msg}".encode('ascii', errors='replace').decode('ascii'))

    def run_command(self, cmd: List[str], capture: bool = True) -> Tuple[int, str, str]:
        """Run a shell command and return result."""
        if self.verbose:
            self.log(f"Running: {' '.join(cmd)}")

        # Validate inputs
        if not cmd or not isinstance(cmd, list):
            return 1, "", "Invalid command format"

        # Check that PROJECT_ROOT is valid
        if not PROJECT_ROOT.exists() or not PROJECT_ROOT.is_dir():
            return 1, "", f"Project root does not exist: {PROJECT_ROOT}"

        try:
            result = subprocess.run(
                cmd,
                capture_output=capture,
                text=True,
                timeout=300,
                cwd=str(PROJECT_ROOT),
            )
            # Handle None outputs
            stdout = result.stdout if result.stdout is not None else ""
            stderr = result.stderr if result.stderr is not None else ""
            return result.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out after 300 seconds"
        except FileNotFoundError as e:
            return 1, "", f"Command not found: {e}"
        except Exception as e:
            return 1, "", f"Command execution failed: {str(e)}"

    def run_tests(self, with_tracking: bool = True) -> bool:
        """Run pytest with optional error tracking."""
        self.log("Running tests...")

        cmd = ["python3", "-m", "pytest", "tests/python/", "-v", "--tb=short"]
        if with_tracking:
            cmd.append("--error-tracking")

        code, stdout, stderr = self.run_command(cmd)

        # Truncate outputs but keep them useful (split on newlines to avoid cutting mid-line)
        output_lines = stdout.split('\n') if stdout else []
        error_lines = stderr.split('\n') if stderr else []

        # Keep first 100 lines or until we hit size limit
        truncated_output = '\n'.join(output_lines[:100])
        if len(output_lines) > 100:
            truncated_output += f"\n... ({len(output_lines) - 100} more lines)"

        truncated_errors = '\n'.join(error_lines[:50])
        if len(error_lines) > 50:
            truncated_errors += f"\n... ({len(error_lines) - 50} more lines)"

        self.results["tests"] = {
            "status": "passed" if code == 0 else "failed",
            "exit_code": code,
            "output": truncated_output,
            "errors": truncated_errors,
        }

        if code == 0:
            self.log("Tests passed!", "OK")
        else:
            self.log("Tests failed!", "ERROR")

        return code == 0

    def analyze_errors(self) -> Dict:
        """Run error pattern analysis."""
        self.log("Analyzing error patterns...")

        error_tracker_path = SCRIPT_DIR / "error_tracker.py"
        if not error_tracker_path.exists() or not error_tracker_path.is_file():
            self.log("Error tracker not found or not a valid file", "WARN")
            self.results["errors"]["status"] = "skipped"
            return {}

        code, stdout, stderr = self.run_command([
            "python3", str(error_tracker_path), "stats"
        ])

        self.results["errors"] = {
            "status": "completed" if code == 0 else "failed",
            "output": stdout if stdout else "",
            "errors": stderr if stderr else "",
        }

        # Run analyze if stats succeeded
        if code == 0:
            try:
                code2, stdout2, stderr2 = self.run_command([
                    "python3", str(error_tracker_path), "analyze"
                ])
                if code2 == 0:
                    self.results["errors"]["analysis"] = stdout2 if stdout2 else ""
            except Exception as e:
                self.log(f"Analysis command failed: {e}", "WARN")

        self.log("Error analysis complete", "OK" if code == 0 else "WARN")
        return self.results["errors"]

    def process_feedback(self, update_lessons: bool = False) -> Dict:
        """Process validated feedback files."""
        self.log("Processing feedback...")

        ingest_script = FEEDBACK_SKILL_DIR / "scripts" / "ingest-feedback.py"
        if not ingest_script.exists() or not ingest_script.is_file():
            self.log("Feedback ingestion script not found or not a valid file", "WARN")
            self.results["feedback"]["status"] = "skipped"
            return {}

        cmd = ["python3", str(ingest_script), "--verbose"]
        if update_lessons:
            cmd.append("--update-lessons")

        code, stdout, stderr = self.run_command(cmd)

        self.results["feedback"] = {
            "status": "completed" if code == 0 else "failed",
            "output": stdout if stdout else "",
            "errors": stderr if stderr else "",
            "lessons_updated": update_lessons and code == 0,
        }

        self.log("Feedback processing complete", "OK" if code == 0 else "WARN")
        return self.results["feedback"]

    def generate_lessons(self, min_occurrences: int = 3) -> Dict:
        """Generate lessons from error patterns."""
        # Validate input
        if not isinstance(min_occurrences, int) or min_occurrences < 1:
            self.log("Invalid min_occurrences, using default 3", "WARN")
            min_occurrences = 3

        self.log("Generating lessons from error patterns...")

        error_tracker_path = SCRIPT_DIR / "error_tracker.py"
        if not error_tracker_path.exists():
            self.log("Error tracker not found", "WARN")
            self.results["lessons"]["status"] = "skipped"
            return {}

        # Check if script is executable/readable
        if not error_tracker_path.is_file():
            self.log("Error tracker is not a valid file", "WARN")
            self.results["lessons"]["status"] = "skipped"
            return {}

        code, stdout, stderr = self.run_command([
            "python3", str(error_tracker_path),
            "generate-lessons",
            f"--min-occurrences={min_occurrences}"
        ])

        self.results["lessons"] = {
            "status": "completed" if code == 0 else "failed",
            "output": stdout if stdout else "",
            "errors": stderr if stderr else "",
        }

        self.log("Lesson generation complete", "OK" if code == 0 else "WARN")
        return self.results["lessons"]

    def generate_report(self) -> str:
        """Generate a combined automation report."""
        report = []
        report.append("=" * 70)
        report.append("AUTOMATION REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)

        for task, result in self.results.items():
            status = result.get("status", "unknown")
            status_icon = {"passed": "✅", "completed": "✅", "failed": "❌", "skipped": "⏭️"}.get(status, "❓")

            report.append(f"\n{status_icon} {task.upper()}: {status}")

            if self.verbose and result.get("output"):
                report.append("-" * 40)
                report.append(result["output"][:500])

        report.append("\n" + "=" * 70)

        # Summary
        passed = sum(1 for r in self.results.values() if r["status"] in ["passed", "completed"])
        failed = sum(1 for r in self.results.values() if r["status"] == "failed")
        skipped = sum(1 for r in self.results.values() if r["status"] == "skipped")

        report.append(f"SUMMARY: {passed} passed, {failed} failed, {skipped} skipped")
        report.append("=" * 70)

        return "\n".join(report)

    def run_full_cycle(self, update_lessons: bool = False) -> int:
        """Run the complete automation cycle."""
        self.log("Starting full automation cycle", "INFO")
        print("=" * 70)

        # Step 1: Run tests
        tests_passed = self.run_tests(with_tracking=True)

        # Step 2: Analyze error patterns
        self.analyze_errors()

        # Step 3: Process feedback
        self.process_feedback(update_lessons=update_lessons)

        # Step 4: Generate lessons if requested
        if update_lessons:
            self.generate_lessons()

        # Generate and print report
        report = self.generate_report()
        print(report)

        # Return exit code based on test results
        return 0 if tests_passed else 1


def main():
    parser = argparse.ArgumentParser(
        description="Unified automation for TopEndSports Content Briefs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run full automation cycle")
    run_parser.add_argument("--update-lessons", action="store_true",
                           help="Update lessons-learned.md")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests with error tracking")
    test_parser.add_argument("--no-tracking", action="store_true",
                            help="Disable error tracking")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate combined report")

    # Lessons command
    lessons_parser = subparsers.add_parser("lessons", help="Generate lessons from patterns")
    lessons_parser.add_argument("--min-occurrences", type=int, default=3,
                               help="Minimum occurrences for lesson generation")

    # Common arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    runner = AutomationRunner(verbose=args.verbose)

    if args.command == "run":
        return runner.run_full_cycle(update_lessons=args.update_lessons)

    elif args.command == "test":
        success = runner.run_tests(with_tracking=not args.no_tracking)
        return 0 if success else 1

    elif args.command == "report":
        runner.analyze_errors()
        runner.process_feedback()
        print(runner.generate_report())
        return 0

    elif args.command == "lessons":
        runner.generate_lessons(min_occurrences=args.min_occurrences)
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
