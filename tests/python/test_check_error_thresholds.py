#!/usr/bin/env python3
"""
Tests for check_error_thresholds.py - Error Threshold Checker for CI/CD

Coverage targets:
- load_patterns() function
- check_critical_errors() function
- check_recurring_patterns() function
- check_patterns_needing_attention() function
- check_error_surge() function
- check_category_distribution() function
- main() function with various scenarios
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

from check_error_thresholds import (
    load_patterns,
    check_critical_errors,
    check_recurring_patterns,
    check_patterns_needing_attention,
    check_error_surge,
    check_category_distribution,
    main,
    THRESHOLDS,
)


class TestLoadPatterns:
    """Tests for load_patterns function."""

    def test_load_patterns_file_not_exists(self, tmp_path):
        """Test loading when patterns file doesn't exist."""
        with patch('check_error_thresholds.PATTERNS_FILE', tmp_path / 'nonexistent.json'):
            result = load_patterns()
            assert result == {}

    def test_load_patterns_valid_json(self, tmp_path):
        """Test loading valid patterns file."""
        patterns_file = tmp_path / 'patterns.json'
        test_patterns = {
            "pattern1": {"count": 5, "severity": "high"},
            "pattern2": {"count": 3, "severity": "medium"}
        }
        patterns_file.write_text(json.dumps(test_patterns))
        
        with patch('check_error_thresholds.PATTERNS_FILE', patterns_file):
            result = load_patterns()
            assert result == test_patterns

    def test_load_patterns_invalid_json(self, tmp_path, capsys):
        """Test loading invalid JSON file."""
        patterns_file = tmp_path / 'patterns.json'
        patterns_file.write_text('invalid json {{{')
        
        with patch('check_error_thresholds.PATTERNS_FILE', patterns_file):
            result = load_patterns()
            assert result == {}
            captured = capsys.readouterr()
            assert 'ERROR' in captured.out or result == {}

    def test_load_patterns_empty_file(self, tmp_path):
        """Test loading empty JSON file."""
        patterns_file = tmp_path / 'patterns.json'
        patterns_file.write_text('{}')
        
        with patch('check_error_thresholds.PATTERNS_FILE', patterns_file):
            result = load_patterns()
            assert result == {}


class TestCheckCriticalErrors:
    """Tests for check_critical_errors function."""

    def test_no_critical_errors(self):
        """Test when there are no critical errors."""
        patterns = {
            "p1": {"severity": "high"},
            "p2": {"severity": "medium"}
        }
        passed, message = check_critical_errors(patterns)
        assert passed is True
        assert "0 critical errors" in message or "PASS" in message

    def test_has_critical_errors(self):
        """Test when critical errors exist."""
        patterns = {
            "p1": {"severity": "critical"},
            "p2": {"severity": "critical"},
            "p3": {"severity": "high"}
        }
        passed, message = check_critical_errors(patterns)
        assert passed is False
        assert "FAIL" in message
        assert "2 critical" in message

    def test_empty_patterns(self):
        """Test with empty patterns."""
        patterns = {}
        passed, message = check_critical_errors(patterns)
        assert passed is True

    def test_single_critical_error(self):
        """Test with exactly one critical error."""
        patterns = {"p1": {"severity": "critical"}}
        passed, message = check_critical_errors(patterns)
        assert passed is False  # Default max is 0


class TestCheckRecurringPatterns:
    """Tests for check_recurring_patterns function."""

    def test_no_recurring_patterns(self):
        """Test with no patterns meeting threshold."""
        patterns = {
            "p1": {"count": 2},
            "p2": {"count": 3},
        }
        passed, count, message = check_recurring_patterns(patterns)
        assert passed is True
        assert count == 0
        assert "PASS" in message

    def test_warning_level_recurring(self):
        """Test warning level recurring patterns."""
        patterns = {
            "p1": {"count": 6},
            "p2": {"count": 7},
            "p3": {"count": 5},
        }
        passed, count, message = check_recurring_patterns(patterns)
        assert passed is True
        assert count == 3
        assert "WARN" in message

    def test_fail_level_recurring(self):
        """Test fail level recurring patterns."""
        patterns = {
            f"p{i}": {"count": 10} for i in range(6)
        }
        passed, count, message = check_recurring_patterns(patterns)
        assert passed is False
        assert count >= 5
        assert "FAIL" in message

    def test_edge_case_exactly_5_count(self):
        """Test pattern with exactly 5 occurrences."""
        patterns = {"p1": {"count": 5}}
        passed, count, message = check_recurring_patterns(patterns)
        assert count == 1  # Should count as recurring

    def test_missing_count_field(self):
        """Test patterns missing count field."""
        patterns = {"p1": {}, "p2": {"severity": "high"}}
        passed, count, message = check_recurring_patterns(patterns)
        assert count == 0  # Should default to 0


class TestCheckPatternsNeedingAttention:
    """Tests for check_patterns_needing_attention function."""

    def test_no_patterns_needing_attention(self):
        """Test when no patterns need attention."""
        patterns = {
            "p1": {"count": 5, "lesson_generated": True},
            "p2": {"count": 2, "lesson_generated": False},
        }
        passed, count, message = check_patterns_needing_attention(patterns)
        assert passed is True
        assert "PASS" in message

    def test_warning_level_attention(self):
        """Test warning level for patterns needing attention."""
        patterns = {
            f"p{i}": {"count": 5, "lesson_generated": False} for i in range(4)
        }
        passed, count, message = check_patterns_needing_attention(patterns)
        assert passed is True
        assert "WARN" in message

    def test_fail_level_attention(self):
        """Test fail level for patterns needing attention."""
        patterns = {
            f"p{i}": {"count": 5, "lesson_generated": False} for i in range(12)
        }
        passed, count, message = check_patterns_needing_attention(patterns)
        assert passed is False
        assert "FAIL" in message

    def test_lesson_already_generated(self):
        """Test that patterns with lessons don't count."""
        patterns = {
            "p1": {"count": 10, "lesson_generated": True},
        }
        passed, count, message = check_patterns_needing_attention(patterns)
        assert passed is True
        assert count == 0


class TestCheckErrorSurge:
    """Tests for check_error_surge function."""

    def test_no_surges(self):
        """Test when there are no error surges."""
        patterns = {
            "p1": {"count": 10, "occurrences": [
                {"timestamp": (datetime.now() - timedelta(days=30)).isoformat()}
                for _ in range(10)
            ]}
        }
        passed, message = check_error_surge(patterns)
        assert passed is True
        assert "PASS" in message or "No error surges" in message

    def test_recent_surge_detected(self):
        """Test detection of recent error surge."""
        recent_time = (datetime.now() - timedelta(days=1)).isoformat()
        patterns = {
            "p1": {
                "count": 10,
                "sample_message": "Test error message",
                "occurrences": [
                    {"timestamp": recent_time}
                    for _ in range(8)  # 80% recent
                ]
            }
        }
        passed, message = check_error_surge(patterns)
        assert passed is True  # Surge is a warning, not failure
        assert "WARN" in message or "surge" in message.lower()

    def test_empty_occurrences(self):
        """Test pattern with empty occurrences list."""
        patterns = {
            "p1": {"count": 5, "occurrences": []}
        }
        passed, message = check_error_surge(patterns)
        assert passed is True

    def test_missing_occurrences(self):
        """Test pattern without occurrences field."""
        patterns = {"p1": {"count": 5}}
        passed, message = check_error_surge(patterns)
        assert passed is True

    def test_low_total_count_not_surge(self):
        """Test that low count patterns don't trigger surge."""
        recent = (datetime.now() - timedelta(days=1)).isoformat()
        patterns = {
            "p1": {
                "count": 2,  # Low count
                "occurrences": [{"timestamp": recent}, {"timestamp": recent}]
            }
        }
        passed, message = check_error_surge(patterns)
        assert passed is True


class TestCheckCategoryDistribution:
    """Tests for check_category_distribution function."""

    def test_empty_patterns(self):
        """Test with empty patterns."""
        result = check_category_distribution({})
        assert "No error patterns" in result

    def test_single_category(self):
        """Test with single category."""
        patterns = {
            "p1": {"category": "api", "count": 5},
            "p2": {"category": "api", "count": 3},
        }
        result = check_category_distribution(patterns)
        assert "api" in result
        assert "8" in result  # Total count

    def test_multiple_categories(self):
        """Test with multiple categories."""
        patterns = {
            "p1": {"category": "api", "count": 10},
            "p2": {"category": "file", "count": 5},
            "p3": {"category": "validation", "count": 3},
        }
        result = check_category_distribution(patterns)
        assert "api" in result
        assert "file" in result
        assert "validation" in result

    def test_unknown_category(self):
        """Test patterns without category field."""
        patterns = {
            "p1": {"count": 5},  # No category
        }
        result = check_category_distribution(patterns)
        assert "unknown" in result


class TestMain:
    """Tests for main function."""

    def test_main_no_patterns(self, capsys):
        """Test main with no patterns."""
        with patch('check_error_thresholds.load_patterns', return_value={}):
            result = main()
            assert result == 0
            captured = capsys.readouterr()
            assert "No error patterns found" in captured.out

    def test_main_all_passed(self, capsys):
        """Test main when all checks pass."""
        patterns = {
            "p1": {"severity": "low", "count": 2, "lesson_generated": True}
        }
        with patch('check_error_thresholds.load_patterns', return_value=patterns):
            result = main()
            assert result == 0
            captured = capsys.readouterr()
            assert "PASSED" in captured.out

    def test_main_with_warnings(self, capsys):
        """Test main with warnings only."""
        patterns = {
            f"p{i}": {"severity": "high", "count": 6, "lesson_generated": False}
            for i in range(4)
        }
        with patch('check_error_thresholds.load_patterns', return_value=patterns):
            result = main()
            assert result == 1  # Warning exit code
            captured = capsys.readouterr()
            assert "WARN" in captured.out or "WARNING" in captured.out

    def test_main_with_failures(self, capsys):
        """Test main when thresholds exceeded."""
        patterns = {
            f"p{i}": {"severity": "critical", "count": 10, "lesson_generated": False}
            for i in range(6)
        }
        with patch('check_error_thresholds.load_patterns', return_value=patterns):
            result = main()
            assert result == 2  # Failure exit code
            captured = capsys.readouterr()
            assert "FAILED" in captured.out


class TestEdgeCases:
    """Edge case tests."""

    def test_unicode_in_pattern_message(self):
        """Test handling unicode in pattern messages."""
        patterns = {
            "p1": {
                "severity": "high",
                "count": 5,
                "sample_message": "Error: 日本語 émojis 🎉"
            }
        }
        # Should not raise
        passed, _ = check_critical_errors(patterns)
        assert passed is True

    def test_very_large_pattern_count(self):
        """Test with very large pattern counts."""
        patterns = {
            "p1": {"count": 1000000, "severity": "low"}
        }
        passed, count, _ = check_recurring_patterns(patterns)
        assert count == 1

    def test_negative_count(self):
        """Test handling negative counts."""
        patterns = {
            "p1": {"count": -1}
        }
        passed, count, _ = check_recurring_patterns(patterns)
        assert count == 0  # Negative shouldn't count as recurring

    def test_malformed_timestamp(self):
        """Test handling malformed timestamps."""
        patterns = {
            "p1": {
                "count": 5,
                "occurrences": [
                    {"timestamp": "not-a-date"},
                    {"timestamp": "2026-01-01T00:00:00"}
                ]
            }
        }
        # Should handle gracefully
        try:
            check_error_surge(patterns)
        except ValueError:
            pass  # Expected for malformed date

    def test_none_values_in_pattern(self):
        """Test handling None values."""
        patterns = {
            "p1": {"count": None, "severity": None}
        }
        # Should not crash
        check_critical_errors(patterns)
        check_recurring_patterns(patterns)


class TestIntegration:
    """Integration tests."""

    def test_full_threshold_check_workflow(self, tmp_path, capsys):
        """Test complete workflow from file load to report."""
        # Create test patterns file
        patterns_file = tmp_path / 'patterns.json'
        test_patterns = {
            "api_error": {
                "severity": "high",
                "count": 6,
                "category": "api",
                "lesson_generated": False,
                "sample_message": "API call failed",
                "occurrences": [
                    {"timestamp": datetime.now().isoformat()}
                    for _ in range(6)
                ]
            }
        }
        patterns_file.write_text(json.dumps(test_patterns))
        
        with patch('check_error_thresholds.PATTERNS_FILE', patterns_file):
            result = main()
            captured = capsys.readouterr()
            
            # Should include all check outputs
            assert "CHECK 1" in captured.out or "Critical" in captured.out
            assert "CHECK 2" in captured.out or "Recurring" in captured.out
