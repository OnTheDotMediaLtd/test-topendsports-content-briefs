"""
Coverage tests for validate_phase_json.py to fill remaining gaps.
Focuses on edge cases and specific code paths not covered by existing tests.
"""

import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

# Add scripts to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))

from validate_phase_json import PhaseJSONValidator, ValidationResult, main


class TestPhaseJSONValidatorEdgeCases:
    """Tests for edge cases in PhaseJSONValidator."""

    def test_validate_file_not_exists(self, tmp_path):
        """Test validation when file doesn't exist."""
        non_existent = tmp_path / "missing.json"
        validator = PhaseJSONValidator(non_existent)
        
        result = validator.validate()
        
        assert result is False
        assert len(validator.errors) > 0
        assert "File not found" in validator.errors[0]

    def test_read_json_permission_error(self, tmp_path):
        """Test reading JSON file with permission error."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"test": true}')
        
        validator = PhaseJSONValidator(json_file)
        
        # Mock open to raise PermissionError
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = validator._read_json()
            
        assert result is False
        assert len(validator.errors) > 0
        assert "Error reading file" in validator.errors[0]

    def test_detect_phase_non_dict_data(self, tmp_path):
        """Test phase detection when data is not a dict."""
        json_file = tmp_path / "test.json"
        json_file.write_text('["not", "a", "dict"]')
        
        validator = PhaseJSONValidator(json_file)
        validator._read_json()
        
        phase = validator._detect_phase()
        assert phase is None

    def test_detect_phase_empty_dict(self, tmp_path):
        """Test phase detection with empty dict."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{}')
        
        validator = PhaseJSONValidator(json_file)
        validator._read_json()
        
        phase = validator._detect_phase()
        assert phase is None

    def test_validate_invalid_phase_number(self, tmp_path):
        """Test validation with invalid phase number."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"test": true}')
        
        validator = PhaseJSONValidator(json_file, phase=4)
        result = validator.validate()
        
        assert result is False
        assert "Invalid phase: 4" in validator.errors

    def test_validate_no_phase_detection(self, tmp_path):
        """Test validation when phase cannot be detected."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"unknown": "structure"}')
        
        validator = PhaseJSONValidator(json_file)
        result = validator.validate()
        
        assert result is False
        assert any("Could not determine phase" in error for error in validator.errors)


class TestPhase1ValidationEdgeCases:
    """Tests for Phase 1 validation edge cases."""

    def test_phase1_secondary_keywords_as_dict(self, tmp_path):
        """Test Phase 1 with secondary keywords as dict structure."""
        data = {
            "primary_keyword": "test",
            "secondary_keywords": {
                "1": {"keyword": "test1", "volume": 1000},
                "2": {"keyword": "test2", "volume": 2000},
                "3": {"keyword": "test3", "volume": 3000},
                "4": {"keyword": "test4", "volume": 4000},
                "5": {"keyword": "test5", "volume": 5000},
                "6": {"keyword": "test6", "volume": 6000},
                "7": {"keyword": "test7", "volume": 7000},
                "8": {"keyword": "test8", "volume": 8000}
            },
            "competitor_analysis": {"comp1": {}, "comp2": {}, "comp3": {}},
            "brand_selection": {"1": "FanDuel", "2": "BetMGM", "3": "Research"},
            "assigned_writer": "Lewis"
        }
        
        json_file = tmp_path / "phase1.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        assert result is True

    def test_phase1_keyword_missing_volume(self, tmp_path):
        """Test Phase 1 with keywords missing volume data."""
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": "test1", "volume": 1000},
                {"keyword": "test2"},  # Missing volume
                {"keyword": "test3", "volume": 3000},
                {"keyword": "test4", "volume": 4000},
                {"keyword": "test5", "volume": 5000},
                {"keyword": "test6", "volume": 6000},
                {"keyword": "test7", "volume": 7000},
                {"keyword": "test8", "volume": 8000}
            ]
        }
        
        json_file = tmp_path / "phase1.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        result = validator.validate()
        
        assert result is False
        # Should have error for missing volume data
        assert any("missing volume data" in error for error in validator.errors)

    def test_phase1_keyword_zero_volume(self, tmp_path):
        """Test Phase 1 with keyword having zero volume."""
        data = {
            "primary_keyword": "test",
            "secondary_keywords": [
                {"keyword": "test1", "volume": 0},  # Zero volume should be valid
                {"keyword": "test2", "volume": 1000},
                {"keyword": "test3", "volume": 3000},
                {"keyword": "test4", "volume": 4000},
                {"keyword": "test5", "volume": 5000},
                {"keyword": "test6", "volume": 6000},
                {"keyword": "test7", "volume": 7000},
                {"keyword": "test8", "volume": 8000}
            ]
        }
        
        json_file = tmp_path / "phase1.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        # Zero volume should be considered valid
        volume_errors = [e for e in validator.errors if "volume data" in e]
        assert len(volume_errors) == 0

    def test_phase1_brand_selection_edge_cases(self, tmp_path):
        """Test Phase 1 brand selection validation edge cases."""
        # Test wrong FanDuel position
        data1 = {
            "primary_keyword": "test",
            "brand_selection": {"1": "BetMGM", "2": "FanDuel"}
        }
        json_file = tmp_path / "phase1_wrong_fanduel.json"
        json_file.write_text(json.dumps(data1))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        brand_error = next((e for e in validator.errors if "FanDuel must be ranked #1" in e), None)
        assert brand_error is not None

        # Test wrong BetMGM position  
        data2 = {
            "primary_keyword": "test",
            "brand_selection": {"1": "FanDuel", "2": "DraftKings"}
        }
        json_file.write_text(json.dumps(data2))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        betmgm_error = next((e for e in validator.errors if "BetMGM must be ranked #2" in e), None)
        assert betmgm_error is not None

        # Test missing research brands
        data3 = {
            "primary_keyword": "test", 
            "brand_selection": {"1": "FanDuel", "2": "BetMGM"}
        }
        json_file.write_text(json.dumps(data3))
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        research_error = next((e for e in validator.errors if "research brands" in e.lower() or "brands #3-10" in e), None)
        assert research_error is not None


class TestPhase2ValidationEdgeCases:
    """Tests for Phase 2 validation edge cases."""

    def test_phase2_h2_sections_volume_check(self, tmp_path):
        """Test Phase 2 H2 sections volume validation."""
        data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {
                "High Volume Section": {
                    "keyword": "high volume",
                    "volume": 2000  # Above 1000 threshold
                },
                "Low Volume Section": {
                    "keyword": "low volume", 
                    "volume": 500  # Below 1000 threshold
                }
            }
        }
        
        json_file = tmp_path / "phase2.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        # Should fail H2 keyword mapping due to low volume section
        h2_error = next((e for e in validator.errors if "not mapped to high-volume keywords" in e), None)
        assert h2_error is not None

    def test_phase2_h3_sections_volume_check(self, tmp_path):
        """Test Phase 2 H3 sections volume validation."""
        data = {
            "content_outline": {"intro": "test"},
            "h2_sections": {"section1": {"keyword": "test", "volume": 1000}},
            "h3_sections": {
                "Good H3": {
                    "keyword": "medium volume",
                    "volume": 200  # Above 100 threshold
                },
                "Bad H3": {
                    "keyword": "low volume",
                    "volume": 50  # Below 100 threshold  
                }
            }
        }
        
        json_file = tmp_path / "phase2.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        # Should fail H3 keyword mapping due to low volume section
        h3_error = next((e for e in validator.errors if "not mapped to medium-volume keywords" in e), None)
        assert h3_error is not None

    def test_phase2_faq_article_type_validation(self, tmp_path):
        """Test Phase 2 FAQ validation for article/review content types."""
        # Test article type requiring 5-7 FAQs
        data_article = {
            "content_outline": {"intro": "test"},
            "content_type": "article",
            "faq": {
                "questions": [
                    {"question": "Q1", "keyword": "kw1"},
                    {"question": "Q2", "keyword": "kw2"},
                    {"question": "Q3", "keyword": "kw3"},
                    {"question": "Q4", "keyword": "kw4"}  # Only 4 questions, need 5-7
                ]
            }
        }
        
        json_file = tmp_path / "phase2_article.json"
        json_file.write_text(json.dumps(data_article))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        faq_error = next((e for e in validator.errors if "Required for articles/reviews: 5-7" in e), None)
        assert faq_error is not None

    def test_phase2_faq_questions_missing_keywords(self, tmp_path):
        """Test Phase 2 FAQ questions missing keyword mapping."""
        data = {
            "content_outline": {"intro": "test"},
            "faq": {
                "questions": [
                    {"question": "Q1", "keyword": "kw1"},
                    {"question": "Q2"},  # Missing keyword
                    {"question": "Q3", "keyword": "kw3"}
                ]
            }
        }
        
        json_file = tmp_path / "phase2.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        
        keyword_error = next((e for e in validator.errors if "missing keyword mapping" in e), None)
        assert keyword_error is not None

    def test_phase2_non_article_type_faq(self, tmp_path):
        """Test Phase 2 FAQ validation for non-article content types."""
        data = {
            "content_outline": {"intro": "test"},
            "content_type": "guide",  # Not article or review
            "faq": {
                "questions": [
                    {"question": "Q1", "keyword": "kw1"}
                ]
            }
        }
        
        json_file = tmp_path / "phase2_guide.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        result = validator.validate()
        
        # May fail due to missing other required fields, check that FAQ validation runs
        # Look for FAQ-related checks in the validator
        faq_checks = [check for check in validator.checks if "FAQ" in check.check_name]
        assert len(faq_checks) > 0


class TestPhase3ValidationEdgeCases:
    """Tests for Phase 3 validation edge cases."""

    def test_phase3_schema_markup_string_format(self, tmp_path):
        """Test Phase 3 schema markup validation with string format."""
        data = {
            "html_content": "<html>content</html>",
            "schema_markup": '{"@type": "Article", "faq": {"@type": "FAQPage"}, "breadcrumb": {"@type": "BreadcrumbList"}}'
        }
        
        json_file = tmp_path / "phase3.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        result = validator.validate()
        
        # Check that schema validation ran, may fail due to missing other fields
        schema_checks = [check for check in validator.checks if "Schema" in check.check_name]
        assert len(schema_checks) > 0

    def test_phase3_brands_tcs_complete_validation(self, tmp_path):
        """Test Phase 3 T&Cs validation with featured brands."""
        data = {
            "html_content": "<html>content</html>",
            "brands_featured": ["FanDuel", "BetMGM", "DraftKings"],
            "terms_and_conditions": {
                "FanDuel": {"terms": "..."},
                "BetMGM": {"terms": "..."}
                # Missing DraftKings T&Cs
            }
        }
        
        json_file = tmp_path / "phase3.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        validator.validate()
        
        tcs_error = next((e for e in validator.errors if "missing for some brands" in e), None)
        assert tcs_error is not None

    def test_phase3_no_featured_brands(self, tmp_path):
        """Test Phase 3 T&Cs validation without featured brands."""
        data = {
            "html_content": "<html>content</html>",
            "terms_and_conditions": {"SomeBrand": {"terms": "..."}}
        }
        
        json_file = tmp_path / "phase3.json"
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=3)
        result = validator.validate()
        
        # May fail due to missing other required fields, but T&Cs check should be present
        # Focus on checking that T&Cs validation runs without error
        assert len(validator.checks) > 0


class TestMainFunctionEdgeCases:
    """Tests for main function edge cases."""

    def test_main_no_args_shows_help(self, monkeypatch):
        """Test main function with no arguments shows help."""
        monkeypatch.setattr('sys.argv', ['validate_phase_json.py'])
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1

    def test_main_all_no_files_found(self, monkeypatch, tmp_path, capsys):
        """Test main with --all flag when no files are found."""
        monkeypatch.setattr('sys.argv', ['validate_phase_json.py', '--all'])
        
        # Change to temp directory with no JSON files
        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "No phase JSON files found" in captured.out
            
        finally:
            os.chdir(old_cwd)

    def test_main_json_output_with_datetime(self, monkeypatch, tmp_path, capsys):
        """Test main function JSON output includes timestamp."""
        json_file = tmp_path / "phase1-test.json"
        json_file.write_text('{"primary_keyword": "test"}')
        
        monkeypatch.setattr('sys.argv', [
            'validate_phase_json.py', str(json_file), '--phase', '1', '--json'
        ])
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1  # Will fail validation but output JSON
        
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        
        assert "timestamp" in output
        assert "validation_type" in output
        assert output["validation_type"] == "phase_json"


class TestValidationResultDataclass:
    """Tests for ValidationResult dataclass edge cases."""

    def test_validation_result_default_severity(self):
        """Test ValidationResult default severity is 'error'."""
        result = ValidationResult(
            check_name="Test",
            passed=False,
            message="Test message"
        )
        
        assert result.severity == "error"

    def test_validation_result_custom_severity(self):
        """Test ValidationResult with custom severity."""
        result = ValidationResult(
            check_name="Test",
            passed=True,
            message="Test message",
            severity="warning"
        )
        
        assert result.severity == "warning"


class TestReportGeneration:
    """Tests for report generation edge cases."""

    def test_get_report_structure(self, tmp_path):
        """Test complete structure of get_report output."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"primary_keyword": "test"}')
        
        validator = PhaseJSONValidator(json_file, phase=1)
        validator.validate()
        
        report = validator.get_report()
        
        # Check all expected keys are present
        expected_keys = {
            "file", "phase", "valid", "error_count", "warning_count",
            "checks_run", "checks", "errors", "warnings"
        }
        assert set(report.keys()) == expected_keys
        
        # Check checks structure
        if report["checks"]:
            check = report["checks"][0]
            check_keys = {"name", "passed", "message", "severity"}
            assert set(check.keys()) == check_keys

    def test_print_report_comprehensive(self, tmp_path, capsys):
        """Test print_report covers all sections."""
        json_file = tmp_path / "test.json"
        # Create data that will generate both errors and warnings
        data = {
            "primary_keyword": "",  # Will cause error
            "content_type": "guide",  # Will cause warning for FAQ
            "faq": {"questions": [{"question": "Q1"}]}
        }
        json_file.write_text(json.dumps(data))
        
        validator = PhaseJSONValidator(json_file, phase=2)
        validator.validate()
        validator.print_report()
        
        captured = capsys.readouterr()
        
        # Should contain all report sections
        assert "Validation Report" in captured.out
        assert "Status:" in captured.out
        assert "Detailed Checks:" in captured.out
        assert "Errors:" in captured.out
        assert "[FAIL]" in captured.out or "[PASS]" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])