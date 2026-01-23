"""
Pytest plugin for automatic error tracking.

This plugin automatically logs test failures to the error tracker,
enabling the self-learning mechanism to detect patterns and generate lessons.

Usage:
    pytest --error-tracking  # Enable error tracking
    pytest --error-tracking --verbose-tracking  # With detailed output
"""

import os
import sys
import pytest
from pathlib import Path

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))

# Import error tracker (lazy import to avoid issues if not available)
error_tracker = None


def get_tracker():
    """Lazily import and create error tracker."""
    global error_tracker
    if error_tracker is None:
        try:
            from error_tracker import ErrorTracker
            error_tracker = ErrorTracker(verbose=False)
        except ImportError:
            return None
    return error_tracker


def pytest_addoption(parser):
    """Add pytest command line options."""
    parser.addoption(
        "--error-tracking",
        action="store_true",
        default=False,
        help="Enable automatic error tracking for test failures"
    )
    parser.addoption(
        "--verbose-tracking",
        action="store_true",
        default=False,
        help="Show verbose error tracking output"
    )


def pytest_configure(config):
    """Configure the plugin."""
    if config.getoption("--error-tracking"):
        config.pluginmanager.register(ErrorTrackingPlugin(config), "error_tracking")


class ErrorTrackingPlugin:
    """Pytest plugin for error tracking."""

    def __init__(self, config):
        self.config = config
        self.verbose = config.getoption("--verbose-tracking")
        self.tracker = get_tracker()
        self.failures = []
        self.errors = []

    def log(self, msg):
        """Print verbose message."""
        if self.verbose:
            print(f"[ERROR-TRACK] {msg}")

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_makereport(self, item, call):
        """Capture test results."""
        if call.when == "call" and call.excinfo is not None:
            # Test failed
            self.failures.append({
                "name": item.name,
                "nodeid": item.nodeid,
                "location": f"{item.fspath}:{item.location[1]}",
                "error": str(call.excinfo.value),
                "traceback": str(call.excinfo.getrepr()),
            })

    def pytest_sessionfinish(self, session, exitstatus):
        """Process failures at end of session."""
        if not self.tracker:
            self.log("Error tracker not available")
            return

        if not self.failures:
            self.log("No failures to track")
            return

        self.log(f"Tracking {len(self.failures)} test failures")

        for failure in self.failures:
            # Determine category from test name
            category = "test"
            test_name = failure["name"].lower()

            if "ahrefs" in test_name or "api" in test_name:
                category = "api"
            elif "validation" in test_name or "validate" in test_name:
                category = "validation"
            elif "file" in test_name or "docx" in test_name:
                category = "file"
            elif "html" in test_name or "schema" in test_name:
                category = "content"

            # Log to error tracker
            self.tracker.add_error(
                source=f"pytest:{failure['nodeid']}",
                error_message=failure["error"][:500],
                context=failure["location"],
                category=category,
                severity="high",
                stack_trace=failure["traceback"][:2000],
                metadata={
                    "test_name": failure["name"],
                    "file": str(failure["location"]),
                }
            )

        # Print summary
        print(f"\n[ERROR-TRACKING] Logged {len(self.failures)} test failures")

        # Check for patterns
        stats = self.tracker.get_stats()
        if stats.get("patterns_needing_attention", 0) > 0:
            print(f"[ERROR-TRACKING] {stats['patterns_needing_attention']} patterns need attention!")
            print("[ERROR-TRACKING] Run: python3 scripts/error_tracker.py generate-lessons")
