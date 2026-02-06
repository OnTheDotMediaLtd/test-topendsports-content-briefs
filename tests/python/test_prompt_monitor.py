"""
Tests for the chat prompt monitoring system.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))

from prompt_monitor import UsageEntry, PromptMonitor, KNOWN_COMMANDS


class TestUsageEntry:
    """Tests for the UsageEntry class."""

    def test_create_usage_entry(self):
        """Test basic usage entry creation."""
        entry = UsageEntry(
            command="/generate-brief",
            status="success",
            context="NFL betting sites",
        )

        assert entry.command == "/generate-brief"
        assert entry.status == "success"
        assert entry.context == "NFL betting sites"
        assert entry.timestamp is not None

    def test_category_detection_brief_generation(self):
        """Test category detection for brief generation."""
        entry = UsageEntry(command="/generate-brief", status="success")
        assert entry.category == "brief_generation"

    def test_category_detection_ahrefs(self):
        """Test category detection for Ahrefs MCP."""
        entry = UsageEntry(command="mcp__ahrefs__keywords-explorer", status="success")
        assert entry.category == "ahrefs"

    def test_category_detection_ahrefs_fallback(self):
        """Test category detection for Ahrefs Python fallback."""
        entry = UsageEntry(command="python3 ahrefs-api.py keywords", status="success")
        assert entry.category == "ahrefs_fallback"

    def test_category_detection_validation(self):
        """Test category detection for validation."""
        entry = UsageEntry(command="validate-phase phase1", status="success")
        assert entry.category == "validation"

    def test_category_detection_conversion(self):
        """Test category detection for conversion."""
        entry = UsageEntry(command="convert_to_docx output.md", status="success")
        assert entry.category == "conversion"

    def test_category_detection_mcp_tool(self):
        """Test category detection for MCP tools."""
        entry = UsageEntry(command="mcp__topendsports-briefs__get_page_info", status="success")
        assert entry.category == "mcp_tool"

    def test_to_dict(self):
        """Test serialization to dictionary."""
        entry = UsageEntry(
            command="/generate-brief",
            status="success",
            context="test",
            duration_ms=5000,
            error_message="",
            metadata={"key": "value"},
        )

        data = entry.to_dict()

        assert data["command"] == "/generate-brief"
        assert data["status"] == "success"
        assert data["context"] == "test"
        assert data["duration_ms"] == 5000
        assert data["metadata"] == {"key": "value"}
        assert "timestamp" in data
        assert "category" in data

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "command": "/generate-brief",
            "status": "success",
            "context": "test",
            "duration_ms": 5000,
            "category": "brief_generation",
            "timestamp": "2025-12-01T10:00:00",
        }

        entry = UsageEntry.from_dict(data)

        assert entry.command == "/generate-brief"
        assert entry.status == "success"
        assert entry.duration_ms == 5000
        assert entry.timestamp == "2025-12-01T10:00:00"


class TestPromptMonitor:
    """Tests for the PromptMonitor class."""

    @pytest.fixture
    def temp_monitor(self, tmp_path, monkeypatch):
        """Create a monitor with temp directories."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ANALYTICS_FILE', monitor_dir / "analytics.json")

        monitor = PromptMonitor(verbose=False)
        return monitor

    def test_log_usage(self, temp_monitor):
        """Test logging a usage entry."""
        entry = temp_monitor.log_usage(
            command="/generate-brief",
            status="success",
            context="test",
        )

        assert entry is not None
        assert len(temp_monitor.entries) == 1
        assert temp_monitor.entries[0].command == "/generate-brief"

    def test_log_multiple_entries(self, temp_monitor):
        """Test logging multiple entries."""
        temp_monitor.log_usage(command="/generate-brief", status="success")
        temp_monitor.log_usage(command="mcp__ahrefs__keywords", status="failure")
        temp_monitor.log_usage(command="python3 ahrefs-api.py", status="success")

        assert len(temp_monitor.entries) == 3

    def test_get_stats_empty(self, temp_monitor):
        """Test stats with no entries."""
        stats = temp_monitor.get_stats(days=30)

        assert stats["total_entries"] == 0
        assert stats["success_rate"] == 0.0

    def test_get_stats_with_entries(self, temp_monitor):
        """Test stats with entries."""
        temp_monitor.log_usage(command="cmd1", status="success")
        temp_monitor.log_usage(command="cmd2", status="success")
        temp_monitor.log_usage(command="cmd3", status="failure")

        stats = temp_monitor.get_stats(days=30)

        assert stats["total_entries"] == 3
        assert stats["success_rate"] == 66.7

    def test_get_stats_by_category(self, temp_monitor):
        """Test stats grouped by category."""
        temp_monitor.log_usage(command="/generate-brief", status="success")
        temp_monitor.log_usage(command="mcp__ahrefs__keywords", status="failure")
        temp_monitor.log_usage(command="mcp__ahrefs__volume", status="success")

        stats = temp_monitor.get_stats(days=30)

        assert "brief_generation" in stats["by_category"]
        assert "ahrefs" in stats["by_category"]
        assert stats["by_category"]["ahrefs"]["total"] == 2
        assert stats["by_category"]["ahrefs"]["success"] == 1
        assert stats["by_category"]["ahrefs"]["failure"] == 1

    def test_get_trends(self, temp_monitor):
        """Test trend analysis."""
        # Add some entries with varying success rates
        for _ in range(5):
            temp_monitor.log_usage(command="mcp__ahrefs__keywords", status="failure")
        for _ in range(2):
            temp_monitor.log_usage(command="mcp__ahrefs__keywords", status="success")

        trends = temp_monitor.get_trends(days=30)

        # Ahrefs should be in problematic because success rate (2/7 = 28%) < expected 70%
        assert len(trends["problematic"]) >= 1
        problematic_categories = [p["category"] for p in trends["problematic"]]
        assert "ahrefs" in problematic_categories

    def test_get_recommendations(self, temp_monitor):
        """Test recommendation generation."""
        # Add failing entries to trigger recommendations
        for _ in range(5):
            temp_monitor.log_usage(command="mcp__ahrefs__keywords", status="failure")

        recommendations = temp_monitor.get_recommendations()

        # Should have at least one recommendation for problematic ahrefs
        assert len(recommendations) >= 1
        high_priority = [r for r in recommendations if r["priority"] == "high"]
        assert len(high_priority) >= 1

    def test_persistence(self, temp_monitor, tmp_path, monkeypatch):
        """Test that entries persist across instances."""
        import prompt_monitor as pm

        # Add some entries
        temp_monitor.log_usage(command="cmd1", status="success")
        temp_monitor.log_usage(command="cmd2", status="failure")

        # Create new monitor instance
        new_monitor = PromptMonitor(verbose=False)

        assert len(new_monitor.entries) == 2

    def test_duration_tracking(self, temp_monitor):
        """Test duration tracking in stats."""
        temp_monitor.log_usage(command="cmd1", status="success", duration_ms=1000)
        temp_monitor.log_usage(command="cmd2", status="success", duration_ms=2000)
        temp_monitor.log_usage(command="cmd3", status="success", duration_ms=3000)

        stats = temp_monitor.get_stats(days=30)

        assert stats["avg_duration_ms"] == 2000


class TestKnownCommands:
    """Tests for known commands configuration."""

    def test_all_commands_have_category(self):
        """Test that all known commands have a category."""
        for pattern, config in KNOWN_COMMANDS.items():
            assert "category" in config, f"Command {pattern} missing category"
            assert config["category"], f"Command {pattern} has empty category"

    def test_all_commands_have_expected_rate(self):
        """Test that all known commands have expected success rate."""
        for pattern, config in KNOWN_COMMANDS.items():
            assert "expected_success_rate" in config
            rate = config["expected_success_rate"]
            assert 0 <= rate <= 1, f"Invalid rate {rate} for {pattern}"

    def test_all_commands_have_description(self):
        """Test that all known commands have descriptions."""
        for pattern, config in KNOWN_COMMANDS.items():
            assert "description" in config
            assert len(config["description"]) > 5


class TestCategoryDetection:
    """Tests for command category detection."""

    @pytest.mark.parametrize("command,expected_category", [
        ("/generate-brief test-page", "brief_generation"),
        ("/submit-feedback keyword", "feedback"),
        ("mcp__topendsports-briefs__get_page_info", "mcp_tool"),
        ("mcp__ahrefs__keywords-explorer-overview", "ahrefs"),
        ("python3 ahrefs-api.py keywords-explorer/overview", "ahrefs_fallback"),
        ("validate-phase phase1 test-page", "validation"),
        ("convert_to_docx output/test.md", "conversion"),
        ("some unknown command", "other"),
    ])
    def test_category_detection(self, command, expected_category):
        """Test various commands are categorized correctly."""
        entry = UsageEntry(command=command, status="success")
        assert entry.category == expected_category


class TestStatusTracking:
    """Tests for status tracking."""

    @pytest.fixture
    def monitor_with_data(self, tmp_path, monkeypatch):
        """Create a monitor with sample data."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ANALYTICS_FILE', monitor_dir / "analytics.json")

        monitor = PromptMonitor(verbose=False)

        # Add various statuses
        monitor.log_usage(command="cmd1", status="success")
        monitor.log_usage(command="cmd2", status="success")
        monitor.log_usage(command="cmd3", status="failure")
        monitor.log_usage(command="cmd4", status="partial")
        monitor.log_usage(command="cmd5", status="skipped")

        return monitor

    def test_status_counts(self, monitor_with_data):
        """Test that status counts are accurate."""
        stats = monitor_with_data.get_stats(days=30)

        assert stats["by_status"]["success"] == 2
        assert stats["by_status"]["failure"] == 1
        assert stats["by_status"]["partial"] == 1
        assert stats["by_status"]["skipped"] == 1

    def test_recent_failures(self, monitor_with_data):
        """Test that recent failures are tracked."""
        monitor_with_data.log_usage(
            command="failing_cmd",
            status="failure",
            error_message="Test error message"
        )

        stats = monitor_with_data.get_stats(days=30)

        assert len(stats["recent_failures"]) >= 1
        failure = next(f for f in stats["recent_failures"] if f["command"] == "failing_cmd")
        assert "Test error" in failure["error"]


class TestExportFeature:
    """Tests for the export to CSV feature."""

    @pytest.fixture
    def monitor_with_data(self, tmp_path, monkeypatch):
        """Create a monitor with sample data."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ANALYTICS_FILE', monitor_dir / "analytics.json")

        monitor = PromptMonitor(verbose=False)

        # Add various entries
        monitor.log_usage(command="/generate-brief", status="success", duration_ms=5000)
        monitor.log_usage(command="mcp__ahrefs__keywords", status="failure", error_message="403 Forbidden")
        monitor.log_usage(command="python3 ahrefs-api.py", status="success", duration_ms=3000)
        monitor.log_usage(command="validate-phase", status="success")
        monitor.log_usage(command="convert_to_docx", status="success")

        return monitor

    def test_export_to_csv_all_entries(self, monitor_with_data, tmp_path):
        """Test exporting all entries to CSV."""
        output_file = tmp_path / "export.csv"

        count = monitor_with_data.export_to_csv(str(output_file))

        assert count == 5
        assert output_file.exists()

        # Read and verify CSV content
        with open(output_file, 'r') as f:
            import csv
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 5
        assert 'timestamp' in rows[0]
        assert 'command' in rows[0]
        assert 'status' in rows[0]
        assert 'category' in rows[0]

    def test_export_to_csv_with_days_filter(self, monitor_with_data, tmp_path):
        """Test exporting entries with days filter."""
        output_file = tmp_path / "export_filtered.csv"

        # Export last 30 days (should get all in this test)
        count = monitor_with_data.export_to_csv(str(output_file), days=30)

        assert count == 5
        assert output_file.exists()

    def test_export_empty_monitor(self, tmp_path, monkeypatch):
        """Test exporting from empty monitor."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)
        output_file = tmp_path / "export_empty.csv"

        count = monitor.export_to_csv(str(output_file))

        assert count == 0
        # File should still be created with headers
        assert output_file.exists()


class TestAlertsFeature:
    """Tests for the alerts feature."""

    @pytest.fixture
    def monitor_with_failures(self, tmp_path, monkeypatch):
        """Create a monitor with many failures."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ANALYTICS_FILE', monitor_dir / "analytics.json")

        monitor = PromptMonitor(verbose=False)

        # Add many failures to trigger alerts
        for _ in range(10):
            monitor.log_usage(command="test_cmd", status="failure", error_message="Test error")

        return monitor

    def test_check_alerts_with_low_success_rate(self, monitor_with_failures):
        """Test alerts when success rate is too low."""
        alerts = monitor_with_failures.check_alerts()

        # Should have at least one alert for low success rate
        assert len(alerts) > 0

        # Check for critical success rate alert
        critical_alerts = [a for a in alerts if a["severity"] == "critical"]
        assert len(critical_alerts) > 0

    def test_check_alerts_normal_operation(self, tmp_path, monkeypatch):
        """Test alerts when system is operating normally."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)

        # Add some successful entries
        for _ in range(10):
            monitor.log_usage(command="test_cmd", status="success")

        alerts = monitor.check_alerts()

        # Should have no alerts
        assert len(alerts) == 0

    def test_check_alerts_ahrefs_failures(self, tmp_path, monkeypatch):
        """Test alerts for high Ahrefs failure rate."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)

        # Add many Ahrefs failures
        for _ in range(10):
            monitor.log_usage(command="mcp__ahrefs__keywords", status="failure")

        alerts = monitor.check_alerts()

        # Should have alert for Ahrefs failures
        ahrefs_alerts = [a for a in alerts if a["category"] == "ahrefs"]
        assert len(ahrefs_alerts) > 0

    def test_check_alerts_consecutive_failures(self, tmp_path, monkeypatch):
        """Test alerts for consecutive failures in a category."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)

        # Add consecutive failures in same category
        for _ in range(6):
            monitor.log_usage(command="/generate-brief", status="failure")

        alerts = monitor.check_alerts()

        # Should have alert for consecutive failures
        assert len(alerts) > 0


class TestArchiveFeature:
    """Tests for the archive feature."""

    @pytest.fixture
    def monitor_with_old_entries(self, tmp_path, monkeypatch):
        """Create a monitor with old entries."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ARCHIVE_DIR', monitor_dir / "archive")

        monitor = PromptMonitor(verbose=False)

        # Add old entries (manually set timestamps)
        from datetime import datetime, timedelta

        for days_ago in [100, 95, 50, 10, 5]:
            entry = UsageEntry(command="test_cmd", status="success")
            entry.timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat()
            monitor.entries.append(entry)

        monitor._save_entries()
        return monitor

    def test_archive_old_entries(self, monitor_with_old_entries, tmp_path):
        """Test archiving entries older than retention period."""
        result = monitor_with_old_entries.archive_old_entries(days=90)

        # Should archive entries older than 90 days
        assert result["archived"] == 2  # 100 and 95 days old
        assert result["retained"] == 3  # 50, 10, 5 days old

        # Check archive file was created
        assert result["archive_file"] is not None
        archive_path = Path(result["archive_file"])
        assert archive_path.exists()

    def test_archive_no_old_entries(self, tmp_path, monkeypatch):
        """Test archiving when no old entries exist."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'ARCHIVE_DIR', monitor_dir / "archive")

        monitor = PromptMonitor(verbose=False)
        result = monitor.archive_old_entries(days=90)

        assert result["archived"] == 0
        assert result["archive_file"] is None

    def test_archive_with_custom_retention(self, monitor_with_old_entries):
        """Test archiving with custom retention period."""
        result = monitor_with_old_entries.archive_old_entries(days=60)

        # Should archive entries older than 60 days
        # 100 > 60, 95 > 60, so 2 should be archived
        # 50 < 60, 10 < 60, 5 < 60, so 3 should be retained
        assert result["archived"] == 2
        assert result["retained"] == 3


class TestHooksFeature:
    """Tests for the hooks feature."""

    @pytest.fixture
    def monitor_with_hooks(self, tmp_path, monkeypatch):
        """Create a monitor with hooks directory."""
        monitor_dir = tmp_path / "logs" / "prompts"
        hooks_dir = monitor_dir / "hooks"
        monitor_dir.mkdir(parents=True)
        hooks_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")
        monkeypatch.setattr(pm, 'HOOKS_DIR', hooks_dir)

        monitor = PromptMonitor(verbose=False)
        return monitor, hooks_dir

    def test_trigger_hooks_no_hooks_found(self, monitor_with_hooks):
        """Test triggering hooks when no hooks exist."""
        monitor, hooks_dir = monitor_with_hooks

        results = monitor.trigger_hooks("test_event", {"key": "value"})

        assert len(results) == 0

    @pytest.mark.skipif(sys.platform == "win32", reason="Shell scripts not executable on Windows")
    def test_trigger_hooks_with_executable_script(self, monitor_with_hooks):
        """Test triggering hooks with executable script."""
        monitor, hooks_dir = monitor_with_hooks

        # Create a simple hook script
        hook_file = hooks_dir / "test_event_hook.sh"
        hook_file.write_text("#!/bin/bash\necho 'Hook executed'\nexit 0\n")
        hook_file.chmod(0o755)

        results = monitor.trigger_hooks("test_event", {"key": "value"})

        assert len(results) == 1
        assert results[0]["exit_code"] == 0
        assert "Hook executed" in results[0]["stdout"]

    @pytest.mark.skipif(sys.platform == "win32", reason="Shell scripts not executable on Windows")
    def test_trigger_hooks_non_executable(self, monitor_with_hooks):
        """Test triggering hooks with non-executable script (should skip)."""
        monitor, hooks_dir = monitor_with_hooks

        # Create a hook script without execute permission
        hook_file = hooks_dir / "test_event_hook.sh"
        hook_file.write_text("#!/bin/bash\necho 'Should not run'\n")
        # Don't set execute permission

        results = monitor.trigger_hooks("test_event", {"key": "value"})

        # Should skip non-executable hooks
        assert len(results) == 0


class TestImprovedRecommendations:
    """Tests for the improved recommendations engine."""

    def test_recommendations_with_specific_actions(self, tmp_path, monkeypatch):
        """Test that recommendations include specific actionable guidance."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)

        # Add Ahrefs failures to trigger specific recommendation
        for _ in range(10):
            monitor.log_usage(command="mcp__ahrefs__keywords", status="failure")

        recommendations = monitor.get_recommendations()

        # Should have recommendations
        assert len(recommendations) > 0

        # Check for specific actionable recommendations
        ahrefs_recs = [r for r in recommendations if r["category"] == "ahrefs"]
        assert len(ahrefs_recs) > 0

        # Should include specific actions
        assert "IMMEDIATE" in ahrefs_recs[0]["recommendation"] or "fallback" in ahrefs_recs[0]["recommendation"].lower()

    def test_recommendations_critical_priority(self, tmp_path, monkeypatch):
        """Test that critical issues get critical priority."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)

        # Add many failures to drop success rate below 60%
        for _ in range(20):
            monitor.log_usage(command="test_cmd", status="failure")
        for _ in range(2):
            monitor.log_usage(command="test_cmd", status="success")

        recommendations = monitor.get_recommendations()

        # Should have critical priority recommendations
        critical_recs = [r for r in recommendations if r["priority"] == "critical"]
        assert len(critical_recs) > 0

    def test_recommendations_sorted_by_priority(self, tmp_path, monkeypatch):
        """Test that recommendations are sorted by priority."""
        monitor_dir = tmp_path / "logs" / "prompts"
        monitor_dir.mkdir(parents=True)

        import prompt_monitor as pm
        monkeypatch.setattr(pm, 'MONITOR_DIR', monitor_dir)
        monkeypatch.setattr(pm, 'USAGE_LOG_FILE', monitor_dir / "usage_log.json")

        monitor = PromptMonitor(verbose=False)

        # Add mix of issues
        for _ in range(15):
            monitor.log_usage(command="test_cmd", status="failure")
        for _ in range(5):
            monitor.log_usage(command="test_cmd", status="success")

        recommendations = monitor.get_recommendations()

        if len(recommendations) > 1:
            # Check that critical/high come before medium/low
            priorities = [r["priority"] for r in recommendations]
            priority_order = ["critical", "high", "medium", "low"]

            # Verify order is maintained
            last_priority_index = -1
            for priority in priorities:
                current_index = priority_order.index(priority)
                assert current_index >= last_priority_index
                last_priority_index = current_index


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
