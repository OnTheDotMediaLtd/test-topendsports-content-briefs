#!/usr/bin/env python3
"""
Error Threshold Checker for CI/CD

Checks error patterns against defined thresholds and fails the build if exceeded.
Used in automated testing to catch degrading quality trends.

Thresholds:
    - Critical errors: 0 allowed
    - Recurring patterns (5+ occurrences): Warn at 3, fail at 5
    - Error surge (50%+ increase in 7 days): Warn
    - Patterns needing attention: Warn at 3, fail at 10

Exit codes:
    0 - All checks passed
    1 - Warnings detected (non-blocking)
    2 - Thresholds exceeded (blocking)
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Tuple

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ERROR_LOG_DIR = PROJECT_ROOT / "logs" / "errors"
PATTERNS_FILE = ERROR_LOG_DIR / "patterns.json"

# Thresholds
THRESHOLDS = {
    "critical_errors_max": 0,          # No critical errors allowed
    "recurring_patterns_warn": 3,      # Warn if 3+ patterns with 5+ occurrences
    "recurring_patterns_fail": 5,      # Fail if 5+ patterns with 5+ occurrences
    "patterns_needing_attention_warn": 3,
    "patterns_needing_attention_fail": 10,
    "error_surge_threshold": 0.5,      # 50% increase in 7 days
}


def load_patterns() -> Dict:
    """Load patterns from file."""
    if not PATTERNS_FILE.exists():
        return {}

    try:
        with open(PATTERNS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"[ERROR] Could not load patterns: {e}")
        return {}


def check_critical_errors(patterns: Dict) -> Tuple[bool, str]:
    """Check for critical errors."""
    critical_count = sum(
        1 for p in patterns.values()
        if p.get("severity") == "critical"
    )

    if critical_count > THRESHOLDS["critical_errors_max"]:
        return False, f"FAIL: {critical_count} critical error patterns detected (max: {THRESHOLDS['critical_errors_max']})"

    return True, f"PASS: {critical_count} critical errors (max: {THRESHOLDS['critical_errors_max']})"


def check_recurring_patterns(patterns: Dict) -> Tuple[bool, int, str]:
    """Check for recurring error patterns."""
    recurring = [
        p for p in patterns.values()
        if p.get("count", 0) >= 5
    ]

    count = len(recurring)

    if count >= THRESHOLDS["recurring_patterns_fail"]:
        return False, count, f"FAIL: {count} recurring patterns (threshold: {THRESHOLDS['recurring_patterns_fail']})"
    elif count >= THRESHOLDS["recurring_patterns_warn"]:
        return True, count, f"WARN: {count} recurring patterns (warning threshold: {THRESHOLDS['recurring_patterns_warn']})"
    else:
        return True, count, f"PASS: {count} recurring patterns"


def check_patterns_needing_attention(patterns: Dict) -> Tuple[bool, int, str]:
    """Check for patterns that need attention but haven't generated lessons."""
    needing_attention = [
        p for p in patterns.values()
        if p.get("count", 0) >= 3 and not p.get("lesson_generated", False)
    ]

    count = len(needing_attention)

    if count >= THRESHOLDS["patterns_needing_attention_fail"]:
        return False, count, f"FAIL: {count} patterns need attention (threshold: {THRESHOLDS['patterns_needing_attention_fail']})"
    elif count >= THRESHOLDS["patterns_needing_attention_warn"]:
        return True, count, f"WARN: {count} patterns need attention (warning threshold: {THRESHOLDS['patterns_needing_attention_warn']})"
    else:
        return True, count, f"PASS: {count} patterns need attention"


def check_error_surge(patterns: Dict) -> Tuple[bool, str]:
    """Check for recent surge in errors."""
    now = datetime.now()
    week_ago = now - timedelta(days=7)

    surges = []
    for fingerprint, pattern in patterns.items():
        occurrences = pattern.get("occurrences", [])
        if not occurrences:
            continue

        # Count recent vs total
        recent_count = sum(
            1 for occ in occurrences
            if datetime.fromisoformat(occ["timestamp"]) > week_ago
        )
        total_count = pattern.get("count", 0)

        if total_count > 2 and recent_count > total_count * THRESHOLDS["error_surge_threshold"]:
            surges.append({
                "fingerprint": fingerprint,
                "message": pattern.get("sample_message", "")[:50],
                "recent": recent_count,
                "total": total_count,
                "percentage": (recent_count / total_count * 100) if total_count > 0 else 0
            })

    if surges:
        msg = f"WARN: {len(surges)} error patterns showing recent surge:\n"
        for surge in surges[:5]:  # Show top 5
            msg += f"  - {surge['message']}: {surge['recent']}/{surge['total']} ({surge['percentage']:.1f}%)\n"
        return True, msg.strip()

    return True, "PASS: No error surges detected"


def check_category_distribution(patterns: Dict) -> str:
    """Show error distribution by category."""
    categories = {}
    for pattern in patterns.values():
        cat = pattern.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + pattern.get("count", 0)

    if not categories:
        return "INFO: No error patterns"

    msg = "INFO: Error distribution by category:\n"
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        msg += f"  - {cat}: {count} errors\n"

    return msg.strip()


def main():
    print("=" * 70)
    print("ERROR THRESHOLD CHECK")
    print("=" * 70)

    patterns = load_patterns()

    if not patterns:
        print("\n[INFO] No error patterns found - all checks passed")
        print("=" * 70)
        return 0

    print(f"\n[INFO] Analyzing {len(patterns)} error patterns...\n")

    has_warnings = False
    has_failures = False

    # Check 1: Critical errors
    passed, msg = check_critical_errors(patterns)
    print(f"[CHECK 1] Critical Errors: {msg}")
    if not passed:
        has_failures = True

    # Check 2: Recurring patterns
    passed, count, msg = check_recurring_patterns(patterns)
    print(f"[CHECK 2] Recurring Patterns: {msg}")
    if not passed:
        has_failures = True
    elif "WARN" in msg:
        has_warnings = True

    # Check 3: Patterns needing attention
    passed, count, msg = check_patterns_needing_attention(patterns)
    print(f"[CHECK 3] Patterns Needing Attention: {msg}")
    if not passed:
        has_failures = True
    elif "WARN" in msg:
        has_warnings = True
        print(f"           Run: python3 scripts/error_tracker.py generate-lessons")

    # Check 4: Error surges
    passed, msg = check_error_surge(patterns)
    print(f"[CHECK 4] Recent Error Surge: {msg}")
    if "WARN" in msg:
        has_warnings = True

    # Distribution info
    print(f"\n{check_category_distribution(patterns)}")

    print("\n" + "=" * 70)

    if has_failures:
        print("[RESULT] FAILED - Error thresholds exceeded!")
        print("=" * 70)
        return 2
    elif has_warnings:
        print("[RESULT] PASSED WITH WARNINGS - Monitor error patterns")
        print("=" * 70)
        return 1
    else:
        print("[RESULT] PASSED - All thresholds met")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    sys.exit(main())
