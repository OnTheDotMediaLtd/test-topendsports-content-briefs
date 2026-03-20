#!/usr/bin/env python3
"""
Final coverage gap tests targeting specific uncovered lines/branches.

Targets:
  validate_feedback.py:
    - Line 111: validate() returns False when _read_file() fails (e.g. UnicodeDecodeError)
    - Branch 378->375: print_report() with 2+ errors (loop iterates back to start)
    - Branch 491->477: main() outer loop with multiple feedback files

  automation.py:
    - Branch 150->160: analyze_errors() when stats command fails (code != 0)
    - Lines 320-321: analyze_content_patterns() when create_auto_feedback() raises
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timedelta

# Paths
TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
# NOTE: Do NOT insert SCRIPTS_DIR into sys.path at module level here —
# it would cache `scripts/validate_feedback.py` as `validate_feedback` in
# sys.modules and break tests/python/test_validate_feedback*.py which expect
# `content-briefs-skill/scripts/validate_feedback.py` (the one with validate_feedback_file).
# Instead, defer the import below using the correct path.

# ─────────────────────────────────────────────────────────────────────────────
# validate_feedback.py gaps
# Import FeedbackValidator from content-briefs-skill/scripts/ (the right module)
# ─────────────────────────────────────────────────────────────────────────────

_CB_SKILL_SCRIPTS = PROJECT_ROOT / "content-briefs-skill" / "scripts"
if str(_CB_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_CB_SKILL_SCRIPTS))
from validate_feedback import FeedbackValidator, ValidationError  # noqa: E402


class TestValidateFeedbackLine111:
    """Line 111: validate() → _read_file() returns False → early return False."""

    def test_validate_returns_false_when_read_file_fails(self, tmp_path):
        """_read_file fails due to UnicodeDecodeError → validate() returns False at line 111."""
        feedback_file = tmp_path / "2024-12-09-test-topic.md"
        # Write valid content so exists/is_file checks pass
        feedback_file.write_text("# Test Content\n\n## Issue\nText.", encoding="utf-8")

        validator = FeedbackValidator(feedback_file)

        # Patch _read_file to return False (simulates encoding error)
        with patch.object(validator, '_read_file', return_value=False):
            result = validator.validate()

        assert result is False, "validate() should return False when _read_file() returns False"

    def test_validate_returns_false_on_unicode_decode_error(self, tmp_path):
        """When open raises UnicodeDecodeError, _read_file() → False → validate() line 111."""
        feedback_file = tmp_path / "2025-01-15-unicode-test.md"
        feedback_file.write_bytes(b"# Header\n\n\xff\xfe bad bytes")  # non-UTF-8 bytes

        validator = FeedbackValidator(feedback_file)
        result = validator.validate()

        # Should fail (can't read the file as UTF-8)
        assert result is False


class TestPrintReportMultipleErrors:
    """Branch 378->375: for loop over errors with 2+ entries iterates back to line 375."""

    def _make_validator_with_errors(self, tmp_path, error_count: int) -> FeedbackValidator:
        """Create a FeedbackValidator with a given number of synthetic errors."""
        feedback_file = tmp_path / "2024-12-09-loop-test.md"
        feedback_file.write_text("# Valid content", encoding="utf-8")
        validator = FeedbackValidator(feedback_file)
        for i in range(error_count):
            validator.errors.append(ValidationError(i + 1, f"Error number {i + 1}", f"Fix {i + 1}"))
        return validator

    def test_print_report_two_errors_with_suggestions(self, tmp_path):
        """print_report with 2 errors that each have suggestions; loop iterates twice (378->375)."""
        validator = self._make_validator_with_errors(tmp_path, 2)
        with patch("builtins.print"):
            validator.print_report()  # Should loop through both errors without error

    def test_print_report_three_errors_no_suggestion_on_second(self, tmp_path):
        """Loop with mixed suggestion/no-suggestion errors covers 378 False branch too."""
        feedback_file = tmp_path / "2024-12-09-mixed-test.md"
        feedback_file.write_text("# Content", encoding="utf-8")
        validator = FeedbackValidator(feedback_file)
        validator.errors.append(ValidationError(1, "Error one", "Suggestion one"))
        validator.errors.append(ValidationError(2, "Error two", None))  # No suggestion
        validator.errors.append(ValidationError(3, "Error three", "Suggestion three"))
        with patch("builtins.print"):
            validator.print_report()

    def test_print_report_two_warnings(self, tmp_path):
        """Warnings loop with 2+ entries covers the warning for-loop iteration branch."""
        feedback_file = tmp_path / "2024-12-09-warn-test.md"
        feedback_file.write_text("# Content", encoding="utf-8")
        validator = FeedbackValidator(feedback_file)
        validator.warnings.append(ValidationError(1, "Warning one", "Fix one"))
        validator.warnings.append(ValidationError(2, "Warning two", None))
        with patch("builtins.print"):
            validator.print_report()


class TestValidateFeedbackMainMultipleFiles:
    """Branch 491->477: outer loop processes multiple files so inner loop restarts outer."""

    def test_main_validates_multiple_files(self, tmp_path):
        """Run main() with a directory containing 2 valid feedback files."""
        from validate_feedback import main

        # Create two valid feedback files
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        f1 = tmp_path / f"{today}-first-topic.md"
        f2 = tmp_path / f"{yesterday}-second-topic.md"

        content = (
            "## Issue\nTest issue content here.\n\n"
            "## Impact\nP2\n\n"
            "## Suggestion\nA fix.\n"
        )
        f1.write_text(content, encoding="utf-8")
        f2.write_text(content, encoding="utf-8")

        with patch("sys.argv", ["validate_feedback.py", str(tmp_path)]):
            with patch("builtins.print"):
                try:
                    main()
                except SystemExit:
                    pass  # main() calls sys.exit(); that's fine


# ─────────────────────────────────────────────────────────────────────────────
# automation.py gaps
# ─────────────────────────────────────────────────────────────────────────────

from automation import AutomationRunner as ContentBriefAutomation


class TestAnalyzeErrorsStatsFail:
    """Branch 150->160: analyze_errors() where the stats command itself fails (code != 0)."""

    def test_stats_command_fails_skips_analyze(self):
        """When stats run_command returns code=1, inner analyze block is skipped (150->160 branch)."""
        auto = ContentBriefAutomation(verbose=False)

        def mock_run_command(cmd, capture=True):
            # Stats command fails
            return 1, "", "error: tracker not found"

        with patch("builtins.print"):
            with patch.object(auto, 'run_command', side_effect=mock_run_command):
                from automation import SCRIPT_DIR
                with patch.object(Path, 'exists', return_value=True):
                    with patch.object(Path, 'is_file', return_value=True):
                        result = auto.analyze_errors()

        assert result is not None
        assert result["status"] == "failed"

    def test_stats_fail_result_has_error_key(self):
        """Failed stats command fills result with empty output and status=failed."""
        auto = ContentBriefAutomation(verbose=False)

        with patch("builtins.print"):
            with patch.object(auto, 'run_command', return_value=(2, "", "syntax error")):
                from automation import SCRIPT_DIR
                with patch.object(Path, 'exists', return_value=True):
                    with patch.object(Path, 'is_file', return_value=True):
                        result = auto.analyze_errors()

        assert "status" in result
        assert result["status"] == "failed"


class TestAnalyzeContentPatternsAutoFeedbackException:
    """Lines 320-321: analyze_content_patterns() with create_auto_feedback() raising."""

    def _make_mock_analyzer(self, feedback_side_effect):
        """Build mock PatternAnalyzer instance with severe alerts and failing create_auto_feedback."""
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_all_patterns.return_value = {"total_patterns": 3}
        mock_analyzer.generate_alerts.return_value = [
            {"severity": "critical", "pattern": "test"},
            {"severity": "high", "pattern": "test2"},
        ]
        mock_analyzer.create_auto_feedback.side_effect = feedback_side_effect
        return mock_analyzer

    def test_auto_feedback_exception_is_non_blocking(self):
        """create_auto_feedback() raises RuntimeError → caught as WARN, lines 320-321 covered."""
        import sys as _sys
        auto = ContentBriefAutomation(verbose=False)
        mock_analyzer = self._make_mock_analyzer(RuntimeError("disk full"))

        # PatternAnalyzer is imported locally via `from pattern_analyzer import PatternAnalyzer`
        # so we patch sys.modules to inject a mock module
        mock_pa_module = MagicMock()
        mock_pa_module.PatternAnalyzer = MagicMock(return_value=mock_analyzer)

        with patch("builtins.print"):
            with patch.dict(_sys.modules, {"pattern_analyzer": mock_pa_module}):
                result = auto.analyze_content_patterns()

        assert result is not None
        assert result.get("status") == "completed"
        mock_analyzer.create_auto_feedback.assert_called_once()

    def test_auto_feedback_oserror_is_non_blocking(self):
        """OSError from create_auto_feedback() is also caught and non-blocking (lines 320-321)."""
        import sys as _sys
        auto = ContentBriefAutomation(verbose=False)
        mock_analyzer = self._make_mock_analyzer(OSError("Permission denied"))

        mock_pa_module = MagicMock()
        mock_pa_module.PatternAnalyzer = MagicMock(return_value=mock_analyzer)

        with patch("builtins.print"):
            with patch.dict(_sys.modules, {"pattern_analyzer": mock_pa_module}):
                result = auto.analyze_content_patterns()

        assert result is not None
        assert result.get("status") == "completed"
