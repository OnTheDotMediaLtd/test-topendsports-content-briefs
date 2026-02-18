#!/usr/bin/env python3
"""
Tests for PatternAnalyzer integration into AutomationRunner.

Verifies that:
1. analyze_content_patterns() is wired into run_full_cycle()
2. PatternAnalyzer import failure is non-blocking
3. Results dict includes 'content_patterns' key
4. Severe patterns trigger auto-feedback creation
5. Report includes content_patterns section
"""

import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Add scripts dir to path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from automation import AutomationRunner


class TestAutomationRunnerInit:
    """Verify AutomationRunner initialises content_patterns in results."""

    def test_results_contains_content_patterns_key(self):
        """AutomationRunner.results must include 'content_patterns' on init."""
        runner = AutomationRunner()
        assert "content_patterns" in runner.results

    def test_content_patterns_initial_status_is_skipped(self):
        """Initial status for content_patterns must be 'skipped'."""
        runner = AutomationRunner()
        assert runner.results["content_patterns"]["status"] == "skipped"

    def test_content_patterns_initial_counts_are_zero(self):
        """Initial pattern counts must be zero."""
        cp = AutomationRunner().results["content_patterns"]
        assert cp.get("patterns_found", 0) == 0
        assert cp.get("severe_patterns", 0) == 0


class TestAnalyzeContentPatterns:
    """Unit tests for the new analyze_content_patterns method."""

    def test_method_exists_on_runner(self):
        """AutomationRunner must expose analyze_content_patterns()."""
        assert hasattr(AutomationRunner, "analyze_content_patterns")
        assert callable(getattr(AutomationRunner, "analyze_content_patterns"))

    def test_returns_dict(self):
        """analyze_content_patterns must return a dict (even on import failure)."""
        runner = AutomationRunner()
        with patch.dict("sys.modules", {"pattern_analyzer": None}):
            result = runner.analyze_content_patterns()
        assert isinstance(result, dict)

    def test_import_failure_is_non_blocking(self):
        """ImportError in PatternAnalyzer must not raise; status becomes skipped or error."""
        runner = AutomationRunner()
        # Simulate a module that raises ImportError when PatternAnalyzer is accessed
        mock_module = MagicMock()
        mock_module.PatternAnalyzer.side_effect = ImportError("mock import error")

        with patch.dict("sys.modules", {"pattern_analyzer": mock_module}):
            try:
                result = runner.analyze_content_patterns()
            except ImportError:
                pytest.fail("analyze_content_patterns() must not propagate ImportError")
        # Either skipped or error, but must not raise
        assert runner.results["content_patterns"]["status"] in ("skipped", "error", "completed")

    def test_generic_exception_is_non_blocking(self):
        """Runtime exceptions in PatternAnalyzer must not propagate."""
        runner = AutomationRunner()
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_all_patterns.side_effect = RuntimeError("mock runtime error")

        mock_module = MagicMock()
        mock_module.PatternAnalyzer.return_value = mock_analyzer

        with patch.dict("sys.modules", {"pattern_analyzer": mock_module}):
            try:
                result = runner.analyze_content_patterns()
            except RuntimeError:
                pytest.fail("analyze_content_patterns() must not propagate RuntimeError")
        assert runner.results["content_patterns"]["status"] in ("error", "skipped", "completed")

    def test_no_patterns_sets_completed_status(self):
        """Zero patterns from analyzer sets completed status with zero counts."""
        runner = AutomationRunner()
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_all_patterns.return_value = {"total_patterns": 0}
        mock_analyzer.generate_alerts.return_value = []

        mock_module = MagicMock()
        mock_module.PatternAnalyzer.return_value = mock_analyzer

        with patch.dict("sys.modules", {"pattern_analyzer": mock_module}):
            result = runner.analyze_content_patterns()

        assert result["status"] == "completed"
        assert result["patterns_found"] == 0
        assert result["severe_patterns"] == 0

    def test_severe_patterns_trigger_auto_feedback(self):
        """Critical/high severity patterns must trigger create_auto_feedback()."""
        runner = AutomationRunner()
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_all_patterns.return_value = {"total_patterns": 2}
        mock_analyzer.generate_alerts.return_value = [
            {"category": "attribution", "severity": "critical", "message": "Generic attribution"},
            {"category": "word_count", "severity": "high", "message": "Word count deficit"},
        ]
        mock_analyzer.create_auto_feedback.return_value = ["feedback/auto-001.json"]

        mock_module = MagicMock()
        mock_module.PatternAnalyzer.return_value = mock_analyzer

        with patch.dict("sys.modules", {"pattern_analyzer": mock_module}):
            result = runner.analyze_content_patterns()

        mock_analyzer.create_auto_feedback.assert_called_once()
        assert result["severe_patterns"] == 2
        assert len(result["auto_feedback_files"]) == 1

    def test_low_severity_patterns_do_not_trigger_auto_feedback(self):
        """Low severity patterns must NOT trigger create_auto_feedback()."""
        runner = AutomationRunner()
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_all_patterns.return_value = {"total_patterns": 1}
        mock_analyzer.generate_alerts.return_value = [
            {"category": "links", "severity": "low", "message": "Minor link issue"},
        ]

        mock_module = MagicMock()
        mock_module.PatternAnalyzer.return_value = mock_analyzer

        with patch.dict("sys.modules", {"pattern_analyzer": mock_module}):
            result = runner.analyze_content_patterns()

        mock_analyzer.create_auto_feedback.assert_not_called()
        assert result["severe_patterns"] == 0

    def test_alerts_capped_at_five_in_results(self):
        """Results must cap alerts at 5 entries for report brevity."""
        runner = AutomationRunner()
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_all_patterns.return_value = {"total_patterns": 8}
        mock_analyzer.generate_alerts.return_value = [
            {"category": f"cat{i}", "severity": "low", "message": f"Issue {i}"}
            for i in range(8)
        ]

        mock_module = MagicMock()
        mock_module.PatternAnalyzer.return_value = mock_analyzer

        with patch.dict("sys.modules", {"pattern_analyzer": mock_module}):
            result = runner.analyze_content_patterns()

        assert len(result.get("alerts", [])) <= 5


class TestRunFullCycleIntegration:
    """Verify analyze_content_patterns is called as part of run_full_cycle."""

    def test_analyze_content_patterns_called_in_full_cycle(self):
        """run_full_cycle must call analyze_content_patterns."""
        runner = AutomationRunner()

        with patch.object(runner, "run_tests", return_value=True), \
             patch.object(runner, "validate_brands", return_value={"status": "skipped"}), \
             patch.object(runner, "analyze_errors", return_value={}), \
             patch.object(runner, "analyze_content_patterns", return_value={"status": "completed"}) as mock_patterns, \
             patch.object(runner, "process_feedback", return_value={}), \
             patch.object(runner, "generate_report", return_value=""):
            runner.run_full_cycle()

        mock_patterns.assert_called_once()

    def test_content_patterns_failure_does_not_affect_exit_code(self):
        """Pattern analysis failure (status=error) must not change exit code."""
        runner = AutomationRunner()

        with patch.object(runner, "run_tests", return_value=True), \
             patch.object(runner, "validate_brands", return_value={"status": "passed"}), \
             patch.object(runner, "analyze_errors", return_value={}), \
             patch.object(runner, "analyze_content_patterns", return_value={"status": "error"}), \
             patch.object(runner, "process_feedback", return_value={}), \
             patch.object(runner, "generate_report", return_value=""):
            exit_code = runner.run_full_cycle()

        assert exit_code == 0  # Tests passed + brands valid => exit 0


class TestGenerateReportIncludesPatterns:
    """Verify the report output includes the content_patterns section."""

    def test_report_contains_content_patterns_section(self):
        """generate_report must include CONTENT_PATTERNS in output."""
        runner = AutomationRunner()
        runner.results["content_patterns"] = {
            "status": "completed",
            "patterns_found": 3,
            "severe_patterns": 1,
            "alerts": [{"category": "attribution", "severity": "high", "message": "Test"}],
        }
        report = runner.generate_report()
        assert "CONTENT_PATTERNS" in report

    def test_report_reflects_pattern_status(self):
        """Report must reflect the actual status from content_patterns results."""
        runner = AutomationRunner()
        runner.results["content_patterns"] = {"status": "skipped"}
        report = runner.generate_report()
        # The skipped icon or text should appear
        assert "skipped" in report.lower() or "⏭️" in report
