"""
Tests targeting coverage gaps in error_tracker.py
Covers: _load_errors edge cases, _save_errors errors, _load_patterns edge cases,
        generate_lessons with existing lessons, _append_lessons_to_file creation,
        print_stats branches, print_analysis branches, main() CLI function.
"""
import json
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import error_tracker
from error_tracker import ErrorTracker, ErrorEntry, main


class TestLoadErrorsEdgeCases:
    """Tests for _load_errors edge cases (lines 192-228)."""

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_load'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_load/patterns.json'))
    def test_load_errors_malformed_entry(self, tmp_path):
        """Test _load_errors with entry that raises exception during from_dict."""
        log_file = tmp_path / "error_log.json"
        data = {
            "errors": [
                {"source": "good", "error_message": "ok"},
                "not_a_dict",  # Will be skipped (not isinstance dict)
                {"source": "also_good", "error_message": "also ok"},
            ]
        }
        log_file.write_text(json.dumps(data))
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                tracker = ErrorTracker(verbose=True)
                # Should have loaded 2 valid entries, skipped the string
                assert len(tracker.errors) == 2

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_json'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_json/patterns.json'))
    def test_load_errors_json_decode_error(self, tmp_path):
        """Test _load_errors with invalid JSON (line 200-202)."""
        log_file = tmp_path / "error_log.json"
        log_file.write_text("{invalid json content")
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                tracker = ErrorTracker(verbose=True)
                assert tracker.errors == []

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_generic'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_generic/patterns.json'))
    def test_load_errors_generic_exception(self, tmp_path):
        """Test _load_errors with generic exception (lines 203-205)."""
        log_file = tmp_path / "error_log.json"
        log_file.write_text('{"errors": []}')
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch('builtins.open', side_effect=PermissionError("no access")):
                    tracker = ErrorTracker(verbose=True)
                    assert tracker.errors == []

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_nofile'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_nofile/patterns.json'))
    def test_load_errors_no_file(self, tmp_path):
        """Test _load_errors when file doesn't exist (line 206)."""
        log_file = tmp_path / "nonexistent.json"
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                tracker = ErrorTracker()
                assert tracker.errors == []

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_notdict'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_notdict/patterns.json'))
    def test_load_errors_non_dict_data(self, tmp_path):
        """Test _load_errors when JSON is not a dict (line 172-174)."""
        log_file = tmp_path / "error_log.json"
        log_file.write_text('[1, 2, 3]')  # Array instead of dict
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                tracker = ErrorTracker(verbose=True)
                assert tracker.errors == []

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_notlist'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_notlist/patterns.json'))
    def test_load_errors_non_list_errors(self, tmp_path):
        """Test _load_errors when errors field is not a list (line 178-180)."""
        log_file = tmp_path / "error_log.json"
        log_file.write_text('{"errors": "not_a_list"}')
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                tracker = ErrorTracker(verbose=True)
                assert tracker.errors == []

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_empty'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_empty/patterns.json'))
    def test_load_errors_empty_file(self, tmp_path):
        """Test _load_errors with empty file (line 164-166)."""
        log_file = tmp_path / "error_log.json"
        log_file.write_text('')
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                tracker = ErrorTracker(verbose=True)
                assert tracker.errors == []

    @patch.object(error_tracker, 'ERROR_LOG_DIR', Path('/tmp/test_et_from_dict_err'))
    @patch.object(error_tracker, 'PATTERNS_FILE', Path('/tmp/test_et_from_dict_err/patterns.json'))
    def test_load_errors_entry_from_dict_exception(self, tmp_path):
        """Test _load_errors when from_dict raises an exception for one entry."""
        log_file = tmp_path / "error_log.json"
        data = {
            "errors": [
                {"source": "good", "error_message": "valid"},
                {"source": "bad", "error_message": "valid"},
            ]
        }
        log_file.write_text(json.dumps(data))
        
        # Make from_dict raise on second call
        original_from_dict = ErrorEntry.from_dict
        call_count = [0]
        
        def flaky_from_dict(d):
            call_count[0] += 1
            if call_count[0] == 2:
                raise TypeError("simulated error")
            return original_from_dict(d)
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(ErrorEntry, 'from_dict', side_effect=flaky_from_dict):
                    tracker = ErrorTracker(verbose=True)
                    assert len(tracker.errors) == 1


class TestSaveErrorsEdgeCases:
    """Tests for _save_errors error handling (lines 253-255)."""

    def test_save_errors_write_failure(self, tmp_path):
        """Test _save_errors when write fails and temp file cleanup."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    tracker.errors = [ErrorEntry("test", "msg")]
                    
                    # Make json.dump fail
                    with patch('builtins.open', side_effect=OSError("disk full")):
                        tracker._save_errors()
                        # Should not raise, just print error


class TestLoadPatternsEdgeCases:
    """Tests for _load_patterns edge cases (lines 270-277)."""

    def test_load_patterns_empty_file(self, tmp_path):
        """Test _load_patterns with empty file."""
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text('')
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', patterns_file):
                    tracker = ErrorTracker(verbose=True)
                    assert tracker.patterns == {}

    def test_load_patterns_non_dict(self, tmp_path):
        """Test _load_patterns when JSON is not a dict."""
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text('[1, 2, 3]')
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', patterns_file):
                    tracker = ErrorTracker(verbose=True)
                    assert tracker.patterns == {}

    def test_load_patterns_json_decode_error(self, tmp_path):
        """Test _load_patterns with invalid JSON."""
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text('{broken json')
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', patterns_file):
                    tracker = ErrorTracker(verbose=True)
                    assert tracker.patterns == {}

    def test_load_patterns_generic_error(self, tmp_path):
        """Test _load_patterns with generic file read error."""
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text('{"key": "value"}')
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', patterns_file):
                    # Monkey-patch open to fail only for patterns file
                    original_open = open
                    def failing_open(path, *args, **kwargs):
                        if str(path) == str(patterns_file):
                            raise IOError("read error")
                        return original_open(path, *args, **kwargs)
                    
                    with patch('builtins.open', side_effect=failing_open):
                        tracker = ErrorTracker(verbose=True)
                        assert tracker.patterns == {}


class TestSavePatternsEdgeCases:
    """Tests for _save_patterns error handling."""

    def test_save_patterns_write_failure(self, tmp_path):
        """Test _save_patterns when write fails."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    tracker.patterns = {"fp1": {"count": 1}}
                    
                    with patch('builtins.open', side_effect=OSError("disk full")):
                        tracker._save_patterns()
                        # Should not raise


class TestGenerateLessonsComplete:
    """Tests for generate_lessons covering lines 546, 554-556."""

    def test_generate_lessons_skips_already_generated(self, tmp_path):
        """Test that already-generated lessons are skipped (line 546)."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    tracker.patterns = {
                        "fp1": {
                            "lesson_generated": True,  # Already generated
                            "count": 10,
                            "source": "test",
                            "category": "api",
                            "severity": "high",
                            "sample_message": "API 403 error",
                            "sample_context": "keyword lookup",
                        }
                    }
                    lessons = tracker.generate_lessons(min_occurrences=3)
                    assert len(lessons) == 0

    def test_generate_lessons_writes_to_file(self, tmp_path):
        """Test generate_lessons actually writes lessons (lines 554-556)."""
        lessons_file = tmp_path / "references" / "lessons-learned.md"
        lessons_file.parent.mkdir(parents=True, exist_ok=True)
        lessons_file.write_text("# Lessons Learned\n\n*Existing content.*\n")
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch.object(error_tracker, 'LESSONS_FILE', lessons_file):
                        tracker = ErrorTracker()
                        tracker.patterns = {
                            "fp1": {
                                "lesson_generated": False,
                                "count": 5,
                                "source": "test_api",
                                "category": "api",
                                "severity": "high",
                                "sample_message": "API 403 forbidden error",
                                "sample_context": "keyword lookup",
                                "first_seen": datetime.now().isoformat(),
                                "last_seen": datetime.now().isoformat(),
                                "occurrences": [],
                            }
                        }
                        lessons = tracker.generate_lessons(min_occurrences=3, dry_run=False)
                        assert len(lessons) == 1
                        assert lessons[0]["title"] == "Handle API Authentication Errors"
                        # Verify file was updated
                        content = lessons_file.read_text()
                        assert "Auto-Generated Lessons" in content
                        assert "Handle API Authentication Errors" in content

    def test_generate_lessons_dry_run(self, tmp_path):
        """Test generate_lessons dry_run mode."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    tracker.patterns = {
                        "fp1": {
                            "lesson_generated": False,
                            "count": 5,
                            "source": "test_api",
                            "category": "validation",
                            "severity": "medium",
                            "sample_message": "Missing required field",
                            "sample_context": "schema check",
                        }
                    }
                    lessons = tracker.generate_lessons(min_occurrences=3, dry_run=True)
                    assert len(lessons) == 1
                    # Pattern should NOT be marked as generated
                    assert tracker.patterns["fp1"]["lesson_generated"] is False

    def test_generate_lessons_all_categories(self, tmp_path):
        """Test lesson generation for all error categories."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    categories = {
                        "api_timeout": {"category": "api", "sample_message": "Connection timeout after 30s"},
                        "api_generic": {"category": "api", "sample_message": "API returned 500"},
                        "validation": {"category": "validation", "sample_message": "Missing required field"},
                        "file": {"category": "file", "sample_message": "File not found"},
                        "content": {"category": "content", "sample_message": "Invalid keyword format"},
                        "test": {"category": "test", "sample_message": "Assertion error in mock"},
                        "process": {"category": "process", "sample_message": "Phase 2 brief generation failed"},
                        "unknown": {"category": "unknown", "sample_message": "Something weird happened"},
                    }
                    
                    for fp, info in categories.items():
                        tracker.patterns[fp] = {
                            "lesson_generated": False,
                            "count": 5,
                            "source": "test_source",
                            "category": info["category"],
                            "severity": "medium",
                            "sample_message": info["sample_message"],
                            "sample_context": "",
                        }
                    
                    lessons = tracker.generate_lessons(min_occurrences=3, dry_run=True)
                    assert len(lessons) == 8
                    titles = [l["title"] for l in lessons]
                    assert "Handle API Timeouts" in titles
                    assert "Handle API Errors Gracefully" in titles
                    assert "Improve Input Validation" in titles
                    assert "Handle File Operations Safely" in titles
                    assert "Improve Content Processing" in titles
                    assert "Fix Recurring Test Failures" in titles
                    assert "Improve Process Reliability" in titles


class TestAppendLessonsToFile:
    """Tests for _append_lessons_to_file edge cases (lines 597-604)."""

    def test_append_lessons_creates_new_file(self, tmp_path):
        """Test creating lessons file when it doesn't exist."""
        lessons_file = tmp_path / "refs" / "lessons-learned.md"
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch.object(error_tracker, 'LESSONS_FILE', lessons_file):
                        tracker = ErrorTracker()
                        lessons = [{
                            "title": "Test Lesson",
                            "problem": "Test problem",
                            "solution": "Test solution",
                            "category": "test",
                            "source": "unit_test",
                            "occurrence_count": 5,
                        }]
                        tracker._append_lessons_to_file(lessons)
                        assert lessons_file.exists()
                        content = lessons_file.read_text()
                        assert "Test Lesson" in content

    def test_append_lessons_empty_list(self, tmp_path):
        """Test _append_lessons_to_file with empty list does nothing."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    tracker._append_lessons_to_file([])
                    # Should return without doing anything

    def test_append_lessons_create_file_fails(self, tmp_path):
        """Test _append_lessons_to_file when creating file fails."""
        impossible_path = tmp_path / "no_access" / "nested" / "lessons.md"
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    
                    with patch.object(error_tracker, 'LESSONS_FILE', impossible_path):
                        # Make the parent mkdir fail so file can't be created
                        original_mkdir = Path.mkdir
                        def failing_mkdir(self_path, *args, **kwargs):
                            if 'no_access' in str(self_path):
                                raise PermissionError("no access")
                            return original_mkdir(self_path, *args, **kwargs)
                        
                        with patch.object(Path, 'mkdir', failing_mkdir):
                            lessons = [{"title": "Test", "problem": "p", "solution": "s"}]
                            tracker._append_lessons_to_file(lessons)
                            # Should handle gracefully

    def test_append_lessons_write_failure(self, tmp_path):
        """Test _append_lessons_to_file when write fails but temp exists."""
        lessons_file = tmp_path / "lessons.md"
        lessons_file.write_text("# Existing\n")
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch.object(error_tracker, 'LESSONS_FILE', lessons_file):
                        tracker = ErrorTracker()
                        lessons = [{"title": "Test", "problem": "p", "solution": "s"}]
                        
                        original_open = open
                        call_count = [0]
                        def failing_write(path, *args, **kwargs):
                            if 'w' in args or kwargs.get('mode', '') == 'w':
                                if '.tmp' in str(path):
                                    call_count[0] += 1
                                    if call_count[0] == 1:
                                        raise IOError("write error")
                            return original_open(path, *args, **kwargs)
                        
                        with patch('builtins.open', side_effect=failing_write):
                            tracker._append_lessons_to_file(lessons)


class TestPrintStatsFormatting:
    """Tests for print_stats display branches (lines 661-675)."""

    def test_print_stats_full_output(self, tmp_path, capsys):
        """Test print_stats with all sections populated."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    
                    # Add errors with different severities and categories
                    now = datetime.now()
                    for sev in ["critical", "high", "medium", "low"]:
                        entry = ErrorEntry("source1", f"{sev} error", category="api", severity=sev)
                        entry.timestamp = now.isoformat()
                        tracker.errors.append(entry)
                    
                    for cat in ["api", "validation", "file"]:
                        entry = ErrorEntry("source2", f"{cat} error", category=cat, severity="medium")
                        entry.timestamp = now.isoformat()
                        tracker.errors.append(entry)
                    
                    # Add pattern
                    tracker.patterns["fp1"] = {
                        "lesson_generated": True, "count": 5,
                        "source": "test", "category": "api", "severity": "high",
                        "sample_message": "test"
                    }
                    tracker.patterns["fp2"] = {
                        "lesson_generated": False, "count": 5,
                        "source": "test", "category": "api", "severity": "high",
                        "sample_message": "test"
                    }
                    
                    tracker.print_stats()
                    
                    captured = capsys.readouterr()
                    assert "ERROR TRACKER STATISTICS" in captured.out
                    assert "critical:" in captured.out
                    assert "By Severity:" in captured.out
                    assert "By Category:" in captured.out
                    assert "By Source:" in captured.out
                    assert "Lessons generated: 1" in captured.out
                    assert "Patterns needing attention: 1" in captured.out


class TestPrintAnalysisFormatting:
    """Tests for print_analysis display branches (lines 688-705)."""

    def test_print_analysis_all_sections(self, tmp_path, capsys):
        """Test print_analysis with critical, recurring, and surge patterns."""
        now = datetime.now()
        recent = now - timedelta(hours=1)
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    
                    # Add critical pattern
                    tracker.patterns["critical_fp"] = {
                        "count": 10,
                        "source": "critical_source",
                        "category": "api",
                        "severity": "critical",
                        "sample_message": "Fatal crash in API handler",
                        "sample_context": "main loop",
                        "first_seen": (now - timedelta(days=10)).isoformat(),
                        "last_seen": now.isoformat(),
                        "occurrences": [
                            {"timestamp": recent.isoformat(), "context": "test"}
                            for _ in range(8)
                        ],
                        "lesson_generated": False,
                    }
                    
                    # Add recurring pattern (count >= 5)
                    tracker.patterns["recurring_fp"] = {
                        "count": 7,
                        "source": "validation_source",
                        "category": "validation",
                        "severity": "high",
                        "sample_message": "Schema validation failed for input",
                        "sample_context": "form submit",
                        "first_seen": (now - timedelta(days=5)).isoformat(),
                        "last_seen": now.isoformat(),
                        "occurrences": [
                            {"timestamp": recent.isoformat(), "context": "test"}
                            for _ in range(5)
                        ],
                        "lesson_generated": False,
                    }
                    
                    tracker.print_analysis()
                    
                    captured = capsys.readouterr()
                    assert "ERROR PATTERN ANALYSIS" in captured.out
                    assert "[CRITICAL ERRORS]" in captured.out
                    assert "Fatal crash" in captured.out
                    assert "[RECURRING PATTERNS]" in captured.out
                    assert "[RECENT SURGE]" in captured.out
                    assert "[BY CATEGORY]" in captured.out

    def test_print_analysis_empty(self, tmp_path, capsys):
        """Test print_analysis with no patterns."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    tracker.print_analysis()
                    
                    captured = capsys.readouterr()
                    assert "ERROR PATTERN ANALYSIS" in captured.out
                    assert "[BY CATEGORY]" in captured.out


class TestMainCLI:
    """Tests for main() CLI function (lines 711-804)."""

    def test_main_log_command(self, tmp_path):
        """Test main() with 'log' command."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker', 'log', '--source', 'test_unit', '--error', 'Test error msg']):
                        result = main()
                        assert result == 0

    def test_main_log_with_all_options(self, tmp_path):
        """Test main() log with category, severity, context, stack-trace."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', [
                        'error_tracker', 'log',
                        '--source', 'test_api',
                        '--error', 'API timeout',
                        '--context', 'keyword lookup',
                        '--category', 'api',
                        '--severity', 'high',
                        '--stack-trace', 'line 42: timeout',
                    ]):
                        result = main()
                        assert result == 0

    def test_main_analyze_command(self, tmp_path, capsys):
        """Test main() with 'analyze' command."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker', 'analyze']):
                        result = main()
                        assert result == 0
                        captured = capsys.readouterr()
                        assert "ERROR PATTERN ANALYSIS" in captured.out

    def test_main_stats_command(self, tmp_path, capsys):
        """Test main() with 'stats' command."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker', 'stats']):
                        result = main()
                        assert result == 0
                        captured = capsys.readouterr()
                        assert "ERROR TRACKER STATISTICS" in captured.out

    def test_main_generate_lessons_command(self, tmp_path, capsys):
        """Test main() with 'generate-lessons' command."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker', 'generate-lessons', '--dry-run', '--min-occurrences', '2']):
                        result = main()
                        assert result == 0
                        captured = capsys.readouterr()
                        assert "No new lessons to generate" in captured.out

    def test_main_generate_lessons_with_results(self, tmp_path, capsys):
        """Test main() generate-lessons when there are patterns to learn from."""
        patterns_file = tmp_path / "patterns.json"
        patterns_data = {
            "fp1": {
                "lesson_generated": False,
                "count": 5,
                "source": "test_api",
                "category": "api",
                "severity": "high",
                "sample_message": "API 403 error occurred",
                "sample_context": "keyword lookup",
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "occurrences": [],
            }
        }
        patterns_file.write_text(json.dumps(patterns_data))
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', patterns_file):
                    with patch('sys.argv', ['error_tracker', 'generate-lessons', '--dry-run']):
                        result = main()
                        assert result == 0
                        captured = capsys.readouterr()
                        assert "Generated 1 lessons" in captured.out

    def test_main_clear_command(self, tmp_path, capsys):
        """Test main() with 'clear' command."""
        # Create some old errors
        old_time = (datetime.now() - timedelta(days=60)).isoformat()
        recent_time = datetime.now().isoformat()
        error_data = {
            "errors": [
                {"source": "old", "error_message": "old error", "timestamp": old_time,
                 "category": "test", "severity": "low", "context": "", "stack_trace": "",
                 "metadata": {}, "fingerprint": "abc123"},
                {"source": "new", "error_message": "new error", "timestamp": recent_time,
                 "category": "test", "severity": "low", "context": "", "stack_trace": "",
                 "metadata": {}, "fingerprint": "def456"},
            ]
        }
        log_file = tmp_path / "error_log.json"
        log_file.write_text(json.dumps(error_data))
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker', 'clear', '--days', '30']):
                        result = main()
                        assert result == 0
                        captured = capsys.readouterr()
                        assert "Cleared 1 errors" in captured.out

    def test_main_clear_with_invalid_timestamps(self, tmp_path, capsys):
        """Test main() clear with errors that have invalid timestamps."""
        error_data = {
            "errors": [
                {"source": "bad_ts", "error_message": "bad timestamp", "timestamp": "not-a-date",
                 "category": "test", "severity": "low", "context": "", "stack_trace": "",
                 "metadata": {}, "fingerprint": "abc123"},
            ]
        }
        log_file = tmp_path / "error_log.json"
        log_file.write_text(json.dumps(error_data))
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', log_file):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker', 'clear', '--days', '30']):
                        result = main()
                        assert result == 0
                        captured = capsys.readouterr()
                        assert "Kept 1 errors with invalid timestamps" in captured.out

    def test_main_no_command(self, tmp_path):
        """Test main() with no command shows help."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker']):
                        result = main()
                        assert result == 1

    def test_main_verbose_flag(self, tmp_path):
        """Test main() with --verbose flag."""
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    with patch('sys.argv', ['error_tracker', '-v', 'stats']):
                        result = main()
                        assert result == 0


class TestAnalyzePatternsEdgeCases:
    """Tests for analyze_patterns edge cases."""

    def test_analyze_patterns_with_recent_surge(self, tmp_path):
        """Test analyze_patterns detects recent surges correctly."""
        now = datetime.now()
        recent = now - timedelta(hours=6)
        old = now - timedelta(days=14)
        
        with patch.object(error_tracker, 'ERROR_LOG_FILE', tmp_path / "error_log.json"):
            with patch.object(error_tracker, 'ERROR_LOG_DIR', tmp_path):
                with patch.object(error_tracker, 'PATTERNS_FILE', tmp_path / "patterns.json"):
                    tracker = ErrorTracker()
                    
                    tracker.patterns["surge_fp"] = {
                        "count": 4,
                        "source": "api_client",
                        "category": "api",
                        "severity": "high",
                        "sample_message": "Rate limit exceeded",
                        "occurrences": [
                            {"timestamp": old.isoformat(), "context": "old"},
                            {"timestamp": recent.isoformat(), "context": "recent1"},
                            {"timestamp": recent.isoformat(), "context": "recent2"},
                            {"timestamp": recent.isoformat(), "context": "recent3"},
                        ],
                    }
                    
                    analysis = tracker.analyze_patterns()
                    assert len(analysis["recent_surge"]) == 1


class TestErrorEntryEdgeCases:
    """Additional ErrorEntry tests."""

    def test_normalize_message_removes_timestamps(self):
        """Test that _normalize_message removes timestamps."""
        entry = ErrorEntry("test", "Error at 2026-02-08 12:00:00 in module")
        normalized = entry._normalize_message()
        assert "2026-02-08" not in normalized

    def test_normalize_message_removes_paths(self):
        """Test that _normalize_message replaces file paths."""
        entry = ErrorEntry("test", "Error in /usr/local/lib/python3.14/site.py")
        normalized = entry._normalize_message()
        assert "/PATH" in normalized

    def test_normalize_message_removes_line_numbers(self):
        """Test that _normalize_message replaces line numbers."""
        entry = ErrorEntry("test", "Error at line 42")
        normalized = entry._normalize_message()
        assert "line n" in normalized.lower()
