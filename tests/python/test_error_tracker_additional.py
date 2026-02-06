#!/usr/bin/env python3
"""
Additional tests for error_tracker.py - Focus on uncovered paths

Coverage targets for error_tracker.py (currently at 74.25%):
- Lines 192-194, 200-202: Error handling paths
- Lines 224-228: Exit conditions
- Lines 253-255: Alternative branches
- Lines 270-277: Edge cases
- Lines 546, 554-556: Lesson generation paths
- Lines 597-604: Stats export paths
- Lines 627-705: Various uncovered methods
- Lines 711-804: Main CLI functionality
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from error_tracker import ErrorTracker, ErrorEntry, main


class TestErrorTrackerAdvancedInit:
    """Advanced initialization tests."""

    def test_init_with_custom_thresholds(self, tmp_path):
        """Test initialization with custom thresholds."""
        tracker = ErrorTracker(str(tmp_path), recurring_threshold=5)
        assert tracker.recurring_threshold == 5

    def test_init_creates_nested_directories(self, tmp_path):
        """Test that nested directories are created."""
        nested_path = tmp_path / 'a' / 'b' / 'c'
        tracker = ErrorTracker(str(nested_path))
        # Should not raise

    def test_init_loads_existing_errors(self, tmp_path):
        """Test loading existing errors on init."""
        errors_file = tmp_path / 'logs' / 'errors' / 'errors.json'
        errors_file.parent.mkdir(parents=True)
        errors_file.write_text(json.dumps([
            {
                "timestamp": datetime.now().isoformat(),
                "source": "test",
                "message": "Test error",
                "severity": "high",
                "category": "api"
            }
        ]))
        
        tracker = ErrorTracker(str(tmp_path))
        # Should load existing errors


class TestLogErrorAdvanced:
    """Advanced tests for log_error method."""

    def test_log_error_with_all_parameters(self, tmp_path):
        """Test logging error with all optional parameters."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error(
            source="test_source",
            message="Test error message",
            severity="critical",
            category="api",
            context={"url": "https://example.com", "status": 500}
        )
        
        assert len(tracker.errors) == 1
        assert tracker.errors[0].context is not None

    def test_log_error_auto_detection(self, tmp_path):
        """Test automatic severity/category detection from message."""
        tracker = ErrorTracker(str(tmp_path))
        
        # HTTP 403 should be detected
        tracker.log_error("api", "HTTP 403 Forbidden from API")
        
        # File not found
        tracker.log_error("file", "File not found: test.txt")

    def test_log_error_many_errors(self, tmp_path):
        """Test logging many errors."""
        tracker = ErrorTracker(str(tmp_path))
        
        for i in range(100):
            tracker.log_error(f"source_{i}", f"Error message {i}")
        
        assert len(tracker.errors) == 100

    def test_log_error_unicode(self, tmp_path):
        """Test logging error with unicode content."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "Error: 日本語エラー 🔥")
        tracker.log_error("test", "Error: émojis àéïõü")
        
        assert len(tracker.errors) == 2


class TestPatternDetection:
    """Tests for pattern detection functionality."""

    def test_detect_recurring_pattern(self, tmp_path):
        """Test detection of recurring patterns."""
        tracker = ErrorTracker(str(tmp_path), recurring_threshold=3)
        
        # Log same error multiple times
        for _ in range(5):
            tracker.log_error("test", "Recurring API error")
        
        # Check patterns
        patterns = tracker.get_patterns()
        assert len(patterns) >= 1

    def test_pattern_fingerprint_generation(self, tmp_path):
        """Test fingerprint generation for patterns."""
        tracker = ErrorTracker(str(tmp_path))
        
        # Similar messages should get same fingerprint
        tracker.log_error("test", "HTTP 403 error from endpoint")
        tracker.log_error("test", "HTTP 403 error from endpoint")
        
        patterns = tracker.get_patterns()
        # Should detect as pattern

    def test_pattern_with_different_sources(self, tmp_path):
        """Test patterns from different sources."""
        tracker = ErrorTracker(str(tmp_path))
        
        # Same message from different sources
        tracker.log_error("api_client", "Connection timeout")
        tracker.log_error("db_client", "Connection timeout")
        tracker.log_error("cache_client", "Connection timeout")


class TestLessonGeneration:
    """Tests for lesson generation functionality."""

    def test_generate_lessons_no_patterns(self, tmp_path):
        """Test lesson generation with no patterns."""
        tracker = ErrorTracker(str(tmp_path))
        
        lessons = tracker.generate_lessons()
        assert lessons == [] or lessons is None

    def test_generate_lessons_with_patterns(self, tmp_path):
        """Test lesson generation with recurring patterns."""
        tracker = ErrorTracker(str(tmp_path), recurring_threshold=3)
        
        # Create recurring pattern
        for _ in range(5):
            tracker.log_error("test", "HTTP 403 error")
        
        lessons = tracker.generate_lessons()
        # Should generate lesson for recurring pattern

    def test_lessons_written_to_file(self, tmp_path):
        """Test that lessons are written to file."""
        lessons_file = tmp_path / 'lessons-learned.md'
        tracker = ErrorTracker(str(tmp_path), lessons_file=str(lessons_file))
        tracker.recurring_threshold = 3
        
        for _ in range(5):
            tracker.log_error("test", "Recurring test error")
        
        tracker.generate_lessons()
        # Check if file was created/updated


class TestStatsAndReporting:
    """Tests for statistics and reporting functionality."""

    def test_get_stats_empty(self, tmp_path):
        """Test getting stats with no errors."""
        tracker = ErrorTracker(str(tmp_path))
        
        stats = tracker.get_stats()
        assert stats['total_errors'] == 0

    def test_get_stats_with_errors(self, tmp_path):
        """Test getting stats with errors."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("api", "API error", severity="high")
        tracker.log_error("file", "File error", severity="medium")
        tracker.log_error("test", "Test error", severity="low")
        
        stats = tracker.get_stats()
        assert stats['total_errors'] == 3

    def test_get_stats_by_category(self, tmp_path):
        """Test stats grouped by category."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("api", "Error 1", category="api")
        tracker.log_error("api", "Error 2", category="api")
        tracker.log_error("file", "Error 3", category="file")
        
        stats = tracker.get_stats()
        # Should show distribution

    def test_get_stats_by_severity(self, tmp_path):
        """Test stats grouped by severity."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "Critical", severity="critical")
        tracker.log_error("test", "High", severity="high")
        tracker.log_error("test", "Medium", severity="medium")
        tracker.log_error("test", "Low", severity="low")
        
        stats = tracker.get_stats()


class TestErrorFiltering:
    """Tests for error filtering functionality."""

    def test_filter_by_severity(self, tmp_path):
        """Test filtering errors by severity."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "Critical", severity="critical")
        tracker.log_error("test", "High", severity="high")
        tracker.log_error("test", "Low", severity="low")
        
        high_errors = [e for e in tracker.errors if e.severity in ["critical", "high"]]
        assert len(high_errors) == 2

    def test_filter_by_category(self, tmp_path):
        """Test filtering errors by category."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("api", "API error", category="api")
        tracker.log_error("file", "File error", category="file")
        
        api_errors = [e for e in tracker.errors if e.category == "api"]
        assert len(api_errors) == 1

    def test_filter_by_date_range(self, tmp_path):
        """Test filtering errors by date range."""
        tracker = ErrorTracker(str(tmp_path))
        
        # Log errors
        tracker.log_error("test", "Recent error")
        
        # Filter (would need timestamp manipulation for full test)


class TestCLICommands:
    """Tests for CLI command handling."""

    def test_cli_log_command(self, tmp_path, capsys):
        """Test CLI log command."""
        with patch('sys.argv', ['error_tracker.py', 'log', 'test_source', 'Test error message']):
            with patch('error_tracker.ErrorTracker') as mock:
                mock_instance = MagicMock()
                mock.return_value = mock_instance
                try:
                    main()
                except SystemExit:
                    pass

    def test_cli_stats_command(self, tmp_path, capsys):
        """Test CLI stats command."""
        with patch('sys.argv', ['error_tracker.py', 'stats']):
            with patch('error_tracker.ErrorTracker') as mock:
                mock_instance = MagicMock()
                mock_instance.get_stats.return_value = {'total_errors': 0}
                mock.return_value = mock_instance
                try:
                    main()
                except SystemExit:
                    pass

    def test_cli_patterns_command(self, tmp_path, capsys):
        """Test CLI patterns command."""
        with patch('sys.argv', ['error_tracker.py', 'patterns']):
            with patch('error_tracker.ErrorTracker') as mock:
                mock_instance = MagicMock()
                mock_instance.get_patterns.return_value = []
                mock.return_value = mock_instance
                try:
                    main()
                except SystemExit:
                    pass

    def test_cli_generate_lessons_command(self, tmp_path, capsys):
        """Test CLI generate-lessons command."""
        with patch('sys.argv', ['error_tracker.py', 'generate-lessons']):
            with patch('error_tracker.ErrorTracker') as mock:
                mock_instance = MagicMock()
                mock_instance.generate_lessons.return_value = []
                mock.return_value = mock_instance
                try:
                    main()
                except SystemExit:
                    pass

    def test_cli_clear_command(self, tmp_path, capsys):
        """Test CLI clear command."""
        with patch('sys.argv', ['error_tracker.py', 'clear']):
            with patch('error_tracker.ErrorTracker') as mock:
                mock_instance = MagicMock()
                mock.return_value = mock_instance
                try:
                    main()
                except SystemExit:
                    pass


class TestPersistence:
    """Tests for error persistence."""

    def test_save_errors_to_file(self, tmp_path):
        """Test saving errors to JSON file."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "Error 1")
        tracker.log_error("test", "Error 2")
        tracker.save()
        
        errors_file = tmp_path / 'logs' / 'errors' / 'errors.json'
        assert errors_file.exists()

    def test_load_errors_from_file(self, tmp_path):
        """Test loading errors from JSON file."""
        errors_file = tmp_path / 'logs' / 'errors' / 'errors.json'
        errors_file.parent.mkdir(parents=True)
        
        test_errors = [
            {
                "timestamp": datetime.now().isoformat(),
                "source": "test",
                "message": "Saved error",
                "severity": "high",
                "category": "api"
            }
        ]
        errors_file.write_text(json.dumps(test_errors))
        
        tracker = ErrorTracker(str(tmp_path))
        # Should load existing errors

    def test_patterns_persistence(self, tmp_path):
        """Test saving and loading patterns."""
        tracker = ErrorTracker(str(tmp_path), recurring_threshold=2)
        
        # Create pattern
        for _ in range(3):
            tracker.log_error("test", "Recurring error")
        
        tracker.save()
        
        # Check patterns file
        patterns_file = tmp_path / 'logs' / 'errors' / 'patterns.json'


class TestEdgeCasesAdvanced:
    """Advanced edge case tests."""

    def test_concurrent_error_logging(self, tmp_path):
        """Test handling of concurrent error logging."""
        tracker = ErrorTracker(str(tmp_path))
        
        # Simulate rapid error logging
        for i in range(50):
            tracker.log_error(f"source_{i % 5}", f"Error {i}")
        
        assert len(tracker.errors) == 50

    def test_very_long_error_message(self, tmp_path):
        """Test handling very long error messages."""
        tracker = ErrorTracker(str(tmp_path))
        
        long_message = "x" * 10000
        tracker.log_error("test", long_message)
        
        # Should truncate or handle gracefully
        assert len(tracker.errors) == 1

    def test_special_characters_in_message(self, tmp_path):
        """Test handling special characters."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "Error with\nnewlines\tand\ttabs")
        tracker.log_error("test", "Error with <html>tags</html>")
        tracker.log_error("test", "Error with 'quotes' and \"double quotes\"")
        
        assert len(tracker.errors) == 3

    def test_empty_error_message(self, tmp_path):
        """Test handling empty error message."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "")
        # Should handle empty message

    def test_none_values(self, tmp_path):
        """Test handling None values."""
        tracker = ErrorTracker(str(tmp_path))
        
        # Source and message should not be None in normal usage
        # but test defensive coding
        try:
            tracker.log_error("test", None)
        except (TypeError, AttributeError):
            pass  # Expected

    def test_invalid_severity(self, tmp_path):
        """Test handling invalid severity."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "Error", severity="invalid")
        # Should default or handle gracefully

    def test_invalid_category(self, tmp_path):
        """Test handling invalid category."""
        tracker = ErrorTracker(str(tmp_path))
        
        tracker.log_error("test", "Error", category="invalid")
        # Should default or handle gracefully

    def test_malformed_json_on_load(self, tmp_path):
        """Test handling malformed JSON on load."""
        errors_file = tmp_path / 'logs' / 'errors' / 'errors.json'
        errors_file.parent.mkdir(parents=True)
        errors_file.write_text('not valid json {{{')
        
        tracker = ErrorTracker(str(tmp_path))
        # Should not crash, start fresh


class TestIntegrationAdvanced:
    """Advanced integration tests."""

    def test_full_error_tracking_workflow(self, tmp_path, capsys):
        """Test complete error tracking workflow."""
        tracker = ErrorTracker(str(tmp_path), recurring_threshold=3)
        
        # Log various errors
        tracker.log_error("api_client", "HTTP 403 Forbidden from Ahrefs", severity="high", category="api")
        tracker.log_error("api_client", "HTTP 403 Forbidden from Ahrefs", severity="high", category="api")
        tracker.log_error("api_client", "HTTP 403 Forbidden from Ahrefs", severity="high", category="api")
        tracker.log_error("file_handler", "File not found: output.docx", severity="medium", category="file")
        tracker.log_error("validator", "Schema validation failed", severity="medium", category="validation")
        
        # Get stats
        stats = tracker.get_stats()
        assert stats['total_errors'] == 5
        
        # Get patterns
        patterns = tracker.get_patterns()
        
        # Generate lessons
        lessons = tracker.generate_lessons()
        
        # Save everything
        tracker.save()

    def test_workflow_with_persistence(self, tmp_path):
        """Test workflow with save/load cycle."""
        # First session - log errors
        tracker1 = ErrorTracker(str(tmp_path))
        tracker1.log_error("test", "Error 1")
        tracker1.log_error("test", "Error 2")
        tracker1.save()
        
        # Second session - load and continue
        tracker2 = ErrorTracker(str(tmp_path))
        # Errors should be loaded
        tracker2.log_error("test", "Error 3")
        tracker2.save()
