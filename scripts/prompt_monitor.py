#!/usr/bin/env python3
"""
Chat Prompt Monitoring System for TopEndSports Content Briefs

Tracks command usage, success rates, and identifies patterns
to improve the brief generation workflow.

Usage:
    python3 prompt_monitor.py log --command "generate-brief" --status "success"
    python3 prompt_monitor.py stats
    python3 prompt_monitor.py trends
    python3 prompt_monitor.py recommendations
    python3 prompt_monitor.py export --output report.csv
    python3 prompt_monitor.py alerts
    python3 prompt_monitor.py archive --days 90

Features:
    - Logs command/prompt usage with context
    - Tracks success/failure rates per command
    - Identifies underused or problematic commands
    - Generates recommendations for workflow improvements
    - Exports usage data to CSV for analysis
    - Alerts on critical issues with non-zero exit codes
    - Archives old entries beyond retention period
    - Hooks for external script integration
"""

import argparse
import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Any

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
MONITOR_DIR = PROJECT_ROOT / "logs" / "prompts"
USAGE_LOG_FILE = MONITOR_DIR / "usage_log.json"
ANALYTICS_FILE = MONITOR_DIR / "analytics.json"
ARCHIVE_DIR = MONITOR_DIR / "archive"
HOOKS_DIR = MONITOR_DIR / "hooks"

# Alert thresholds
ALERT_THRESHOLDS = {
    "critical_success_rate": 60.0,  # Alert if overall success rate < 60%
    "category_failure_threshold": 5,  # Alert if category has 5+ consecutive failures
    "high_error_count": 10,  # Alert if 10+ errors in last hour
    "ahrefs_failure_rate": 80.0,  # Alert if Ahrefs failure rate > 80%
}

# Retention policy
RETENTION_DAYS = 90  # Archive entries older than 90 days

# Known commands and their expected patterns
KNOWN_COMMANDS = {
    "/generate-brief": {
        "category": "brief_generation",
        "expected_success_rate": 0.9,
        "description": "Generate a complete 3-phase brief",
    },
    "/submit-feedback": {
        "category": "feedback",
        "expected_success_rate": 0.95,
        "description": "Submit feedback on a brief",
    },
    "mcp__topendsports-briefs__": {
        "category": "mcp_tool",
        "expected_success_rate": 0.85,
        "description": "MCP server tool calls",
    },
    "mcp__ahrefs__": {
        "category": "ahrefs",
        "expected_success_rate": 0.7,
        "description": "Ahrefs API calls",
    },
    "python3 ahrefs-api.py": {
        "category": "ahrefs_fallback",
        "expected_success_rate": 0.85,
        "description": "Python Ahrefs fallback",
    },
    "validate-phase": {
        "category": "validation",
        "expected_success_rate": 0.8,
        "description": "Phase validation",
    },
    "convert_to_docx": {
        "category": "conversion",
        "expected_success_rate": 0.95,
        "description": "DOCX conversion",
    },
}


class UsageEntry:
    """Represents a single command usage entry."""

    def __init__(
        self,
        command: str,
        status: str,
        context: str = "",
        duration_ms: Optional[int] = None,
        error_message: str = "",
        metadata: Optional[Dict] = None,
    ):
        self.timestamp = datetime.now().isoformat()
        self.command = command
        self.status = status  # success, failure, partial, skipped
        self.context = context
        self.duration_ms = duration_ms
        self.error_message = error_message
        self.metadata = metadata or {}
        self.category = self._detect_category()

    def _detect_category(self) -> str:
        """Detect command category from known patterns."""
        cmd_lower = self.command.lower()

        for pattern, config in KNOWN_COMMANDS.items():
            if pattern.lower() in cmd_lower:
                return config["category"]

        # Default categories based on content
        if "phase" in cmd_lower:
            return "phase_execution"
        if "brief" in cmd_lower:
            return "brief_generation"
        if "keyword" in cmd_lower or "ahrefs" in cmd_lower:
            return "keyword_research"
        if "docx" in cmd_lower or "convert" in cmd_lower:
            return "conversion"
        if "validate" in cmd_lower or "check" in cmd_lower:
            return "validation"

        return "other"

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "command": self.command,
            "status": self.status,
            "context": self.context,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "metadata": self.metadata,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'UsageEntry':
        """Create UsageEntry from dictionary."""
        entry = cls(
            command=data.get("command", "unknown"),
            status=data.get("status", "unknown"),
            context=data.get("context", ""),
            duration_ms=data.get("duration_ms"),
            error_message=data.get("error_message", ""),
            metadata=data.get("metadata", {}),
        )
        entry.timestamp = data.get("timestamp", entry.timestamp)
        entry.category = data.get("category", entry.category)
        return entry


class PromptMonitor:
    """Main monitoring class for command usage tracking."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.entries: List[UsageEntry] = []

        # Ensure directory exists
        MONITOR_DIR.mkdir(parents=True, exist_ok=True)

        # Load existing data
        self._load_entries()

    def log(self, msg: str):
        """Print verbose message."""
        if self.verbose:
            print(f"[DEBUG] {msg}")

    def _load_entries(self):
        """Load existing entries from file."""
        if USAGE_LOG_FILE.exists():
            try:
                # Check if file is empty
                if USAGE_LOG_FILE.stat().st_size == 0:
                    self.log("Usage log file is empty, starting fresh")
                    self.entries = []
                    return

                with open(USAGE_LOG_FILE, 'r') as f:
                    data = json.load(f)
                    # Validate data structure
                    if not isinstance(data, dict):
                        self.log("Invalid usage log format, starting fresh")
                        self.entries = []
                        return

                    entries_data = data.get("entries", [])
                    if not isinstance(entries_data, list):
                        self.log("Invalid entries list format, starting fresh")
                        self.entries = []
                        return

                    # Load entries with error handling per entry
                    self.entries = []
                    for e in entries_data:
                        try:
                            if isinstance(e, dict):
                                self.entries.append(UsageEntry.from_dict(e))
                        except Exception as entry_error:
                            self.log(f"Skipping malformed entry: {entry_error}")
                            continue

                self.log(f"Loaded {len(self.entries)} existing entries")
            except json.JSONDecodeError as e:
                self.log(f"JSON decode error in usage log: {e}, starting fresh")
                self.entries = []
            except Exception as e:
                self.log(f"Could not load entries: {e}, starting fresh")
                self.entries = []
        else:
            self.entries = []

    def _save_entries(self):
        """Save entries to file with atomic write."""
        temp_file = USAGE_LOG_FILE.with_suffix('.tmp')
        try:
            # Write to temp file first
            with open(temp_file, 'w') as f:
                json.dump({
                    "last_updated": datetime.now().isoformat(),
                    "total_count": len(self.entries),
                    "entries": [e.to_dict() for e in self.entries]
                }, f, indent=2)

            # Replace original file atomically
            temp_file.replace(USAGE_LOG_FILE)
            self.log(f"Saved {len(self.entries)} entries")
        except Exception as e:
            print(f"[ERROR] Could not save entries: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

    def log_usage(
        self,
        command: str,
        status: str,
        context: str = "",
        duration_ms: Optional[int] = None,
        error_message: str = "",
        metadata: Optional[Dict] = None,
    ) -> UsageEntry:
        """Log a command usage."""
        # Input validation
        if not command or not isinstance(command, str):
            raise ValueError("command must be a non-empty string")
        if not status or not isinstance(status, str):
            raise ValueError("status must be a non-empty string")

        # Validate status is in allowed values
        allowed_statuses = ["success", "failure", "partial", "skipped"]
        if status not in allowed_statuses:
            raise ValueError(f"status must be one of {allowed_statuses}")

        # Truncate excessively long inputs
        command = command[:1000]
        context = context[:1000] if context else ""
        error_message = error_message[:2000] if error_message else ""

        # Validate duration_ms if provided
        if duration_ms is not None and (not isinstance(duration_ms, int) or duration_ms < 0):
            raise ValueError("duration_ms must be a non-negative integer")

        entry = UsageEntry(
            command=command,
            status=status,
            context=context,
            duration_ms=duration_ms,
            error_message=error_message,
            metadata=metadata,
        )

        self.entries.append(entry)

        # Limit total entries stored to prevent unbounded growth (keep most recent 5000)
        if len(self.entries) > 5000:
            self.log("Warning: Usage log exceeding 5000 entries, removing oldest")
            self.entries = self.entries[-5000:]

        self._save_entries()

        status_icon = {"success": "✅", "failure": "❌", "partial": "⚠️", "skipped": "⏭️"}.get(status, "•")
        print(f"[LOGGED] {status_icon} {command} ({entry.category})")

        return entry

    def get_stats(self, days: int = 30) -> Dict:
        """Get usage statistics for the specified period."""
        now = datetime.now()
        cutoff = now - timedelta(days=days)

        stats = {
            "period_days": days,
            "total_entries": 0,
            "by_status": defaultdict(int),
            "by_category": defaultdict(lambda: {"total": 0, "success": 0, "failure": 0}),
            "by_command": defaultdict(lambda: {"total": 0, "success": 0, "failure": 0}),
            "success_rate": 0.0,
            "avg_duration_ms": None,
            "recent_failures": [],
        }

        durations = []

        for entry in self.entries:
            try:
                ts = datetime.fromisoformat(entry.timestamp)
                if ts < cutoff:
                    continue
            except ValueError:
                continue

            stats["total_entries"] += 1
            stats["by_status"][entry.status] += 1

            # By category
            cat_stats = stats["by_category"][entry.category]
            cat_stats["total"] += 1
            if entry.status == "success":
                cat_stats["success"] += 1
            elif entry.status == "failure":
                cat_stats["failure"] += 1

            # By command (truncate long commands)
            cmd_key = entry.command[:50] if len(entry.command) > 50 else entry.command
            cmd_stats = stats["by_command"][cmd_key]
            cmd_stats["total"] += 1
            if entry.status == "success":
                cmd_stats["success"] += 1
            elif entry.status == "failure":
                cmd_stats["failure"] += 1
                if len(stats["recent_failures"]) < 10:
                    stats["recent_failures"].append({
                        "command": entry.command,
                        "error": entry.error_message[:100],
                        "timestamp": entry.timestamp,
                    })

            if entry.duration_ms:
                durations.append(entry.duration_ms)

        # Calculate success rate
        total = stats["total_entries"]
        if total > 0:
            success = stats["by_status"].get("success", 0)
            stats["success_rate"] = round(success / total * 100, 1)

        # Calculate average duration
        if durations:
            stats["avg_duration_ms"] = round(sum(durations) / len(durations))

        return stats

    def get_trends(self, days: int = 30) -> Dict:
        """Analyze trends in command usage."""
        stats = self.get_stats(days)

        trends = {
            "improving": [],
            "declining": [],
            "stable": [],
            "underused": [],
            "problematic": [],
        }

        # Handle empty stats
        if not stats.get("by_category"):
            return trends

        # Analyze each category
        for category, cat_stats in stats["by_category"].items():
            total = cat_stats.get("total", 0)
            if total == 0:
                continue

            # Safe division with default
            success_count = cat_stats.get("success", 0)
            success_rate = success_count / total if total > 0 else 0

            # Check against expected rate
            expected_rate = 0.8  # Default
            for pattern, config in KNOWN_COMMANDS.items():
                if config.get("category") == category:
                    expected_rate = config.get("expected_success_rate", 0.8)
                    break

            if success_rate < expected_rate - 0.1:
                trends["problematic"].append({
                    "category": category,
                    "success_rate": round(success_rate * 100, 1),
                    "expected_rate": round(expected_rate * 100, 1),
                    "total_uses": total,
                })
            elif success_rate > expected_rate + 0.1:
                trends["improving"].append({
                    "category": category,
                    "success_rate": round(success_rate * 100, 1),
                    "total_uses": total,
                })
            else:
                trends["stable"].append({
                    "category": category,
                    "success_rate": round(success_rate * 100, 1),
                    "total_uses": total,
                })

        # Find underused categories
        for pattern, config in KNOWN_COMMANDS.items():
            cat = config.get("category", "unknown")
            if cat not in stats["by_category"] or stats["by_category"][cat].get("total", 0) < 5:
                trends["underused"].append({
                    "category": cat,
                    "description": config.get("description", "No description"),
                })

        return trends

    def get_recommendations(self) -> List[Dict]:
        """Generate recommendations based on usage patterns."""
        stats = self.get_stats(30)
        trends = self.get_trends(30)
        recommendations = []

        # Check for problematic categories with specific actionable recommendations
        for prob in trends["problematic"]:
            category = prob["category"]
            success_rate = prob["success_rate"]
            expected_rate = prob["expected_rate"]
            gap = expected_rate - success_rate

            # More specific recommendations based on category and gap severity
            if category == "ahrefs":
                if gap > 30:
                    action = "IMMEDIATE: Switch to Python fallback (ahrefs-api.py) as default. MCP integration critically unstable."
                elif gap > 15:
                    action = "Add retry logic with automatic fallback to Python API after 2 MCP failures. Update CLAUDE.md to prioritize fallback."
                else:
                    action = "Monitor MCP connectivity. Document common 403 errors and resolution steps in lessons-learned.md."
            elif category == "brief_generation":
                action = f"Analyze last {prob['total_uses']} brief attempts. Check for: (1) missing phase files, (2) keyword research skips, (3) incomplete deliverables. Update GUARDRAILS.md."
            elif category == "validation":
                action = "Review validation scripts for false negatives. Add --skip-optional flag for non-critical checks. Document common validation failures."
            elif category == "conversion":
                action = "Check DOCX converter dependencies. Verify pandoc version. Add fallback to manual template generation."
            else:
                action = f"Review error logs for {category}. Identify top 3 failure patterns. Add specific error handling and user guidance."

            recommendations.append({
                "priority": "high" if gap > 20 else "medium",
                "category": category,
                "issue": f"Low success rate ({success_rate}% vs expected {expected_rate}%)",
                "recommendation": action,
                "gap_severity": gap,
            })

        # Check for underused features with specific promotion strategies
        for underused in trends["underused"]:
            category = underused["category"]

            # Specific promotion strategies per category
            if category == "feedback":
                action = "Add feedback prompt to end of every brief generation. Include quick rating (1-5) in completion message."
            elif category == "validation":
                action = "Make validation mandatory between phases. Update ORCHESTRATOR.md to block phase progression without validation pass."
            elif category == "conversion":
                action = "Auto-trigger DOCX conversion after Phase 3 completion. Add to /generate-brief command checklist."
            else:
                action = f"Add usage example for '{underused['description']}' to CLAUDE.md quick start section. Create /example-{category} command."

            recommendations.append({
                "priority": "medium",
                "category": category,
                "issue": f"Feature '{underused['description']}' is underutilized",
                "recommendation": action,
            })

        # Check overall success rate with specific thresholds
        if stats["success_rate"] < 60:
            recommendations.append({
                "priority": "critical",
                "category": "overall",
                "issue": f"CRITICAL: Overall success rate is {stats['success_rate']}%",
                "recommendation": "STOP: Review system stability. Analyze all failures from last 7 days. Schedule team review of workflow. Check for breaking changes in dependencies.",
            })
        elif stats["success_rate"] < 70:
            recommendations.append({
                "priority": "high",
                "category": "overall",
                "issue": f"Overall success rate is {stats['success_rate']}%",
                "recommendation": "Run comprehensive error analysis. Update error handling in top 3 failing commands. Add pre-flight checks to catch issues early.",
            })
        elif stats["success_rate"] < 80:
            recommendations.append({
                "priority": "medium",
                "category": "overall",
                "issue": f"Overall success rate is {stats['success_rate']}%",
                "recommendation": "Review recent failures. Update documentation for common pitfalls. Consider adding validation steps before critical operations.",
            })

        # Check for Ahrefs fallback usage with specific guidance
        ahrefs_main = stats["by_category"].get("ahrefs", {})
        ahrefs_fallback = stats["by_category"].get("ahrefs_fallback", {})

        ahrefs_main_total = ahrefs_main.get("total", 0)
        ahrefs_fallback_total = ahrefs_fallback.get("total", 0)

        if ahrefs_main_total > 0:
            ahrefs_failure_rate = (ahrefs_main.get("failure", 0) / ahrefs_main_total) * 100

            if ahrefs_failure_rate > 80:
                recommendations.append({
                    "priority": "critical",
                    "category": "ahrefs",
                    "issue": f"Ahrefs MCP failure rate: {ahrefs_failure_rate:.1f}%",
                    "recommendation": "IMMEDIATE: Update CLAUDE.md and ORCHESTRATOR.md to use Python fallback as PRIMARY method. Disable MCP until fixed. Add health check before brief generation.",
                })
            elif ahrefs_failure_rate > 50:
                recommendations.append({
                    "priority": "high",
                    "category": "ahrefs",
                    "issue": f"Ahrefs MCP failures exceed successes ({ahrefs_failure_rate:.1f}% failure rate)",
                    "recommendation": "Switch to Python fallback (ahrefs-api.py) as default. Add MCP status check command. Document authentication renewal process.",
                })

        # Check if Python fallback is being used effectively
        if ahrefs_fallback_total > 0 and ahrefs_main_total == 0:
            recommendations.append({
                "priority": "low",
                "category": "ahrefs",
                "issue": "Only using Python fallback, MCP never attempted",
                "recommendation": "MCP may be fixed. Test mcp__ahrefs connectivity. If working, update to try MCP first with fallback on failure.",
            })

        # Check for performance issues
        if stats["avg_duration_ms"] and stats["avg_duration_ms"] > 30000:
            recommendations.append({
                "priority": "medium",
                "category": "performance",
                "issue": f"Average command duration: {stats['avg_duration_ms']}ms (>30s)",
                "recommendation": "Profile slow commands. Consider: (1) parallel API calls, (2) caching keyword data, (3) async operations. Add timeout warnings.",
            })

        # Check for recent error patterns
        recent_errors = stats.get("recent_failures", [])
        if len(recent_errors) >= 5:
            # Analyze error patterns
            error_messages = [f.get("error", "") for f in recent_errors]
            common_error = max(set(error_messages), key=error_messages.count) if error_messages else ""

            if common_error and error_messages.count(common_error) >= 3:
                recommendations.append({
                    "priority": "high",
                    "category": "errors",
                    "issue": f"Repeated error pattern detected: '{common_error[:50]}'",
                    "recommendation": f"This error occurred {error_messages.count(common_error)} times. Add specific error handling or validation to prevent this. Update error message with resolution steps.",
                })

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 99))

        return recommendations

    def export_to_csv(self, output_file: str, days: Optional[int] = None) -> int:
        """Export usage data to CSV format for analysis.

        Args:
            output_file: Path to output CSV file
            days: Optional number of days to export (None = all data)

        Returns:
            Number of entries exported
        """
        now = datetime.now()
        cutoff = now - timedelta(days=days) if days else None

        entries_to_export = []
        for entry in self.entries:
            try:
                if cutoff:
                    ts = datetime.fromisoformat(entry.timestamp)
                    if ts < cutoff:
                        continue
                entries_to_export.append(entry)
            except ValueError:
                continue

        # Write CSV
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'command', 'status', 'category', 'duration_ms',
                         'error_message', 'context', 'metadata']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in entries_to_export:
                row = {
                    'timestamp': entry.timestamp,
                    'command': entry.command,
                    'status': entry.status,
                    'category': entry.category,
                    'duration_ms': entry.duration_ms or '',
                    'error_message': entry.error_message,
                    'context': entry.context,
                    'metadata': json.dumps(entry.metadata) if entry.metadata else '',
                }
                writer.writerow(row)

        print(f"[EXPORT] Exported {len(entries_to_export)} entries to {output_path}")
        return len(entries_to_export)

    def check_alerts(self) -> List[Dict]:
        """Check for critical issues that require attention.

        Returns:
            List of alert dictionaries with severity and message
        """
        alerts = []
        stats = self.get_stats(days=7)  # Check last 7 days for alerts

        # Alert 1: Critical overall success rate
        if stats["total_entries"] >= 5 and stats["success_rate"] < ALERT_THRESHOLDS["critical_success_rate"]:
            alerts.append({
                "severity": "critical",
                "category": "overall",
                "message": f"Overall success rate ({stats['success_rate']}%) below critical threshold ({ALERT_THRESHOLDS['critical_success_rate']}%)",
                "value": stats["success_rate"],
            })

        # Alert 2: High error count in last hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_errors = 0
        for entry in self.entries:
            try:
                ts = datetime.fromisoformat(entry.timestamp)
                if ts > one_hour_ago and entry.status == "failure":
                    recent_errors += 1
            except ValueError:
                continue

        if recent_errors >= ALERT_THRESHOLDS["high_error_count"]:
            alerts.append({
                "severity": "critical",
                "category": "errors",
                "message": f"High error count in last hour: {recent_errors} failures",
                "value": recent_errors,
            })

        # Alert 3: Ahrefs failure rate
        ahrefs_stats = stats["by_category"].get("ahrefs", {})
        if ahrefs_stats.get("total", 0) >= 3:
            ahrefs_total = ahrefs_stats["total"]
            ahrefs_failures = ahrefs_stats.get("failure", 0)
            ahrefs_failure_rate = (ahrefs_failures / ahrefs_total) * 100

            if ahrefs_failure_rate >= ALERT_THRESHOLDS["ahrefs_failure_rate"]:
                alerts.append({
                    "severity": "high",
                    "category": "ahrefs",
                    "message": f"Ahrefs failure rate ({ahrefs_failure_rate:.1f}%) exceeds threshold ({ALERT_THRESHOLDS['ahrefs_failure_rate']}%)",
                    "value": ahrefs_failure_rate,
                })

        # Alert 4: Consecutive failures in a category
        category_consecutive_failures = defaultdict(int)
        for entry in reversed(self.entries[-50:]):  # Check last 50 entries
            if entry.status == "failure":
                category_consecutive_failures[entry.category] += 1
            elif entry.category in category_consecutive_failures:
                # Reset count on success
                category_consecutive_failures[entry.category] = 0

        for category, consecutive_count in category_consecutive_failures.items():
            if consecutive_count >= ALERT_THRESHOLDS["category_failure_threshold"]:
                alerts.append({
                    "severity": "high",
                    "category": category,
                    "message": f"Category '{category}' has {consecutive_count} consecutive failures",
                    "value": consecutive_count,
                })

        # Alert 5: No successful brief generation in last 3 days
        three_days_ago = datetime.now() - timedelta(days=3)
        has_recent_brief_success = False
        for entry in self.entries:
            try:
                ts = datetime.fromisoformat(entry.timestamp)
                if (ts > three_days_ago and
                    entry.category == "brief_generation" and
                    entry.status == "success"):
                    has_recent_brief_success = True
                    break
            except ValueError:
                continue

        brief_attempts = [e for e in self.entries
                         if e.category == "brief_generation"]
        if len(brief_attempts) > 0 and not has_recent_brief_success:
            alerts.append({
                "severity": "high",
                "category": "brief_generation",
                "message": "No successful brief generation in last 3 days",
                "value": 0,
            })

        return alerts

    def archive_old_entries(self, days: int = RETENTION_DAYS) -> Dict[str, int]:
        """Archive entries older than specified days.

        Args:
            days: Number of days to retain (default: 90)

        Returns:
            Dictionary with counts of archived and retained entries
        """
        cutoff = datetime.now() - timedelta(days=days)

        archived_entries = []
        retained_entries = []

        for entry in self.entries:
            try:
                ts = datetime.fromisoformat(entry.timestamp)
                if ts < cutoff:
                    archived_entries.append(entry)
                else:
                    retained_entries.append(entry)
            except ValueError:
                # Keep entries with invalid timestamps
                retained_entries.append(entry)

        if archived_entries:
            # Create archive directory
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

            # Save archived entries
            archive_file = ARCHIVE_DIR / f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(archive_file, 'w') as f:
                json.dump({
                    "archived_at": datetime.now().isoformat(),
                    "cutoff_date": cutoff.isoformat(),
                    "retention_days": days,
                    "entry_count": len(archived_entries),
                    "entries": [e.to_dict() for e in archived_entries]
                }, f, indent=2)

            # Update current entries to only retained ones
            self.entries = retained_entries
            self._save_entries()

            print(f"[ARCHIVE] Archived {len(archived_entries)} entries to {archive_file}")
            print(f"[ARCHIVE] Retained {len(retained_entries)} recent entries")
        else:
            print(f"[ARCHIVE] No entries older than {days} days found")

        return {
            "archived": len(archived_entries),
            "retained": len(retained_entries),
            "archive_file": str(archive_file) if archived_entries else None,
        }

    def trigger_hooks(self, event_type: str, data: Dict) -> List[Dict]:
        """Trigger external hook scripts based on events.

        Args:
            event_type: Type of event (e.g., 'critical_alert', 'low_success_rate')
            data: Event data to pass to hooks

        Returns:
            List of hook results
        """
        # Ensure hooks directory exists
        HOOKS_DIR.mkdir(parents=True, exist_ok=True)

        results = []

        # Find hook scripts for this event type
        hook_pattern = f"{event_type}*.sh"
        hook_files = list(HOOKS_DIR.glob(hook_pattern))

        if not hook_files:
            self.log(f"No hooks found for event: {event_type}")
            return results

        for hook_file in hook_files:
            if not hook_file.is_file() or not os.access(hook_file, os.X_OK):
                self.log(f"Hook not executable: {hook_file}")
                continue

            try:
                # Pass data as JSON via stdin
                proc = subprocess.run(
                    [str(hook_file)],
                    input=json.dumps(data),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                results.append({
                    "hook": hook_file.name,
                    "exit_code": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                })

                self.log(f"Hook {hook_file.name} executed: exit code {proc.returncode}")

            except subprocess.TimeoutExpired:
                results.append({
                    "hook": hook_file.name,
                    "exit_code": -1,
                    "error": "Timeout after 30 seconds",
                })
                self.log(f"Hook {hook_file.name} timed out")
            except Exception as e:
                results.append({
                    "hook": hook_file.name,
                    "exit_code": -1,
                    "error": str(e),
                })
                self.log(f"Hook {hook_file.name} failed: {e}")

        return results

    def print_stats(self, days: int = 30):
        """Print formatted statistics."""
        stats = self.get_stats(days)

        print("=" * 60)
        print(f"PROMPT MONITOR STATISTICS (Last {days} days)")
        print("=" * 60)

        print(f"\nTotal entries: {stats['total_entries']}")
        print(f"Overall success rate: {stats['success_rate']}%")
        if stats['avg_duration_ms']:
            print(f"Avg duration: {stats['avg_duration_ms']}ms")

        if stats['by_status']:
            print("\nBy Status:")
            for status, count in sorted(stats['by_status'].items()):
                icon = {"success": "✅", "failure": "❌", "partial": "⚠️", "skipped": "⏭️"}.get(status, "•")
                print(f"  {icon} {status}: {count}")

        if stats['by_category']:
            print("\nBy Category:")
            for category, cat_stats in sorted(stats['by_category'].items()):
                total = cat_stats['total']
                rate = round(cat_stats['success'] / total * 100) if total > 0 else 0
                print(f"  {category}: {total} uses ({rate}% success)")

        if stats['recent_failures']:
            print("\nRecent Failures:")
            for failure in stats['recent_failures'][:5]:
                print(f"  - {failure['command'][:40]}: {failure['error'][:50]}")

        print("=" * 60)

    def print_trends(self, days: int = 30):
        """Print trend analysis."""
        trends = self.get_trends(days)

        print("=" * 60)
        print(f"TREND ANALYSIS (Last {days} days)")
        print("=" * 60)

        if trends["improving"]:
            print("\n✅ IMPROVING:")
            for item in trends["improving"]:
                print(f"  {item['category']}: {item['success_rate']}% success ({item['total_uses']} uses)")

        if trends["stable"]:
            print("\n➡️ STABLE:")
            for item in trends["stable"]:
                print(f"  {item['category']}: {item['success_rate']}% success ({item['total_uses']} uses)")

        if trends["problematic"]:
            print("\n⚠️ NEEDS ATTENTION:")
            for item in trends["problematic"]:
                print(f"  {item['category']}: {item['success_rate']}% (expected {item['expected_rate']}%)")

        if trends["underused"]:
            print("\n📭 UNDERUSED:")
            for item in trends["underused"]:
                print(f"  {item['category']}: {item['description']}")

        print("=" * 60)

    def print_recommendations(self):
        """Print recommendations."""
        recommendations = self.get_recommendations()

        print("=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)

        if not recommendations:
            print("\n✅ No issues detected - system performing well!")
        else:
            for rec in recommendations:
                priority_icon = {"critical": "🔴🔴", "high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec["priority"], "⚪")
                print(f"\n{priority_icon} [{rec['priority'].upper()}] {rec['category']}")
                print(f"   Issue: {rec['issue']}")
                print(f"   Action: {rec['recommendation']}")

        print("\n" + "=" * 60)

    def print_alerts(self) -> int:
        """Print alerts and return exit code based on severity.

        Returns:
            Exit code: 0 if no alerts, 1 if warnings, 2 if critical alerts
        """
        alerts = self.check_alerts()

        print("=" * 60)
        print("ALERT STATUS CHECK")
        print("=" * 60)

        if not alerts:
            print("\n✅ No alerts - system operating normally")
            print("=" * 60)
            return 0

        # Categorize alerts
        critical = [a for a in alerts if a["severity"] == "critical"]
        high = [a for a in alerts if a["severity"] == "high"]
        medium = [a for a in alerts if a["severity"] == "medium"]

        exit_code = 0

        if critical:
            exit_code = 2
            print(f"\n🔴 CRITICAL ALERTS ({len(critical)}):")
            for alert in critical:
                print(f"  [{alert['category']}] {alert['message']}")
                # Trigger critical alert hooks
                self.trigger_hooks("critical_alert", alert)

        if high:
            exit_code = max(exit_code, 1)
            print(f"\n⚠️  HIGH PRIORITY ALERTS ({len(high)}):")
            for alert in high:
                print(f"  [{alert['category']}] {alert['message']}")
                # Trigger high priority hooks
                self.trigger_hooks("high_alert", alert)

        if medium:
            print(f"\n🟡 MEDIUM PRIORITY ALERTS ({len(medium)}):")
            for alert in medium:
                print(f"  [{alert['category']}] {alert['message']}")

        print("\n" + "=" * 60)
        print(f"Exit code: {exit_code} (0=OK, 1=Warning, 2=Critical)")
        print("=" * 60)

        return exit_code


def main():
    parser = argparse.ArgumentParser(
        description="Chat prompt monitoring for TopEndSports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log command usage")
    log_parser.add_argument("--cmd", "-c", required=True, dest="cmd_name", help="Command name")
    log_parser.add_argument("--status", "-s", required=True,
                           choices=["success", "failure", "partial", "skipped"])
    log_parser.add_argument("--context", default="", help="Additional context")
    log_parser.add_argument("--duration", type=int, help="Duration in milliseconds")
    log_parser.add_argument("--error", default="", help="Error message if failed")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument("--days", type=int, default=30, help="Number of days")

    # Trends command
    trends_parser = subparsers.add_parser("trends", help="Analyze trends")
    trends_parser.add_argument("--days", type=int, default=30, help="Number of days")

    # Recommendations command
    rec_parser = subparsers.add_parser("recommendations", help="Get recommendations")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export usage data to CSV")
    export_parser.add_argument("--output", "-o", required=True, help="Output CSV file path")
    export_parser.add_argument("--days", type=int, help="Number of days to export (default: all)")

    # Alerts command
    alerts_parser = subparsers.add_parser("alerts", help="Check for critical issues")

    # Archive command
    archive_parser = subparsers.add_parser("archive", help="Archive old entries")
    archive_parser.add_argument("--days", type=int, default=90,
                               help="Archive entries older than N days (default: 90)")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear old entries")
    clear_parser.add_argument("--days", type=int, default=60, help="Keep entries from last N days")

    # Common arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    monitor = PromptMonitor(verbose=args.verbose)

    if args.command == "log":
        monitor.log_usage(
            command=args.cmd_name,
            status=args.status,
            context=args.context,
            duration_ms=args.duration,
            error_message=args.error,
        )

    elif args.command == "stats":
        monitor.print_stats(days=args.days)

    elif args.command == "trends":
        monitor.print_trends(days=args.days)

    elif args.command == "recommendations":
        monitor.print_recommendations()

    elif args.command == "export":
        count = monitor.export_to_csv(args.output, days=args.days)
        if count > 0:
            print(f"[OK] Successfully exported {count} entries")
            return 0
        else:
            print("[ERROR] No entries to export")
            return 1

    elif args.command == "alerts":
        exit_code = monitor.print_alerts()
        return exit_code

    elif args.command == "archive":
        result = monitor.archive_old_entries(days=args.days)
        if result["archived"] > 0:
            print(f"[OK] Successfully archived {result['archived']} entries")
        return 0  # No error if nothing to archive

    elif args.command == "clear":
        cutoff = datetime.now() - timedelta(days=args.days)
        before_count = len(monitor.entries)
        kept_entries = []
        skipped_count = 0

        for e in monitor.entries:
            try:
                if datetime.fromisoformat(e.timestamp) > cutoff:
                    kept_entries.append(e)
            except (ValueError, AttributeError) as err:
                # Keep entries with invalid timestamps
                kept_entries.append(e)
                skipped_count += 1

        monitor.entries = kept_entries
        monitor._save_entries()

        cleared_count = before_count - len(monitor.entries)
        print(f"[OK] Cleared {cleared_count} entries older than {args.days} days")
        if skipped_count > 0:
            print(f"[WARN] Kept {skipped_count} entries with invalid timestamps")

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
