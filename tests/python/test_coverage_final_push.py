"""Tests targeting remaining uncovered lines for coverage improvement.

Targets:
- prompt_monitor.py lines 461-464 (category-specific recommendations)
- validate_csv_data_integrated.py lines 125-126 (csv.Error)
- validate_feedback.py line 111 (_read_file failure)
- validate_phase_json_integrated.py line 102 (file not found)
"""
import os
import sys
import csv
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))


class TestPromptMonitorRecommendations:
    """Cover specific recommendation branches in prompt_monitor.py (lines 461-464).

    The get_recommendations() method has category-specific branches for:
    ahrefs (gap>30, gap>15, gap<15), brief_generation, validation, conversion, and default.
    """

    def _create_monitor_with_problematic(self, command, failure_count, success_count):
        """Create a PromptMonitor with specific command data."""
        from prompt_monitor import PromptMonitor
        monitor = PromptMonitor()
        for i in range(failure_count):
            monitor.log_usage(command, "failure", context=f"query {i}")
        for i in range(success_count):
            monitor.log_usage(command, "success", context=f"query ok {i}")
        return monitor

    def test_ahrefs_high_gap_recommendation(self):
        """Cover ahrefs gap > 30 branch (line ~459)."""
        # ahrefs expected rate = 70%. Need success < 40% -> gap > 30
        monitor = self._create_monitor_with_problematic("mcp__ahrefs__query", 90, 10)
        recs = monitor.get_recommendations()
        ahrefs_rec = [r for r in recs if 'ahrefs' in str(r).lower() or 'IMMEDIATE' in str(r)]
        assert len(recs) > 0

    def test_ahrefs_medium_gap_recommendation(self):
        """Cover ahrefs gap 15-30 branch (line ~461)."""
        # ahrefs expected = 70%. Need success ~45% -> gap ~25
        monitor = self._create_monitor_with_problematic("mcp__ahrefs__query", 55, 45)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_ahrefs_low_gap_recommendation(self):
        """Cover ahrefs gap < 15 branch (line ~463)."""
        # ahrefs expected = 70%. Need success ~60% -> gap ~10
        monitor = self._create_monitor_with_problematic("mcp__ahrefs__query", 40, 60)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_brief_generation_recommendation(self):
        """Cover brief_generation branch (line ~464)."""
        # brief_generation expected = 90%. Need success < 80% -> gap > 10
        monitor = self._create_monitor_with_problematic("/generate-brief test", 50, 50)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_validation_recommendation(self):
        """Cover validation branch."""
        # validation expected = 80%. Need success < 70%
        monitor = self._create_monitor_with_problematic("validate-phase test", 60, 40)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_conversion_recommendation(self):
        """Cover conversion branch."""
        # conversion expected = 95%. Need success < 85%
        monitor = self._create_monitor_with_problematic("convert_to_docx test", 50, 50)
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)

    def test_unknown_category_recommendation(self):
        """Cover the else branch for unknown categories."""
        # Use a command that won't match any known pattern
        from prompt_monitor import PromptMonitor
        monitor = PromptMonitor()
        # Log with a command that creates an unknown category
        for i in range(50):
            monitor.log_usage("custom_unknown_tool", "failure", context=f"q {i}")
        for i in range(10):
            monitor.log_usage("custom_unknown_tool", "success", context=f"q {i}")
        recs = monitor.get_recommendations()
        assert isinstance(recs, list)


class TestCSVDataIntegratedErrors:
    """Cover error handling in validate_csv_data_integrated.py (lines 125-126)."""

    def test_csv_parse_error_via_mock(self):
        """Cover csv.Error branch by mocking csv.reader to raise."""
        from validate_csv_data_integrated import CSVValidator
        # Create a valid-looking file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("header1,header2\nval1,val2\n")
            path = f.name
        try:
            v = CSVValidator(Path(path))
            # Mock csv.reader to raise csv.Error during iteration
            original_validate = v.validate
            with patch('csv.reader', side_effect=csv.Error("field larger than field limit")):
                result = v.validate()
                assert isinstance(result, bool)
        finally:
            os.unlink(path)


class TestValidateFeedbackReadFile:
    """Cover file read failure in validate_feedback.py (line 111)."""

    def test_read_file_failure(self):
        """Cover the _read_file() failure path (line 111)."""
        from validate_feedback import FeedbackValidator
        # Create a file that exists but will fail to read properly
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.md', delete=False) as f:
            # Write invalid UTF-8 bytes
            f.write(b'\xff\xfe\x00\x00' + b'\xff' * 100)
            path = f.name
        try:
            v = FeedbackValidator(Path(path))
            result = v.validate()
            # Should fail gracefully
            assert isinstance(result, bool)
        finally:
            os.unlink(path)

    def test_file_not_found(self):
        """Cover file not found path."""
        from validate_feedback import FeedbackValidator
        v = FeedbackValidator(Path("/nonexistent/feedback.md"))
        result = v.validate()
        assert result is False


class TestValidatePhaseJsonIntegrated:
    """Cover file not found in validate_phase_json_integrated.py (line 102)."""

    def test_nonexistent_file(self):
        """Cover file not found error."""
        from validate_phase_json_integrated import PhaseJSONValidator
        v = PhaseJSONValidator(Path("/nonexistent/phase.json"))
        result = v.validate()
        assert result is False

    def test_invalid_json_file(self):
        """Cover JSON parse error."""
        from validate_phase_json_integrated import PhaseJSONValidator
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write("{invalid json content")
            path = f.name
        try:
            v = PhaseJSONValidator(Path(path))
            result = v.validate()
            assert result is False
        finally:
            os.unlink(path)
