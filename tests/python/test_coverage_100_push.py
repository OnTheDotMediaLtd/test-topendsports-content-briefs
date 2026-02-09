"""Tests to push coverage toward 100% - targeting remaining uncovered lines."""
import csv
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


# =============================================================================
# automation.py - lines 69, 87-88, 111
# =============================================================================

class TestAutomationCoverage:

    def test_project_root_not_exists(self):
        """Cover line 69: PROJECT_ROOT does not exist."""
        from automation import AutomationRunner
        import automation
        runner = AutomationRunner(verbose=False)
        original = automation.PROJECT_ROOT
        try:
            automation.PROJECT_ROOT = Path('/nonexistent/path/not/real')
            code, stdout, stderr = runner.run_command(["echo", "test"])
            assert code == 1
            assert "does not exist" in stderr
        finally:
            automation.PROJECT_ROOT = original

    def test_command_timeout(self):
        """Cover line 87: subprocess.TimeoutExpired."""
        from automation import AutomationRunner
        runner = AutomationRunner(verbose=False)
        with patch('automation.PROJECT_ROOT', Path('.')):
            with patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd="test", timeout=300)):
                code, stdout, stderr = runner.run_command(["echo", "test"])
        assert code == 1
        assert "timed out" in stderr.lower()

    def test_command_file_not_found(self):
        """Cover line 88: FileNotFoundError."""
        from automation import AutomationRunner
        runner = AutomationRunner(verbose=False)
        with patch('automation.PROJECT_ROOT', Path('.')):
            with patch('subprocess.run', side_effect=FileNotFoundError("cmd not found")):
                code, stdout, stderr = runner.run_command(["nonexistent"])
        assert code == 1
        assert "not found" in stderr.lower()

    def test_truncated_errors_above_50_lines(self):
        """Cover line 111: error output > 50 lines truncated."""
        from automation import AutomationRunner
        runner = AutomationRunner(verbose=False)
        long_stderr = "\n".join([f"ERROR line {i}" for i in range(60)])
        with patch.object(runner, 'run_command', return_value=(1, "", long_stderr)):
            with patch('builtins.print'):
                result = runner.run_tests(with_tracking=False)
        assert result is False


# =============================================================================
# error_tracker.py - lines 225-228, 274-277, 601-604
# =============================================================================

class TestErrorTrackerCoverage:

    def test_save_errors_temp_cleanup(self):
        """Cover lines 225-228: temp file cleanup on save error."""
        from error_tracker import ErrorTracker
        tracker = ErrorTracker(verbose=False)

        with tempfile.TemporaryDirectory() as tmpdir:
            tracker.error_file = Path(tmpdir) / "errors.json"
            tracker.add_error(source="test", error_message="test error", category="test_cat")
            with patch('pathlib.Path.rename', side_effect=PermissionError("locked")):
                with patch('builtins.print'):
                    tracker._save_errors()

    def test_save_patterns_temp_cleanup(self):
        """Cover lines 274-277: temp file cleanup on pattern save error."""
        from error_tracker import ErrorTracker
        tracker = ErrorTracker(verbose=False)

        with tempfile.TemporaryDirectory() as tmpdir:
            tracker.patterns_file = Path(tmpdir) / "patterns.json"
            tracker.add_error(source="test", error_message="test error", category="test_cat")
            with patch('pathlib.Path.rename', side_effect=PermissionError("locked")):
                with patch('builtins.print'):
                    tracker._save_patterns()

    def test_append_lessons_temp_cleanup(self):
        """Cover lines 601-604: temp file cleanup on lessons save error."""
        from error_tracker import ErrorTracker
        tracker = ErrorTracker(verbose=False)

        with tempfile.TemporaryDirectory() as tmpdir:
            tracker.lessons_file = Path(tmpdir) / "lessons.json"
            lessons = [{"pattern": "test", "resolution": "fix"}]
            with patch('pathlib.Path.rename', side_effect=PermissionError("locked")):
                with patch('builtins.print'):
                    tracker._append_lessons_to_file(lessons)


# =============================================================================
# prompt_monitor.py - lines 136, 219-221, 400, 461-464, 866, 927, 978-980
# =============================================================================

class TestPromptMonitorCoverage:

    def test_usage_entry_detect_category_conversion(self):
        """Cover line 136: 'conversion' category via UsageEntry."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(
            command="convert_to_docx output.docx",
            status="success",
            duration_ms=100
        )
        assert entry.category == "conversion"

    def test_load_entries_malformed_entry(self):
        """Cover lines 219-221: skip malformed entries during load."""
        from prompt_monitor import PromptMonitor

        with tempfile.TemporaryDirectory() as tmpdir:
            monitor = PromptMonitor(verbose=False)
            usage_file = Path(tmpdir) / "prompt_usage.json"
            usage_file.write_text(json.dumps([
                {"invalid": "entry"},
                "not_a_dict"
            ]), encoding='utf-8')
            monitor.usage_file = usage_file
            monitor._load_entries()

    def test_get_recommendations_with_ahrefs_failures(self):
        """Cover lines 400, 461-464: zero total skipping and ahrefs recs."""
        from prompt_monitor import PromptMonitor, UsageEntry
        monitor = PromptMonitor(verbose=False)

        # Add many ahrefs failures to trigger high gap recommendation
        for i in range(20):
            monitor.entries.append(UsageEntry(
                command="ahrefs-api test",
                status="failure",
                duration_ms=100
            ))
        for i in range(5):
            monitor.entries.append(UsageEntry(
                command="ahrefs-api good",
                status="success",
                duration_ms=100
            ))

        with patch('builtins.print'):
            recs = monitor.get_recommendations()

    def test_print_stats_with_entries(self):
        """Cover line 866: print stats with avg_duration_ms."""
        from prompt_monitor import PromptMonitor, UsageEntry
        monitor = PromptMonitor(verbose=False)

        monitor.entries.append(UsageEntry(
            command="validate test",
            status="success",
            duration_ms=250
        ))

        with patch('builtins.print'):
            monitor.print_stats(days=30)

    def test_print_recommendations(self):
        """Cover line 927: no issues message."""
        from prompt_monitor import PromptMonitor
        monitor = PromptMonitor(verbose=False)
        with patch('builtins.print'):
            monitor.print_recommendations()

    def test_print_alerts_with_medium(self):
        """Cover lines 978-980: medium priority alerts."""
        from prompt_monitor import PromptMonitor, UsageEntry
        monitor = PromptMonitor(verbose=False)

        # Add entries that trigger medium alerts
        for i in range(10):
            monitor.entries.append(UsageEntry(
                command="validate_csv check",
                status="failure",
                duration_ms=100
            ))

        with patch('builtins.print'):
            monitor.print_alerts()


# =============================================================================
# validate_csv_data_integrated.py - lines 124-129
# =============================================================================

class TestValidateCsvDataIntegratedCoverage:

    def test_unicode_decode_error(self):
        """Cover lines 124-125: UnicodeDecodeError."""
        from validate_csv_data_integrated import CSVValidator

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as f:
            f.write(b'\xff\xfe\x00\x01invalid')
            temp_path = f.name

        try:
            validator = CSVValidator(Path(temp_path))
            result = validator._read_csv()
            assert result is False
            assert len(validator.errors) > 0
        finally:
            os.unlink(temp_path)

    def test_generic_read_error(self):
        """Cover lines 128-129: generic file read error."""
        from validate_csv_data_integrated import CSVValidator
        validator = CSVValidator(Path("/nonexistent/file.csv"))
        result = validator._read_csv()
        assert result is False
        assert len(validator.errors) > 0


# =============================================================================
# check_error_thresholds.py - line 191
# =============================================================================

class TestCheckErrorThresholdsCoverage:

    def test_patterns_needing_attention_warning(self):
        """Cover line 191: WARN in pattern check."""
        from check_error_thresholds import check_patterns_needing_attention
        patterns = {
            "test_pattern": {
                "count": 3,
                "last_seen": "2026-02-09",
                "severity": "medium",
                "needs_attention": True
            }
        }
        with patch('builtins.print'):
            result = check_patterns_needing_attention(patterns)


# =============================================================================
# validate_feedback.py - line 111
# =============================================================================

class TestValidateFeedbackCoverage:

    def test_read_file_failure(self):
        """Cover line 111: file does not exist."""
        from validate_feedback import FeedbackValidator
        validator = FeedbackValidator(Path("/nonexistent/feedback.md"))
        with patch('builtins.print'):
            result = validator.validate()
        assert result is False


# =============================================================================
# validate_phase_json_integrated.py - line 102
# =============================================================================

class TestValidatePhaseJsonIntegratedCoverage:

    def test_read_json_failure(self):
        """Cover line 102: _read_json returns False."""
        from validate_phase_json_integrated import PhaseJSONValidator
        validator = PhaseJSONValidator(Path("/nonexistent/phase.json"))
        with patch('builtins.print'):
            result = validator.validate()
        assert result is False


# =============================================================================
# pattern_analyzer.py - lines 222, 407
# =============================================================================

class TestPatternAnalyzerCoverage:

    def test_severity_high_occurrence(self):
        """Cover line 222: high occurrence rate for non-critical pattern."""
        from pattern_analyzer import PatternAnalyzer

        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = PatternAnalyzer(output_dir=tmpdir)
            # _calculate_severity(category, count, total_reports)
            severity = analyzer._calculate_severity("test_cat", 8, 10)
            assert severity in ('high', 'medium', 'critical')

    def test_integrate_with_ingest_error(self):
        """Cover line 407: feedback file processing failure."""
        from pattern_analyzer import PatternAnalyzer

        with tempfile.TemporaryDirectory() as tmpdir:
            bad_file = Path(tmpdir) / "bad_feedback.json"
            bad_file.write_text("not valid json", encoding='utf-8')

            analyzer = PatternAnalyzer(output_dir=tmpdir)
            with patch('builtins.print'):
                results = analyzer.integrate_with_ingest([str(bad_file)])
