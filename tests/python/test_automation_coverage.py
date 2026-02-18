#!/usr/bin/env python3
"""Additional coverage tests for automation.py.

Targets uncovered lines:
- Line 55-56: UnicodeEncodeError in log()
- Line 69: verbose logging in run_command
- Line 87-88: TimeoutExpired exception
- Line 111: Tests failed logging
- Lines 148-158: Exception in analyze command
- Lines 155-156: Analysis command failure
- Lines 204-206: generate_lessons invalid file check
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from automation import AutomationRunner as ContentBriefAutomation


class TestAutomationLogUnicodeError:
    """Cover the UnicodeEncodeError handler in log()."""

    def test_log_unicode_encode_error(self):
        """Cover lines 55-56: UnicodeEncodeError fallback in log()."""
        auto = ContentBriefAutomation(verbose=False)

        # Mock print to raise UnicodeEncodeError on first call, succeed on second
        call_count = [0]
        original_print = print

        def mock_print(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise UnicodeEncodeError('cp1252', '', 0, 1, 'char not supported')
            # Second call is the ASCII fallback
            return original_print(*args, **kwargs)

        with patch('builtins.print', side_effect=mock_print):
            auto.log("Test message with special chars")
        assert call_count[0] == 2  # First fails, second succeeds


class TestAutomationRunCommand:
    """Cover edge cases in run_command()."""

    def test_verbose_logging(self):
        """Cover line 69: verbose mode logging."""
        auto = ContentBriefAutomation(verbose=True)

        with patch('builtins.print'):
            with patch('automation.subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(
                    returncode=0,
                    stdout="output",
                    stderr=""
                )
                code, out, err = auto.run_command(["echo", "test"])
                assert code == 0

    def test_timeout_expired(self):
        """Cover lines 87-88: subprocess.TimeoutExpired."""
        auto = ContentBriefAutomation(verbose=False)

        with patch('builtins.print'):
            with patch('automation.subprocess.run', side_effect=subprocess.TimeoutExpired(cmd=["test"], timeout=300)):
                code, out, err = auto.run_command(["long_running_cmd"])
                assert code == 1
                assert "timed out" in err.lower()

    def test_file_not_found(self):
        """Cover line 87: FileNotFoundError."""
        auto = ContentBriefAutomation(verbose=False)

        with patch('builtins.print'):
            with patch('automation.subprocess.run', side_effect=FileNotFoundError("no such command")):
                code, out, err = auto.run_command(["nonexistent_cmd"])
                assert code == 1
                assert "not found" in err.lower()


class TestAutomationRunTests:
    """Cover test failure logging."""

    def test_tests_failed_logging(self):
        """Cover line 111: log 'Tests failed!' when exit code != 0."""
        auto = ContentBriefAutomation(verbose=False)

        with patch('builtins.print'):
            with patch.object(auto, 'run_command', return_value=(1, "FAILED tests", "error output")):
                result = auto.run_tests(with_tracking=False)
                assert result is False
                assert auto.results["tests"]["status"] == "failed"


class TestAutomationAnalyzeErrors:
    """Cover analyze_errors edge cases."""

    def test_analyze_command_exception(self):
        """Cover lines 155-156: Exception during analyze command."""
        auto = ContentBriefAutomation(verbose=False)

        call_count = [0]

        def mock_run_command(cmd, capture=True):
            call_count[0] += 1
            if call_count[0] == 1:
                # First call (stats) succeeds
                return 0, "stats output", ""
            else:
                # Second call (analyze) raises exception
                raise RuntimeError("analyze failed")

        with patch('builtins.print'):
            with patch.object(auto, 'run_command', side_effect=mock_run_command):
                # Need error_tracker.py to exist
                from automation import SCRIPT_DIR
                with patch.object(Path, 'exists', return_value=True):
                    with patch.object(Path, 'is_file', return_value=True):
                        result = auto.analyze_errors()
                        assert result is not None


class TestAutomationGenerateLessons:
    """Cover generate_lessons edge cases."""

    def test_invalid_min_occurrences(self):
        """Cover line ~196: invalid min_occurrences parameter."""
        auto = ContentBriefAutomation(verbose=False)

        with patch('builtins.print'):
            with patch.object(auto, 'run_command', return_value=(0, "lessons output", "")):
                from automation import SCRIPT_DIR
                with patch.object(Path, 'exists', return_value=True):
                    with patch.object(Path, 'is_file', return_value=True):
                        result = auto.generate_lessons(min_occurrences=-1)
                        # Should use default of 3

    def test_error_tracker_not_a_file(self):
        """Cover lines 204-206: error tracker exists but is not a file."""
        auto = ContentBriefAutomation(verbose=False)

        with patch('builtins.print'):
            from automation import SCRIPT_DIR
            error_tracker = SCRIPT_DIR / "error_tracker.py"
            with patch.object(Path, 'exists', return_value=True):
                with patch.object(Path, 'is_file', return_value=False):
                    result = auto.generate_lessons()
                    assert auto.results["lessons"]["status"] == "skipped"


class TestValidateBrands:
    """Tests for the validate_brands() brand validation gate."""

    def test_validate_brands_gate_not_found(self, tmp_path):
        """validate_brands skips when gate script does not exist."""
        auto = ContentBriefAutomation(verbose=False)

        # Point to a non-existent gate script by monkeypatching the method
        with patch('builtins.print'):
            # Patch run_command to not be called; gate check happens before it
            # We simulate: gate script missing → skipped
            with patch('automation.SCRIPT_DIR', tmp_path):
                result = auto.validate_brands()
                assert auto.results["brands"]["status"] == "skipped"

    def test_validate_brands_no_brief_files(self, tmp_path):
        """validate_brands skips gracefully when no brief files in output_dir."""
        auto = ContentBriefAutomation(verbose=False)

        # Create a real gate script placeholder in tmp_path
        gate_script = tmp_path / "validate_brands_gate.py"
        gate_script.write_text("# placeholder\n", encoding='utf-8')

        # Patch both SCRIPT_DIR and PROJECT_ROOT so no standard output dirs exist
        fake_root = tmp_path / "project"
        fake_root.mkdir()

        with patch('builtins.print'):
            with patch('automation.SCRIPT_DIR', tmp_path):
                with patch('automation.PROJECT_ROOT', fake_root):
                    # output_dir is a separate empty tmp dir (no .md files)
                    empty_dir = tmp_path / "empty_output"
                    empty_dir.mkdir()
                    result = auto.validate_brands(output_dir=empty_dir)
                    assert auto.results["brands"]["status"] == "skipped"

    def test_validate_brands_all_pass(self, tmp_path):
        """validate_brands returns passed when all briefs are valid."""
        auto = ContentBriefAutomation(verbose=False)

        # Create gate script placeholder
        gate_script = tmp_path / "validate_brands_gate.py"
        gate_script.write_text("# placeholder\n", encoding='utf-8')

        # Patch PROJECT_ROOT so no standard output dirs leak in
        fake_root = tmp_path / "project"
        fake_root.mkdir()

        # Create brief files in a dedicated output dir
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        brief = output_dir / "canada-writer-brief.md"
        brief.write_text("# Canada Sports Betting\n\n### FanDuel\nFanDuel is great.\n", encoding='utf-8')

        with patch('builtins.print'):
            with patch('automation.SCRIPT_DIR', tmp_path):
                with patch('automation.PROJECT_ROOT', fake_root):
                    with patch.object(auto, 'run_command', return_value=(0, "All brands validated", "")):
                        result = auto.validate_brands(output_dir=output_dir)
                        assert auto.results["brands"]["status"] == "passed"
                        assert auto.results["brands"]["files_checked"] == 1

    def test_validate_brands_fake_brand_blocked(self, tmp_path):
        """validate_brands returns failed when brief contains fake brands."""
        auto = ContentBriefAutomation(verbose=False)

        # Create gate script placeholder
        gate_script = tmp_path / "validate_brands_gate.py"
        gate_script.write_text("# placeholder\n", encoding='utf-8')

        # Patch PROJECT_ROOT so no standard output dirs leak in
        fake_root = tmp_path / "project"
        fake_root.mkdir()

        # Create brief file with suspicious brand
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        brief = output_dir / "canada-writer-brief.md"
        brief.write_text("# Canada Sports Betting\n\n### Treasure Spins\nFake brand.\n", encoding='utf-8')

        with patch('builtins.print'):
            with patch('automation.SCRIPT_DIR', tmp_path):
                with patch('automation.PROJECT_ROOT', fake_root):
                    with patch.object(auto, 'run_command', return_value=(1, "", "BLOCKED: Fake brands found")):
                        result = auto.validate_brands(output_dir=output_dir)
                        assert auto.results["brands"]["status"] == "failed"
