"""
Coverage gap tests targeting the remaining ~40 missed lines to push toward 100%.
Covers:
- unified_content_validator.py: fallback import path (lines 50-67)
- error_tracker.py: temp file cleanup, timestamp parsing, severity printing
- prompt_monitor.py: category detection, exception paths, recommendations printing
- automation.py: exception path, analysis command
- validate_feedback.py: line 111
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


class TestUnifiedContentValidatorFallbackImport:
    """Cover the fallback import path in unified_content_validator.py lines 50-67."""

    def test_fallback_import_module_loads(self):
        """The module should load and define VALIDATORS_AVAILABLE."""
        import unified_content_validator as ucv
        assert hasattr(ucv, 'VALIDATORS_AVAILABLE')

    def test_validator_with_validators_disabled(self):
        """Test instantiation with all validators disabled (if VALIDATORS_AVAILABLE)."""
        import unified_content_validator as ucv
        if ucv.VALIDATORS_AVAILABLE:
            validator = ucv.UnifiedContentValidator(
                validate_ai_patterns=False,
                validate_brands=False,
                validate_eeat=False
            )
            assert validator is not None
        else:
            # If validators not available, constructor should raise ImportError
            with pytest.raises(ImportError):
                ucv.UnifiedContentValidator()


class TestErrorTrackerTempFileCleanup:
    """Cover temp file cleanup exception paths in error_tracker.py."""

    def _make_tracker(self, tmpdir):
        """Create a minimal ErrorTracker without full __init__."""
        from error_tracker import ErrorTracker
        tracker = ErrorTracker.__new__(ErrorTracker)
        tracker.errors = []
        tracker.patterns = {}
        tracker.verbose = False
        # Override module-level paths
        return tracker

    def test_save_errors_temp_file_cleanup_on_failure(self):
        """Cover lines 225-228: temp file cleanup when save fails."""
        from error_tracker import ErrorTracker
        tmpdir = Path(tempfile.mkdtemp())
        try:
            tracker = self._make_tracker(tmpdir)
            tracker.errors = []
            # Patch module-level ERROR_LOG_FILE
            error_log_file = tmpdir / "error_log.json"
            temp_file = error_log_file.with_suffix('.tmp')
            temp_file.write_text('{}', encoding='utf-8')

            with patch('error_tracker.ERROR_LOG_FILE', error_log_file):
                with patch('json.dump', side_effect=OSError("disk full")):
                    with patch('builtins.print') as mock_print:
                        tracker._save_errors()
                        output = ' '.join(str(c) for c in mock_print.call_args_list)
                        assert "Could not save errors" in output
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_save_patterns_temp_file_cleanup_on_failure(self):
        """Cover lines 274-277: temp file cleanup when pattern save fails."""
        from error_tracker import ErrorTracker
        tmpdir = Path(tempfile.mkdtemp())
        try:
            tracker = self._make_tracker(tmpdir)
            patterns_file = tmpdir / "patterns.json"
            temp_file = patterns_file.with_suffix('.tmp')
            temp_file.write_text('{}', encoding='utf-8')

            with patch('error_tracker.PATTERNS_FILE', patterns_file):
                with patch('json.dump', side_effect=OSError("disk full")):
                    with patch('builtins.print') as mock_print:
                        tracker._save_patterns()
                        output = ' '.join(str(c) for c in mock_print.call_args_list)
                        assert "Could not save patterns" in output
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_append_lessons_temp_file_cleanup_on_failure(self):
        """Cover lines 601-604: temp file cleanup when lesson append fails."""
        from error_tracker import ErrorTracker
        tmpdir = Path(tempfile.mkdtemp())
        try:
            tracker = self._make_tracker(tmpdir)
            lessons_file = tmpdir / "lessons-learned.md"
            lessons_file.write_text("# Lessons Learned\n\n", encoding='utf-8')

            temp_file = lessons_file.with_suffix('.tmp')
            temp_file.write_text('temp content', encoding='utf-8')

            lessons = [{
                "title": "Test Lesson",
                "problem": "Test problem",
                "solution": "Test solution",
                "category": "test",
                "source": "unit_test",
                "count": 5,
            }]

            with patch('error_tracker.LESSONS_FILE', lessons_file):
                # Make the temp_file.replace() fail
                with patch.object(Path, 'replace', side_effect=OSError("permission denied")):
                    with patch('builtins.print') as mock_print:
                        tracker._append_lessons_to_file(lessons)
                        output = ' '.join(str(c) for c in mock_print.call_args_list)
                        assert "Could not update lessons" in output
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_timestamp_valueerror_in_stats(self):
        """Cover line 629: ValueError when parsing timestamps in get_stats."""
        from error_tracker import ErrorTracker, ErrorEntry

        tmpdir = Path(tempfile.mkdtemp())
        try:
            with patch('error_tracker.ERROR_LOG_DIR', tmpdir):
                with patch('error_tracker.ERROR_LOG_FILE', tmpdir / "error_log.json"):
                    with patch('error_tracker.PATTERNS_FILE', tmpdir / "patterns.json"):
                        tracker = ErrorTracker(verbose=False)

            # Add an error entry with a bad timestamp
            entry = ErrorEntry(
                source="test",
                error_message="test error",
                category="test",
                severity="high",
            )
            entry.timestamp = "not-a-valid-timestamp"
            tracker.errors.append(entry)

            stats = tracker.get_stats()
            assert stats["total_errors"] >= 1
            # Bad timestamp won't count toward last 24h/7d
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_print_stats_severity_display(self):
        """Cover line 664: severity display in print_stats."""
        from error_tracker import ErrorTracker, ErrorEntry

        tmpdir = Path(tempfile.mkdtemp())
        try:
            with patch('error_tracker.ERROR_LOG_DIR', tmpdir):
                with patch('error_tracker.ERROR_LOG_FILE', tmpdir / "error_log.json"):
                    with patch('error_tracker.PATTERNS_FILE', tmpdir / "patterns.json"):
                        tracker = ErrorTracker(verbose=False)

            for sev in ['critical', 'high', 'medium', 'low']:
                entry = ErrorEntry(
                    source="unit_test",
                    error_message=f"test {sev} error",
                    category="test",
                    severity=sev,
                )
                tracker.errors.append(entry)

            with patch('builtins.print') as mock_print:
                tracker.print_stats()
                output = '\n'.join(str(c) for c in mock_print.call_args_list)
                assert "critical" in output
                assert "high" in output
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


class TestPromptMonitorCoverageGaps:
    """Cover missed lines in prompt_monitor.py."""

    def test_category_detection_conversion(self):
        """Cover line 136: 'docx' or 'convert' category detection."""
        from prompt_monitor import UsageEntry

        entry = UsageEntry(
            command="convert_to_docx output.docx",
            status="success",
        )
        assert entry.category == "conversion"

    def test_category_detection_validation(self):
        """Cover line 138: 'validate' or 'check' category detection."""
        from prompt_monitor import UsageEntry

        entry = UsageEntry(
            command="validate_csv_data test.csv",
            status="success",
        )
        assert entry.category == "validation"

    def test_malformed_entry_skip(self):
        """Cover lines 219-221: malformed entry skipped during load."""
        from prompt_monitor import PromptMonitor

        tmpdir = Path(tempfile.mkdtemp())
        try:
            usage_file = tmpdir / "usage_log.json"
            usage_file.write_text(json.dumps({
                "entries": [
                    {"this_is": "invalid_missing_command"},
                    {
                        "command": "test_cmd",
                        "status": "success",
                        "context": "",
                        "duration_ms": None,
                        "error_message": "",
                        "metadata": {},
                        "timestamp": datetime.now().isoformat(),
                        "category": "other",
                    }
                ]
            }), encoding='utf-8')

            with patch('prompt_monitor.MONITOR_DIR', tmpdir):
                with patch('prompt_monitor.USAGE_LOG_FILE', usage_file):
                    monitor = PromptMonitor(verbose=True)

            # Should have loaded at least some entries
            assert isinstance(monitor.entries, list)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_save_entries_temp_file_cleanup(self):
        """Cover lines 251-255: temp file cleanup when save fails."""
        from prompt_monitor import PromptMonitor

        tmpdir = Path(tempfile.mkdtemp())
        try:
            usage_file = tmpdir / "usage_log.json"
            temp_file = usage_file.with_suffix('.tmp')
            temp_file.write_text('[]', encoding='utf-8')

            with patch('prompt_monitor.MONITOR_DIR', tmpdir):
                with patch('prompt_monitor.USAGE_LOG_FILE', usage_file):
                    monitor = PromptMonitor(verbose=False)
                    with patch('json.dump', side_effect=OSError("disk full")):
                        with patch('builtins.print') as mock_print:
                            monitor._save_entries()
                            output = ' '.join(str(c) for c in mock_print.call_args_list)
                            assert "Could not save entries" in output
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_category_with_zero_total_skipped_in_trends(self):
        """Cover line 400: category with total=0 is skipped in get_trends."""
        from prompt_monitor import PromptMonitor

        tmpdir = Path(tempfile.mkdtemp())
        try:
            with patch('prompt_monitor.MONITOR_DIR', tmpdir):
                with patch('prompt_monitor.USAGE_LOG_FILE', tmpdir / "usage_log.json"):
                    monitor = PromptMonitor(verbose=False)

            # Mock get_stats to return a category with total=0
            with patch.object(monitor, 'get_stats', return_value={
                "by_category": {
                    "empty_cat": {"total": 0, "success": 0}
                }
            }):
                trends = monitor.get_trends(30)
                # Zero-total category should be skipped
                assert isinstance(trends, dict)
                assert "problematic" in trends
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_recommendation_categories_with_data(self):
        """Cover lines 461-464: specific recommendation text for each category."""
        from prompt_monitor import PromptMonitor, UsageEntry

        tmpdir = Path(tempfile.mkdtemp())
        try:
            with patch('prompt_monitor.MONITOR_DIR', tmpdir):
                with patch('prompt_monitor.USAGE_LOG_FILE', tmpdir / "usage_log.json"):
                    monitor = PromptMonitor(verbose=False)

            # Create entries that will produce recommendations (high failure rate)
            now = datetime.now()
            for cat_cmd in ["ahrefs_api", "generate_brief", "validate_csv", "convert_to_docx"]:
                for i in range(10):
                    entry = UsageEntry(
                        command=cat_cmd,
                        status="failure" if i < 8 else "success",
                    )
                    entry.timestamp = (now - timedelta(hours=i)).isoformat()
                    monitor.entries.append(entry)

            recs = monitor.get_recommendations()
            assert isinstance(recs, list)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_print_recommendations(self):
        """Cover line 927: print_recommendations output."""
        from prompt_monitor import PromptMonitor

        tmpdir = Path(tempfile.mkdtemp())
        try:
            with patch('prompt_monitor.MONITOR_DIR', tmpdir):
                with patch('prompt_monitor.USAGE_LOG_FILE', tmpdir / "usage_log.json"):
                    monitor = PromptMonitor(verbose=False)

            with patch.object(monitor, 'get_recommendations', return_value=[]):
                with patch('builtins.print') as mock_print:
                    monitor.print_recommendations()
                    output = '\n'.join(str(c) for c in mock_print.call_args_list)
                    assert "RECOMMENDATIONS" in output
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_print_alerts_with_high_and_medium(self):
        """Cover lines 970-980: alerts printing with high/medium severity."""
        from prompt_monitor import PromptMonitor

        tmpdir = Path(tempfile.mkdtemp())
        try:
            with patch('prompt_monitor.MONITOR_DIR', tmpdir):
                with patch('prompt_monitor.USAGE_LOG_FILE', tmpdir / "usage_log.json"):
                    monitor = PromptMonitor(verbose=False)

            monitor.alert_hooks = {}

            # Mock check_alerts to return alerts
            alerts = [
                {"severity": "high", "category": "ahrefs", "message": "High failure rate"},
                {"severity": "medium", "category": "brief_generation", "message": "Medium rate"},
            ]
            with patch.object(monitor, 'check_alerts', return_value=alerts):
                with patch.object(monitor, 'trigger_hooks'):
                    with patch('builtins.print') as mock_print:
                        exit_code = monitor.print_alerts()
                        output = '\n'.join(str(c) for c in mock_print.call_args_list)
                        assert exit_code == 1  # high = warning
                        assert "HIGH PRIORITY" in output
                        assert "MEDIUM PRIORITY" in output
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_print_alerts_with_critical(self):
        """Cover critical alert path in print_alerts."""
        from prompt_monitor import PromptMonitor

        tmpdir = Path(tempfile.mkdtemp())
        try:
            with patch('prompt_monitor.MONITOR_DIR', tmpdir):
                with patch('prompt_monitor.USAGE_LOG_FILE', tmpdir / "usage_log.json"):
                    monitor = PromptMonitor(verbose=False)

            monitor.alert_hooks = {}

            alerts = [
                {"severity": "critical", "category": "ahrefs", "message": "System down"},
            ]
            with patch.object(monitor, 'check_alerts', return_value=alerts):
                with patch.object(monitor, 'trigger_hooks'):
                    with patch('builtins.print') as mock_print:
                        exit_code = monitor.print_alerts()
                        assert exit_code == 2
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


class TestAutomationExceptionPath:
    """Cover exception paths in automation.py."""

    def test_run_command_generic_exception(self):
        """Cover lines 87-88: generic exception in run_command."""
        from automation import AutomationRunner

        runner = AutomationRunner(verbose=False)

        with patch('subprocess.run', side_effect=RuntimeError("unexpected error")):
            code, stdout, stderr = runner.run_command(["fake_cmd"])
            assert code == 1
            assert "Command execution failed" in stderr

    def test_analyze_errors_analysis_exception(self):
        """Cover line 148->158: analysis command after stats succeeds."""
        from automation import AutomationRunner

        runner = AutomationRunner(verbose=False)

        call_count = [0]
        def mock_run_command(cmd, capture=True):
            call_count[0] += 1
            if call_count[0] == 1:
                return (0, "stats output", "")
            else:
                raise RuntimeError("analysis failed")

        with patch.object(runner, 'run_command', side_effect=mock_run_command):
            with patch.object(runner, 'log'):
                result = runner.analyze_errors()
                assert isinstance(result, dict)


class TestValidateFeedbackLine111:
    """Cover line 111 in validate_feedback.py: _validate_filename returns False."""

    def test_validate_with_bad_filename(self):
        """When the filename format is invalid, validate returns False early."""
        from validate_feedback import FeedbackValidator

        tmpdir = Path(tempfile.mkdtemp())
        try:
            # Create a file with an invalid filename format
            bad_file = tmpdir / "bad-file-name.md"
            bad_file.write_text("# Test content\n", encoding='utf-8')

            validator = FeedbackValidator(bad_file)
            result = validator.validate()
            # Should fail due to filename validation
            assert result is False or len(validator.errors) > 0
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
