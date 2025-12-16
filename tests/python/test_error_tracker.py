"""
Tests for the self-learning error tracker.
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

from error_tracker import ErrorEntry, ErrorTracker, ERROR_CATEGORIES


class TestErrorEntry:
    """Tests for the ErrorEntry class."""

    def test_create_error_entry(self):
        """Test basic error entry creation."""
        entry = ErrorEntry(
            source="test_source",
            error_message="Test error message",
            context="test context",
            category="api",
            severity="high",
        )

        assert entry.source == "test_source"
        assert entry.error_message == "Test error message"
        assert entry.context == "test context"
        assert entry.category == "api"
        assert entry.severity == "high"
        assert entry.fingerprint is not None
        assert entry.timestamp is not None

    def test_fingerprint_consistency(self):
        """Test that same errors generate same fingerprint."""
        entry1 = ErrorEntry(
            source="test",
            error_message="HTTP 403 error",
            category="api",
        )
        entry2 = ErrorEntry(
            source="test",
            error_message="HTTP 403 error",
            category="api",
        )

        assert entry1.fingerprint == entry2.fingerprint

    def test_fingerprint_differs_for_different_errors(self):
        """Test that different errors generate different fingerprints."""
        entry1 = ErrorEntry(
            source="test",
            error_message="HTTP 403 error",
            category="api",
        )
        entry2 = ErrorEntry(
            source="test",
            error_message="HTTP 500 error",
            category="api",
        )

        assert entry1.fingerprint != entry2.fingerprint

    def test_to_dict(self):
        """Test serialization to dictionary."""
        entry = ErrorEntry(
            source="test",
            error_message="Test error",
            context="ctx",
            category="api",
            severity="high",
            stack_trace="stack",
            metadata={"key": "value"},
        )

        data = entry.to_dict()

        assert data["source"] == "test"
        assert data["error_message"] == "Test error"
        assert data["context"] == "ctx"
        assert data["category"] == "api"
        assert data["severity"] == "high"
        assert data["stack_trace"] == "stack"
        assert data["metadata"] == {"key": "value"}
        assert "fingerprint" in data
        assert "timestamp" in data

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "source": "test",
            "error_message": "Test error",
            "context": "ctx",
            "category": "api",
            "severity": "high",
            "stack_trace": "stack",
            "metadata": {"key": "value"},
            "fingerprint": "abc123",
            "timestamp": "2025-12-01T10:00:00",
        }

        entry = ErrorEntry.from_dict(data)

        assert entry.source == "test"
        assert entry.error_message == "Test error"
        assert entry.fingerprint == "abc123"
        assert entry.timestamp == "2025-12-01T10:00:00"

    def test_normalize_message_removes_timestamps(self):
        """Test that timestamp normalization works."""
        entry = ErrorEntry(
            source="test",
            error_message="Error at 2025-12-01 10:30:45 in file.py",
            category="api",
        )

        normalized = entry._normalize_message()
        assert "2025-12-01" not in normalized
        assert "10:30:45" not in normalized


class TestErrorTracker:
    """Tests for the ErrorTracker class."""

    @pytest.fixture
    def temp_tracker(self, tmp_path, monkeypatch):
        """Create an error tracker with temp directories."""
        error_dir = tmp_path / "logs" / "errors"
        error_dir.mkdir(parents=True)

        # Monkeypatch the paths
        import error_tracker as et
        monkeypatch.setattr(et, 'ERROR_LOG_DIR', error_dir)
        monkeypatch.setattr(et, 'ERROR_LOG_FILE', error_dir / "error_log.json")
        monkeypatch.setattr(et, 'PATTERNS_FILE', error_dir / "patterns.json")
        monkeypatch.setattr(et, 'LESSONS_FILE', tmp_path / "lessons-learned.md")

        # Create a dummy lessons file
        (tmp_path / "lessons-learned.md").write_text("# Lessons Learned\n\n")

        tracker = ErrorTracker(verbose=False)
        return tracker

    def test_add_error(self, temp_tracker):
        """Test adding an error."""
        entry = temp_tracker.add_error(
            source="test",
            error_message="Test error",
            context="test context",
        )

        assert entry is not None
        assert len(temp_tracker.errors) == 1
        assert temp_tracker.errors[0].source == "test"

    def test_add_multiple_errors(self, temp_tracker):
        """Test adding multiple errors."""
        temp_tracker.add_error(source="test1", error_message="Error 1")
        temp_tracker.add_error(source="test2", error_message="Error 2")
        temp_tracker.add_error(source="test3", error_message="Error 3")

        assert len(temp_tracker.errors) == 3

    def test_auto_detect_category_api(self, temp_tracker):
        """Test auto-detection of API category."""
        entry = temp_tracker.add_error(
            source="test",
            error_message="HTTP 403 Forbidden error from API",
        )

        assert entry.category == "api"

    def test_auto_detect_category_validation(self, temp_tracker):
        """Test auto-detection of validation category."""
        entry = temp_tracker.add_error(
            source="test",
            error_message="Missing required field in schema",
        )

        assert entry.category == "validation"

    def test_auto_detect_category_file(self, temp_tracker):
        """Test auto-detection of file category."""
        entry = temp_tracker.add_error(
            source="test",
            error_message="File not found: output.md",
        )

        assert entry.category == "file"

    def test_auto_detect_severity_critical(self, temp_tracker):
        """Test auto-detection of critical severity."""
        entry = temp_tracker.add_error(
            source="test",
            error_message="FATAL: System crash occurred",
        )

        assert entry.severity == "critical"

    def test_auto_detect_severity_high_for_tests(self, temp_tracker):
        """Test that test failures default to high severity."""
        entry = temp_tracker.add_error(
            source="test_something",
            error_message="Assertion failed",
        )

        assert entry.severity == "high"

    def test_pattern_tracking(self, temp_tracker):
        """Test that patterns are tracked for recurring errors."""
        # Add same error 3 times
        for _ in range(3):
            temp_tracker.add_error(
                source="test",
                error_message="Repeated error",
                category="api",
            )

        # Check patterns
        assert len(temp_tracker.patterns) == 1
        fingerprint = list(temp_tracker.patterns.keys())[0]
        assert temp_tracker.patterns[fingerprint]["count"] == 3

    def test_get_stats(self, temp_tracker):
        """Test statistics generation."""
        temp_tracker.add_error(source="test1", error_message="Error 1", category="api", severity="high")
        temp_tracker.add_error(source="test2", error_message="Error 2", category="file", severity="medium")
        temp_tracker.add_error(source="test1", error_message="Error 3", category="api", severity="high")

        stats = temp_tracker.get_stats()

        assert stats["total_errors"] == 3
        assert stats["by_category"]["api"] == 2
        assert stats["by_category"]["file"] == 1
        assert stats["by_severity"]["high"] == 2
        assert stats["by_severity"]["medium"] == 1

    def test_analyze_patterns(self, temp_tracker):
        """Test pattern analysis."""
        # Add recurring error
        for _ in range(5):
            temp_tracker.add_error(
                source="test",
                error_message="Recurring API error",
                category="api",
                severity="high",
            )

        # Add non-recurring error
        temp_tracker.add_error(
            source="test",
            error_message="One-off error",
            category="file",
        )

        analysis = temp_tracker.analyze_patterns()

        assert len(analysis["recurring"]) == 1
        assert analysis["recurring"][0]["count"] == 5

    def test_generate_lessons_dry_run(self, temp_tracker):
        """Test lesson generation in dry run mode."""
        # Add enough errors to trigger lesson generation
        for _ in range(4):
            temp_tracker.add_error(
                source="test_api",
                error_message="HTTP 403 error from Ahrefs API",
                category="api",
            )

        lessons = temp_tracker.generate_lessons(min_occurrences=3, dry_run=True)

        assert len(lessons) >= 1
        assert lessons[0]["category"] == "api"
        # Pattern should not be marked as generated in dry run
        fingerprint = list(temp_tracker.patterns.keys())[0]
        assert temp_tracker.patterns[fingerprint]["lesson_generated"] == False

    def test_persistence(self, temp_tracker, tmp_path, monkeypatch):
        """Test that errors persist across tracker instances."""
        import error_tracker as et

        # Add some errors
        temp_tracker.add_error(source="test1", error_message="Persistent error 1")
        temp_tracker.add_error(source="test2", error_message="Persistent error 2")

        # Create new tracker instance (should load saved data)
        new_tracker = ErrorTracker(verbose=False)

        assert len(new_tracker.errors) == 2


class TestCategoryDetection:
    """Tests for error category detection."""

    @pytest.mark.parametrize("message,expected_category", [
        ("HTTP 403 Forbidden", "api"),
        ("Connection timeout after 30s", "api"),
        ("Rate limit exceeded", "api"),
        ("Missing required field: name", "validation"),
        ("Invalid format for date", "validation"),
        ("Schema validation failed", "validation"),
        ("File not found: test.md", "file"),
        ("Permission denied for /etc/passwd", "file"),
        ("Could not read file", "file"),
        ("HTML syntax error", "content"),
        ("CSS selector problem", "content"),
        ("Keyword not found", "content"),
        ("Test assertion failed", "test"),
        ("Import error in test module", "test"),
        ("Phase 1 generation failed", "process"),
        ("Brief conversion error", "process"),
        ("Unknown error type", "unknown"),
    ])
    def test_category_detection(self, message, expected_category):
        """Test various error messages are categorized correctly."""
        entry = ErrorEntry(
            source="test",
            error_message=message,
        )
        tracker = ErrorTracker.__new__(ErrorTracker)
        tracker._detect_category = ErrorTracker._detect_category.__get__(tracker, ErrorTracker)

        detected = tracker._detect_category(message)
        assert detected == expected_category


class TestLessonGeneration:
    """Tests for lesson generation from patterns."""

    @pytest.fixture
    def tracker_with_patterns(self, tmp_path, monkeypatch):
        """Create a tracker with pre-populated patterns."""
        error_dir = tmp_path / "logs" / "errors"
        error_dir.mkdir(parents=True)

        import error_tracker as et
        monkeypatch.setattr(et, 'ERROR_LOG_DIR', error_dir)
        monkeypatch.setattr(et, 'ERROR_LOG_FILE', error_dir / "error_log.json")
        monkeypatch.setattr(et, 'PATTERNS_FILE', error_dir / "patterns.json")
        monkeypatch.setattr(et, 'LESSONS_FILE', tmp_path / "lessons-learned.md")

        # Create lessons file
        lessons_file = tmp_path / "lessons-learned.md"
        lessons_file.write_text("# Lessons Learned\n\nExisting content.\n")

        tracker = ErrorTracker(verbose=False)

        # Add patterns for different categories
        for _ in range(5):
            tracker.add_error(source="test", error_message="HTTP 403 error", category="api")
        for _ in range(5):
            tracker.add_error(source="test", error_message="Missing field", category="validation")
        for _ in range(5):
            tracker.add_error(source="test", error_message="Test assertion failed", category="test")

        return tracker, lessons_file

    def test_lesson_content_for_api_errors(self, tracker_with_patterns):
        """Test lesson content generation for API errors."""
        tracker, _ = tracker_with_patterns

        lessons = tracker.generate_lessons(dry_run=True)

        api_lessons = [l for l in lessons if l["category"] == "api"]
        assert len(api_lessons) >= 1
        assert "API" in api_lessons[0]["title"]
        assert "solution" in api_lessons[0]

    def test_lesson_content_for_validation_errors(self, tracker_with_patterns):
        """Test lesson content generation for validation errors."""
        tracker, _ = tracker_with_patterns

        lessons = tracker.generate_lessons(dry_run=True)

        validation_lessons = [l for l in lessons if l["category"] == "validation"]
        assert len(validation_lessons) >= 1
        assert "Validation" in validation_lessons[0]["title"]

    def test_lesson_file_update(self, tracker_with_patterns):
        """Test that lessons are appended to file."""
        tracker, lessons_file = tracker_with_patterns

        lessons = tracker.generate_lessons(dry_run=False)

        content = lessons_file.read_text()
        assert "Auto-Generated Lessons" in content
        assert "Existing content." in content  # Original content preserved

    def test_no_duplicate_lessons(self, tracker_with_patterns):
        """Test that lessons aren't generated twice."""
        tracker, _ = tracker_with_patterns

        lessons1 = tracker.generate_lessons(dry_run=False)
        lessons2 = tracker.generate_lessons(dry_run=False)

        # Second run should return empty (already generated)
        assert len(lessons2) == 0


class TestErrorCategories:
    """Tests for error category configuration."""

    def test_all_categories_have_keywords(self):
        """Test that all categories have at least one keyword."""
        for category, keywords in ERROR_CATEGORIES.items():
            assert len(keywords) > 0, f"Category {category} has no keywords"

    def test_category_keywords_are_lowercase(self):
        """Test that all keywords are lowercase for matching."""
        for category, keywords in ERROR_CATEGORIES.items():
            for keyword in keywords:
                assert keyword == keyword.lower(), f"Keyword '{keyword}' should be lowercase"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
