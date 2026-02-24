"""
Tests for validate_phase_json_integrated.py - Coverage expansion.

This module imports from tes-shared-infrastructure which is not installed,
so we mock the import and test the actual validator logic.
"""

import json
import sys
import os
import importlib
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open


# ---------------------------------------------------------------------------
# Helper: import the module with mocked tes_shared dependency
# ---------------------------------------------------------------------------

def _import_module():
    """Import validate_phase_json_integrated with mocked tes_shared."""
    mock_tes_shared = MagicMock()
    mock_tes_shared.validators.json_schema.JSONSchemaValidator = MagicMock

    with patch.dict(sys.modules, {
        'tes_shared': mock_tes_shared,
        'tes_shared.validators': mock_tes_shared.validators,
        'tes_shared.validators.json_schema': mock_tes_shared.validators.json_schema,
    }):
        module_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'scripts', 'validate_phase_json_integrated.py'
        )
        spec = importlib.util.spec_from_file_location(
            'validate_phase_json_integrated', module_path
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return mod


MOD = _import_module()
PhaseJSONValidator = MOD.PhaseJSONValidator
ValidationResult = MOD.ValidationResult


# ---------------------------------------------------------------------------
# ValidationResult dataclass tests
# ---------------------------------------------------------------------------

class TestValidationResult:
    def test_default_severity(self):
        vr = ValidationResult(check_name="test", passed=True, message="ok")
        assert vr.severity == "error"

    def test_custom_severity(self):
        vr = ValidationResult(check_name="test", passed=False, message="bad", severity="warning")
        assert vr.severity == "warning"

    def test_fields(self):
        vr = ValidationResult("name", True, "msg", "info")
        assert vr.check_name == "name"
        assert vr.passed is True
        assert vr.message == "msg"
        assert vr.severity == "info"


# ---------------------------------------------------------------------------
# PhaseJSONValidator - init and file handling
# ---------------------------------------------------------------------------

class TestPhaseJSONValidatorInit:
    def test_init_defaults(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text("{}", encoding="utf-8")
        v = PhaseJSONValidator(f)
        assert v.json_file == f
        assert v.phase is None
        assert v.data is None
        assert v.errors == []
        assert v.warnings == []
        assert v.checks == []

    def test_init_with_phase(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text("{}", encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        assert v.phase == 2


class TestValidateFileHandling:
    def test_file_not_found(self, tmp_path):
        f = tmp_path / "nonexistent.json"
        v = PhaseJSONValidator(f)
        result = v.validate()
        assert result is False
        assert any("File not found" in e for e in v.errors)

    def test_invalid_json(self, tmp_path):
        f = tmp_path / "bad.json"
        f.write_text("{invalid json", encoding="utf-8")
        v = PhaseJSONValidator(f)
        result = v.validate()
        assert result is False
        assert any("Invalid JSON" in e for e in v.errors)

    def test_read_error(self, tmp_path):
        f = tmp_path / "err.json"
        f.write_text("{}", encoding="utf-8")
        v = PhaseJSONValidator(f)
        with patch("builtins.open", side_effect=IOError("disk error")):
            result = v._read_json()
        assert result is False
        assert any("Error reading file" in e for e in v.errors)

    def test_no_phase_detected(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text('{"random": "data"}', encoding="utf-8")
        v = PhaseJSONValidator(f)
        result = v.validate()
        assert result is False
        assert any("Could not determine phase" in e for e in v.errors)

    def test_invalid_phase(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text('{"primary_keyword": "test", "secondary_keywords": []}', encoding="utf-8")
        v = PhaseJSONValidator(f, phase=5)
        result = v.validate()
        assert result is False
        assert any("Invalid phase" in e for e in v.errors)


# ---------------------------------------------------------------------------
# Phase detection
# ---------------------------------------------------------------------------

class TestPhaseDetection:
    def test_detect_phase_1(self, tmp_path):
        data = {"primary_keyword": "test", "secondary_keywords": ["a", "b"]}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f)
        v.data = data
        assert v._detect_phase() == 1

    def test_detect_phase_2(self, tmp_path):
        data = {"content_outline": {"section": "test"}, "h2_sections": {}}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f)
        v.data = data
        assert v._detect_phase() == 2

    def test_detect_phase_2_h2_only(self, tmp_path):
        data = {"h2_sections": {"heading": {}}}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f)
        v.data = data
        assert v._detect_phase() == 2

    def test_detect_phase_3_html(self, tmp_path):
        data = {"html_content": "<p>test</p>"}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f)
        v.data = data
        assert v._detect_phase() == 3

    def test_detect_phase_3_schema(self, tmp_path):
        data = {"schema_markup": {"@type": "Article"}}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f)
        v.data = data
        assert v._detect_phase() == 3

    def test_detect_phase_none_for_non_dict(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text("[]", encoding="utf-8")
        v = PhaseJSONValidator(f)
        v.data = []
        assert v._detect_phase() is None

    def test_detect_phase_none_unknown(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text('{"foo": "bar"}', encoding="utf-8")
        v = PhaseJSONValidator(f)
        v.data = {"foo": "bar"}
        assert v._detect_phase() is None


# ---------------------------------------------------------------------------
# _add_check
# ---------------------------------------------------------------------------

class TestAddCheck:
    def test_add_passing_check(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text("{}", encoding="utf-8")
        v = PhaseJSONValidator(f)
        v._add_check("test", True, "all good")
        assert len(v.checks) == 1
        assert v.checks[0].passed is True
        assert len(v.errors) == 0
        assert len(v.warnings) == 0

    def test_add_failing_error_check(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text("{}", encoding="utf-8")
        v = PhaseJSONValidator(f)
        v._add_check("test", False, "failed", severity="error")
        assert len(v.errors) == 1
        assert "test: failed" in v.errors[0]

    def test_add_failing_warning_check(self, tmp_path):
        f = tmp_path / "test.json"
        f.write_text("{}", encoding="utf-8")
        v = PhaseJSONValidator(f)
        v._add_check("test", False, "warn", severity="warning")
        assert len(v.warnings) == 1
        assert len(v.errors) == 0


# ---------------------------------------------------------------------------
# Phase 1 validation
# ---------------------------------------------------------------------------

class TestPhase1Validation:
    def _make_valid_phase1(self):
        return {
            "primary_keyword": "best betting apps",
            "secondary_keywords": [
                {"keyword": f"kw{i}", "volume": 1000 + i} for i in range(10)
            ],
            "competitor_analysis": {"comp1": {}, "comp2": {}, "comp3": {}},
            "brand_selection": {
                "1": "FanDuel", "2": "BetMGM",
                "3": "DraftKings", "4": "Caesars"
            },
            "assigned_writer": "Lewis"
        }

    def test_valid_phase1(self, tmp_path):
        data = self._make_valid_phase1()
        f = tmp_path / "phase1.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        assert v.validate() is True
        assert len(v.errors) == 0

    def test_missing_primary_keyword(self, tmp_path):
        data = self._make_valid_phase1()
        data["primary_keyword"] = ""
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("Primary keyword" in c.message for c in v.checks if not c.passed)

    def test_secondary_keywords_too_few(self, tmp_path):
        data = self._make_valid_phase1()
        data["secondary_keywords"] = [{"keyword": "a", "volume": 100}]
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("secondary keywords" in c.message.lower() for c in v.checks if not c.passed)

    def test_secondary_keywords_as_dict(self, tmp_path):
        data = self._make_valid_phase1()
        data["secondary_keywords"] = {str(i): f"kw{i}" for i in range(10)}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        # Should convert dict to values list and pass count check
        passed_checks = [c for c in v.checks if "Secondary Keywords Count" in c.check_name]
        assert len(passed_checks) == 1
        assert passed_checks[0].passed is True

    def test_keyword_missing_volume(self, tmp_path):
        data = self._make_valid_phase1()
        data["secondary_keywords"] = [
            {"keyword": "kw1"},  # missing volume
            {"keyword": "kw2", "volume": 500},
        ] + [{"keyword": f"kw{i}", "volume": 100 * i} for i in range(3, 12)]
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("missing volume data" in c.message for c in v.checks if not c.passed)

    def test_keyword_volume_zero_is_valid(self, tmp_path):
        data = self._make_valid_phase1()
        data["secondary_keywords"] = [
            {"keyword": f"kw{i}", "volume": 0} for i in range(10)
        ]
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        # volume=0 should be valid (explicit zero is data)
        volume_checks = [c for c in v.checks if "Keyword Volume Data" == c.check_name]
        assert len(volume_checks) == 1
        assert volume_checks[0].passed is True

    def test_no_competitors(self, tmp_path):
        data = self._make_valid_phase1()
        data["competitor_analysis"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("competitors" in c.message.lower() for c in v.checks if not c.passed)

    def test_brand_no_selection(self, tmp_path):
        data = self._make_valid_phase1()
        data["brand_selection"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("No brands selected" in c.message for c in v.checks if not c.passed)

    def test_brand_wrong_first(self, tmp_path):
        data = self._make_valid_phase1()
        data["brand_selection"]["1"] = "DraftKings"
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("FanDuel MUST be ranked #1" in c.message for c in v.checks if not c.passed)

    def test_brand_wrong_second(self, tmp_path):
        data = self._make_valid_phase1()
        data["brand_selection"]["2"] = "DraftKings"
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("BetMGM MUST be ranked #2" in c.message for c in v.checks if not c.passed)

    def test_brand_no_research_3_10(self, tmp_path):
        data = self._make_valid_phase1()
        data["brand_selection"] = {"1": "FanDuel", "2": "BetMGM"}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("Research brands #3-10 required" in c.message for c in v.checks if not c.passed)

    def test_invalid_writer(self, tmp_path):
        data = self._make_valid_phase1()
        data["assigned_writer"] = "Unknown Writer"
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        assert any("Invalid writer" in c.message for c in v.checks if not c.passed)

    def test_empty_secondary_keywords(self, tmp_path):
        data = self._make_valid_phase1()
        data["secondary_keywords"] = []
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        # 0 keywords, 8-15 required -> fail
        assert any("secondary keywords" in c.message.lower() for c in v.checks if not c.passed)

    def test_keywords_not_dict_items(self, tmp_path):
        """Keywords as plain strings (not dicts) - no volume check."""
        data = self._make_valid_phase1()
        data["secondary_keywords"] = [f"kw{i}" for i in range(10)]
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        # Plain strings have no volume to check - should still pass volume gate
        volume_checks = [c for c in v.checks if "Keyword Volume Data" == c.check_name]
        assert len(volume_checks) == 1
        assert volume_checks[0].passed is True


# ---------------------------------------------------------------------------
# Phase 2 validation
# ---------------------------------------------------------------------------

class TestPhase2Validation:
    def _make_valid_phase2(self):
        return {
            "content_outline": {"intro": "Introduction", "body": "Main content"},
            "h2_sections": {
                "Best Betting Apps": {"keyword": "best betting apps", "volume": 5000},
                "Top Sportsbooks": {"keyword": "top sportsbooks", "volume": 3000},
            },
            "faq": {"questions": [f"Q{i}?" for i in range(8)]},
            "source_requirements": {"tier1_preferred": True}
        }

    def test_valid_phase2(self, tmp_path):
        data = self._make_valid_phase2()
        f = tmp_path / "phase2.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        assert v.validate() is True

    def test_missing_content_outline(self, tmp_path):
        data = self._make_valid_phase2()
        data["content_outline"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        assert any("Content outline" in c.message for c in v.checks if not c.passed)

    def test_no_h2_sections(self, tmp_path):
        data = self._make_valid_phase2()
        data["h2_sections"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        assert any("h2 sections" in c.message.lower() for c in v.checks if not c.passed)

    def test_h2_low_volume_keyword(self, tmp_path):
        data = self._make_valid_phase2()
        data["h2_sections"] = {
            "Low Volume": {"keyword": "obscure term", "volume": 50}
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        assert any("not mapped to high-volume" in c.message for c in v.checks if not c.passed)

    def test_h2_missing_keyword(self, tmp_path):
        data = self._make_valid_phase2()
        data["h2_sections"] = {
            "No Keyword": {"volume": 5000}  # keyword missing
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        assert any("not mapped to high-volume" in c.message for c in v.checks if not c.passed)

    def test_h2_non_dict_content(self, tmp_path):
        """H2 section content is a string, not a dict - should pass keyword mapping."""
        data = self._make_valid_phase2()
        data["h2_sections"] = {"Heading": "just a string"}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        # Non-dict content skips keyword check, so h2_keyword_valid stays True
        mapping_checks = [c for c in v.checks if "Keyword Mapping" in c.check_name]
        assert len(mapping_checks) == 1
        assert mapping_checks[0].passed is True

    def test_faq_too_few_questions(self, tmp_path):
        data = self._make_valid_phase2()
        data["faq"] = {"questions": ["Q1?", "Q2?"]}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        assert any("FAQ" in c.check_name and not c.passed for c in v.checks)

    def test_faq_not_dict(self, tmp_path):
        data = self._make_valid_phase2()
        data["faq"] = "not a dict"
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        # faq not dict -> questions = [] -> count 0 < 7 -> fail
        assert any("FAQ" in c.check_name and not c.passed for c in v.checks)

    def test_source_requirements_present(self, tmp_path):
        data = self._make_valid_phase2()
        data["source_requirements"] = {"tier1_preferred": False}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        src_checks = [c for c in v.checks if "Source Requirements" in c.check_name]
        assert len(src_checks) == 1
        # tier1_preferred=False but sources dict is truthy -> passes with generic message
        assert src_checks[0].passed is True

    def test_source_requirements_empty(self, tmp_path):
        data = self._make_valid_phase2()
        data["source_requirements"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        src_checks = [c for c in v.checks if "Source Requirements" in c.check_name]
        assert len(src_checks) == 1
        assert src_checks[0].passed is False

    def test_source_requirements_not_dict(self, tmp_path):
        data = self._make_valid_phase2()
        data["source_requirements"] = "string"
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=2)
        v.validate()
        # not a dict -> tier1_preference = False, but bool(sources) = True -> passes
        src_checks = [c for c in v.checks if "Source Requirements" in c.check_name]
        assert len(src_checks) == 1


# ---------------------------------------------------------------------------
# Phase 3 validation
# ---------------------------------------------------------------------------

class TestPhase3Validation:
    def _make_valid_phase3(self):
        return {
            "html_content": "<article><h1>Test</h1></article>",
            "schema_markup": {"@type": "Article", "faqPage": {}, "breadcrumbList": {}},
            "brands_featured": ["FanDuel", "BetMGM"],
            "terms_and_conditions": {"FanDuel": "T&C...", "BetMGM": "T&C..."},
            "interactive_elements": {"calculator": True},
            "responsible_gambling_section": "Please gamble responsibly."
        }

    def test_valid_phase3(self, tmp_path):
        data = self._make_valid_phase3()
        f = tmp_path / "phase3.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        assert v.validate() is True

    def test_missing_html_content(self, tmp_path):
        data = self._make_valid_phase3()
        data["html_content"] = ""
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        assert any("HTML content missing" in c.message for c in v.checks if not c.passed)

    def test_missing_schema_markup(self, tmp_path):
        data = self._make_valid_phase3()
        data["schema_markup"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        assert any("Schema markup missing" in c.message for c in v.checks if not c.passed)

    def test_schema_with_article_faq_breadcrumb(self, tmp_path):
        data = self._make_valid_phase3()
        data["schema_markup"] = {
            "@type": "Article",
            "faq": {"@type": "FAQPage"},
            "breadcrumb": {"@type": "BreadcrumbList"}
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        schema_checks = [c for c in v.checks if "Schema" in c.check_name]
        assert all(c.passed for c in schema_checks)

    def test_tcs_missing_for_some_brands(self, tmp_path):
        data = self._make_valid_phase3()
        data["terms_and_conditions"] = {"FanDuel": "T&C..."}  # missing BetMGM
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        assert any("T&Cs missing" in c.message for c in v.checks if not c.passed)

    def test_tcs_no_brands_featured(self, tmp_path):
        data = self._make_valid_phase3()
        data["brands_featured"] = []
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        # empty brands_featured -> T&C check not triggered (no brands to check)
        tcs_checks = [c for c in v.checks if "Terms" in c.check_name]
        assert len(tcs_checks) == 0

    def test_no_interactive_elements(self, tmp_path):
        data = self._make_valid_phase3()
        data["interactive_elements"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        ie_checks = [c for c in v.checks if "Interactive" in c.check_name]
        assert len(ie_checks) == 1
        assert ie_checks[0].passed is False
        # severity is warning, not error -> validate() should still return True
        assert len(v.errors) == 0

    def test_missing_responsible_gambling(self, tmp_path):
        data = self._make_valid_phase3()
        data["responsible_gambling_section"] = ""
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        assert any("responsible gambling" in c.message.lower() for c in v.checks if not c.passed)

    def test_no_tcs_dict_brands_present(self, tmp_path):
        data = self._make_valid_phase3()
        data["terms_and_conditions"] = {}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        tcs_checks = [c for c in v.checks if "Terms" in c.check_name]
        assert len(tcs_checks) == 1
        assert tcs_checks[0].passed is False


# ---------------------------------------------------------------------------
# get_report and print_report
# ---------------------------------------------------------------------------

class TestReporting:
    def test_get_report_structure(self, tmp_path):
        data = {"primary_keyword": "test", "secondary_keywords": []}
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        report = v.get_report()
        assert "file" in report
        assert "phase" in report
        assert "valid" in report
        assert "error_count" in report
        assert "warning_count" in report
        assert "checks_run" in report
        assert "checks" in report
        assert "errors" in report
        assert "warnings" in report
        assert "integration_note" in report
        assert "protected_features_validated" in report

    def test_get_report_valid(self, tmp_path):
        data = {
            "primary_keyword": "best betting apps",
            "secondary_keywords": [
                {"keyword": f"kw{i}", "volume": 1000 + i} for i in range(10)
            ],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        report = v.get_report()
        assert report["valid"] is True
        assert report["error_count"] == 0

    def test_print_report_passed(self, tmp_path, capsys):
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 100} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DK"},
            "assigned_writer": "Tom"
        }
        f = tmp_path / "report.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        v.print_report()
        out = capsys.readouterr().out
        assert "PASSED" in out or "Validation Report" in out

    def test_print_report_failed(self, tmp_path, capsys):
        data = {"primary_keyword": "", "secondary_keywords": []}
        f = tmp_path / "report.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=1)
        v.validate()
        v.print_report()
        out = capsys.readouterr().out
        assert "FAILED" in out
        assert "Errors:" in out

    def test_print_report_with_warnings(self, tmp_path, capsys):
        data = {
            "html_content": "<p>test</p>",
            "schema_markup": {"@type": "Article"},
            "interactive_elements": {},
            "responsible_gambling_section": "Gamble responsibly"
        }
        f = tmp_path / "report.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        v = PhaseJSONValidator(f, phase=3)
        v.validate()
        v.print_report()
        out = capsys.readouterr().out
        assert "Warnings:" in out


# ---------------------------------------------------------------------------
# main() function
# ---------------------------------------------------------------------------

class TestMain:
    def test_main_no_args(self):
        with patch("sys.argv", ["prog"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 1

    def test_main_single_file_valid(self, tmp_path):
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 500} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DK"},
            "assigned_writer": "Gustavo Cantella"
        }
        f = tmp_path / "phase1.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        with patch("sys.argv", ["prog", str(f), "--phase", "1"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 0

    def test_main_single_file_invalid(self, tmp_path):
        data = {"primary_keyword": "", "secondary_keywords": []}
        f = tmp_path / "bad.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        with patch("sys.argv", ["prog", str(f), "--phase", "1"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 1

    def test_main_json_output(self, tmp_path, capsys):
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 500} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DK"},
            "assigned_writer": "Lewis"
        }
        f = tmp_path / "phase1.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        with patch("sys.argv", ["prog", str(f), "--phase", "1", "--json"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 0
        out = capsys.readouterr().out
        output_data = json.loads(out)
        assert output_data["validation_type"] == "phase_json_integrated"
        assert "integration_info" in output_data

    def test_main_all_flag_no_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        with patch("sys.argv", ["prog", "--all"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 1

    def test_main_all_flag_with_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 500} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DK"},
            "assigned_writer": "Tom"
        }
        f = tmp_path / "phase1-test.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        with patch("sys.argv", ["prog", "--all"]):
            with pytest.raises(SystemExit) as exc_info:
                MOD.main()
            assert exc_info.value.code == 0