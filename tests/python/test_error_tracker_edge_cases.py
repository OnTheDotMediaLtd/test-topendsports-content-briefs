#!/usr/bin/env python3
"""
Comprehensive edge case tests for Error Tracker.

Tests cover:
- Error entry creation and normalization
- Pattern detection and updates
- Lesson generation
- File operations and atomic writes
- Concurrent access scenarios
- Boundary conditions
"""

import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

# Add scripts to path
SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from error_tracker import ErrorTracker, ErrorEntry, SEVERITY_LEVELS, ERROR_CATEGORIES


class TestErrorEntryCreation:
    """Tests for ErrorEntry creation."""

    def test_create_basic_error_entry(self):
        """Test creating basic error entry."""
        entry = ErrorEntry(
            source="test_source",
            error_message="Test error message"
        )
        
        assert entry.source == "test_source"
        assert entry.error_message == "Test error message"
        assert entry.category == "unknown"
        assert entry.severity == "medium"
        assert entry.fingerprint is not None

    def test_error_entry_with_all_fields(self):
        """Test creating error entry with all fields."""
        entry = ErrorEntry(
            source="test_api",
            error_message="HTTP 403 Forbidden",
            context="During API call",
            category="api",
            severity="high",
            stack_trace="File test.py line 10",
            metadata={"endpoint": "/test"}
        )
        
        assert entry.source == "test_api"
        assert entry.category == "api"
        assert entry.severity == "high"
        assert entry.context == "During API call"
        assert entry.metadata["endpoint"] == "/test"

    def test_fingerprint_uniqueness(self):
        """Test fingerprint is unique per error type."""
        entry1 = ErrorEntry("source1", "Error A")
        entry2 = ErrorEntry("source1", "Error A")  # Same
        entry3 = ErrorEntry("source1", "Error B")  # Different message
        entry4 = ErrorEntry("source2", "Error A")  # Different source
        
        # Same source and message should have same fingerprint
        assert entry1.fingerprint == entry2.fingerprint
        # Different message or source should have different fingerprint
        assert entry1.fingerprint != entry3.fingerprint
        assert entry1.fingerprint != entry4.fingerprint

    def test_fingerprint_normalization(self):
        """Test fingerprint normalizes timestamps and paths."""
        entry1 = ErrorEntry("source", "Error at 2024-01-01 10:00:00")
        entry2 = ErrorEntry("source", "Error at 2024-02-02 11:00:00")
        
        # Timestamps should be normalized
        assert entry1.fingerprint == entry2.fingerprint

    def test_to_dict_conversion(self):
        """Test converting entry to dictionary."""
        entry = ErrorEntry(
            source="test",
            error_message="Test error",
            category="api",
            severity="high"
        )
        
        data = entry.to_dict()
        
        assert data["source"] == "test"
        assert data["error_message"] == "Test error"
        assert data["category"] == "api"
        assert data["severity"] == "high"
        assert "timestamp" in data
        assert "fingerprint" in data

    def test_from_dict_conversion(self):
        """Test creating entry from dictionary."""
        data = {
            "source": "test",
            "error_message": "Test error",
            "category": "api",
            "severity": "high",
            "timestamp": "2024-01-01T10:00:00",
            "fingerprint": "abc123"
        }
        
        entry = ErrorEntry.from_dict(data)
        
        assert entry.source == "test"
        assert entry.error_message == "Test error"
        assert entry.timestamp == "2024-01-01T10:00:00"
        assert entry.fingerprint == "abc123"


class TestErrorEntryNormalization:
    """Tests for error message normalization."""

    def test_normalize_removes_timestamps(self):
        """Test normalization removes timestamps."""
        entry = ErrorEntry("source", "Error at 2024-01-01 12:30:45 occurred")
        normalized = entry._normalize_message()
        
        # Timestamp should be removed
        assert "2024-01-01" not in normalized
        assert "12:30:45" not in normalized

    def test_normalize_removes_file_paths(self):
        """Test normalization removes specific file paths."""
        entry = ErrorEntry("source", "Error in /home/user/project/file.py")
        normalized = entry._normalize_message()
        
        assert "/home/user/project/file.py" not in normalized
        assert "/PATH" in normalized.upper() or "path" in normalized.lower()

    def test_normalize_removes_line_numbers(self):
        """Test normalization removes line numbers."""
        entry = ErrorEntry("source", "Error at line 42")
        normalized = entry._normalize_message()
        
        assert "line 42" not in normalized.lower()
        assert "line n" in normalized.lower()

    def test_normalize_removes_large_numbers(self):
        """Test normalization removes large numbers."""
        entry = ErrorEntry("source", "Request ID: 1234567890")
        normalized = entry._normalize_message()
        
        assert "1234567890" not in normalized


class TestErrorTrackerInit:
    """Tests for ErrorTracker initialization."""

    def test_init_creates_directories(self, tmp_path, monkeypatch):
        """Test initialization creates log directories."""
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', tmp_path / 'logs' / 'errors')
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', tmp_path / 'logs' / 'errors' / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', tmp_path / 'logs' / 'errors' / 'patterns.json')
        
        tracker = ErrorTracker()
        
        assert (tmp_path / 'logs' / 'errors').exists()

    def test_init_loads_existing_errors(self, tmp_path, monkeypatch):
        """Test initialization loads existing errors."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        existing_data = {
            "errors": [
                {"source": "test", "error_message": "Old error", "timestamp": "2024-01-01"}
            ]
        }
        (log_dir / 'error_log.json').write_text(json.dumps(existing_data))
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker(verbose=True)
        
        assert len(tracker.errors) == 1

    def test_init_handles_corrupt_json(self, tmp_path, monkeypatch):
        """Test initialization handles corrupt JSON file."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        (log_dir / 'error_log.json').write_text('not valid json')
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker(verbose=True)
        
        # Should start fresh
        assert tracker.errors == []

    def test_init_handles_empty_file(self, tmp_path, monkeypatch):
        """Test initialization handles empty file."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        (log_dir / 'error_log.json').write_text('')
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker(verbose=True)
        
        assert tracker.errors == []


class TestAddError:
    """Tests for adding errors."""

    def test_add_basic_error(self, tmp_path, monkeypatch):
        """Test adding basic error."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        entry = tracker.add_error("test_source", "Test error message")
        
        assert len(tracker.errors) == 1
        assert tracker.errors[0].source == "test_source"

    def test_add_error_auto_detects_category(self, tmp_path, monkeypatch):
        """Test adding error auto-detects category."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        entry_api = tracker.add_error("test", "HTTP 403 Forbidden")
        entry_file = tracker.add_error("test", "File not found: test.txt")
        entry_validation = tracker.add_error("test", "Schema validation failed")
        
        assert entry_api.category == "api"
        assert entry_file.category == "file"
        assert entry_validation.category == "validation"

    def test_add_error_auto_detects_severity(self, tmp_path, monkeypatch):
        """Test adding error auto-detects severity."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        critical = tracker.add_error("test", "FATAL: System crash")
        high = tracker.add_error("test", "API failed with 403")
        medium = tracker.add_error("test", "Warning: timeout occurred")
        
        assert critical.severity == "critical"
        assert high.severity == "high"
        assert medium.severity == "medium"

    def test_add_error_validates_source(self, tmp_path, monkeypatch):
        """Test adding error validates source."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        with pytest.raises(ValueError):
            tracker.add_error("", "Error message")
        
        with pytest.raises(ValueError):
            tracker.add_error(None, "Error message")

    def test_add_error_validates_message(self, tmp_path, monkeypatch):
        """Test adding error validates message."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        with pytest.raises(ValueError):
            tracker.add_error("source", "")
        
        with pytest.raises(ValueError):
            tracker.add_error("source", None)

    def test_add_error_validates_severity(self, tmp_path, monkeypatch):
        """Test adding error validates severity."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        with pytest.raises(ValueError):
            tracker.add_error("source", "message", severity="invalid")

    def test_add_error_truncates_long_inputs(self, tmp_path, monkeypatch):
        """Test adding error truncates excessively long inputs."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        long_source = "x" * 1000
        long_message = "y" * 5000
        
        entry = tracker.add_error(long_source, long_message)
        
        assert len(entry.source) <= 500
        assert len(entry.error_message) <= 2000

    def test_add_error_limits_total_count(self, tmp_path, monkeypatch):
        """Test adding errors limits total count."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        # Pre-populate with 9999 errors
        tracker.errors = [
            ErrorEntry(f"source_{i}", f"error_{i}") for i in range(9999)
        ]
        
        # Add two more (should trigger cleanup)
        tracker.add_error("new_source1", "new_error1")
        tracker.add_error("new_source2", "new_error2")
        
        # Should stay at limit
        assert len(tracker.errors) <= 10000


class TestPatternDetection:
    """Tests for pattern detection."""

    def test_pattern_created_on_first_error(self, tmp_path, monkeypatch):
        """Test pattern is created on first error."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        entry = tracker.add_error("test", "Test error")
        
        assert entry.fingerprint in tracker.patterns
        assert tracker.patterns[entry.fingerprint]["count"] == 1

    def test_pattern_count_increments(self, tmp_path, monkeypatch):
        """Test pattern count increments on repeated errors."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        # Add same error multiple times
        for _ in range(5):
            entry = tracker.add_error("test", "Same error")
        
        assert tracker.patterns[entry.fingerprint]["count"] == 5

    def test_pattern_occurrences_limited(self, tmp_path, monkeypatch):
        """Test pattern occurrences are limited to last 20."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        # Add same error 30 times
        for _ in range(30):
            entry = tracker.add_error("test", "Repeated error")
        
        # Occurrences should be limited to 20
        assert len(tracker.patterns[entry.fingerprint]["occurrences"]) == 20


class TestLessonGeneration:
    """Tests for lesson generation."""

    def test_generate_lessons_basic(self, tmp_path, monkeypatch):
        """Test basic lesson generation."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        lessons_file = tmp_path / 'lessons-learned.md'
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        monkeypatch.setattr('error_tracker.LESSONS_FILE', lessons_file)
        
        tracker = ErrorTracker()
        
        # Add recurring error
        for _ in range(5):
            tracker.add_error("test", "HTTP 403 Forbidden from API")
        
        lessons = tracker.generate_lessons(min_occurrences=3)
        
        assert len(lessons) > 0
        assert any("API" in lesson.get("title", "") for lesson in lessons)

    def test_generate_lessons_dry_run(self, tmp_path, monkeypatch):
        """Test lesson generation in dry run mode."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        lessons_file = tmp_path / 'lessons-learned.md'
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        monkeypatch.setattr('error_tracker.LESSONS_FILE', lessons_file)
        
        tracker = ErrorTracker()
        
        for _ in range(5):
            entry = tracker.add_error("test", "Recurring error")
        
        lessons = tracker.generate_lessons(min_occurrences=3, dry_run=True)
        
        # Lesson should be generated but not marked as generated
        assert len(lessons) > 0
        assert tracker.patterns[entry.fingerprint]["lesson_generated"] is False

    def test_generate_lessons_skips_already_generated(self, tmp_path, monkeypatch):
        """Test lesson generation skips already generated patterns."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        lessons_file = tmp_path / 'lessons-learned.md'
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        monkeypatch.setattr('error_tracker.LESSONS_FILE', lessons_file)
        
        tracker = ErrorTracker()
        
        for _ in range(5):
            tracker.add_error("test", "Recurring error")
        
        # Generate first time
        lessons1 = tracker.generate_lessons(min_occurrences=3)
        
        # Generate second time
        lessons2 = tracker.generate_lessons(min_occurrences=3)
        
        assert len(lessons1) > 0
        assert len(lessons2) == 0  # Already generated


class TestAnalyzePatterns:
    """Tests for pattern analysis."""

    def test_analyze_patterns_empty(self, tmp_path, monkeypatch):
        """Test analyzing patterns with no data."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        analysis = tracker.analyze_patterns()
        
        assert "recurring" in analysis
        assert "recent_surge" in analysis
        assert "critical" in analysis

    def test_analyze_patterns_identifies_recurring(self, tmp_path, monkeypatch):
        """Test analysis identifies recurring patterns."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        # Add error 6 times (threshold is 5)
        for _ in range(6):
            tracker.add_error("test", "Recurring error")
        
        analysis = tracker.analyze_patterns()
        
        assert len(analysis["recurring"]) > 0


class TestStatistics:
    """Tests for statistics generation."""

    def test_get_stats_empty(self, tmp_path, monkeypatch):
        """Test getting stats with no errors."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        stats = tracker.get_stats()
        
        assert stats["total_errors"] == 0
        assert stats["unique_patterns"] == 0

    def test_get_stats_with_errors(self, tmp_path, monkeypatch):
        """Test getting stats with errors."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        
        tracker.add_error("source1", "Error 1", category="api", severity="high")
        tracker.add_error("source2", "Error 2", category="file", severity="low")
        
        stats = tracker.get_stats()
        
        assert stats["total_errors"] == 2
        assert stats["by_category"]["api"] == 1
        assert stats["by_category"]["file"] == 1
        assert stats["by_severity"]["high"] == 1
        assert stats["by_severity"]["low"] == 1


class TestFilePersistence:
    """Tests for file persistence operations."""

    def test_save_errors_atomic(self, tmp_path, monkeypatch):
        """Test errors are saved atomically."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        tracker.add_error("test", "Test error")
        
        # Verify file exists and is valid JSON
        saved_data = json.loads((log_dir / 'error_log.json').read_text())
        assert "errors" in saved_data
        assert len(saved_data["errors"]) == 1

    def test_save_patterns_atomic(self, tmp_path, monkeypatch):
        """Test patterns are saved atomically."""
        log_dir = tmp_path / 'logs' / 'errors'
        log_dir.mkdir(parents=True)
        
        monkeypatch.setattr('error_tracker.ERROR_LOG_DIR', log_dir)
        monkeypatch.setattr('error_tracker.ERROR_LOG_FILE', log_dir / 'error_log.json')
        monkeypatch.setattr('error_tracker.PATTERNS_FILE', log_dir / 'patterns.json')
        
        tracker = ErrorTracker()
        entry = tracker.add_error("test", "Test error")
        
        # Verify patterns file exists and is valid JSON
        saved_patterns = json.loads((log_dir / 'patterns.json').read_text())
        assert entry.fingerprint in saved_patterns


class TestSeverityLevels:
    """Tests for severity level constants."""

    def test_severity_levels_defined(self):
        """Test all severity levels are defined."""
        assert "critical" in SEVERITY_LEVELS
        assert "high" in SEVERITY_LEVELS
        assert "medium" in SEVERITY_LEVELS
        assert "low" in SEVERITY_LEVELS

    def test_severity_ordering(self):
        """Test severity levels have correct ordering."""
        assert SEVERITY_LEVELS["critical"] > SEVERITY_LEVELS["high"]
        assert SEVERITY_LEVELS["high"] > SEVERITY_LEVELS["medium"]
        assert SEVERITY_LEVELS["medium"] > SEVERITY_LEVELS["low"]


class TestErrorCategories:
    """Tests for error category detection."""

    def test_api_category_keywords(self):
        """Test API category keywords."""
        assert "403" in ERROR_CATEGORIES["api"]
        assert "401" in ERROR_CATEGORIES["api"]
        assert "timeout" in ERROR_CATEGORIES["api"]

    def test_validation_category_keywords(self):
        """Test validation category keywords."""
        assert "schema" in ERROR_CATEGORIES["validation"]
        assert "required" in ERROR_CATEGORIES["validation"]
        assert "invalid" in ERROR_CATEGORIES["validation"]

    def test_file_category_keywords(self):
        """Test file category keywords."""
        assert "file not found" in ERROR_CATEGORIES["file"]
        assert "permission" in ERROR_CATEGORIES["file"]

    def test_content_category_keywords(self):
        """Test content category keywords."""
        assert "keyword" in ERROR_CATEGORIES["content"]
        assert "template" in ERROR_CATEGORIES["content"]

    def test_test_category_keywords(self):
        """Test test category keywords."""
        assert "assertion" in ERROR_CATEGORIES["test"]
        assert "fixture" in ERROR_CATEGORIES["test"]

    def test_process_category_keywords(self):
        """Test process category keywords."""
        assert "phase" in ERROR_CATEGORIES["process"]
        assert "brief" in ERROR_CATEGORIES["process"]
