"""
Expanded tests for prompt_monitor.py to increase coverage.
Targets: CLI functions, print methods, edge cases, validation.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))

from prompt_monitor import (
    UsageEntry, PromptMonitor, KNOWN_COMMANDS,
    ALERT_THRESHOLDS, RETENTION_DAYS, main
)


class TestUsageEntryAdvanced:
    """Advanced tests for UsageEntry class."""

    def test_usage_entry_with_metadata(self):
        """Test usage entry with complex metadata."""
        metadata = {
            "keywords": ["nfl", "betting"],
            "phase": 2,
            "retry_count": 3,
            "nested": {"key": "value"}
        }
        entry = UsageEntry(
            command="/generate-brief",
            status="success",
            metadata=metadata
        )
        assert entry.metadata == metadata
        assert entry.metadata["keywords"] == ["nfl", "betting"]

    def test_usage_entry_duration_tracking(self):
        """Test duration tracking in usage entry."""
        entry = UsageEntry(
            command="/generate-brief",
            status="success",
            duration_ms=12500
        )
        assert entry.duration_ms == 12500

    def test_usage_entry_error_message(self):
        """Test error message in failure entry."""
        entry = UsageEntry(
            command="mcp__ahrefs__keywords",
            status="failure",
            error_message="HTTP 403: Forbidden - API key invalid"
        )
        assert "403" in entry.error_message
        assert entry.status == "failure"

    def test_category_detection_phase_execution(self):
        """Test category detection for phase execution."""
        entry = UsageEntry(command="execute-phase-2 test-page", status="success")
        assert entry.category == "phase_execution"

    def test_category_detection_keyword_research(self):
        """Test category detection for keyword research."""
        entry = UsageEntry(command="get keyword data from ahrefs", status="success")
        assert entry.category == "keyword_research"

    def test_category_detection_check_command(self):
        """Test category detection for check command."""
        entry = UsageEntry(command="check-content-quality", status="success")
        assert entry.category == "validation"

    def test_from_dict_with_missing_fields(self):
        """Test from_dict handles missing optional fields."""
        data = {
            "command": "test",
            "status": "success"
        }
        entry = UsageEntry.from_dict(data)
        assert entry.command == "test"
        assert entry.status == "success"
        assert entry.context == ""
        assert entry.duration_ms is None


class TestPromptMonitorValidation:
    """Tests for input validation in PromptMonitor."""

    @pytest.fixture
    def temp_monitor(self, tmp_path, monkeypatch):
        """Create a monitor with temp directories."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ANALYTICS_FILE', monitor_dir / "analytics.json")
        monkeypatch.setattr(pm, 'ARCHIVE_DIR', monitor_dir / "archive")
        monkeypatch.setattr(pm, 'HOOKS_DIR', monitor_dir / "hooks")

        monitor = PromptMonitor(verbose=False)
        return monitor

    def test_log_usage_empty_command_raises(self, temp_monitor):
        """Test that empty command raises ValueError."""
        with pytest.raises(ValueError, match="command must be a non-empty string"):
            temp_monitor.log_usage(command="", status="success")

    def test_log_usage_none_command_raises(self, temp_monitor):
        """Test that None command raises ValueError."""
        with pytest.raises(ValueError, match="command must be a non-empty string"):
            temp_monitor.log_usage(command=None, status="success")

    def test_log_usage_empty_status_raises(self, temp_monitor):
        """Test that empty status raises ValueError."""
        with pytest.raises(ValueError, match="status must be a non-empty string"):
            temp_monitor.log_usage(command="test", status="")

    def test_log_usage_invalid_status_raises(self, temp_monitor):
        """Test that invalid status raises ValueError."""
        with pytest.raises(ValueError, match="status must be one of"):
            temp_monitor.log_usage(command="test", status="invalid")

    def test_log_usage_negative_duration_raises(self, temp_monitor):
        """Test that negative duration raises ValueError."""
        with pytest.raises(ValueError, match="duration_ms must be a non-negative integer"):
            temp_monitor.log_usage(command="test", status="success", duration_ms=-100)

    def test_log_usage_float_duration_raises(self, temp_monitor):
        """Test that float duration raises ValueError."""
        with pytest.raises(ValueError, match="duration_ms must be a non-negative integer"):
            temp_monitor.log_usage(command="test", status="success", duration_ms=100.5)

    def test_log_usage_truncates_long_command(self, temp_monitor):
        """Test that overly long commands are truncated."""
        long_command = "x" * 2000
        entry = temp_monitor.log_usage(command=long_command, status="success")
        assert len(entry.command) == 1000

    def test_log_usage_truncates_long_context(self, temp_monitor):
        """Test that overly long context is truncated."""
        long_context = "x" * 2000
        entry = temp_monitor.log_usage(command="test", status="success", context=long_context)
        assert len(entry.context) == 1000

    def test_log_usage_truncates_long_error(self, temp_monitor):
        """Test that overly long error messages are truncated."""
        long_error = "x" * 3000
        entry = temp_monitor.log_usage(command="test", status="failure", error_message=long_error)
        assert len(entry.error_message) == 2000


class TestPromptMonitorEntryLimits:
    """Tests for entry limit enforcement."""

    @pytest.fixture
    def temp_monitor(self, tmp_path, monkeypatch):
        """Create a monitor with temp directories."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ANALYTICS_FILE', monitor_dir / "analytics.json")

        monitor = PromptMonitor(verbose=True)  # Enable verbose for coverage
        return monitor

    def test_entry_limit_enforcement(self, temp_monitor):
        """Test that entries are limited to prevent unbounded growth."""
        # Add more than 5000 entries
        temp_monitor.entries = [
            UsageEntry(command=f"cmd_{i}", status="success")
            for i in range(5100)
        ]
        temp_monitor._save_entries()

        # Add one more entry - should trigger cleanup
        temp_monitor.log_usage(command="new_cmd", status="success")

        # Should be capped at 5000
        assert len(temp_monitor.entries) <= 5001


class TestPromptMonitorLoadErrors:
    """Tests for error handling when loading entries."""

    def test_load_empty_file(self, tmp_path, monkeypatch):
        """Test loading from empty usage log file."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        usage_log = monitor_dir / "usage_log.json"
        usage_log.write_text("")

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', usage_log)

        monitor = PromptMonitor(verbose=True)
        assert monitor.entries == []

    def test_load_invalid_json(self, tmp_path, monkeypatch):
        """Test loading from invalid JSON file."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        usage_log = monitor_dir / "usage_log.json"
        usage_log.write_text("not valid json {{{")

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', usage_log)

        monitor = PromptMonitor(verbose=True)
        assert monitor.entries == []

    def test_load_invalid_data_structure(self, tmp_path, monkeypatch):
        """Test loading from JSON with invalid structure."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        usage_log = monitor_dir / "usage_log.json"
        usage_log.write_text('["not", "a", "dict"]')

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', usage_log)

        monitor = PromptMonitor(verbose=True)
        assert monitor.entries == []

    def test_load_invalid_entries_list(self, tmp_path, monkeypatch):
        """Test loading from JSON with invalid entries list."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        usage_log = monitor_dir / "usage_log.json"
        usage_log.write_text('{"entries": "not a list"}')

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', usage_log)

        monitor = PromptMonitor(verbose=True)
        assert monitor.entries == []

    def test_load_with_malformed_entry(self, tmp_path, monkeypatch):
        """Test loading skips malformed entries."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        usage_log = monitor_dir / "usage_log.json"
        usage_log.write_text(json.dumps({
            "entries": [
                {"command": "good", "status": "success"},
                "malformed string entry",
                {"command": "also_good", "status": "failure"}
            ]
        }))

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', usage_log)

        monitor = PromptMonitor(verbose=True)
        assert len(monitor.entries) == 2


class TestPromptMonitorGetStatsAdvanced:
    """Advanced tests for get_stats method."""

    @pytest.fixture
    def monitor_with_data(self, tmp_path, monkeypatch):
        """Create a monitor with varied sample data."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)

        # Add entries with specific timestamps
        for i in range(20):
            entry = UsageEntry(
                command=f"/generate-brief-{i}",
                status="success" if i % 3 else "failure",
                duration_ms=1000 + i * 100
            )
            monitor.entries.append(entry)

        return monitor

    def test_stats_filters_by_date(self, monitor_with_data):
        """Test that stats correctly filters by date cutoff."""
        # Add an old entry
        old_entry = UsageEntry(command="old", status="success")
        old_entry.timestamp = (datetime.now() - timedelta(days=60)).isoformat()
        monitor_with_data.entries.append(old_entry)

        stats = monitor_with_data.get_stats(days=30)
        # Should not include the old entry
        assert stats["total_entries"] == 20

    def test_stats_handles_invalid_timestamps(self, monitor_with_data):
        """Test that stats skips entries with invalid timestamps."""
        bad_entry = UsageEntry(command="bad", status="success")
        bad_entry.timestamp = "not-a-valid-timestamp"
        monitor_with_data.entries.append(bad_entry)

        stats = monitor_with_data.get_stats(days=30)
        # Should skip the invalid entry
        assert stats["total_entries"] == 20

    def test_stats_command_truncation(self, monitor_with_data):
        """Test that long commands are truncated in stats."""
        long_cmd_entry = UsageEntry(
            command="x" * 100,
            status="success"
        )
        monitor_with_data.entries.append(long_cmd_entry)

        stats = monitor_with_data.get_stats(days=30)
        # Check that truncated command key exists
        cmd_keys = list(stats["by_command"].keys())
        assert all(len(k) <= 50 for k in cmd_keys)


class TestPromptMonitorTrendsAdvanced:
    """Advanced tests for get_trends method."""

    @pytest.fixture
    def temp_monitor(self, tmp_path, monkeypatch):
        """Create a monitor with temp directories."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        return PromptMonitor(verbose=False)

    def test_trends_empty_monitor(self, temp_monitor):
        """Test trends with no entries."""
        trends = temp_monitor.get_trends(days=30)
        assert trends["improving"] == []
        assert trends["declining"] == []
        assert trends["stable"] == []

    def test_trends_improving_category(self, temp_monitor):
        """Test detection of improving category."""
        # Add high success rate entries for ahrefs
        for _ in range(10):
            temp_monitor.log_usage(command="mcp__ahrefs__keywords", status="success")

        trends = temp_monitor.get_trends(days=30)
        # High success rate should be in improving
        improving_cats = [t["category"] for t in trends["improving"]]
        assert "ahrefs" in improving_cats


class TestPromptMonitorRecommendationsAdvanced:
    """Advanced tests for recommendations."""

    @pytest.fixture
    def temp_monitor(self, tmp_path, monkeypatch):
        """Create a monitor with temp directories."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        return PromptMonitor(verbose=False)

    def test_recommendations_for_validation_category(self, temp_monitor):
        """Test specific recommendations for validation failures."""
        for _ in range(10):
            temp_monitor.log_usage(command="validate-phase-1", status="failure")

        recommendations = temp_monitor.get_recommendations()
        validation_recs = [r for r in recommendations if r["category"] == "validation"]
        assert len(validation_recs) > 0
        assert "validation" in validation_recs[0]["recommendation"].lower()

    def test_recommendations_for_conversion_category(self, temp_monitor):
        """Test specific recommendations for conversion failures."""
        for _ in range(10):
            temp_monitor.log_usage(command="convert_to_docx", status="failure")

        recommendations = temp_monitor.get_recommendations()
        conversion_recs = [r for r in recommendations if r["category"] == "conversion"]
        assert len(conversion_recs) > 0

    def test_recommendations_performance_warning(self, temp_monitor):
        """Test performance recommendations for slow commands."""
        for _ in range(10):
            temp_monitor.log_usage(command="slow_cmd", status="success", duration_ms=50000)

        recommendations = temp_monitor.get_recommendations()
        perf_recs = [r for r in recommendations if r["category"] == "performance"]
        assert len(perf_recs) > 0

    def test_recommendations_repeated_error_pattern(self, temp_monitor):
        """Test detection of repeated error patterns."""
        for _ in range(5):
            temp_monitor.log_usage(
                command="test_cmd",
                status="failure",
                error_message="Connection timeout"
            )

        recommendations = temp_monitor.get_recommendations()
        error_recs = [r for r in recommendations if r["category"] == "errors"]
        assert len(error_recs) > 0

    def test_recommendations_python_fallback_only(self, temp_monitor):
        """Test recommendation when only Python fallback is used."""
        for _ in range(10):
            temp_monitor.log_usage(command="python3 ahrefs-api.py", status="success")

        recommendations = temp_monitor.get_recommendations()
        ahrefs_recs = [r for r in recommendations if r["category"] == "ahrefs"]
        assert len(ahrefs_recs) > 0
        assert "MCP" in ahrefs_recs[0]["recommendation"]


class TestPromptMonitorAlertsAdvanced:
    """Advanced tests for alerts feature."""

    @pytest.fixture
    def temp_monitor(self, tmp_path, monkeypatch):
        """Create a monitor with temp directories."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'HOOKS_DIR', monitor_dir / "hooks")

        return PromptMonitor(verbose=False)

    def test_alert_high_error_count(self, temp_monitor):
        """Test alert for high error count in last hour."""
        # Add many recent failures
        for _ in range(15):
            temp_monitor.log_usage(command="test", status="failure")

        alerts = temp_monitor.check_alerts()
        error_alerts = [a for a in alerts if a["category"] == "errors"]
        assert len(error_alerts) > 0

    def test_alert_no_brief_success(self, temp_monitor):
        """Test alert when no successful brief generation in 3 days."""
        # Add old brief attempt
        entry = UsageEntry(command="/generate-brief", status="failure")
        entry.timestamp = (datetime.now() - timedelta(days=4)).isoformat()
        temp_monitor.entries.append(entry)
        temp_monitor._save_entries()

        alerts = temp_monitor.check_alerts()
        brief_alerts = [a for a in alerts if a["category"] == "brief_generation"]
        assert len(brief_alerts) > 0


class TestPromptMonitorPrintMethods:
    """Tests for print/output methods."""

    @pytest.fixture
    def temp_monitor(self, tmp_path, monkeypatch):
        """Create a monitor with temp directories."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'HOOKS_DIR', monitor_dir / "hooks")

        return PromptMonitor(verbose=False)

    def test_print_stats(self, temp_monitor, capsys):
        """Test print_stats output."""
        temp_monitor.log_usage(command="test", status="success")
        temp_monitor.log_usage(command="test2", status="failure")

        temp_monitor.print_stats(days=30)

        captured = capsys.readouterr()
        assert "PROMPT MONITOR STATISTICS" in captured.out
        assert "success" in captured.out

    def test_print_trends(self, temp_monitor, capsys):
        """Test print_trends output."""
        temp_monitor.log_usage(command="test", status="success")

        temp_monitor.print_trends(days=30)

        captured = capsys.readouterr()
        assert "TREND ANALYSIS" in captured.out

    def test_print_recommendations(self, temp_monitor, capsys):
        """Test print_recommendations output."""
        # Empty monitor should show no issues
        temp_monitor.print_recommendations()

        captured = capsys.readouterr()
        assert "RECOMMENDATIONS" in captured.out

    def test_print_recommendations_with_issues(self, temp_monitor, capsys):
        """Test print_recommendations with issues."""
        for _ in range(20):
            temp_monitor.log_usage(command="test", status="failure")

        temp_monitor.print_recommendations()

        captured = capsys.readouterr()
        assert "CRITICAL" in captured.out or "HIGH" in captured.out

    def test_print_alerts_no_alerts(self, temp_monitor, capsys):
        """Test print_alerts when no alerts."""
        for _ in range(10):
            temp_monitor.log_usage(command="test", status="success")

        exit_code = temp_monitor.print_alerts()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No alerts" in captured.out

    def test_print_alerts_with_critical(self, temp_monitor, capsys):
        """Test print_alerts with critical alerts."""
        for _ in range(20):
            temp_monitor.log_usage(command="test", status="failure")

        exit_code = temp_monitor.print_alerts()

        assert exit_code == 2
        captured = capsys.readouterr()
        assert "CRITICAL" in captured.out


class TestPromptMonitorCLI:
    """Tests for CLI main function."""

    @pytest.fixture
    def temp_dirs(self, tmp_path, monkeypatch):
        """Set up temp directories for CLI tests."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ANALYTICS_FILE', monitor_dir / "analytics.json")
        monkeypatch.setattr(pm, 'ARCHIVE_DIR', monitor_dir / "archive")
        monkeypatch.setattr(pm, 'HOOKS_DIR', monitor_dir / "hooks")

        return tmp_path

    def test_main_no_args(self, temp_dirs, monkeypatch):
        """Test main with no arguments shows help."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py'])

        result = main()
        assert result == 1

    def test_main_log_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with log command."""
        monkeypatch.setattr('sys.argv', [
            'prompt_monitor.py', 'log',
            '--cmd', 'test_command',
            '--status', 'success',
            '--context', 'test context'
        ])

        result = main()
        assert result == 0 or result is None

        captured = capsys.readouterr()
        assert "[LOGGED]" in captured.out

    def test_main_log_with_duration(self, temp_dirs, monkeypatch, capsys):
        """Test main with log command including duration."""
        monkeypatch.setattr('sys.argv', [
            'prompt_monitor.py', 'log',
            '--cmd', 'test_command',
            '--status', 'success',
            '--duration', '5000'
        ])

        result = main()
        assert result == 0 or result is None

    def test_main_log_with_error(self, temp_dirs, monkeypatch, capsys):
        """Test main with log command for failure."""
        monkeypatch.setattr('sys.argv', [
            'prompt_monitor.py', 'log',
            '--cmd', 'test_command',
            '--status', 'failure',
            '--error', 'Test error message'
        ])

        result = main()
        assert result == 0 or result is None

    def test_main_stats_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with stats command."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'stats'])

        result = main()
        assert result == 0 or result is None

        captured = capsys.readouterr()
        assert "STATISTICS" in captured.out

    def test_main_stats_with_days(self, temp_dirs, monkeypatch, capsys):
        """Test main with stats command and custom days."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'stats', '--days', '7'])

        result = main()
        assert result == 0 or result is None

    def test_main_trends_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with trends command."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'trends'])

        result = main()
        assert result == 0 or result is None

        captured = capsys.readouterr()
        assert "TREND ANALYSIS" in captured.out

    def test_main_recommendations_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with recommendations command."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'recommendations'])

        result = main()
        assert result == 0 or result is None

        captured = capsys.readouterr()
        assert "RECOMMENDATIONS" in captured.out

    def test_main_export_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with export command."""
        output_file = temp_dirs / "export.csv"
        monkeypatch.setattr('sys.argv', [
            'prompt_monitor.py', 'export',
            '--output', str(output_file)
        ])

        result = main()
        # May be 0 or 1 depending on whether entries exist
        assert result in [0, 1]

    def test_main_alerts_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with alerts command."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'alerts'])

        result = main()
        # Exit code depends on alert status
        assert result in [0, 1, 2]

    def test_main_archive_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with archive command."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'archive'])

        result = main()
        assert result == 0

    def test_main_archive_with_days(self, temp_dirs, monkeypatch, capsys):
        """Test main with archive command and custom days."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'archive', '--days', '60'])

        result = main()
        assert result == 0

    def test_main_clear_command(self, temp_dirs, monkeypatch, capsys):
        """Test main with clear command."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', 'clear', '--days', '30'])

        result = main()
        assert result == 0 or result is None

        captured = capsys.readouterr()
        assert "Cleared" in captured.out

    def test_main_verbose_flag(self, temp_dirs, monkeypatch, capsys):
        """Test main with verbose flag."""
        monkeypatch.setattr('sys.argv', ['prompt_monitor.py', '-v', 'stats'])

        result = main()
        assert result == 0 or result is None


class TestKnownCommandsConfig:
    """Tests for KNOWN_COMMANDS configuration."""

    def test_known_commands_categories_not_empty(self):
        """Test that all categories are non-empty strings."""
        for pattern, config in KNOWN_COMMANDS.items():
            cat = config.get("category", "")
            assert cat, f"Empty category for {pattern}"
            assert isinstance(cat, str)

    def test_known_commands_success_rates_valid(self):
        """Test that success rates are valid floats between 0 and 1."""
        for pattern, config in KNOWN_COMMANDS.items():
            rate = config.get("expected_success_rate")
            assert rate is not None, f"Missing success rate for {pattern}"
            assert isinstance(rate, (int, float))
            assert 0 <= rate <= 1, f"Invalid rate {rate} for {pattern}"

    def test_known_commands_descriptions_meaningful(self):
        """Test that descriptions are meaningful."""
        for pattern, config in KNOWN_COMMANDS.items():
            desc = config.get("description", "")
            assert len(desc) >= 5, f"Description too short for {pattern}"


class TestAlertThresholds:
    """Tests for alert threshold constants."""

    def test_critical_success_rate_threshold(self):
        """Test critical success rate threshold is valid."""
        assert 0 < ALERT_THRESHOLDS["critical_success_rate"] < 100

    def test_category_failure_threshold(self):
        """Test category failure threshold is valid."""
        assert ALERT_THRESHOLDS["category_failure_threshold"] > 0

    def test_high_error_count_threshold(self):
        """Test high error count threshold is valid."""
        assert ALERT_THRESHOLDS["high_error_count"] > 0

    def test_ahrefs_failure_rate_threshold(self):
        """Test ahrefs failure rate threshold is valid."""
        assert 0 < ALERT_THRESHOLDS["ahrefs_failure_rate"] < 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
