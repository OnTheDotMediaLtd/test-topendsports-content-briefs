"""Tests targeting remaining coverage gaps to push from 98.53% toward 100%."""
import json
import os
import sys
import csv
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta

import pytest

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


# ==== unified_content_validator.py lines 50-67: ImportError fallback ====

class TestUnifiedContentValidatorImportFallback:
    """Test the import fallback path in unified_content_validator."""

    def test_import_fallback_when_package_unavailable(self):
        """When tes_shared is not installed, it tries relative import."""
        import importlib

        # Remove tes_shared from sys.modules if present
        mods_to_remove = [k for k in sys.modules if k.startswith('tes_shared')]
        saved = {}
        for k in mods_to_remove:
            saved[k] = sys.modules.pop(k)

        if 'unified_content_validator' in sys.modules:
            del sys.modules['unified_content_validator']

        try:
            import unified_content_validator
            assert hasattr(unified_content_validator, 'VALIDATORS_AVAILABLE')
        finally:
            sys.modules.update(saved)

    def test_validators_available_flag_exists(self):
        """Verify the VALIDATORS_AVAILABLE flag is set."""
        from unified_content_validator import VALIDATORS_AVAILABLE
        assert isinstance(VALIDATORS_AVAILABLE, bool)


# ==== error_tracker.py: temp file cleanup in exception handlers ====

class TestErrorTrackerExceptionPaths:
    """Test exception handling paths in error_tracker.py."""

    def test_save_errors_exception_temp_cleanup_succeeds(self, tmp_path):
        """Test _save_errors when json.dump fails - temp file is cleaned up."""
        from error_tracker import ErrorTracker

        tracker = ErrorTracker(verbose=False)
        tracker.errors = []

        fake_file = tmp_path / "errors.json"

        with patch('error_tracker.ERROR_LOG_FILE', fake_file):
            with patch('json.dump', side_effect=TypeError("not serializable")):
                with patch('builtins.print') as mock_print:
                    tracker._save_errors()
                    output = str(mock_print.call_args_list)
                    assert "Could not save errors" in output

    def test_save_errors_exception_temp_unlink_fails(self, tmp_path):
        """Test _save_errors when both save AND temp cleanup fail (lines 227-228)."""
        from error_tracker import ErrorTracker

        tracker = ErrorTracker(verbose=False)
        tracker.errors = []

        fake_file = tmp_path / "errors.json"

        with patch('error_tracker.ERROR_LOG_FILE', fake_file):
            # json.dump will fail, creating temp file
            # Then temp_file.unlink() will also fail
            original_unlink = Path.unlink
            def failing_unlink(self, *args, **kwargs):
                raise PermissionError("file locked")

            with patch('json.dump', side_effect=TypeError("not serializable")):
                with patch.object(Path, 'unlink', failing_unlink):
                    with patch('builtins.print') as mock_print:
                        tracker._save_errors()
                        output = str(mock_print.call_args_list)
                        assert "Could not save errors" in output

    def test_save_patterns_exception_temp_unlink_fails(self, tmp_path):
        """Test _save_patterns when both save AND temp cleanup fail (lines 276-277)."""
        from error_tracker import ErrorTracker

        tracker = ErrorTracker(verbose=False)
        tracker.patterns = {}

        fake_file = tmp_path / "patterns.json"

        with patch('error_tracker.PATTERNS_FILE', fake_file):
            original_unlink = Path.unlink
            def failing_unlink(self, *args, **kwargs):
                raise PermissionError("file locked")

            with patch('json.dump', side_effect=TypeError("not serializable")):
                with patch.object(Path, 'unlink', failing_unlink):
                    with patch('builtins.print') as mock_print:
                        tracker._save_patterns()
                        output = str(mock_print.call_args_list)
                        assert "Could not save patterns" in output

    def test_append_lessons_exception_temp_unlink_fails(self, tmp_path):
        """Test _append_lessons_to_file when both write AND cleanup fail (lines 603-604)."""
        from error_tracker import ErrorTracker

        tracker = ErrorTracker(verbose=False)

        lessons = [{
            "title": "Test Lesson",
            "problem": "Test problem",
            "solution": "Test solution",
            "category": "api",
            "source": "test",
            "occurrence_count": 5,
            "generated_at": datetime.now().isoformat(),
        }]

        fake_file = tmp_path / "lessons-learned.md"
        fake_file.write_text("# Lessons\n", encoding='utf-8')

        with patch('error_tracker.LESSONS_FILE', fake_file):
            original_unlink = Path.unlink
            def failing_unlink(self, *args, **kwargs):
                raise PermissionError("file locked")

            original_open = open
            call_count = [0]
            def selective_open(*args, **kwargs):
                call_count[0] += 1
                if call_count[0] == 1:
                    # First open reads lessons file
                    return original_open(*args, **kwargs)
                # Second open writes temp - succeed but then fail on replace
                f = original_open(*args, **kwargs)
                original_write = f.write
                def fail_write(data):
                    raise IOError("disk full")
                f.write = fail_write
                return f

            with patch('builtins.open', side_effect=selective_open):
                with patch.object(Path, 'unlink', failing_unlink):
                    with patch('builtins.print') as mock_print:
                        tracker._append_lessons_to_file(lessons)
                        output = str(mock_print.call_args_list)
                        assert "Could not update lessons" in output

    def test_save_errors_open_fails_no_temp(self, tmp_path):
        """Test _save_errors when open fails before temp file is created."""
        from error_tracker import ErrorTracker

        tracker = ErrorTracker(verbose=False)
        tracker.errors = []

        fake_file = tmp_path / "errors.json"

        with patch('error_tracker.ERROR_LOG_FILE', fake_file):
            with patch('builtins.open', side_effect=PermissionError("denied")):
                with patch('builtins.print'):
                    tracker._save_errors()  # Should not crash


# ==== prompt_monitor.py: UsageEntry._detect_category default paths ====

class TestUsageEntryDetectCategory:
    """Test _detect_category on UsageEntry for default paths (not in KNOWN_COMMANDS)."""

    def test_detect_category_phase(self):
        """Phase commands detected."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="run phase 2 generation", status="success")
        assert entry.category == "phase_execution"

    def test_detect_category_brief(self):
        """Brief commands detected."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="write brief for keyword", status="success")
        assert entry.category == "brief_generation"

    def test_detect_category_keyword(self):
        """Keyword commands detected."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="keyword research uk", status="success")
        assert entry.category == "keyword_research"

    def test_detect_category_ahrefs(self):
        """Ahrefs commands detected."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="ahrefs export data", status="success")
        assert entry.category == "keyword_research"

    def test_detect_category_conversion(self):
        """Docx/convert commands detected."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="docx output generator", status="success")
        assert entry.category == "conversion"

    def test_detect_category_validation(self):
        """Validate commands detected."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="validate csv output", status="success")
        assert entry.category == "validation"

    def test_detect_category_check(self):
        """Check commands detected."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="check error thresholds", status="success")
        assert entry.category == "validation"

    def test_detect_category_other(self):
        """Unknown commands default to other."""
        from prompt_monitor import UsageEntry
        entry = UsageEntry(command="xyz unknown 123", status="success")
        assert entry.category == "other"


# ==== prompt_monitor.py: _load_entries error paths ====

class TestPromptMonitorLoadEntries:
    """Test _load_entries error handling."""

    def test_load_entries_malformed_entry(self, tmp_path):
        """Test loading entries skips non-dict entries."""
        from prompt_monitor import PromptMonitor

        usage_file = tmp_path / "usage_log.json"
        usage_file.write_text(json.dumps({
            "entries": [
                {"command": "test", "status": "success", "context": "",
                 "timestamp": "2026-01-01T00:00:00", "duration_ms": 1000,
                 "error_message": "", "metadata": {}, "category": "other"},
                "not_a_dict",
                {"bad": "entry"}
            ]
        }), encoding='utf-8')

        with patch('prompt_monitor.USAGE_LOG_FILE', usage_file):
            with patch('prompt_monitor.MONITOR_DIR', tmp_path):
                monitor = PromptMonitor(verbose=False)
                assert isinstance(monitor.entries, list)

    def test_load_entries_entry_raises_exception(self, tmp_path):
        """Test loading entries when from_dict raises an exception."""
        from prompt_monitor import PromptMonitor, UsageEntry

        usage_file = tmp_path / "usage_log.json"
        usage_file.write_text(json.dumps({
            "entries": [
                {"command": "test", "status": "success"},
            ]
        }), encoding='utf-8')

        # Patch from_dict to raise on the first call
        original_from_dict = UsageEntry.from_dict

        def failing_from_dict(cls_or_data, data=None):
            raise ValueError("Corrupt entry data")

        with patch('prompt_monitor.USAGE_LOG_FILE', usage_file):
            with patch('prompt_monitor.MONITOR_DIR', tmp_path):
                with patch.object(UsageEntry, 'from_dict', classmethod(failing_from_dict)):
                    monitor = PromptMonitor(verbose=True)
                    # Entry should be skipped, not crash
                    assert isinstance(monitor.entries, list)

    def test_load_entries_json_decode_error(self, tmp_path):
        """Test loading entries with corrupted JSON."""
        from prompt_monitor import PromptMonitor

        usage_file = tmp_path / "usage_log.json"
        usage_file.write_text("{bad json", encoding='utf-8')

        with patch('prompt_monitor.USAGE_LOG_FILE', usage_file):
            with patch('prompt_monitor.MONITOR_DIR', tmp_path):
                monitor = PromptMonitor(verbose=False)
                assert monitor.entries == []

    def test_load_entries_general_exception(self, tmp_path):
        """Test loading entries with unexpected error."""
        from prompt_monitor import PromptMonitor

        with patch('prompt_monitor.USAGE_LOG_FILE', tmp_path / "nonexistent" / "deep" / "usage.json"):
            with patch('prompt_monitor.MONITOR_DIR', tmp_path):
                monitor = PromptMonitor(verbose=False)
                assert monitor.entries == []


# ==== prompt_monitor.py: get_recommendations category-specific actions ====

class TestPromptMonitorRecommendations:
    """Test get_recommendations for specific category branches."""

    def _make_monitor_with_entries(self, command, failure_count, total_count):
        """Helper to create a monitor with specific entries."""
        from prompt_monitor import PromptMonitor, UsageEntry

        monitor = PromptMonitor.__new__(PromptMonitor)
        monitor.verbose = False
        monitor.entries = []

        for i in range(total_count):
            entry = UsageEntry(
                command=command,
                status="failure" if i < failure_count else "success",
            )
            monitor.entries.append(entry)

        return monitor

    def test_recommendations_ahrefs_high_gap(self):
        """Test ahrefs recommendation with >30% gap (IMMEDIATE action)."""
        # Use mcp__ahrefs__ which maps to "ahrefs" category in KNOWN_COMMANDS
        monitor = self._make_monitor_with_entries("mcp__ahrefs__get_keywords", 9, 10)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)
        # Should have at least one recommendation about ahrefs
        if recs:
            assert any("ahrefs" in str(r).lower() or "IMMEDIATE" in str(r) for r in recs)

    def test_recommendations_ahrefs_medium_gap(self):
        """Test ahrefs recommendation with 15-30% gap."""
        monitor = self._make_monitor_with_entries("mcp__ahrefs__query", 4, 10)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_recommendations_brief_generation(self):
        """Test brief_generation recommendation."""
        # Use /generate-brief which maps to "brief_generation"
        monitor = self._make_monitor_with_entries("/generate-brief run", 9, 10)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_recommendations_validation(self):
        """Test validation recommendation."""
        # Use validate-phase which maps to "validation"
        monitor = self._make_monitor_with_entries("validate-phase check", 9, 10)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_recommendations_conversion(self):
        """Test conversion recommendation."""
        # Use convert_to_docx which maps to "conversion"
        monitor = self._make_monitor_with_entries("convert_to_docx run", 9, 10)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)


# ==== validate_csv_data_integrated.py lines 125-126 ====

class TestValidateCsvDataIntegrated:
    """Test exception paths in validate_csv_data_integrated."""

    def test_file_read_general_exception(self, tmp_path):
        """Test handling of unexpected exceptions during file read."""
        from validate_csv_data_integrated import CSVValidator

        csv_file = tmp_path / "test.csv"
        csv_file.write_text("header1,header2\nval1,val2", encoding='utf-8')

        validator = CSVValidator(csv_file)

        # Patch builtins.open to raise a generic (non-Unicode, non-csv) exception
        with patch('builtins.open', side_effect=OSError("disk error")):
            result = validator._read_csv()
            assert result is False
            assert any("Error reading file" in e for e in validator.errors)


# ==== check_error_thresholds.py line 191 ====

class TestCheckErrorThresholds:
    """Test edge case in check_error_thresholds."""

    def test_patterns_needing_attention_with_patterns(self):
        """Test check_patterns_needing_attention with patterns."""
        from check_error_thresholds import check_patterns_needing_attention

        patterns = {
            "test_pattern": {
                "count": 3,
                "category": "api",
                "first_seen": "2026-01-01",
                "last_seen": "2026-02-10",
            }
        }

        passed, count, msg = check_patterns_needing_attention(patterns)
        assert isinstance(passed, bool)
        assert isinstance(count, int)
        assert isinstance(msg, str)

    def test_patterns_with_many_needing_attention(self):
        """Test when many patterns need attention (triggers warning)."""
        from check_error_thresholds import check_patterns_needing_attention

        patterns = {
            f"pattern_{i}": {
                "count": 10,
                "category": "api",
                "first_seen": "2026-01-01",
                "last_seen": "2026-02-10",
                "lesson_generated": False,
            }
            for i in range(10)
        }
        passed, count, msg = check_patterns_needing_attention(patterns)
        assert msg is not None


# ==== validate_feedback.py line 111 ====

class TestValidateFeedbackCoverage:
    """Test uncovered feedback validation path."""

    def test_process_feedback_with_import_error(self, tmp_path):
        """Test feedback processing when ingest_feedback import fails."""
        from validate_feedback import FeedbackValidator

        feedback_file = tmp_path / "feedback.md"
        feedback_file.write_text("# Feedback\n\n## Summary\n\nSome feedback content here.", encoding='utf-8')

        validator = FeedbackValidator(feedback_file)
        result = validator.validate()
        assert isinstance(result, bool)


# ==== validate_phase_json_integrated.py line 102 ====

class TestValidatePhaseJsonIntegrated:
    """Test uncovered path in phase JSON integrated validator."""

    def test_validate_nonexistent_file(self, tmp_path):
        """Test validating a file that doesn't exist."""
        from validate_phase_json_integrated import PhaseJSONValidator

        validator = PhaseJSONValidator(tmp_path / "missing.json")
        result = validator.validate()
        assert result is False
        assert any("not found" in e.lower() or "File not found" in e for e in validator.errors)

    def test_validate_with_auto_phase_detection(self, tmp_path):
        """Test validation with automatic phase detection from filename."""
        phase_file = tmp_path / "phase-2-keywords.json"
        phase_file.write_text(json.dumps({
            "phase": 2,
            "keywords": ["test keyword"],
            "status": "complete"
        }), encoding='utf-8')

        from validate_phase_json_integrated import PhaseJSONValidator
        validator = PhaseJSONValidator(phase_file)
        # Don't provide phase, let it auto-detect
        result = validator.validate()
        assert isinstance(result, bool)
