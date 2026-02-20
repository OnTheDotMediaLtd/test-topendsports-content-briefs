#!/usr/bin/env python3
"""
Unit tests for scripts/validate_brands_gate.py using direct imports + mocking.
Covers the lines missed by the subprocess-based tests (which don't trace coverage).

Targets:
- validate_brief_brands(): all branches (not found, read error, valid, invalid)
- main(): no args, error detail, pass, fail, strict flag, suggestions, all output paths
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure scripts/ is on path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from validate_brands_gate import validate_brief_brands, main


# ─────────────────────────────────────────────────────────────
# Helpers — build mock BrandValidator result
# ─────────────────────────────────────────────────────────────

def make_result(valid=True, verified=None, unknown=None, suspicious=None,
                errors=None, warnings=None, suggestions=None):
    r = MagicMock()
    r.valid = valid
    r.verified_brands = verified or []
    r.unknown_brands = unknown or []
    r.suspicious_brands = suspicious or []
    r.errors = errors or []
    r.warnings = warnings or []
    r.suggestions = suggestions or {}
    return r


# ─────────────────────────────────────────────────────────────
# validate_brief_brands()
# ─────────────────────────────────────────────────────────────

class TestValidateBriefBrands:
    def test_file_not_found_returns_false(self):
        is_valid, details = validate_brief_brands(Path("/nonexistent/brief.md"))
        assert is_valid is False
        assert details["error"] == "File not found"

    def test_read_error_returns_false(self, tmp_path):
        """Exception during read_text returns False with error detail."""
        f = tmp_path / "brief.md"
        f.write_text("content", encoding="utf-8")

        with patch("pathlib.Path.read_text", side_effect=IOError("disk full")):
            is_valid, details = validate_brief_brands(f)

        assert is_valid is False
        assert "disk full" in details["error"]

    @patch("validate_brands_gate.BrandValidator")
    def test_valid_brands_returns_true(self, mock_cls, tmp_path):
        brief = tmp_path / "brief.md"
        brief.write_text("# Betting guide\n\nFanDuel is great.", encoding="utf-8")

        mock_validator = MagicMock()
        mock_cls.return_value = mock_validator
        mock_validator.validate.return_value = make_result(
            valid=True,
            verified=["FanDuel"],
        )

        is_valid, details = validate_brief_brands(brief, strict=False)

        assert is_valid is True
        assert "FanDuel" in details["verified_brands"]
        mock_cls.assert_called_once_with(strict_mode=False)

    @patch("validate_brands_gate.BrandValidator")
    def test_suspicious_brands_returns_false(self, mock_cls, tmp_path):
        brief = tmp_path / "brief.md"
        brief.write_text("GhostBet Casino is top.", encoding="utf-8")

        mock_validator = MagicMock()
        mock_cls.return_value = mock_validator
        mock_validator.validate.return_value = make_result(
            valid=False,
            suspicious=["GhostBet Casino"],
            errors=["Suspicious brand: GhostBet Casino"],
        )

        is_valid, details = validate_brief_brands(brief, strict=False)

        assert is_valid is False
        assert "GhostBet Casino" in details["suspicious_brands"]
        assert details["errors"]

    @patch("validate_brands_gate.BrandValidator")
    def test_strict_mode_passed_to_validator(self, mock_cls, tmp_path):
        brief = tmp_path / "brief.md"
        brief.write_text("FanDuel", encoding="utf-8")

        mock_validator = MagicMock()
        mock_cls.return_value = mock_validator
        mock_validator.validate.return_value = make_result(valid=True)

        validate_brief_brands(brief, strict=True)
        mock_cls.assert_called_once_with(strict_mode=True)

    @patch("validate_brands_gate.BrandValidator")
    def test_suggestions_propagated(self, mock_cls, tmp_path):
        brief = tmp_path / "brief.md"
        brief.write_text("Wyns is cool.", encoding="utf-8")

        mock_validator = MagicMock()
        mock_cls.return_value = mock_validator
        mock_validator.validate.return_value = make_result(
            valid=False,
            unknown=["Wyns"],
            suggestions={"Wyns": ["WynnBET"]},
        )

        is_valid, details = validate_brief_brands(brief, strict=True)

        assert "Wyns" in details["unknown_brands"]
        assert details["suggestions"]["Wyns"] == ["WynnBET"]

    @patch("validate_brands_gate.BrandValidator")
    def test_warnings_propagated(self, mock_cls, tmp_path):
        brief = tmp_path / "brief.md"
        brief.write_text("Content.", encoding="utf-8")

        mock_validator = MagicMock()
        mock_cls.return_value = mock_validator
        mock_validator.validate.return_value = make_result(
            valid=True,
            warnings=["No brands detected"],
        )

        is_valid, details = validate_brief_brands(brief)
        assert "No brands detected" in details["warnings"]


# ─────────────────────────────────────────────────────────────
# main()
# ─────────────────────────────────────────────────────────────

class TestMain:
    def test_no_args_exits_2(self):
        with patch("sys.argv", ["validate_brands_gate.py"]):
            with pytest.raises(SystemExit) as exc:
                main()
        assert exc.value.code == 2

    def test_missing_file_exits_2(self):
        with patch("sys.argv", ["script.py", "/tmp/no_such_brief_xyz.md"]):
            with pytest.raises(SystemExit) as exc:
                main()
        assert exc.value.code == 2

    @patch("validate_brands_gate.validate_brief_brands")
    def test_error_detail_exits_2(self, mock_validate, tmp_path):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (False, {"error": "Something broke"})

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit) as exc:
                main()
        assert exc.value.code == 2

    @patch("validate_brands_gate.validate_brief_brands")
    def test_all_verified_exits_0(self, mock_validate, tmp_path):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": ["FanDuel", "BetMGM"],
            "unknown_brands": [],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit) as exc:
                main()
        assert exc.value.code == 0

    @patch("validate_brands_gate.validate_brief_brands")
    def test_suspicious_brands_exits_1(self, mock_validate, tmp_path):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (False, {
            "verified_brands": [],
            "unknown_brands": [],
            "suspicious_brands": ["FakeBet"],
            "errors": ["Suspicious: FakeBet"],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit) as exc:
                main()
        assert exc.value.code == 1

    @patch("validate_brands_gate.validate_brief_brands")
    def test_strict_flag_passed(self, mock_validate, tmp_path):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": [],
            "unknown_brands": [],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f), "--strict"]):
            with pytest.raises(SystemExit):
                main()

        mock_validate.assert_called_once_with(f, strict=True)

    @patch("validate_brands_gate.validate_brief_brands")
    def test_no_strict_flag_default_false(self, mock_validate, tmp_path):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": [],
            "unknown_brands": [],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit):
                main()

        mock_validate.assert_called_once_with(f, strict=False)

    @patch("validate_brands_gate.validate_brief_brands")
    def test_unknown_brands_shown_with_suggestion(self, mock_validate, tmp_path, capsys):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": [],
            "unknown_brands": ["Wyns"],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {"Wyns": ["WynnBET"]},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "Wyns" in captured.out
        assert "WynnBET" in captured.out

    @patch("validate_brands_gate.validate_brief_brands")
    def test_unknown_brands_shown_without_suggestion(self, mock_validate, tmp_path, capsys):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": [],
            "unknown_brands": ["TotallyUnknown"],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "TotallyUnknown" in captured.out

    @patch("validate_brands_gate.validate_brief_brands")
    def test_errors_and_warnings_sections_shown(self, mock_validate, tmp_path, capsys):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (False, {
            "verified_brands": [],
            "unknown_brands": [],
            "suspicious_brands": ["GhostBet"],
            "errors": ["Suspicious: GhostBet"],
            "warnings": ["Please review"],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "Suspicious: GhostBet" in captured.out
        assert "Please review" in captured.out

    @patch("validate_brands_gate.validate_brief_brands")
    def test_strict_mode_shows_in_header(self, mock_validate, tmp_path, capsys):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": [],
            "unknown_brands": [],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f), "--strict"]):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "STRICT" in captured.out

    @patch("validate_brands_gate.validate_brief_brands")
    def test_lenient_mode_shows_in_header(self, mock_validate, tmp_path, capsys):
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": [],
            "unknown_brands": [],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "LENIENT" in captured.out

    @patch("validate_brands_gate.validate_brief_brands")
    def test_empty_sections_not_printed(self, mock_validate, tmp_path, capsys):
        """No verified/unknown/suspicious sections when all lists are empty."""
        f = tmp_path / "b.md"
        f.write_text("x", encoding="utf-8")

        mock_validate.return_value = (True, {
            "verified_brands": [],
            "unknown_brands": [],
            "suspicious_brands": [],
            "errors": [],
            "warnings": [],
            "suggestions": {},
        })

        with patch("sys.argv", ["script.py", str(f)]):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "Verified brands" not in captured.out
        assert "Unknown brands" not in captured.out
        assert "Suspicious" not in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
