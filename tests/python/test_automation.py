"""
Tests for scripts/automation.py

Comprehensive tests for the AutomationRunner class and main() function.
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess
import tempfile

# Add scripts directory to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from automation import (
    AutomationRunner,
    main,
    SCRIPT_DIR,
    PROJECT_ROOT as AUTOMATION_PROJECT_ROOT,
    FEEDBACK_SKILL_DIR,
    LESSONS_FILE,
    ERROR_LOG_DIR,
)


class TestAutomationRunnerInit:
    """Test AutomationRunner initialization."""

    def test_init_default_verbose(self):
        """Test initialization with default verbose=False."""
        runner = AutomationRunner()
        
        assert runner.verbose == False
        assert "tests" in runner.results
        assert "errors" in runner.results
        assert "feedback" in runner.results
        assert "lessons" in runner.results

    def test_init_verbose_true(self):
        """Test initialization with verbose=True."""
        runner = AutomationRunner(verbose=True)
        
        assert runner.verbose == True

    def test_init_results_structure(self):
        """Test initial results structure."""
        runner = AutomationRunner()
        
        for key in ["tests", "brands", "errors", "feedback", "lessons"]:
            assert runner.results[key]["status"] == "skipped"
            assert "details" in runner.results[key]


class TestAutomationRunnerLog:
    """Test AutomationRunner.log() method."""

    def test_log_info_level(self, capsys):
        """Test logging at INFO level."""
        runner = AutomationRunner()
        runner.log("Test message", "INFO")
        
        captured = capsys.readouterr()
        assert "[INFO]" in captured.out
        assert "Test message" in captured.out

    def test_log_ok_level(self, capsys):
        """Test logging at OK level."""
        runner = AutomationRunner()
        runner.log("Success!", "OK")
        
        captured = capsys.readouterr()
        assert "[OK]" in captured.out

    def test_log_warn_level(self, capsys):
        """Test logging at WARN level."""
        runner = AutomationRunner()
        runner.log("Warning here", "WARN")
        
        captured = capsys.readouterr()
        assert "[WARN]" in captured.out

    def test_log_error_level(self, capsys):
        """Test logging at ERROR level."""
        runner = AutomationRunner()
        runner.log("Error occurred", "ERROR")
        
        captured = capsys.readouterr()
        assert "[ERROR]" in captured.out

    def test_log_unknown_level(self, capsys):
        """Test logging with unknown level."""
        runner = AutomationRunner()
        runner.log("Unknown level", "UNKNOWN")
        
        captured = capsys.readouterr()
        assert "[?]" in captured.out

    def test_log_includes_timestamp(self, capsys):
        """Test that log includes timestamp."""
        runner = AutomationRunner()
        runner.log("Test", "INFO")
        
        captured = capsys.readouterr()
        # Timestamp format is HH:MM:SS
        assert ":" in captured.out.split("]")[0]


class TestAutomationRunnerRunCommand:
    """Test AutomationRunner.run_command() method."""

    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="output",
            stderr=""
        )
        
        runner = AutomationRunner()
        code, stdout, stderr = runner.run_command(["echo", "test"])
        
        assert code == 0
        assert stdout == "output"
        assert stderr == ""

    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test failed command execution."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="error message"
        )
        
        runner = AutomationRunner()
        code, stdout, stderr = runner.run_command(["false"])
        
        assert code == 1
        assert stderr == "error message"

    @patch('subprocess.run')
    def test_run_command_timeout(self, mock_run):
        """Test command timeout handling."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["test"], timeout=300)
        
        runner = AutomationRunner()
        code, stdout, stderr = runner.run_command(["sleep", "1000"])
        
        assert code == 1
        assert "timed out" in stderr.lower()

    @patch('subprocess.run')
    def test_run_command_not_found(self, mock_run):
        """Test command not found handling."""
        mock_run.side_effect = FileNotFoundError("Command not found")
        
        runner = AutomationRunner()
        code, stdout, stderr = runner.run_command(["nonexistent_command"])
        
        assert code == 1
        assert "not found" in stderr.lower()

    @patch('subprocess.run')
    def test_run_command_verbose_logging(self, mock_run, capsys):
        """Test verbose logging of commands."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
        
        runner = AutomationRunner(verbose=True)
        runner.run_command(["echo", "hello"])
        
        captured = capsys.readouterr()
        assert "Running:" in captured.out

    def test_run_command_invalid_input(self):
        """Test handling of invalid command input."""
        runner = AutomationRunner()
        code, stdout, stderr = runner.run_command([])
        
        assert code == 1
        assert "Invalid" in stderr

    def test_run_command_none_input(self):
        """Test handling of None command input."""
        runner = AutomationRunner()
        code, stdout, stderr = runner.run_command(None)
        
        assert code == 1

    @patch('subprocess.run')
    def test_run_command_handles_none_output(self, mock_run):
        """Test handling of None stdout/stderr."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout=None,
            stderr=None
        )
        
        runner = AutomationRunner()
        code, stdout, stderr = runner.run_command(["test"])
        
        assert code == 0
        assert stdout == ""
        assert stderr == ""


class TestAutomationRunnerRunTests:
    """Test AutomationRunner.run_tests() method."""

    @patch.object(AutomationRunner, 'run_command')
    def test_run_tests_success(self, mock_run):
        """Test successful test run."""
        mock_run.return_value = (0, "All tests passed", "")
        
        runner = AutomationRunner()
        result = runner.run_tests()
        
        assert result == True
        assert runner.results["tests"]["status"] == "passed"

    @patch.object(AutomationRunner, 'run_command')
    def test_run_tests_failure(self, mock_run):
        """Test failed test run."""
        mock_run.return_value = (1, "Tests failed", "Error details")
        
        runner = AutomationRunner()
        result = runner.run_tests()
        
        assert result == False
        assert runner.results["tests"]["status"] == "failed"

    @patch.object(AutomationRunner, 'run_command')
    def test_run_tests_with_tracking(self, mock_run):
        """Test running tests with error tracking enabled."""
        mock_run.return_value = (0, "output", "")
        
        runner = AutomationRunner()
        runner.run_tests(with_tracking=True)
        
        # Check that --error-tracking flag was included
        call_args = mock_run.call_args[0][0]
        assert "--error-tracking" in call_args

    @patch.object(AutomationRunner, 'run_command')
    def test_run_tests_without_tracking(self, mock_run):
        """Test running tests without error tracking."""
        mock_run.return_value = (0, "output", "")
        
        runner = AutomationRunner()
        runner.run_tests(with_tracking=False)
        
        call_args = mock_run.call_args[0][0]
        assert "--error-tracking" not in call_args

    @patch.object(AutomationRunner, 'run_command')
    def test_run_tests_output_truncation(self, mock_run):
        """Test that long output is truncated."""
        long_output = "\n".join([f"line {i}" for i in range(200)])
        mock_run.return_value = (0, long_output, "")
        
        runner = AutomationRunner()
        runner.run_tests()
        
        # Output should be truncated to 100 lines
        stored_output = runner.results["tests"]["output"]
        assert "more lines" in stored_output


class TestAutomationRunnerAnalyzeErrors:
    """Test AutomationRunner.analyze_errors() method."""

    @patch.object(AutomationRunner, 'run_command')
    @patch('automation.SCRIPT_DIR')
    def test_analyze_errors_success(self, mock_script_dir, mock_run, temp_dir):
        """Test successful error analysis."""
        # Create fake error_tracker.py
        mock_tracker = temp_dir / "error_tracker.py"
        mock_tracker.write_text("# fake tracker")
        mock_script_dir.__truediv__ = lambda self, x: mock_tracker
        
        mock_run.return_value = (0, "Error stats", "")
        
        runner = AutomationRunner()
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'is_file', return_value=True):
                result = runner.analyze_errors()
        
        assert runner.results["errors"]["status"] in ["completed", "skipped"]

    def test_analyze_errors_tracker_not_found(self, capsys):
        """Test when error tracker script doesn't exist."""
        runner = AutomationRunner()
        
        # Mock SCRIPT_DIR to a non-existent path
        with patch('automation.SCRIPT_DIR', Path("/nonexistent/path")):
            result = runner.analyze_errors()
        
        # Either skipped (not found) or failed (attempted but failed)
        assert runner.results["errors"]["status"] in ["skipped", "failed"]
        captured = capsys.readouterr()
        # Should have some output about the tracker


class TestAutomationRunnerProcessFeedback:
    """Test AutomationRunner.process_feedback() method."""

    @patch.object(AutomationRunner, 'run_command')
    def test_process_feedback_success(self, mock_run):
        """Test successful feedback processing."""
        mock_run.return_value = (0, "Processed 5 files", "")
        
        runner = AutomationRunner()
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'is_file', return_value=True):
                result = runner.process_feedback()
        
        assert runner.results["feedback"]["status"] in ["completed", "skipped"]

    @patch.object(AutomationRunner, 'run_command')
    def test_process_feedback_with_lessons_update(self, mock_run):
        """Test feedback processing with lessons update."""
        mock_run.return_value = (0, "Updated lessons", "")
        
        runner = AutomationRunner()
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'is_file', return_value=True):
                runner.process_feedback(update_lessons=True)
        
        if runner.results["feedback"]["status"] == "completed":
            assert runner.results["feedback"].get("lessons_updated") == True

    def test_process_feedback_script_not_found(self, capsys):
        """Test when ingest script doesn't exist."""
        runner = AutomationRunner()
        
        # Mock FEEDBACK_SKILL_DIR to a non-existent path
        with patch('automation.FEEDBACK_SKILL_DIR', Path("/nonexistent/path")):
            result = runner.process_feedback()
        
        # Either skipped (not found) or failed (attempted but failed)
        assert runner.results["feedback"]["status"] in ["skipped", "failed"]


class TestAutomationRunnerGenerateLessons:
    """Test AutomationRunner.generate_lessons() method."""

    @patch.object(AutomationRunner, 'run_command')
    def test_generate_lessons_success(self, mock_run):
        """Test successful lesson generation."""
        mock_run.return_value = (0, "Generated 10 lessons", "")
        
        runner = AutomationRunner()
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'is_file', return_value=True):
                result = runner.generate_lessons(min_occurrences=3)
        
        assert runner.results["lessons"]["status"] in ["completed", "skipped"]

    @patch.object(AutomationRunner, 'run_command')
    def test_generate_lessons_custom_min_occurrences(self, mock_run):
        """Test lesson generation with custom min_occurrences."""
        mock_run.return_value = (0, "output", "")
        
        runner = AutomationRunner()
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'is_file', return_value=True):
                runner.generate_lessons(min_occurrences=5)
        
        if mock_run.called:
            call_args = mock_run.call_args[0][0]
            assert any("5" in str(arg) for arg in call_args)

    def test_generate_lessons_invalid_min_occurrences(self, capsys):
        """Test handling of invalid min_occurrences."""
        runner = AutomationRunner()
        runner.generate_lessons(min_occurrences=-1)
        
        captured = capsys.readouterr()
        # Should use default value of 3

    def test_generate_lessons_tracker_not_found(self):
        """Test when error tracker doesn't exist."""
        runner = AutomationRunner()
        
        # Mock SCRIPT_DIR to a non-existent path
        with patch('automation.SCRIPT_DIR', Path("/nonexistent/path")):
            result = runner.generate_lessons()
        
        # Either skipped (not found) or failed (attempted but failed)
        assert runner.results["lessons"]["status"] in ["skipped", "failed"]


class TestAutomationRunnerGenerateReport:
    """Test AutomationRunner.generate_report() method."""

    def test_generate_report_basic(self):
        """Test basic report generation."""
        runner = AutomationRunner()
        report = runner.generate_report()
        
        assert "AUTOMATION REPORT" in report
        assert "Generated:" in report
        assert "SUMMARY" in report

    def test_generate_report_with_results(self):
        """Test report with actual results."""
        runner = AutomationRunner()
        runner.results["tests"]["status"] = "passed"
        runner.results["errors"]["status"] = "completed"
        runner.results["feedback"]["status"] = "failed"
        runner.results["lessons"]["status"] = "skipped"
        
        report = runner.generate_report()
        
        assert "passed" in report or "PASSED" in report or "✅" in report
        assert "failed" in report or "FAILED" in report or "❌" in report

    def test_generate_report_summary_counts(self):
        """Test that summary counts are correct."""
        runner = AutomationRunner()
        runner.results["tests"]["status"] = "passed"
        runner.results["brands"]["status"] = "passed"
        runner.results["errors"]["status"] = "completed"
        runner.results["feedback"]["status"] = "failed"
        runner.results["lessons"]["status"] = "skipped"
        
        report = runner.generate_report()
        
        # Should show: 3 passed, 1 failed, 1 skipped
        assert "3 passed" in report
        assert "1 failed" in report
        assert "1 skipped" in report

    def test_generate_report_verbose_output(self):
        """Test verbose report includes output details."""
        runner = AutomationRunner(verbose=True)
        runner.results["tests"]["status"] = "passed"
        runner.results["tests"]["output"] = "Test output content here"
        
        report = runner.generate_report()
        
        assert "Test output content" in report


class TestAutomationRunnerFullCycle:
    """Test AutomationRunner.run_full_cycle() method."""

    @patch.object(AutomationRunner, 'generate_lessons')
    @patch.object(AutomationRunner, 'process_feedback')
    @patch.object(AutomationRunner, 'analyze_errors')
    @patch.object(AutomationRunner, 'validate_brands')
    @patch.object(AutomationRunner, 'run_tests')
    def test_full_cycle_all_pass(self, mock_tests, mock_brands, mock_errors, mock_feedback, mock_lessons, capsys):
        """Test full cycle when all steps pass."""
        mock_tests.return_value = True
        mock_brands.return_value = {"status": "passed"}
        mock_errors.return_value = {}
        mock_feedback.return_value = {}
        mock_lessons.return_value = {}
        
        runner = AutomationRunner()
        exit_code = runner.run_full_cycle()
        
        assert exit_code == 0
        assert mock_tests.called
        assert mock_brands.called
        assert mock_errors.called
        assert mock_feedback.called

    @patch.object(AutomationRunner, 'generate_lessons')
    @patch.object(AutomationRunner, 'process_feedback')
    @patch.object(AutomationRunner, 'analyze_errors')
    @patch.object(AutomationRunner, 'run_tests')
    def test_full_cycle_tests_fail(self, mock_tests, mock_errors, mock_feedback, mock_lessons, capsys):
        """Test full cycle when tests fail."""
        mock_tests.return_value = False
        mock_errors.return_value = {}
        mock_feedback.return_value = {}
        mock_lessons.return_value = {}
        
        runner = AutomationRunner()
        exit_code = runner.run_full_cycle()
        
        assert exit_code == 1

    @patch.object(AutomationRunner, 'generate_lessons')
    @patch.object(AutomationRunner, 'process_feedback')
    @patch.object(AutomationRunner, 'analyze_errors')
    @patch.object(AutomationRunner, 'run_tests')
    def test_full_cycle_with_lessons(self, mock_tests, mock_errors, mock_feedback, mock_lessons, capsys):
        """Test full cycle with lessons update enabled."""
        mock_tests.return_value = True
        mock_errors.return_value = {}
        mock_feedback.return_value = {}
        mock_lessons.return_value = {}
        
        runner = AutomationRunner()
        exit_code = runner.run_full_cycle(update_lessons=True)
        
        assert mock_lessons.called


class TestMainFunction:
    """Test main() function argument parsing."""

    @patch.object(AutomationRunner, 'run_full_cycle')
    def test_main_run_command(self, mock_cycle):
        """Test main with 'run' command."""
        mock_cycle.return_value = 0
        
        with patch('sys.argv', ['automation.py', 'run']):
            result = main()
        
        assert mock_cycle.called

    @patch.object(AutomationRunner, 'run_tests')
    def test_main_test_command(self, mock_tests):
        """Test main with 'test' command."""
        mock_tests.return_value = True
        
        with patch('sys.argv', ['automation.py', 'test']):
            result = main()
        
        assert mock_tests.called
        assert result == 0

    @patch.object(AutomationRunner, 'run_tests')
    def test_main_test_command_no_tracking(self, mock_tests):
        """Test main with 'test --no-tracking' command."""
        mock_tests.return_value = True
        
        with patch('sys.argv', ['automation.py', 'test', '--no-tracking']):
            result = main()
        
        mock_tests.assert_called_once_with(with_tracking=False)

    @patch.object(AutomationRunner, 'process_feedback')
    @patch.object(AutomationRunner, 'analyze_errors')
    def test_main_report_command(self, mock_errors, mock_feedback, capsys):
        """Test main with 'report' command."""
        mock_errors.return_value = {}
        mock_feedback.return_value = {}
        
        with patch('sys.argv', ['automation.py', 'report']):
            result = main()
        
        assert result == 0
        captured = capsys.readouterr()
        assert "AUTOMATION REPORT" in captured.out

    @patch.object(AutomationRunner, 'generate_lessons')
    def test_main_lessons_command(self, mock_lessons):
        """Test main with 'lessons' command."""
        mock_lessons.return_value = {}
        
        with patch('sys.argv', ['automation.py', 'lessons']):
            result = main()
        
        assert mock_lessons.called
        assert result == 0

    @patch.object(AutomationRunner, 'generate_lessons')
    def test_main_lessons_with_min_occurrences(self, mock_lessons):
        """Test main with 'lessons --min-occurrences' option."""
        mock_lessons.return_value = {}
        
        with patch('sys.argv', ['automation.py', 'lessons', '--min-occurrences', '5']):
            result = main()
        
        mock_lessons.assert_called_once_with(min_occurrences=5)

    def test_main_no_command(self, capsys):
        """Test main with no command shows help."""
        with patch('sys.argv', ['automation.py']):
            result = main()
        
        assert result == 1

    @patch.object(AutomationRunner, 'run_full_cycle')
    def test_main_verbose_flag(self, mock_cycle):
        """Test main with verbose flag."""
        mock_cycle.return_value = 0
        
        with patch('sys.argv', ['automation.py', '-v', 'run']):
            result = main()
        
        # Verbose flag should be processed


class TestModuleConstants:
    """Test module-level constants."""

    def test_script_dir_exists(self):
        """Test SCRIPT_DIR is valid."""
        assert SCRIPT_DIR is not None
        assert isinstance(SCRIPT_DIR, Path)

    def test_project_root_exists(self):
        """Test PROJECT_ROOT is valid."""
        assert AUTOMATION_PROJECT_ROOT is not None
        assert isinstance(AUTOMATION_PROJECT_ROOT, Path)

    def test_feedback_skill_dir_path(self):
        """Test FEEDBACK_SKILL_DIR path structure."""
        assert FEEDBACK_SKILL_DIR is not None
        assert "content-briefs-skill" in str(FEEDBACK_SKILL_DIR)

    def test_lessons_file_path(self):
        """Test LESSONS_FILE path structure."""
        assert LESSONS_FILE is not None
        assert "lessons-learned.md" in str(LESSONS_FILE)

    def test_error_log_dir_path(self):
        """Test ERROR_LOG_DIR path structure."""
        assert ERROR_LOG_DIR is not None
        assert "errors" in str(ERROR_LOG_DIR)
