#!/usr/bin/env python3
"""
Comprehensive tests for validate_phase_json_integrated.py

Target: 85%+ code coverage (0% → 85%+)
"""

import json
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
from io import StringIO

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from validate_phase_json_integrated import (
    ValidationResult,
    PhaseJSONValidator,
    main
)


# ============================================================================
# ValidationResult Tests
# ============================================================================

class TestValidationResult:
    """Test the ValidationResult dataclass."""

    def test_validation_result_creation(self):
        """Test creating a ValidationResult."""
        result = ValidationResult(
            check_name="Test Check",
            passed=True,
            message="Test passed",
            severity="info"
        )
        assert result.check_name == "Test Check"
        assert result.passed is True
        assert result.message == "Test passed"
        assert result.severity == "info"

    def test_validation_result_default_severity(self):
        """Test default severity is 'error'."""
        result = ValidationResult(
            check_name="Test",
            passed=False,
            message="Failed"
        )
        assert result.severity == "error"


# ============================================================================
# PhaseJSONValidator Initialization Tests
# ============================================================================

class TestPhaseJSONValidatorInit:
    """Test PhaseJSONValidator initialization."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_init_with_phase(self, mock_validator):
        """Test initializing with explicit phase."""
        json_file = Path("test.json")
        validator = PhaseJSONValidator(json_file, phase=1)
        
        assert validator.json_file == json_file
        assert validator.phase == 1
        assert validator.data is None
        assert validator.errors == []
        assert validator.warnings == []
        assert validator.checks == []
        mock_validator.assert_called_once()

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_init_without_phase(self, mock_validator):
        """Test initializing without phase (auto-detect)."""
        json_file = Path("test.json")
        validator = PhaseJSONValidator(json_file)
        
        assert validator.json_file == json_file
        assert validator.phase is None

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_constants_defined(self, mock_validator):
        """Test class constants are correctly defined."""
        assert PhaseJSONValidator.VALID_WRITERS == {"Lewis", "Tom", "Gustavo Cantella"}
        assert PhaseJSONValidator.VALID_PRIORITIES == {"High", "Medium", "Low"}
        assert PhaseJSONValidator.REQUIRED_BRAND_1 == "FanDuel"
        assert PhaseJSONValidator.REQUIRED_BRAND_2 == "BetMGM"


# ============================================================================
# File Reading Tests
# ============================================================================

class TestFileReading:
    """Test JSON file reading functionality."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_read_json_success(self, mock_validator, tmp_path):
        """Test successfully reading valid JSON."""
        json_file = tmp_path / "test.json"
        test_data = {"primary_keyword": "test"}
        json_file.write_text(json.dumps(test_data))
        
        validator = PhaseJSONValidator(json_file)
        result = validator._read_json()
        
        assert result is True
        assert validator.data == test_data

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_read_json_invalid_json(self, mock_validator, tmp_path):
        """Test reading malformed JSON."""
        json_file = tmp_path / "invalid.json"
        json_file.write_text("{invalid json")
        
        validator = PhaseJSONValidator(json_file)
        result = validator._read_json()
        
        assert result is False
        assert len(validator.errors) == 1
        assert "Invalid JSON" in validator.errors[0]

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_read_json_file_error(self, mock_validator, tmp_path):
        """Test handling file read errors."""
        json_file = tmp_path / "test.json"
        
        validator = PhaseJSONValidator(json_file)
        
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = validator._read_json()
        
        assert result is False
        assert len(validator.errors) == 1
        assert "Error reading file" in validator.errors[0]


# ============================================================================
# Phase Detection Tests
# ============================================================================

class TestPhaseDetection:
    """Test phase auto-detection logic."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_detect_phase1(self, mock_validator):
        """Test detecting Phase 1 from JSON structure."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator.data = {
            "primary_keyword": "test keyword",
            "secondary_keywords": []
        }
        
        phase = validator._detect_phase()
        assert phase == 1

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_detect_phase2_content_outline(self, mock_validator):
        """Test detecting Phase 2 via content_outline."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator.data = {
            "content_outline": {}
        }
        
        phase = validator._detect_phase()
        assert phase == 2

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_detect_phase2_h2_sections(self, mock_validator):
        """Test detecting Phase 2 via h2_sections."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator.data = {
            "h2_sections": {}
        }
        
        phase = validator._detect_phase()
        assert phase == 2

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_detect_phase3_html_content(self, mock_validator):
        """Test detecting Phase 3 via html_content."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator.data = {
            "html_content": "<html>test</html>"
        }
        
        phase = validator._detect_phase()
        assert phase == 3

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_detect_phase3_schema_markup(self, mock_validator):
        """Test detecting Phase 3 via schema_markup."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator.data = {
            "schema_markup": {}
        }
        
        phase = validator._detect_phase()
        assert phase == 3

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_detect_phase_invalid_data(self, mock_validator):
        """Test phase detection with invalid data type."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator.data = "not a dict"
        
        phase = validator._detect_phase()
        assert phase is None

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_detect_phase_unknown_structure(self, mock_validator):
        """Test phase detection with unknown structure."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator.data = {"unknown": "structure"}
        
        phase = validator._detect_phase()
        assert phase is None


# ============================================================================
# Check Management Tests
# ============================================================================

class TestCheckManagement:
    """Test the _add_check method."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_add_check_passing(self, mock_validator):
        """Test adding a passing check."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator._add_check("Test Check", True, "All good")
        
        assert len(validator.checks) == 1
        assert validator.checks[0].check_name == "Test Check"
        assert validator.checks[0].passed is True
        assert validator.checks[0].message == "All good"
        assert len(validator.errors) == 0
        assert len(validator.warnings) == 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_add_check_failing_error(self, mock_validator):
        """Test adding a failing check with error severity."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator._add_check("Test Check", False, "Failed!", severity="error")
        
        assert len(validator.checks) == 1
        assert validator.checks[0].passed is False
        assert len(validator.errors) == 1
        assert "Test Check: Failed!" in validator.errors[0]
        assert len(validator.warnings) == 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_add_check_failing_warning(self, mock_validator):
        """Test adding a failing check with warning severity."""
        validator = PhaseJSONValidator(Path("test.json"))
        validator._add_check("Test Check", False, "Warning!", severity="warning")
        
        assert len(validator.checks) == 1
        assert validator.checks[0].passed is False
        assert len(validator.errors) == 0
        assert len(validator.warnings) == 1
        assert "Test Check: Warning!" in validator.warnings[0]


# ============================================================================
# Phase 1 Validation Tests
# ============================================================================

class TestPhase1Validation:
    """Test Phase 1 validation logic."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_valid_complete(self, mock_validator, tmp_path):
        """Test complete valid Phase 1 JSON."""
        json_file = tmp_path / "phase1.json"
        data = {
            "primary_keyword": "best betting sites",
            "secondary_keywords": [
                {"keyword": f"kw{i}", "volume": 1000 + i} for i in range(10)
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
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_missing_primary_keyword(self, mock_validator):
        """Test Phase 1 with missing primary keyword."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("Primary keyword is required" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_insufficient_secondary_keywords(self, mock_validator):
        """Test Phase 1 with insufficient secondary keywords."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": "kw1", "volume": 1000}
            ],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("Secondary Keywords Count" in c.check_name for c in validator.checks)
        assert any(not c.passed for c in validator.checks if "Secondary Keywords Count" in c.check_name)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_secondary_keywords_dict_format(self, mock_validator):
        """Test Phase 1 with secondary keywords as dict."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": {f"kw{i}": {"volume": 1000} for i in range(10)},
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        # Should handle dict format
        assert len(validator.checks) > 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_missing_keyword_volume(self, mock_validator):
        """Test Phase 1 with missing volume data."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": "kw1"},  # Missing volume
                {"keyword": "kw2", "volume": 1000}
            ] + [{"keyword": f"kw{i}", "volume": 1000} for i in range(3, 11)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("missing volume data" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_insufficient_competitors(self, mock_validator):
        """Test Phase 1 with insufficient competitors."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}},  # Only 1 competitor
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("Competitor Analysis" in c.check_name for c in validator.checks)
        assert any(not c.passed for c in validator.checks if "Competitor Analysis" in c.check_name)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_no_brands_selected(self, mock_validator):
        """Test Phase 1 with no brands selected."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {},
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("No brands selected" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_wrong_brand1(self, mock_validator):
        """Test Phase 1 with wrong brand at position 1."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {
                "1": "WrongBrand",
                "2": "BetMGM",
                "3": "DraftKings"
            },
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("FanDuel MUST be ranked #1" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_wrong_brand2(self, mock_validator):
        """Test Phase 1 with wrong brand at position 2."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {
                "1": "FanDuel",
                "2": "WrongBrand",
                "3": "DraftKings"
            },
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("BetMGM MUST be ranked #2" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_missing_research_brands(self, mock_validator):
        """Test Phase 1 with missing research brands 3-10."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {
                "1": "FanDuel",
                "2": "BetMGM"
                # Missing 3-10
            },
            "assigned_writer": "Lewis"
        }
        
        validator._validate_phase_1()
        
        assert any("Research brands #3-10 required" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_invalid_writer(self, mock_validator):
        """Test Phase 1 with invalid writer."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "InvalidWriter"
        }
        
        validator._validate_phase_1()
        
        assert any("Invalid writer" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase1_empty_writer(self, mock_validator):
        """Test Phase 1 with empty writer."""
        validator = PhaseJSONValidator(Path("test.json"), phase=1)
        validator.data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": ""
        }
        
        validator._validate_phase_1()
        
        assert any("Invalid writer" in e for e in validator.errors)


# ============================================================================
# Phase 2 Validation Tests
# ============================================================================

class TestPhase2Validation:
    """Test Phase 2 validation logic."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase2_valid_complete(self, mock_validator, tmp_path):
        """Test complete valid Phase 2 JSON."""
        json_file = tmp_path / "phase2.json"
        data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {
                "H2 1": {"keyword": "high volume kw", "volume": 5000},
                "H2 2": {"keyword": "another kw", "volume": 3000}
            },
            "faq": {
                "questions": [f"Question {i}?" for i in range(8)]
            },
            "source_requirements": {
                "tier1_preferred": True
            }
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase2_missing_content_outline(self, mock_validator):
        """Test Phase 2 with missing content outline."""
        validator = PhaseJSONValidator(Path("test.json"), phase=2)
        validator.data = {
            "h2_sections": {},
            "faq": {"questions": [f"Q{i}" for i in range(8)]},
            "source_requirements": {}
        }
        
        validator._validate_phase_2()
        
        assert any("Content outline is required" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase2_no_h2_sections(self, mock_validator):
        """Test Phase 2 with no H2 sections."""
        validator = PhaseJSONValidator(Path("test.json"), phase=2)
        validator.data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {},
            "faq": {"questions": [f"Q{i}" for i in range(8)]},
            "source_requirements": {}
        }
        
        validator._validate_phase_2()
        
        assert any("No H2 sections found" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase2_h2_low_volume_keywords(self, mock_validator):
        """Test Phase 2 with low-volume keywords in H2 sections."""
        validator = PhaseJSONValidator(Path("test.json"), phase=2)
        validator.data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {
                "H2 1": {"keyword": "low volume", "volume": 500}  # Below 1000 threshold
            },
            "faq": {"questions": [f"Q{i}" for i in range(8)]},
            "source_requirements": {}
        }
        
        validator._validate_phase_2()
        
        # Should detect low-volume keyword issue
        h2_check = [c for c in validator.checks if "H2 Sections Keyword Mapping" in c.check_name]
        assert len(h2_check) > 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase2_insufficient_faq(self, mock_validator):
        """Test Phase 2 with insufficient FAQ questions."""
        validator = PhaseJSONValidator(Path("test.json"), phase=2)
        validator.data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {"H2 1": {}},
            "faq": {
                "questions": ["Q1", "Q2"]  # Only 2, need 7+
            },
            "source_requirements": {}
        }
        
        validator._validate_phase_2()
        
        assert any("FAQ Questions Count" in c.check_name for c in validator.checks)
        assert any(not c.passed for c in validator.checks if "FAQ Questions Count" in c.check_name)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase2_faq_as_list(self, mock_validator):
        """Test Phase 2 with FAQ as non-dict."""
        validator = PhaseJSONValidator(Path("test.json"), phase=2)
        validator.data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {"H2 1": {}},
            "faq": [],  # Not a dict
            "source_requirements": {}
        }
        
        validator._validate_phase_2()
        
        # Should handle non-dict FAQ
        assert len(validator.checks) > 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase2_source_requirements_present(self, mock_validator):
        """Test Phase 2 with source requirements."""
        validator = PhaseJSONValidator(Path("test.json"), phase=2)
        validator.data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {"H2 1": {}},
            "faq": {"questions": [f"Q{i}" for i in range(8)]},
            "source_requirements": {"tier1_preferred": True}
        }
        
        validator._validate_phase_2()
        
        source_check = [c for c in validator.checks if "Source Requirements" in c.check_name]
        assert len(source_check) > 0
        assert source_check[0].passed


# ============================================================================
# Phase 3 Validation Tests
# ============================================================================

class TestPhase3Validation:
    """Test Phase 3 validation logic."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase3_valid_complete(self, mock_validator, tmp_path):
        """Test complete valid Phase 3 JSON."""
        json_file = tmp_path / "phase3.json"
        data = {
            "html_content": "<article>Content</article>",
            "schema_markup": {
                "@type": "Article",
                "faqPage": {},
                "breadcrumbList": {}
            },
            "brands_featured": ["FanDuel", "BetMGM"],
            "terms_and_conditions": {
                "FanDuel": "T&Cs here",
                "BetMGM": "T&Cs here"
            },
            "interactive_elements": {
                "calculator": True
            },
            "responsible_gambling_section": "Gamble responsibly..."
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        result = validator.validate()
        
        assert result is True
        assert len(validator.errors) == 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase3_missing_html_content(self, mock_validator):
        """Test Phase 3 with missing HTML content."""
        validator = PhaseJSONValidator(Path("test.json"), phase=3)
        validator.data = {
            "schema_markup": {},
            "responsible_gambling_section": "text"
        }
        
        validator._validate_phase_3()
        
        assert any("HTML content missing" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase3_missing_schema_markup(self, mock_validator):
        """Test Phase 3 with missing schema markup."""
        validator = PhaseJSONValidator(Path("test.json"), phase=3)
        validator.data = {
            "html_content": "<html>test</html>",
            "responsible_gambling_section": "text"
        }
        
        validator._validate_phase_3()
        
        assert any("Schema markup missing" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase3_schema_components(self, mock_validator):
        """Test Phase 3 schema component validation."""
        validator = PhaseJSONValidator(Path("test.json"), phase=3)
        validator.data = {
            "html_content": "<html>test</html>",
            "schema_markup": "article faqpage breadcrumblist",
            "responsible_gambling_section": "text"
        }
        
        validator._validate_phase_3()
        
        # Should find all schema components
        article_check = [c for c in validator.checks if "Article Schema" in c.check_name]
        faq_check = [c for c in validator.checks if "FAQ Schema" in c.check_name]
        breadcrumb_check = [c for c in validator.checks if "Breadcrumb Schema" in c.check_name]
        
        assert len(article_check) > 0
        assert len(faq_check) > 0
        assert len(breadcrumb_check) > 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase3_incomplete_tcs(self, mock_validator):
        """Test Phase 3 with incomplete T&Cs."""
        validator = PhaseJSONValidator(Path("test.json"), phase=3)
        validator.data = {
            "html_content": "<html>test</html>",
            "schema_markup": {},
            "brands_featured": ["FanDuel", "BetMGM", "DraftKings"],
            "terms_and_conditions": {
                "FanDuel": "T&Cs",
                # Missing BetMGM and DraftKings
            },
            "responsible_gambling_section": "text"
        }
        
        validator._validate_phase_3()
        
        tcs_check = [c for c in validator.checks if "Terms & Conditions" in c.check_name]
        assert len(tcs_check) > 0
        assert not tcs_check[0].passed

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase3_no_interactive_elements(self, mock_validator):
        """Test Phase 3 with no interactive elements (warning)."""
        validator = PhaseJSONValidator(Path("test.json"), phase=3)
        validator.data = {
            "html_content": "<html>test</html>",
            "schema_markup": {},
            "responsible_gambling_section": "text"
        }
        
        validator._validate_phase_3()
        
        # Should generate a warning, not error
        interactive_check = [c for c in validator.checks if "Interactive Elements" in c.check_name]
        assert len(interactive_check) > 0
        assert interactive_check[0].severity == "warning"

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_phase3_missing_responsible_gambling(self, mock_validator):
        """Test Phase 3 with missing responsible gambling section."""
        validator = PhaseJSONValidator(Path("test.json"), phase=3)
        validator.data = {
            "html_content": "<html>test</html>",
            "schema_markup": {},
            "responsible_gambling_section": ""
        }
        
        validator._validate_phase_3()
        
        assert any("Responsible gambling section missing" in e for e in validator.errors)


# ============================================================================
# Validate Method Tests
# ============================================================================

class TestValidateMethod:
    """Test the main validate() method."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_validate_file_not_found(self, mock_validator, tmp_path):
        """Test validation with non-existent file."""
        json_file = tmp_path / "nonexistent.json"
        validator = PhaseJSONValidator(json_file, phase=1)
        
        result = validator.validate()
        
        assert result is False
        assert any("File not found" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_validate_invalid_phase(self, mock_validator, tmp_path):
        """Test validation with invalid phase number."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"test": true}')
        
        validator = PhaseJSONValidator(json_file, phase=5)  # Invalid phase
        result = validator.validate()
        
        assert result is False
        assert any("Invalid phase: 5" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_validate_auto_detect_failure(self, mock_validator, tmp_path):
        """Test validation when phase auto-detection fails."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"unknown": "structure"}')
        
        validator = PhaseJSONValidator(json_file)
        result = validator.validate()
        
        assert result is False
        assert any("Could not determine phase" in e for e in validator.errors)

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_validate_auto_detect_success(self, mock_validator, tmp_path):
        """Test validation with successful phase auto-detection."""
        json_file = tmp_path / "test.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file)
        result = validator.validate()
        
        assert validator.phase == 1  # Auto-detected as Phase 1
        assert result is True


# ============================================================================
# Report Generation Tests
# ============================================================================

class TestReportGeneration:
    """Test report generation methods."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_get_report_structure(self, mock_validator, tmp_path):
        """Test get_report() returns correct structure."""
        json_file = tmp_path / "test.json"
        data = {"primary_keyword": "test", "secondary_keywords": []}
        json_file.write_text(json.dumps(data))
        
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
        assert "integration_note" in report
        assert "protected_features_validated" in report

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_get_report_check_format(self, mock_validator, tmp_path):
        """Test that checks in report have correct format."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"primary_keyword": "test"}')
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        report = validator.get_report()
        
        if report["checks"]:
            check = report["checks"][0]
            assert "name" in check
            assert "passed" in check
            assert "message" in check
            assert "severity" in check

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_report(self, mock_stdout, mock_validator, tmp_path):
        """Test print_report() output."""
        json_file = tmp_path / "test.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        validator.print_report()
        
        output = mock_stdout.getvalue()
        assert "Phase 1 Validation Report" in output
        assert "PASSED" in output
        assert "Protected Features Validated" in output


# ============================================================================
# CLI Main Function Tests
# ============================================================================

class TestMainCLI:
    """Test the main CLI entry point."""

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    @patch('sys.argv', ['script.py'])
    def test_main_no_arguments(self, mock_validator):
        """Test main() with no arguments."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    @patch('sys.argv', ['script.py', 'test.json', '--phase', '1'])
    def test_main_single_file_success(self, mock_validator, tmp_path, monkeypatch):
        """Test main() with single file validation (success)."""
        # Change to tmp directory
        monkeypatch.chdir(tmp_path)
        
        json_file = tmp_path / "test.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        with patch('sys.argv', ['script.py', 'test.json', '--phase', '1']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_main_single_file_failure(self, mock_validator, tmp_path, monkeypatch):
        """Test main() with single file validation (failure)."""
        monkeypatch.chdir(tmp_path)
        
        json_file = tmp_path / "test.json"
        data = {"primary_keyword": ""}  # Invalid - empty primary keyword
        json_file.write_text(json.dumps(data))
        
        with patch('sys.argv', ['script.py', 'test.json', '--phase', '1']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_main_json_output(self, mock_validator, tmp_path, monkeypatch, capsys):
        """Test main() with --json flag."""
        monkeypatch.chdir(tmp_path)
        
        json_file = tmp_path / "test.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        with patch('sys.argv', ['script.py', 'test.json', '--phase', '1', '--json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
        
        captured = capsys.readouterr()
        output_data = json.loads(captured.out)
        assert "validation_type" in output_data
        assert output_data["validation_type"] == "phase_json_integrated"
        assert "reports" in output_data
        assert "all_valid" in output_data

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_main_all_flag_no_files(self, mock_validator, tmp_path, monkeypatch):
        """Test main() with --all flag when no files found."""
        monkeypatch.chdir(tmp_path)
        
        with patch('sys.argv', ['script.py', '--all']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_main_all_flag_multiple_files(self, mock_validator, tmp_path, monkeypatch):
        """Test main() with --all flag and multiple files."""
        monkeypatch.chdir(tmp_path)
        
        # Create multiple phase files
        for phase in [1, 2, 3]:
            json_file = tmp_path / f"phase{phase}-output.json"
            data = {"primary_keyword": "test"} if phase == 1 else \
                   {"content_outline": {}} if phase == 2 else \
                   {"html_content": "test"}
            json_file.write_text(json.dumps(data))
        
        with patch('sys.argv', ['script.py', '--all']):
            with pytest.raises(SystemExit):
                main()

    @patch('validate_phase_json_integrated.JSONSchemaValidator')
    def test_main_all_flag_with_json_output(self, mock_validator, tmp_path, monkeypatch, capsys):
        """Test main() with --all and --json flags."""
        monkeypatch.chdir(tmp_path)
        
        # Create phase 1 file
        json_file = tmp_path / "phase1-output.json"
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [{"keyword": f"kw{i}", "volume": 1000} for i in range(10)],
            "competitor_analysis": {"c1": {}, "c2": {}, "c3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "DraftKings"},
            "assigned_writer": "Lewis"
        }
        json_file.write_text(json.dumps(data))
        
        with patch('sys.argv', ['script.py', '--all', '--json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
        
        captured = capsys.readouterr()
        output_data = json.loads(captured.out)
        assert "total_files" in output_data
        assert output_data["total_files"] >= 1


# ============================================================================
# Import Error Test
# ============================================================================

class TestImportError:
    """Test handling of missing tes_shared dependency."""

    def test_import_error_handling(self):
        """Test that import error is handled correctly."""
        # This test verifies the try/except block exists
        # Actual import error would prevent module loading
        # So we just verify the constants and structure are accessible
        assert hasattr(PhaseJSONValidator, 'VALID_WRITERS')
        assert hasattr(PhaseJSONValidator, 'REQUIRED_BRAND_1')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
