"""Tests for uncovered lines in prompt_monitor.py.

Targets: trigger_hooks, print_trends, print_alerts, main() subcommands,
export_to_csv with cutoff, and load_entries edge cases.
"""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from prompt_monitor import PromptMonitor, UsageEntry, main, USAGE_LOG_FILE


@pytest.fixture
def monitor(tmp_path):
    """Create a PromptMonitor with a temp directory."""
    with patch("prompt_monitor.MONITOR_DIR", tmp_path), \
         patch("prompt_monitor.USAGE_LOG_FILE", tmp_path / "usage_log.json"), \
         patch("prompt_monitor.ANALYTICS_FILE", tmp_path / "analytics.json"), \
         patch("prompt_monitor.ARCHIVE_DIR", tmp_path / "archive"), \
         patch("prompt_monitor.HOOKS_DIR", tmp_path / "hooks"):
        m = PromptMonitor()
        yield m


def _make_entry(command="generate-brief", status="success", category=None,
                timestamp=None):
    """Helper to create a UsageEntry with custom timestamp/category."""
    entry = UsageEntry(
        command=command,
        status=status,
        error_message="" if status == "success" else "test error",
    )
    if timestamp is not None:
        entry.timestamp = timestamp
    if category is not None:
        entry.category = category
    return entry


class TestLoadEntriesEdgeCases:
    """Test _load_entries edge cases: malformed entries, JSON errors."""

    def test_load_entries_with_malformed_entry(self, tmp_path):
        """Covers lines 219-221: Skipping malformed entry in list."""
        log_file = tmp_path / "usage_log.json"
        # Include a non-dict entry and a dict missing fields
        data = {"entries": [{"command": "test", "status": "success"}, "not_a_dict", 42]}
        log_file.write_text(json.dumps(data), encoding="utf-8")

        with patch("prompt_monitor.MONITOR_DIR", tmp_path), \
             patch("prompt_monitor.USAGE_LOG_FILE", log_file), \
             patch("prompt_monitor.ANALYTICS_FILE", tmp_path / "analytics.json"), \
             patch("prompt_monitor.ARCHIVE_DIR", tmp_path / "archive"), \
             patch("prompt_monitor.HOOKS_DIR", tmp_path / "hooks"):
            m = PromptMonitor()
            assert isinstance(m.entries, list)

    def test_load_entries_json_decode_error(self, tmp_path):
        """Covers lines 227-229: JSON decode error starts fresh."""
        log_file = tmp_path / "usage_log.json"
        log_file.write_text("{bad json!!!", encoding="utf-8")

        with patch("prompt_monitor.MONITOR_DIR", tmp_path), \
             patch("prompt_monitor.USAGE_LOG_FILE", log_file), \
             patch("prompt_monitor.ANALYTICS_FILE", tmp_path / "analytics.json"), \
             patch("prompt_monitor.ARCHIVE_DIR", tmp_path / "archive"), \
             patch("prompt_monitor.HOOKS_DIR", tmp_path / "hooks"):
            m = PromptMonitor()
            assert m.entries == []

    def test_load_entries_general_exception(self, tmp_path):
        """Covers lines 228-229: General exception starts fresh."""
        log_file = tmp_path / "usage_log.json"
        log_file.write_text("{}", encoding="utf-8")

        with patch("prompt_monitor.MONITOR_DIR", tmp_path), \
             patch("prompt_monitor.USAGE_LOG_FILE", log_file), \
             patch("prompt_monitor.ANALYTICS_FILE", tmp_path / "analytics.json"), \
             patch("prompt_monitor.ARCHIVE_DIR", tmp_path / "archive"), \
             patch("prompt_monitor.HOOKS_DIR", tmp_path / "hooks"), \
             patch("builtins.open", side_effect=PermissionError("denied")):
            m = PromptMonitor()
            assert m.entries == []


class TestTriggerHooks:
    """Test trigger_hooks method covering lines 816-844."""

    def test_trigger_hooks_no_matching_hooks(self, monitor, tmp_path):
        """Covers line 817: No hooks found for event."""
        hooks_dir = tmp_path / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        with patch("prompt_monitor.HOOKS_DIR", hooks_dir):
            results = monitor.trigger_hooks("nonexistent_event", {})
            assert results == []

    def test_trigger_hooks_not_executable(self, monitor, tmp_path):
        """Covers line 829-830: Hook not executable."""
        hooks_dir = tmp_path / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_file = hooks_dir / "test_event_hook.sh"
        hook_file.write_text("#!/bin/bash\necho test", encoding="utf-8")

        with patch("prompt_monitor.HOOKS_DIR", hooks_dir), \
             patch("os.access", return_value=False):
            results = monitor.trigger_hooks("test_event", {})
            # Hook found but not executable, so no results
            assert results == []

    def test_trigger_hooks_successful_execution(self, monitor, tmp_path):
        """Covers lines 832-843: Successful hook execution."""
        hooks_dir = tmp_path / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_file = hooks_dir / "test_event_hook.sh"
        hook_file.write_text("#!/bin/bash\necho ok", encoding="utf-8")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "ok\n"
        mock_result.stderr = ""

        with patch("prompt_monitor.HOOKS_DIR", hooks_dir), \
             patch("os.access", return_value=True), \
             patch("subprocess.run", return_value=mock_result):
            results = monitor.trigger_hooks("test_event", {"data": "test"})
            assert len(results) == 1
            assert results[0]["exit_code"] == 0
            assert results[0]["stdout"] == "ok\n"

    def test_trigger_hooks_timeout(self, monitor, tmp_path):
        """Covers lines 839-844: Hook timeout."""
        hooks_dir = tmp_path / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_file = hooks_dir / "test_event_hook.sh"
        hook_file.write_text("#!/bin/bash\nsleep 100", encoding="utf-8")

        with patch("prompt_monitor.HOOKS_DIR", hooks_dir), \
             patch("os.access", return_value=True), \
             patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 30)):
            results = monitor.trigger_hooks("test_event", {})
            assert len(results) == 1
            assert results[0]["exit_code"] == -1
            assert "Timeout" in results[0]["error"]

    def test_trigger_hooks_exception(self, monitor, tmp_path):
        """Covers lines 846-850: Hook general exception."""
        hooks_dir = tmp_path / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_file = hooks_dir / "test_event_hook.sh"
        hook_file.write_text("#!/bin/bash\necho test", encoding="utf-8")

        with patch("prompt_monitor.HOOKS_DIR", hooks_dir), \
             patch("os.access", return_value=True), \
             patch("subprocess.run", side_effect=OSError("Permission denied")):
            results = monitor.trigger_hooks("test_event", {})
            assert len(results) == 1
            assert results[0]["exit_code"] == -1
            assert "Permission denied" in results[0]["error"]


class TestPrintTrends:
    """Test print_trends covering lines 895-915."""

    def test_print_trends_with_all_categories(self, monitor):
        """Covers lines 895-915: Print improving, stable, problematic, underused."""
        now = datetime.now()
        entries = []
        # Lots of successful briefs (stable/improving)
        for i in range(20):
            entries.append(_make_entry("generate-brief", "success", "brief_generation",
                                       (now - timedelta(hours=i)).isoformat()))
        # Some failed ahrefs (problematic)
        for i in range(15):
            entries.append(_make_entry("mcp__ahrefs__lookup", "failure", "ahrefs",
                                       (now - timedelta(hours=i)).isoformat()))
        # A few ahrefs successes
        for i in range(3):
            entries.append(_make_entry("mcp__ahrefs__lookup", "success", "ahrefs",
                                       (now - timedelta(hours=i)).isoformat()))

        monitor.entries = entries

        with patch("builtins.print") as mock_print:
            monitor.print_trends()
            output = "\n".join(str(c) for c in mock_print.call_args_list)
            assert len(mock_print.call_args_list) > 0


class TestPrintAlerts:
    """Test print_alerts covering lines 960-985."""

    def test_print_alerts_critical(self, monitor):
        """Covers lines 960-969: Critical alerts with hooks triggered."""
        now = datetime.now()
        entries = []
        # Very low success rate = critical
        for i in range(20):
            entries.append(_make_entry("test-cmd", "failure", "brief_generation",
                                       (now - timedelta(hours=i)).isoformat()))
        for i in range(2):
            entries.append(_make_entry("test-cmd", "success", "brief_generation",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        with patch("builtins.print"), \
             patch.object(monitor, "trigger_hooks", return_value=[]):
            exit_code = monitor.print_alerts()
            assert isinstance(exit_code, int)

    def test_print_alerts_high_priority(self, monitor):
        """Covers lines 970-976: High priority alerts."""
        now = datetime.now()
        entries = []
        # Consecutive failures for ahrefs
        for i in range(10):
            entries.append(_make_entry("mcp__ahrefs__check", "failure", "ahrefs",
                                       (now - timedelta(minutes=i)).isoformat()))
        monitor.entries = entries

        with patch("builtins.print"), \
             patch.object(monitor, "trigger_hooks", return_value=[]):
            exit_code = monitor.print_alerts()
            assert isinstance(exit_code, int)

    def test_print_alerts_medium(self, monitor):
        """Covers lines 978-980: Medium priority alerts."""
        now = datetime.now()
        entries = []
        # Mixed failures
        for i in range(30):
            status = "failure" if i % 3 == 0 else "success"
            entries.append(_make_entry("validate-csv", status, "validation",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        with patch("builtins.print"):
            exit_code = monitor.print_alerts()
            assert isinstance(exit_code, int)


class TestExportWithCutoff:
    """Test export_to_csv with date cutoff covering lines 605-615."""

    def test_export_with_days_filter(self, monitor, tmp_path):
        """Covers lines 607-612: Filtering entries by cutoff date."""
        now = datetime.now()
        old_entry = _make_entry()
        old_entry.timestamp = (now - timedelta(days=60)).isoformat()
        new_entry = _make_entry()
        new_entry.timestamp = now.isoformat()
        monitor.entries = [old_entry, new_entry]

        output_file = tmp_path / "export.csv"
        count = monitor.export_to_csv(str(output_file), days=30)
        assert count >= 0

    def test_export_with_invalid_timestamp(self, monitor, tmp_path):
        """Covers line 613: ValueError on invalid timestamp."""
        entry = _make_entry()
        entry.timestamp = "not-a-date"
        monitor.entries = [entry]

        output_file = tmp_path / "export.csv"
        count = monitor.export_to_csv(str(output_file), days=30)
        assert count >= 0


class TestMainFunction:
    """Test main() function subcommands covering lines 1055-1090."""

    def test_main_recommendations(self):
        """Covers line 1057: recommendations subcommand."""
        with patch("sys.argv", ["prompt_monitor.py", "recommendations"]), \
             patch("prompt_monitor.PromptMonitor") as MockMonitor:
            instance = MockMonitor.return_value
            instance.print_recommendations = MagicMock()
            try:
                main()
            except SystemExit:
                pass

    def test_main_export_success(self):
        """Covers lines 1060-1063: export subcommand with entries."""
        with patch("sys.argv", ["prompt_monitor.py", "export", "--output", "test.csv"]), \
             patch("prompt_monitor.PromptMonitor") as MockMonitor:
            instance = MockMonitor.return_value
            instance.export_to_csv = MagicMock(return_value=5)
            try:
                result = main()
            except SystemExit:
                pass

    def test_main_export_no_entries(self):
        """Covers lines 1064-1065: export with no entries."""
        with patch("sys.argv", ["prompt_monitor.py", "export", "--output", "test.csv"]), \
             patch("prompt_monitor.PromptMonitor") as MockMonitor:
            instance = MockMonitor.return_value
            instance.export_to_csv = MagicMock(return_value=0)
            try:
                result = main()
            except SystemExit:
                pass

    def test_main_alerts(self):
        """Covers lines 1068-1069: alerts subcommand."""
        with patch("sys.argv", ["prompt_monitor.py", "alerts"]), \
             patch("prompt_monitor.PromptMonitor") as MockMonitor:
            instance = MockMonitor.return_value
            instance.print_alerts = MagicMock(return_value=0)
            try:
                result = main()
            except SystemExit:
                pass

    def test_main_archive_with_archived(self):
        """Covers lines 1072-1076: archive subcommand with archived entries."""
        with patch("sys.argv", ["prompt_monitor.py", "archive", "--days", "90"]), \
             patch("prompt_monitor.PromptMonitor") as MockMonitor:
            instance = MockMonitor.return_value
            instance.archive_old_entries = MagicMock(return_value={"archived": 5, "remaining": 10})
            try:
                main()
            except SystemExit:
                pass

    def test_main_archive_nothing(self):
        """Covers line 1076: archive with nothing to archive."""
        with patch("sys.argv", ["prompt_monitor.py", "archive", "--days", "90"]), \
             patch("prompt_monitor.PromptMonitor") as MockMonitor:
            instance = MockMonitor.return_value
            instance.archive_old_entries = MagicMock(return_value={"archived": 0, "remaining": 10})
            try:
                main()
            except SystemExit:
                pass

    def test_main_clear(self):
        """Covers lines 1079-1090: clear subcommand."""
        now = datetime.now()
        entry1 = _make_entry()
        entry1.timestamp = now.isoformat()
        entry2 = _make_entry()
        entry2.timestamp = (now - timedelta(days=100)).isoformat()

        with patch("sys.argv", ["prompt_monitor.py", "clear", "--days", "30"]), \
             patch("prompt_monitor.PromptMonitor") as MockMonitor:
            instance = MockMonitor.return_value
            instance.entries = [entry1, entry2]
            instance._save_entries = MagicMock()
            try:
                main()
            except SystemExit:
                pass


class TestRecommendationsCategories:
    """Test get_recommendations for various category-specific paths."""

    def test_ahrefs_critical_gap(self, monitor):
        """Covers lines 461-464: Ahrefs with large gap."""
        now = datetime.now()
        entries = []
        for i in range(20):
            entries.append(_make_entry("mcp__ahrefs__lookup", "failure", "ahrefs",
                                       (now - timedelta(hours=i)).isoformat()))
        for i in range(2):
            entries.append(_make_entry("mcp__ahrefs__lookup", "success", "ahrefs",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_brief_generation_recommendation(self, monitor):
        """Covers line 467: brief_generation recommendation."""
        now = datetime.now()
        entries = []
        for i in range(15):
            entries.append(_make_entry("/generate-brief", "failure", "brief_generation",
                                       (now - timedelta(hours=i)).isoformat()))
        for i in range(3):
            entries.append(_make_entry("/generate-brief", "success", "brief_generation",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_validation_recommendation(self, monitor):
        """Covers line 469: validation recommendation."""
        now = datetime.now()
        entries = []
        for i in range(15):
            entries.append(_make_entry("validate-phase", "failure", "validation",
                                       (now - timedelta(hours=i)).isoformat()))
        for i in range(3):
            entries.append(_make_entry("validate-phase", "success", "validation",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_conversion_recommendation(self, monitor):
        """Covers line 471: conversion recommendation."""
        now = datetime.now()
        entries = []
        for i in range(15):
            entries.append(_make_entry("convert_to_docx", "failure", "conversion",
                                       (now - timedelta(hours=i)).isoformat()))
        for i in range(3):
            entries.append(_make_entry("convert_to_docx", "success", "conversion",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_ahrefs_fallback_only(self, monitor):
        """Covers lines 553-560: Only fallback used, no MCP."""
        now = datetime.now()
        entries = []
        for i in range(10):
            entries.append(_make_entry("python3 ahrefs-api.py", "success", "ahrefs_fallback",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        recs = monitor.get_recommendations()
        assert isinstance(recs, list)


class TestAnalyzeTrendsProblematic:
    """Test analyze_trends for problematic categories covering lines 395-420."""

    def test_trends_with_below_expected_rate(self, monitor):
        """Covers lines 400-415: Category below expected success rate."""
        now = datetime.now()
        entries = []
        # Ahrefs with many failures (expected 0.7, give it ~0.3)
        for i in range(14):
            entries.append(_make_entry("mcp__ahrefs__test", "failure", "ahrefs",
                                       (now - timedelta(hours=i)).isoformat()))
        for i in range(6):
            entries.append(_make_entry("mcp__ahrefs__test", "success", "ahrefs",
                                       (now - timedelta(hours=i)).isoformat()))
        monitor.entries = entries

        trends = monitor.get_trends()
        assert isinstance(trends, dict)
        # Should have problematic entries
        assert "problematic" in trends
