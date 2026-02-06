#!/usr/bin/env python3
"""
Comprehensive tests for Phase JSON Validation Script.

Tests cover:
- Phase 1, 2, 3 validation rules
- Edge cases and boundary conditions
- Error handling and JSON parsing
- Report generation
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add scripts to path
SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_phase_json import PhaseJSONValidator, ValidationResult


class TestPhaseJSONValidatorInit:
    """Tests for PhaseJSONValidator initialization."""

    def test_init_with_path_and_phase(self, tmp_path):
        """Test initialization with both path and phase."""
        json_file = tmp_path / "test.json"
        json_file.write_text("{}")
        
        validator = PhaseJSONValidator(json_file, phase=1)
        assert validator.json_file == json_file
        assert validator.phase == 1
        assert validator.data is None
        assert validator.errors == []
        assert validator.warnings == []

    def test_init_without_phase_auto_detect(self, tmp_path):
        """Test initialization without phase triggers auto-detection."""
        json_file = tmp_path / "test.json"
        json_file.write_text("{}")
        
        validator = PhaseJSONValidator(json_file)
        assert validator.phase is None


class TestPhaseJSONValidatorReadJSON:
    """Tests for JSON reading functionality."""

    def test_read_valid_json(self, tmp_path):
        """Test reading valid JSON file."""
        json_file = tmp_path / "valid.json"
        json_file.write_text('{"key": "value"}')
        
        validator = PhaseJSONValidator(json_file)
        result = validator._read_json()
        
        assert result is True
        assert validator.data == {"key": "value"}

    def test_read_invalid_json_syntax(self, tmp_path):
        """Test reading invalid JSON syntax."""
        json_file = tmp_path / "invalid.json"
        json_file.write_text('{"key": invalid}')
        
        validator = PhaseJSONValidator(json_file)
        result = validator._read_json()
        
        assert result is False
        assert len(validator.errors) > 0
        assert "Invalid JSON" in validator.errors[0]

    def test_read_empty_json_file(self, tmp_path):
        """Test reading empty JSON file."""
        json_file = tmp_path / "empty.json"
        json_file.write_text('')
        
        validator = PhaseJSONValidator(json_file)
        result = validator._read_json()
        
        assert result is False

    def test_read_nonexistent_file(self, tmp_path):
        """Test reading non-existent file."""
        json_file = tmp_path / "nonexistent.json"
        
        validator = PhaseJSONValidator(json_file)
        result = validator.validate()
        
        assert result is False
        assert "File not found" in validator.errors[0]


class TestPhaseDetection:
    """Tests for automatic phase detection."""

    def test_detect_phase_1(self, tmp_path):
        """Test detecting Phase 1 JSON structure."""
        json_file = tmp_path / "phase1.json"
        phase1_data = {
            "primary_keyword": "betting sites",
            "secondary_keywords": ["sports betting", "online betting"]
        }
        json_file.write_text(json.dumps(phase1_data))
        
        validator = PhaseJSONValidator(json_file)
        validator._read_json()
        detected_phase = validator._detect_phase()
        
        assert detected_phase == 1

    def test_detect_phase_2(self, tmp_path):
        """Test detecting Phase 2 JSON structure."""
        json_file = tmp_path / "phase2.json"
        phase2_data = {
            "content_outline": {"intro": "text", "body": "text"},
            "h2_sections": {"Section 1": {}}
        }
        json_file.write_text(json.dumps(phase2_data))
        
        validator = PhaseJSONValidator(json_file)
        validator._read_json()
        detected_phase = validator._detect_phase()
        
        assert detected_phase == 2

    def test_detect_phase_3(self, tmp_path):
        """Test detecting Phase 3 JSON structure."""
        json_file = tmp_path / "phase3.json"
        phase3_data = {
            "html_content": "<html></html>",
            "schema_markup": {"@type": "Article"}
        }
        json_file.write_text(json.dumps(phase3_data))
        
        validator = PhaseJSONValidator(json_file)
        validator._read_json()
        detected_phase = validator._detect_phase()
        
        assert detected_phase == 3

    def test_detect_phase_unknown(self, tmp_path):
        """Test detecting unknown phase structure."""
        json_file = tmp_path / "unknown.json"
        unknown_data = {"random_field": "value"}
        json_file.write_text(json.dumps(unknown_data))
        
        validator = PhaseJSONValidator(json_file)
        validator._read_json()
        detected_phase = validator._detect_phase()
        
        assert detected_phase is None

    def test_detect_phase_with_non_dict_data(self, tmp_path):
        """Test phase detection with non-dict JSON data."""
        json_file = tmp_path / "array.json"
        json_file.write_text('[1, 2, 3]')
        
        validator = PhaseJSONValidator(json_file)
        validator._read_json()
        detected_phase = validator._detect_phase()
        
        assert detected_phase is None


class TestPhase1Validation:
    """Tests for Phase 1 validation rules."""

    def test_valid_phase1_data(self, tmp_path):
        """Test valid Phase 1 data passes validation."""
        json_file = tmp_path / "phase1_valid.json"
        valid_data = {
            "primary_keyword": "best betting sites",
            "secondary_keywords": [
                {"keyword": f"keyword_{i}", "volume": 1000 + i * 100}
                for i in range(10)
            ],
            "competitor_analysis": {
                "comp1": {}, "comp2": {}, "comp3": {}
            },
            "brand_selection": {
                "1": "FanDuel",
                "2": "BetMGM",
                "3": "DraftKings"
            },
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(valid_data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        # Check individual validations passed
        checks_passed = {c.check_name: c.passed for c in validator.checks}
        assert checks_passed.get("Primary Keyword Present") is True
        assert checks_passed.get("Writer Assignment") is True

    def test_missing_primary_keyword(self, tmp_path):
        """Test validation fails without primary keyword."""
        json_file = tmp_path / "no_primary.json"
        data = {
            "secondary_keywords": [],
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Primary Keyword Present") is False

    def test_secondary_keywords_count_too_few(self, tmp_path):
        """Test validation fails with too few secondary keywords."""
        json_file = tmp_path / "few_keywords.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": f"kw_{i}", "volume": 100} for i in range(5)
            ],
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Secondary Keywords Count") is False

    def test_secondary_keywords_count_too_many(self, tmp_path):
        """Test validation fails with too many secondary keywords."""
        json_file = tmp_path / "many_keywords.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": f"kw_{i}", "volume": 100} for i in range(20)
            ],
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Secondary Keywords Count") is False

    def test_secondary_keywords_as_dict(self, tmp_path):
        """Test secondary keywords as dictionary format."""
        json_file = tmp_path / "dict_keywords.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": {
                str(i): {"keyword": f"kw_{i}", "volume": 100} for i in range(10)
            },
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        # Should handle dict format correctly
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Secondary Keywords Count") is True

    def test_missing_keyword_volume(self, tmp_path):
        """Test validation catches missing volume data."""
        json_file = tmp_path / "missing_volume.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": "kw1"},  # Missing volume
                {"keyword": "kw2", "volume": 100}
            ] + [{"keyword": f"kw_{i}", "volume": 100} for i in range(8)],
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        # Should have error about missing volume
        volume_errors = [e for e in validator.errors if "volume" in e.lower()]
        assert len(volume_errors) > 0

    def test_insufficient_competitors(self, tmp_path):
        """Test validation fails with insufficient competitors."""
        json_file = tmp_path / "few_competitors.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw_{i}", "volume": 100} for i in range(10)],
            "competitor_analysis": {"comp1": {}, "comp2": {}},
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Competitor Analysis") is False

    def test_invalid_brand_selection_not_fanduel_first(self, tmp_path):
        """Test validation fails when FanDuel is not ranked #1."""
        json_file = tmp_path / "wrong_brand.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw_{i}", "volume": 100} for i in range(10)],
            "brand_selection": {
                "1": "DraftKings",  # Should be FanDuel
                "2": "BetMGM"
            },
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Brand Selection") is False

    def test_invalid_writer(self, tmp_path):
        """Test validation fails with invalid writer name."""
        json_file = tmp_path / "invalid_writer.json"
        data = {
            "primary_keyword": "test",
            "assigned_writer": "InvalidWriter"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Writer Assignment") is False

    @pytest.mark.parametrize("writer", ["Lewis", "Tom", "Gustavo Cantella"])
    def test_valid_writers(self, tmp_path, writer):
        """Test all valid writer names pass validation."""
        json_file = tmp_path / f"writer_{writer.replace(' ', '_')}.json"
        data = {
            "primary_keyword": "test",
            "assigned_writer": writer
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Writer Assignment") is True


class TestPhase2Validation:
    """Tests for Phase 2 validation rules."""

    def test_valid_phase2_data(self, tmp_path):
        """Test valid Phase 2 data passes validation."""
        json_file = tmp_path / "phase2_valid.json"
        valid_data = {
            "content_outline": {"intro": "text", "body": "text"},
            "h2_sections": {
                "Section 1": {"keyword": "test kw", "volume": 5000}
            },
            "h3_sections": {
                "Subsection 1": {"keyword": "sub kw", "volume": 500}
            },
            "content_type": "article",
            "faq": {
                "questions": [
                    {"question": f"Q{i}?", "keyword": f"q_kw_{i}"} for i in range(6)
                ]
            },
            "source_requirements": {"tier1_preferred": True}
        }
        json_file.write_text(json.dumps(valid_data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        result = validator.validate()
        
        # Should pass most checks
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Content Outline Present") is True

    def test_missing_content_outline(self, tmp_path):
        """Test validation fails without content outline."""
        json_file = tmp_path / "no_outline.json"
        data = {"h2_sections": {}}
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Content Outline Present") is False

    def test_no_h2_sections(self, tmp_path):
        """Test validation fails without H2 sections."""
        json_file = tmp_path / "no_h2.json"
        data = {"content_outline": {"test": "content"}}
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("H2 Sections Present") is False

    def test_faq_count_for_article(self, tmp_path):
        """Test FAQ count validation for article type."""
        json_file = tmp_path / "article_faq.json"
        data = {
            "content_outline": {"test": "content"},
            "content_type": "article",
            "faq": {
                "questions": [
                    {"question": f"Q{i}?", "keyword": f"kw_{i}"} for i in range(3)
                ]
            }
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("FAQ Questions Count") is False  # Only 3, need 5-7

    def test_faq_count_for_review(self, tmp_path):
        """Test FAQ count validation for review type."""
        json_file = tmp_path / "review_faq.json"
        data = {
            "content_outline": {"test": "content"},
            "content_type": "review",
            "faq": {
                "questions": [
                    {"question": f"Q{i}?", "keyword": f"kw_{i}"} for i in range(6)
                ]
            }
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("FAQ Questions Count") is True

    def test_h2_section_low_volume_keyword(self, tmp_path):
        """Test H2 sections with low-volume keywords fail validation."""
        json_file = tmp_path / "low_volume_h2.json"
        data = {
            "content_outline": {"test": "content"},
            "h2_sections": {
                "Section 1": {"keyword": "test", "volume": 100}  # Below 1000 threshold
            }
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("H2 Sections Keyword Mapping") is False


class TestPhase3Validation:
    """Tests for Phase 3 validation rules."""

    def test_valid_phase3_data(self, tmp_path):
        """Test valid Phase 3 data passes validation."""
        json_file = tmp_path / "phase3_valid.json"
        valid_data = {
            "html_content": "<html><body>Content</body></html>",
            "schema_markup": {
                "@type": "Article",
                "faq": "@type FAQPage",
                "breadcrumblist": "@type BreadcrumbList"
            },
            "responsible_gambling_section": "Gamble responsibly. 21+.",
            "brands_featured": ["FanDuel", "DraftKings"],
            "terms_and_conditions": {
                "FanDuel": "T&Cs apply",
                "DraftKings": "T&Cs apply"
            },
            "interactive_elements": {"calculator": True}
        }
        json_file.write_text(json.dumps(valid_data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        result = validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("HTML Content Present") is True
        assert checks.get("Responsible Gambling Section") is True

    def test_missing_html_content(self, tmp_path):
        """Test validation fails without HTML content."""
        json_file = tmp_path / "no_html.json"
        data = {"schema_markup": {}}
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("HTML Content Present") is False

    def test_missing_schema_markup(self, tmp_path):
        """Test validation fails without schema markup."""
        json_file = tmp_path / "no_schema.json"
        data = {"html_content": "<html></html>"}
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Schema Markup Present") is False

    def test_missing_responsible_gambling(self, tmp_path):
        """Test validation fails without responsible gambling section."""
        json_file = tmp_path / "no_rg.json"
        data = {
            "html_content": "<html></html>",
            "schema_markup": {}
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Responsible Gambling Section") is False

    def test_missing_tcs_for_brands(self, tmp_path):
        """Test validation fails when brands are missing T&Cs."""
        json_file = tmp_path / "missing_tcs.json"
        data = {
            "html_content": "<html></html>",
            "schema_markup": {},
            "brands_featured": ["FanDuel", "DraftKings"],
            "terms_and_conditions": {
                "FanDuel": "T&Cs"
                # Missing DraftKings
            }
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        validator.validate()
        
        checks = {c.check_name: c.passed for c in validator.checks}
        assert checks.get("Terms & Conditions") is False


class TestValidationReport:
    """Tests for validation report generation."""

    def test_get_report_structure(self, tmp_path):
        """Test report dictionary structure."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"primary_keyword": "test"}')
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        report = validator.get_report()
        
        assert "file" in report
        assert "phase" in report
        assert "valid" in report
        assert "error_count" in report
        assert "warning_count" in report
        assert "checks_run" in report
        assert "checks" in report
        assert "errors" in report
        assert "warnings" in report

    def test_print_report_executes(self, tmp_path):
        """Test print_report executes without error."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"primary_keyword": "test"}')
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        # Just test it doesn't crash
        validator.print_report()


class TestValidationResultDataclass:
    """Tests for ValidationResult dataclass."""

    def test_validation_result_creation(self):
        """Test creating ValidationResult."""
        result = ValidationResult(
            check_name="Test Check",
            passed=True,
            message="Check passed",
            severity="error"
        )
        
        assert result.check_name == "Test Check"
        assert result.passed is True
        assert result.message == "Check passed"
        assert result.severity == "error"

    def test_validation_result_default_severity(self):
        """Test ValidationResult default severity is 'error'."""
        result = ValidationResult(
            check_name="Test",
            passed=False,
            message="Failed"
        )
        
        assert result.severity == "error"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_json_object(self, tmp_path):
        """Test validation with empty JSON object."""
        json_file = tmp_path / "empty_obj.json"
        json_file.write_text('{}')
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        # Should fail validation
        assert result is False

    def test_deeply_nested_json(self, tmp_path):
        """Test validation with deeply nested JSON."""
        json_file = tmp_path / "nested.json"
        nested_data = {
            "primary_keyword": "test",
            "nested": {"level1": {"level2": {"level3": "value"}}}
        }
        json_file.write_text(json.dumps(nested_data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        # Should not crash on deep nesting
        assert validator.data is not None

    def test_unicode_content(self, tmp_path):
        """Test validation with Unicode content."""
        json_file = tmp_path / "unicode.json"
        unicode_data = {
            "primary_keyword": "bésting sîtes ñ",
            "secondary_keywords": [
                {"keyword": "キーワード", "volume": 1000}
            ],
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(unicode_data, ensure_ascii=False), encoding='utf-8')
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        # Should handle unicode without errors
        assert validator.data is not None

    def test_null_values_in_json(self, tmp_path):
        """Test validation handles null values."""
        json_file = tmp_path / "nulls.json"
        null_data = {
            "primary_keyword": None,
            "secondary_keywords": None,
            "assigned_writer": None
        }
        json_file.write_text(json.dumps(null_data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        # Should handle nulls gracefully
        assert result is False  # Nulls don't count as present

    def test_very_large_json(self, tmp_path):
        """Test validation with large JSON file."""
        json_file = tmp_path / "large.json"
        large_data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": f"keyword_{i}", "volume": i * 10}
                for i in range(1000)
            ],
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(large_data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        # Should handle large files
        assert validator.data is not None
        assert len(validator.data["secondary_keywords"]) == 1000

    def test_invalid_phase_number(self, tmp_path):
        """Test validation with invalid phase number."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{}')
        
        validator = PhaseJSONValidator(json_file, phase=99)
        result = validator.validate()
        
        assert result is False
        assert any("Invalid phase" in e for e in validator.errors)

    def test_json_with_trailing_comma(self, tmp_path):
        """Test validation handles JSON with trailing comma (should fail)."""
        json_file = tmp_path / "trailing.json"
        # Note: This is invalid JSON
        json_file.write_text('{"key": "value",}')
        
        validator = PhaseJSONValidator(json_file)
        result = validator.validate()
        
        # Should fail to parse
        assert result is False

    def test_keyword_volume_zero(self, tmp_path):
        """Test validation with keyword volume of zero."""
        json_file = tmp_path / "zero_volume.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": f"kw_{i}", "volume": 0} for i in range(10)
            ],
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        # Volume of 0 should be considered present (it's a valid value)
        checks = {c.check_name: c.passed for c in validator.checks}
        # Check that keyword validation ran
        assert "Keyword Volume Data" in checks or "Keyword 1 Volume Data" in checks


class TestAddCheck:
    """Tests for the _add_check method."""

    def test_add_check_passed(self, tmp_path):
        """Test adding a passed check."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{}')
        
        validator = PhaseJSONValidator(json_file)
        validator._add_check("Test Check", True, "Check passed")
        
        assert len(validator.checks) == 1
        assert validator.checks[0].passed is True
        assert len(validator.errors) == 0

    def test_add_check_failed_error(self, tmp_path):
        """Test adding a failed check with error severity."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{}')
        
        validator = PhaseJSONValidator(json_file)
        validator._add_check("Test Check", False, "Check failed", severity="error")
        
        assert len(validator.checks) == 1
        assert validator.checks[0].passed is False
        assert len(validator.errors) == 1
        assert "Check failed" in validator.errors[0]

    def test_add_check_failed_warning(self, tmp_path):
        """Test adding a failed check with warning severity."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{}')
        
        validator = PhaseJSONValidator(json_file)
        validator._add_check("Test Check", False, "Check warned", severity="warning")
        
        assert len(validator.checks) == 1
        assert len(validator.errors) == 0
        assert len(validator.warnings) == 1


class TestMainFunction:
    """Tests for the main CLI function."""

    def test_main_no_args(self, monkeypatch):
        """Test main function with no arguments shows help."""
        import validate_phase_json as module
        
        monkeypatch.setattr('sys.argv', ['validate_phase_json.py'])
        
        with pytest.raises(SystemExit) as exc_info:
            module.main()
        
        assert exc_info.value.code == 1

    def test_main_with_valid_file(self, tmp_path, monkeypatch):
        """Test main function with valid file."""
        import validate_phase_json as module
        
        json_file = tmp_path / "test.json"
        json_file.write_text('{"primary_keyword": "test"}')
        
        monkeypatch.setattr('sys.argv', ['validate_phase_json.py', str(json_file), '--phase', '1'])
        
        # Should exit with 0 or 1 (pass or fail)
        with pytest.raises(SystemExit) as exc_info:
            module.main()
        assert exc_info.value.code in [0, 1]

    def test_main_json_output(self, tmp_path, monkeypatch):
        """Test main function with JSON output flag."""
        import validate_phase_json as module
        
        json_file = tmp_path / "test.json"
        json_file.write_text('{"primary_keyword": "test"}')
        
        monkeypatch.setattr('sys.argv', [
            'validate_phase_json.py', str(json_file), '--phase', '1', '--json'
        ])
        
        # Should exit without crashing
        with pytest.raises(SystemExit) as exc_info:
            module.main()
        assert exc_info.value.code in [0, 1]
