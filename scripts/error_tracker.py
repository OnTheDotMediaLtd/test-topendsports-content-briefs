#!/usr/bin/env python3
"""
Self-Learning Error Tracker for TopEndSports Content Briefs

Automatically tracks errors from tests, scripts, and brief generation,
detects patterns, and suggests updates to lessons-learned.md.

Usage:
    # Log an error
    python3 error_tracker.py log --source "test_ahrefs" --error "API 403" --context "keywords lookup"

    # Analyze patterns
    python3 error_tracker.py analyze

    # Generate lessons from patterns
    python3 error_tracker.py generate-lessons

    # Show statistics
    python3 error_tracker.py stats

Features:
    - Structured error logging with categories and severity
    - Pattern detection for recurring issues
    - Automatic lesson generation from error patterns
    - Integration with existing feedback system
    - CI/CD compatible output formats
"""

import argparse
import json
import os
import sys
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Any

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ERROR_LOG_DIR = PROJECT_ROOT / "logs" / "errors"
ERROR_LOG_FILE = ERROR_LOG_DIR / "error_log.json"
PATTERNS_FILE = ERROR_LOG_DIR / "patterns.json"
LESSONS_FILE = PROJECT_ROOT / "content-briefs-skill" / "references" / "lessons-learned.md"

# Error categories
ERROR_CATEGORIES = {
    "api": ["403", "401", "timeout", "rate_limit", "rate limit", "network", "connection"],
    "validation": ["schema", "required", "missing", "invalid", "format"],
    "file": ["file not found", "not_found", "permission", "read", "write", "path"],
    "content": ["keyword", "template", "brand", "html", "css", "js", "selector"],
    "test": ["assertion", "fixture", "mock", "import", "syntax"],
    "process": ["phase", "brief", "generation", "conversion"],
}

# Severity levels
SEVERITY_LEVELS = {
    "critical": 4,  # System breaking, immediate fix needed
    "high": 3,      # Major functionality affected
    "medium": 2,    # Some functionality affected
    "low": 1,       # Minor issue, cosmetic
}


class ErrorEntry:
    """Represents a single error entry."""

    def __init__(
        self,
        source: str,
        error_message: str,
        context: str = "",
        category: str = "unknown",
        severity: str = "medium",
        stack_trace: str = "",
        metadata: Optional[Dict] = None
    ):
        self.timestamp = datetime.now().isoformat()
        self.source = source
        self.error_message = error_message
        self.context = context
        self.category = category
        self.severity = severity
        self.stack_trace = stack_trace
        self.metadata = metadata or {}

        # Generate a fingerprint for deduplication
        self.fingerprint = self._generate_fingerprint()

    def _generate_fingerprint(self) -> str:
        """Generate a unique fingerprint for this error type."""
        # Create a normalized version of the error for deduplication
        normalized = f"{self.source}:{self.category}:{self._normalize_message()}"
        return hashlib.md5(normalized.encode()).hexdigest()[:12]

    def _normalize_message(self) -> str:
        """Normalize error message for pattern matching."""
        msg = self.error_message.lower()
        # Remove timestamps
        msg = re.sub(r'\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}', '', msg)
        # Remove specific file paths but keep structure
        msg = re.sub(r'/[\w/\-\.]+', '/PATH', msg)
        # Remove line numbers
        msg = re.sub(r'line \d+', 'line N', msg)
        # Remove specific numbers that might vary
        msg = re.sub(r'\b\d{5,}\b', 'N', msg)
        return msg.strip()

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "source": self.source,
            "error_message": self.error_message,
            "context": self.context,
            "category": self.category,
            "severity": self.severity,
            "stack_trace": self.stack_trace,
            "metadata": self.metadata,
            "fingerprint": self.fingerprint,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ErrorEntry':
        """Create ErrorEntry from dictionary."""
        entry = cls(
            source=data.get("source", "unknown"),
            error_message=data.get("error_message", ""),
            context=data.get("context", ""),
            category=data.get("category", "unknown"),
            severity=data.get("severity", "medium"),
            stack_trace=data.get("stack_trace", ""),
            metadata=data.get("metadata", {}),
        )
        entry.timestamp = data.get("timestamp", entry.timestamp)
        entry.fingerprint = data.get("fingerprint", entry.fingerprint)
        return entry


class ErrorTracker:
    """Main error tracking class with pattern detection and learning."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors: List[ErrorEntry] = []
        self.patterns: Dict[str, Dict] = {}

        # Ensure directories exist
        ERROR_LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Load existing data
        self._load_errors()
        self._load_patterns()

    def log(self, msg: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[DEBUG] {msg}")

    def _load_errors(self):
        """Load existing errors from file."""
        if ERROR_LOG_FILE.exists():
            try:
                # Check if file is empty
                if ERROR_LOG_FILE.stat().st_size == 0:
                    self.log("Error log file is empty, starting fresh")
                    self.errors = []
                    return

                with open(ERROR_LOG_FILE, 'r') as f:
                    data = json.load(f)
                    # Validate data structure
                    if not isinstance(data, dict):
                        self.log("Invalid error log format, starting fresh")
                        self.errors = []
                        return

                    errors_data = data.get("errors", [])
                    if not isinstance(errors_data, list):
                        self.log("Invalid errors list format, starting fresh")
                        self.errors = []
                        return

                    # Load entries with error handling per entry
                    self.errors = []
                    for e in errors_data:
                        try:
                            if isinstance(e, dict):
                                self.errors.append(ErrorEntry.from_dict(e))
                        except Exception as entry_error:
                            self.log(f"Skipping malformed entry: {entry_error}")
                            continue

                self.log(f"Loaded {len(self.errors)} existing errors")
            except json.JSONDecodeError as e:
                self.log(f"JSON decode error in error log: {e}, starting fresh")
                self.errors = []
            except Exception as e:
                self.log(f"Could not load errors: {e}, starting fresh")
                self.errors = []
        else:
            self.errors = []

    def _save_errors(self):
        """Save errors to file with atomic write."""
        temp_file = ERROR_LOG_FILE.with_suffix('.tmp')
        try:
            # Write to temp file first (atomic operation)
            with open(temp_file, 'w') as f:
                json.dump({
                    "last_updated": datetime.now().isoformat(),
                    "total_count": len(self.errors),
                    "errors": [e.to_dict() for e in self.errors]
                }, f, indent=2)

            # Replace original file atomically
            temp_file.replace(ERROR_LOG_FILE)
            self.log(f"Saved {len(self.errors)} errors")
        except Exception as e:
            print(f"[ERROR] Could not save errors: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

    def _load_patterns(self):
        """Load existing patterns from file."""
        if PATTERNS_FILE.exists():
            try:
                # Check if file is empty
                if PATTERNS_FILE.stat().st_size == 0:
                    self.log("Patterns file is empty, starting fresh")
                    self.patterns = {}
                    return

                with open(PATTERNS_FILE, 'r') as f:
                    data = json.load(f)
                    # Validate it's a dictionary
                    if not isinstance(data, dict):
                        self.log("Invalid patterns format, starting fresh")
                        self.patterns = {}
                        return

                    self.patterns = data
                self.log(f"Loaded {len(self.patterns)} patterns")
            except json.JSONDecodeError as e:
                self.log(f"JSON decode error in patterns: {e}, starting fresh")
                self.patterns = {}
            except Exception as e:
                self.log(f"Could not load patterns: {e}, starting fresh")
                self.patterns = {}
        else:
            self.patterns = {}

    def _save_patterns(self):
        """Save patterns to file with atomic write."""
        temp_file = PATTERNS_FILE.with_suffix('.tmp')
        try:
            # Write to temp file first
            with open(temp_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)

            # Replace original file atomically
            temp_file.replace(PATTERNS_FILE)
            self.log(f"Saved {len(self.patterns)} patterns")
        except Exception as e:
            print(f"[ERROR] Could not save patterns: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

    def _detect_category(self, error_message: str) -> str:
        """Auto-detect error category from message."""
        msg_lower = error_message.lower()

        for category, keywords in ERROR_CATEGORIES.items():
            for keyword in keywords:
                if keyword in msg_lower:
                    return category

        return "unknown"

    def _detect_severity(self, error_message: str, source: str) -> str:
        """Auto-detect error severity."""
        msg_lower = error_message.lower()

        # Critical patterns
        if any(p in msg_lower for p in ["crash", "fatal", "cannot start", "critical"]):
            return "critical"

        # High patterns
        if any(p in msg_lower for p in ["failed", "error", "exception", "403", "401"]):
            return "high"

        # Medium patterns
        if any(p in msg_lower for p in ["warning", "timeout", "retry", "missing"]):
            return "medium"

        # Source-based detection
        if "test" in source.lower():
            return "high"  # Test failures are always important

        return "medium"

    def add_error(
        self,
        source: str,
        error_message: str,
        context: str = "",
        category: Optional[str] = None,
        severity: Optional[str] = None,
        stack_trace: str = "",
        metadata: Optional[Dict] = None
    ) -> ErrorEntry:
        """Add a new error to the tracker."""
        # Input validation
        if not source or not isinstance(source, str):
            raise ValueError("source must be a non-empty string")
        if not error_message or not isinstance(error_message, str):
            raise ValueError("error_message must be a non-empty string")

        # Truncate excessively long inputs to prevent memory issues
        source = source[:500]
        error_message = error_message[:2000]
        context = context[:1000] if context else ""
        stack_trace = stack_trace[:5000] if stack_trace else ""

        # Validate severity if provided
        if severity and severity not in SEVERITY_LEVELS:
            raise ValueError(f"severity must be one of {list(SEVERITY_LEVELS.keys())}")

        # Auto-detect category and severity if not provided
        if category is None:
            category = self._detect_category(error_message)

        if severity is None:
            severity = self._detect_severity(error_message, source)

        entry = ErrorEntry(
            source=source,
            error_message=error_message,
            context=context,
            category=category,
            severity=severity,
            stack_trace=stack_trace,
            metadata=metadata,
        )

        self.errors.append(entry)

        # Limit total errors stored to prevent unbounded growth (keep most recent 10000)
        if len(self.errors) > 10000:
            self.log("Warning: Error log exceeding 10000 entries, removing oldest")
            self.errors = self.errors[-10000:]

        self._save_errors()

        # Update patterns
        self._update_pattern(entry)

        print(f"[LOGGED] {entry.severity.upper()} error from {entry.source}: {entry.error_message[:80]}")
        return entry

    def _update_pattern(self, entry: ErrorEntry):
        """Update pattern tracking for this error."""
        fingerprint = entry.fingerprint

        if fingerprint not in self.patterns:
            self.patterns[fingerprint] = {
                "first_seen": entry.timestamp,
                "last_seen": entry.timestamp,
                "count": 0,
                "source": entry.source,
                "category": entry.category,
                "severity": entry.severity,
                "sample_message": entry.error_message[:200],
                "sample_context": entry.context,
                "occurrences": [],
                "lesson_generated": False,
            }

        pattern = self.patterns[fingerprint]
        pattern["last_seen"] = entry.timestamp
        pattern["count"] += 1
        pattern["occurrences"].append({
            "timestamp": entry.timestamp,
            "context": entry.context[:100],
        })

        # Keep only last 20 occurrences
        pattern["occurrences"] = pattern["occurrences"][-20:]

        self._save_patterns()

        # Check if this is a recurring pattern worth learning from
        if pattern["count"] >= 3 and not pattern["lesson_generated"]:
            print(f"[PATTERN] Recurring error detected ({pattern['count']} times): {pattern['sample_message'][:50]}")

    def analyze_patterns(self) -> Dict[str, List[Dict]]:
        """Analyze error patterns and return insights."""
        analysis = {
            "recurring": [],      # Errors that happen repeatedly
            "recent_surge": [],   # Errors with recent increase
            "critical": [],       # Critical severity errors
            "by_category": defaultdict(list),
            "by_source": defaultdict(list),
        }

        now = datetime.now()
        week_ago = now - timedelta(days=7)

        for fingerprint, pattern in self.patterns.items():
            pattern_data = {
                "fingerprint": fingerprint,
                **pattern
            }

            # Categorize by count
            if pattern["count"] >= 5:
                analysis["recurring"].append(pattern_data)

            # Check for recent surge
            recent_count = sum(
                1 for occ in pattern.get("occurrences", [])
                if datetime.fromisoformat(occ["timestamp"]) > week_ago
            )
            if recent_count > pattern["count"] / 2 and pattern["count"] > 2:
                analysis["recent_surge"].append(pattern_data)

            # Critical errors
            if pattern["severity"] == "critical":
                analysis["critical"].append(pattern_data)

            # By category
            analysis["by_category"][pattern["category"]].append(pattern_data)

            # By source
            analysis["by_source"][pattern["source"]].append(pattern_data)

        # Sort by count
        for key in ["recurring", "recent_surge", "critical"]:
            analysis[key].sort(key=lambda x: x["count"], reverse=True)

        return analysis

    def generate_lessons(self, min_occurrences: int = 3, dry_run: bool = False) -> List[Dict]:
        """Generate lessons from recurring error patterns."""
        lessons = []

        for fingerprint, pattern in self.patterns.items():
            # Skip if already generated or not enough occurrences
            if pattern["lesson_generated"]:
                continue
            if pattern["count"] < min_occurrences:
                continue

            # Generate lesson based on category
            lesson = self._create_lesson_from_pattern(fingerprint, pattern)
            if lesson:
                lessons.append(lesson)

                if not dry_run:
                    pattern["lesson_generated"] = True

        if not dry_run and lessons:
            self._save_patterns()
            self._append_lessons_to_file(lessons)

        return lessons

    def _create_lesson_from_pattern(self, fingerprint: str, pattern: Dict) -> Optional[Dict]:
        """Create a lesson entry from an error pattern."""
        category = pattern["category"]
        source = pattern["source"]
        message = pattern["sample_message"]
        count = pattern["count"]

        lesson = {
            "fingerprint": fingerprint,
            "title": "",
            "problem": "",
            "solution": "",
            "category": category,
            "source": source,
            "occurrence_count": count,
            "generated_at": datetime.now().isoformat(),
        }

        # Generate lesson based on category
        if category == "api":
            if "403" in message or "401" in message:
                lesson["title"] = "Handle API Authentication Errors"
                lesson["problem"] = f"API calls failing with auth errors ({count} occurrences)"
                lesson["solution"] = "Use Python fallback (ahrefs-api.py) when MCP returns 403. Check API credentials and rate limits."
            elif "timeout" in message.lower():
                lesson["title"] = "Handle API Timeouts"
                lesson["problem"] = f"API calls timing out ({count} occurrences)"
                lesson["solution"] = "Implement retry with exponential backoff. Consider caching results."
            else:
                lesson["title"] = "Handle API Errors Gracefully"
                lesson["problem"] = f"API errors occurring ({count} occurrences): {message[:50]}"
                lesson["solution"] = "Add error handling and fallback mechanisms for API calls."

        elif category == "validation":
            lesson["title"] = "Improve Input Validation"
            lesson["problem"] = f"Validation failures ({count} occurrences): {message[:50]}"
            lesson["solution"] = "Add pre-validation checks before processing. Provide clearer error messages."

        elif category == "file":
            lesson["title"] = "Handle File Operations Safely"
            lesson["problem"] = f"File operation errors ({count} occurrences): {message[:50]}"
            lesson["solution"] = "Check file existence before operations. Use absolute paths."

        elif category == "content":
            lesson["title"] = "Improve Content Processing"
            lesson["problem"] = f"Content processing errors ({count} occurrences): {message[:50]}"
            lesson["solution"] = "Validate content structure before processing. Add format checks."

        elif category == "test":
            lesson["title"] = "Fix Recurring Test Failures"
            lesson["problem"] = f"Test failures ({count} occurrences): {message[:50]}"
            lesson["solution"] = "Review test expectations and fixtures. Consider edge cases."

        elif category == "process":
            lesson["title"] = "Improve Process Reliability"
            lesson["problem"] = f"Process errors ({count} occurrences): {message[:50]}"
            lesson["solution"] = "Add validation between phases. Implement better error recovery."

        else:
            lesson["title"] = f"Address Recurring {source} Error"
            lesson["problem"] = f"Repeated errors ({count} occurrences): {message[:50]}"
            lesson["solution"] = "Investigate root cause and add appropriate handling."

        return lesson

    def _append_lessons_to_file(self, lessons: List[Dict]):
        """Append generated lessons to lessons-learned.md."""
        if not lessons:
            return

        # Create lessons file if it doesn't exist
        if not LESSONS_FILE.exists():
            try:
                LESSONS_FILE.parent.mkdir(parents=True, exist_ok=True)
                LESSONS_FILE.write_text("# Lessons Learned\n\n*This file tracks lessons learned from errors and feedback.*\n")
                self.log(f"Created new lessons file: {LESSONS_FILE}")
            except Exception as e:
                print(f"[ERROR] Could not create lessons file: {e}")
                return

        temp_file = LESSONS_FILE.with_suffix('.tmp')
        try:
            # Read current content
            with open(LESSONS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()

            # Generate new section
            date_str = datetime.now().strftime('%Y-%m-%d')
            new_section = [
                f"\n\n## Auto-Generated Lessons ({date_str})",
                "*Generated from error pattern analysis*\n"
            ]

            for lesson in lessons:
                # Validate lesson data
                title = lesson.get('title', 'Untitled Lesson')
                problem = lesson.get('problem', 'No problem description')
                solution = lesson.get('solution', 'No solution provided')
                category = lesson.get('category', 'unknown')
                source = lesson.get('source', 'unknown')
                count = lesson.get('occurrence_count', 0)

                new_section.append(f"### {title}")
                new_section.append(f"**Problem**: {problem}")
                new_section.append(f"**Solution**: {solution}")
                new_section.append(f"*Category: {category} | Source: {source} | Occurrences: {count}*")
                new_section.append("")

            updated_content = content + "\n".join(new_section)

            # Write to temp file first
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            # Replace original file atomically
            temp_file.replace(LESSONS_FILE)

            print(f"[OK] Added {len(lessons)} lessons to {LESSONS_FILE}")

        except Exception as e:
            print(f"[ERROR] Could not update lessons file: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

    def get_stats(self) -> Dict:
        """Get statistics about tracked errors."""
        now = datetime.now()
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)

        stats = {
            "total_errors": len(self.errors),
            "unique_patterns": len(self.patterns),
            "errors_last_24h": 0,
            "errors_last_7d": 0,
            "by_severity": defaultdict(int),
            "by_category": defaultdict(int),
            "by_source": defaultdict(int),
            "lessons_generated": 0,
            "patterns_needing_attention": 0,
        }

        for error in self.errors:
            try:
                ts = datetime.fromisoformat(error.timestamp)
                if ts > day_ago:
                    stats["errors_last_24h"] += 1
                if ts > week_ago:
                    stats["errors_last_7d"] += 1
            except ValueError:
                pass

            stats["by_severity"][error.severity] += 1
            stats["by_category"][error.category] += 1
            stats["by_source"][error.source] += 1

        for pattern in self.patterns.values():
            if pattern.get("lesson_generated"):
                stats["lessons_generated"] += 1
            if pattern["count"] >= 3 and not pattern.get("lesson_generated"):
                stats["patterns_needing_attention"] += 1

        return stats

    def print_stats(self):
        """Print statistics in a formatted way."""
        stats = self.get_stats()

        print("=" * 60)
        print("ERROR TRACKER STATISTICS")
        print("=" * 60)
        print(f"\nTotal errors logged: {stats['total_errors']}")
        print(f"Unique patterns: {stats['unique_patterns']}")
        print(f"Errors in last 24h: {stats['errors_last_24h']}")
        print(f"Errors in last 7d: {stats['errors_last_7d']}")
        print(f"Lessons generated: {stats['lessons_generated']}")
        print(f"Patterns needing attention: {stats['patterns_needing_attention']}")

        if stats['by_severity']:
            print("\nBy Severity:")
            for severity in ['critical', 'high', 'medium', 'low']:
                count = stats['by_severity'].get(severity, 0)
                if count:
                    print(f"  {severity}: {count}")

        if stats['by_category']:
            print("\nBy Category:")
            for category, count in sorted(stats['by_category'].items(), key=lambda x: -x[1]):
                print(f"  {category}: {count}")

        if stats['by_source']:
            print("\nBy Source:")
            for source, count in sorted(stats['by_source'].items(), key=lambda x: -x[1])[:10]:
                print(f"  {source}: {count}")

        print("=" * 60)

    def print_analysis(self):
        """Print pattern analysis."""
        analysis = self.analyze_patterns()

        print("=" * 60)
        print("ERROR PATTERN ANALYSIS")
        print("=" * 60)

        if analysis["critical"]:
            print("\n[CRITICAL ERRORS]")
            for p in analysis["critical"][:5]:
                print(f"  - {p['sample_message'][:60]} ({p['count']} times)")

        if analysis["recurring"]:
            print("\n[RECURRING PATTERNS]")
            for p in analysis["recurring"][:10]:
                print(f"  - [{p['category']}] {p['sample_message'][:50]} ({p['count']} times)")

        if analysis["recent_surge"]:
            print("\n[RECENT SURGE]")
            for p in analysis["recent_surge"][:5]:
                print(f"  - {p['sample_message'][:50]} (surge detected)")

        print("\n[BY CATEGORY]")
        for category, patterns in analysis["by_category"].items():
            total = sum(p["count"] for p in patterns)
            print(f"  {category}: {len(patterns)} patterns, {total} total errors")

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Self-learning error tracker for TopEndSports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log a new error")
    log_parser.add_argument("--source", required=True, help="Error source (e.g., test_ahrefs)")
    log_parser.add_argument("--error", required=True, help="Error message")
    log_parser.add_argument("--context", default="", help="Additional context")
    log_parser.add_argument("--category", help="Error category")
    log_parser.add_argument("--severity", choices=["critical", "high", "medium", "low"])
    log_parser.add_argument("--stack-trace", default="", help="Stack trace")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze error patterns")

    # Generate lessons command
    lessons_parser = subparsers.add_parser("generate-lessons", help="Generate lessons from patterns")
    lessons_parser.add_argument("--min-occurrences", type=int, default=3, help="Minimum occurrences")
    lessons_parser.add_argument("--dry-run", action="store_true", help="Preview without writing")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear old errors")
    clear_parser.add_argument("--days", type=int, default=30, help="Clear errors older than N days")

    # Common arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    tracker = ErrorTracker(verbose=args.verbose)

    if args.command == "log":
        tracker.add_error(
            source=args.source,
            error_message=args.error,
            context=args.context,
            category=args.category,
            severity=args.severity,
            stack_trace=args.stack_trace,
        )

    elif args.command == "analyze":
        tracker.print_analysis()

    elif args.command == "generate-lessons":
        lessons = tracker.generate_lessons(
            min_occurrences=args.min_occurrences,
            dry_run=args.dry_run,
        )
        if lessons:
            print(f"\n[INFO] Generated {len(lessons)} lessons:")
            for lesson in lessons:
                print(f"  - {lesson['title']}")
        else:
            print("[INFO] No new lessons to generate")

    elif args.command == "stats":
        tracker.print_stats()

    elif args.command == "clear":
        cutoff = datetime.now() - timedelta(days=args.days)
        before_count = len(tracker.errors)
        kept_errors = []
        skipped_count = 0

        for e in tracker.errors:
            try:
                if datetime.fromisoformat(e.timestamp) > cutoff:
                    kept_errors.append(e)
            except (ValueError, AttributeError) as err:
                # Keep errors with invalid timestamps
                kept_errors.append(e)
                skipped_count += 1

        tracker.errors = kept_errors
        tracker._save_errors()

        cleared_count = before_count - len(tracker.errors)
        print(f"[OK] Cleared {cleared_count} errors older than {args.days} days")
        if skipped_count > 0:
            print(f"[WARN] Kept {skipped_count} errors with invalid timestamps")

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
