#!/usr/bin/env python3
"""
Tests for phase3_regression_test.py
Covers all check functions, generate/run/compare/report functions, and main().

Target: bring phase3_regression_test.py from 0% to 90%+ coverage.
"""

import json
import sys
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from phase3_regression_test import (
    check_brand_positioning,
    check_keyword_mapping,
    check_tcs_present,
    check_docx_conversion,
    check_ahrefs_data,
    check_secondary_keywords,
    check_faq_count,
    generate_mock_brief_data,
    run_regression_test,
    compare_regression_results,
    generate_regression_report,
    print_summary,
    main,
    TEST_SCENARIOS,
    REGRESSION_CRITERIA,
)


# ===========================================================================
# check_brand_positioning
# ===========================================================================

class TestCheckBrandPositioning:
    def test_passes_when_fanduel_1_betmgm_2(self):
        data = {"brand_rankings": {"FanDuel": 1, "BetMGM": 2, "DraftKings": 3}}
        result = check_brand_positioning(data)
        assert result["passed"] is True
        assert "FanDuel #1" in result["details"]

    def test_fails_when_betmgm_not_2(self):
        data = {"brand_rankings": {"FanDuel": 1, "DraftKings": 2}}
        result = check_brand_positioning(data)
        assert result["passed"] is False
        assert "BetMGM not in position #2" in result["details"]

    def test_fails_when_fanduel_not_1(self):
        data = {"brand_rankings": {"BetMGM": 1, "FanDuel": 2}}
        result = check_brand_positioning(data)
        assert result["passed"] is False
        assert "FanDuel not in position #1" in result["details"]

    def test_fails_when_no_brand_rankings(self):
        data = {}
        result = check_brand_positioning(data)
        assert result["passed"] is False
        assert "Brand rankings data missing" in result["details"]

    def test_returns_dict_with_required_keys(self):
        data = {}
        result = check_brand_positioning(data)
        assert "passed" in result
        assert "details" in result
        assert "level" in result


# ===========================================================================
# check_keyword_mapping
# ===========================================================================

class TestCheckKeywordMapping:
    def _make_keywords(self, count, all_mapped=True):
        keywords = []
        for i in range(count):
            kw = {"keyword": f"keyword_{i}", "volume": 100}
            if all_mapped:
                kw["section_mapping"] = f"H2-{i}"
            keywords.append(kw)
        return keywords

    def test_passes_with_8_mapped_keywords(self):
        data = {"secondary_keywords": self._make_keywords(8, all_mapped=True)}
        result = check_keyword_mapping(data)
        assert result["passed"] is True
        assert "8 keywords" in result["details"]

    def test_passes_with_10_mapped_keywords(self):
        data = {"secondary_keywords": self._make_keywords(10, all_mapped=True)}
        result = check_keyword_mapping(data)
        assert result["passed"] is True

    def test_fails_when_fewer_than_8_keywords(self):
        data = {"secondary_keywords": self._make_keywords(5, all_mapped=True)}
        result = check_keyword_mapping(data)
        assert result["passed"] is False
        assert "Only 5 secondary keywords" in result["details"]

    def test_fails_when_not_all_mapped(self):
        keywords = self._make_keywords(8, all_mapped=True)
        # Remove mapping from a few
        keywords[0].pop("section_mapping")
        keywords[1].pop("section_mapping")
        data = {"secondary_keywords": keywords}
        result = check_keyword_mapping(data)
        assert result["passed"] is False
        assert "only 6 mapped" in result["details"]

    def test_fails_when_no_secondary_keywords_key(self):
        data = {}
        result = check_keyword_mapping(data)
        assert result["passed"] is False
        assert "Secondary keywords missing" in result["details"]


# ===========================================================================
# check_tcs_present
# ===========================================================================

class TestCheckTcsPresent:
    def test_passes_when_tcs_covers_all_brands(self):
        data = {
            "brands": ["FanDuel", "BetMGM", "DraftKings"],
            "tcs_sections": [{"brand": "FanDuel"}, {"brand": "BetMGM"}, {"brand": "DraftKings"}]
        }
        result = check_tcs_present(data)
        assert result["passed"] is True
        assert "T&Cs present for all 3 brands" in result["details"]

    def test_passes_when_tcs_exceeds_brands(self):
        data = {
            "brands": ["FanDuel", "BetMGM"],
            "tcs_sections": [{"brand": "FanDuel"}, {"brand": "BetMGM"}, {"brand": "Extra"}]
        }
        result = check_tcs_present(data)
        assert result["passed"] is True

    def test_fails_when_tcs_missing_for_some_brands(self):
        data = {
            "brands": ["FanDuel", "BetMGM", "DraftKings"],
            "tcs_sections": [{"brand": "FanDuel"}]
        }
        result = check_tcs_present(data)
        assert result["passed"] is False
        assert "T&Cs missing for 2 brands" in result["details"]

    def test_fails_when_data_missing(self):
        data = {}
        result = check_tcs_present(data)
        assert result["passed"] is False
        assert "Brands or T&Cs data missing" in result["details"]

    def test_fails_when_only_brands_present(self):
        data = {"brands": ["FanDuel"]}
        result = check_tcs_present(data)
        assert result["passed"] is False


# ===========================================================================
# check_docx_conversion
# ===========================================================================

class TestCheckDocxConversion:
    def test_passes_when_docx_files_present(self):
        data = {"output_files": ["brief.docx", "brief.md", "control.docx"]}
        result = check_docx_conversion(data)
        assert result["passed"] is True
        assert "DOCX files generated: 2" in result["details"]

    def test_fails_when_no_docx_files(self):
        data = {"output_files": ["brief.md", "control.md"]}
        result = check_docx_conversion(data)
        assert result["passed"] is False
        assert "No DOCX files found" in result["details"]

    def test_fails_when_output_files_missing(self):
        data = {}
        result = check_docx_conversion(data)
        assert result["passed"] is False
        assert "Output files data missing" in result["details"]

    def test_level_is_advisory(self):
        data = {}
        result = check_docx_conversion(data)
        assert result["level"] == "ADVISORY"


# ===========================================================================
# check_ahrefs_data
# ===========================================================================

class TestCheckAhrefsData:
    def test_passes_when_source_is_real(self):
        data = {"ahrefs_data": {"source": "real", "keyword_difficulty": 65}}
        result = check_ahrefs_data(data)
        assert result["passed"] is True
        assert "Real Ahrefs data confirmed" in result["details"]

    def test_fails_when_source_is_estimated(self):
        data = {"ahrefs_data": {"source": "estimated"}}
        result = check_ahrefs_data(data)
        assert result["passed"] is False
        assert "estimated data" in result["details"]

    def test_fails_when_source_unclear(self):
        data = {"ahrefs_data": {"keyword_difficulty": 65}}
        result = check_ahrefs_data(data)
        assert result["passed"] is False
        assert "Ahrefs data source unclear" in result["details"]

    def test_fails_when_ahrefs_missing(self):
        data = {}
        result = check_ahrefs_data(data)
        assert result["passed"] is False
        assert "Ahrefs data missing" in result["details"]


# ===========================================================================
# check_secondary_keywords
# ===========================================================================

class TestCheckSecondaryKeywords:
    def test_passes_with_8_keywords(self):
        data = {"secondary_keywords": [{}] * 8}
        result = check_secondary_keywords(data)
        assert result["passed"] is True
        assert "8 secondary keywords" in result["details"]

    def test_passes_with_15_keywords(self):
        data = {"secondary_keywords": [{}] * 15}
        result = check_secondary_keywords(data)
        assert result["passed"] is True

    def test_fails_with_fewer_than_8(self):
        data = {"secondary_keywords": [{}] * 5}
        result = check_secondary_keywords(data)
        assert result["passed"] is False
        assert "Only 5 secondary keywords" in result["details"]

    def test_fails_with_more_than_15(self):
        data = {"secondary_keywords": [{}] * 20}
        result = check_secondary_keywords(data)
        assert result["passed"] is False
        assert "20 secondary keywords (exceeds 15)" in result["details"]

    def test_fails_when_missing(self):
        data = {}
        result = check_secondary_keywords(data)
        assert result["passed"] is False
        assert "Secondary keywords missing" in result["details"]


# ===========================================================================
# check_faq_count
# ===========================================================================

class TestCheckFaqCount:
    def test_passes_with_7_faqs(self):
        data = {"faq_section": [{}] * 7}
        result = check_faq_count(data)
        assert result["passed"] is True
        assert "7 FAQs present" in result["details"]

    def test_passes_with_10_faqs(self):
        data = {"faq_section": [{}] * 10}
        result = check_faq_count(data)
        assert result["passed"] is True

    def test_fails_with_fewer_than_7(self):
        data = {"faq_section": [{}] * 4}
        result = check_faq_count(data)
        assert result["passed"] is False
        assert "Only 4 FAQs" in result["details"]

    def test_fails_when_missing(self):
        data = {}
        result = check_faq_count(data)
        assert result["passed"] is False
        assert "FAQ section missing" in result["details"]

    def test_level_is_info(self):
        data = {}
        result = check_faq_count(data)
        assert result["level"] == "INFO"


# ===========================================================================
# generate_mock_brief_data
# ===========================================================================

class TestGenerateMockBriefData:
    def test_generates_valid_data_for_fanduel_review(self):
        scenario = TEST_SCENARIOS["fanduel_review"]
        data = generate_mock_brief_data("fanduel_review", scenario)

        assert "brand_rankings" in data
        assert data["brand_rankings"]["FanDuel"] == 1
        assert data["brand_rankings"]["BetMGM"] == 2
        assert "secondary_keywords" in data
        assert len(data["secondary_keywords"]) == 9
        assert "brands" in data
        assert "tcs_sections" in data
        assert "output_files" in data
        assert "ahrefs_data" in data
        assert "faq_section" in data

    def test_generates_valid_data_for_best_betting_sites(self):
        scenario = TEST_SCENARIOS["best_betting_sites"]
        data = generate_mock_brief_data("best_betting_sites", scenario)
        assert data["url"] == "/sport/betting/best-betting-sites.htm"

    def test_generates_valid_data_for_betmgm_bonus_code(self):
        scenario = TEST_SCENARIOS["betmgm_bonus_code"]
        data = generate_mock_brief_data("betmgm_bonus_code", scenario)
        assert data["ahrefs_data"]["source"] == "real"
        assert len(data["faq_section"]) == 8

    def test_output_files_include_docx(self):
        scenario = TEST_SCENARIOS["fanduel_review"]
        data = generate_mock_brief_data("fanduel_review", scenario)
        docx_files = [f for f in data["output_files"] if f.endswith(".docx")]
        assert len(docx_files) == 3  # writer-brief, control-sheet, ai-enhancement


# ===========================================================================
# run_regression_test
# ===========================================================================

class TestRunRegressionTest:
    def test_runs_all_criteria(self):
        scenario = TEST_SCENARIOS["fanduel_review"]
        brief_data = generate_mock_brief_data("fanduel_review", scenario)
        results = run_regression_test("fanduel_review", scenario, brief_data)

        assert results["scenario_name"] == "fanduel_review"
        assert results["scenario_type"] == "Individual Review"
        assert results["url"] == "/sport/betting/fanduel-review.htm"
        assert "checks" in results
        assert len(results["checks"]) == len(REGRESSION_CRITERIA)

    def test_all_checks_pass_with_good_data(self):
        scenario = TEST_SCENARIOS["fanduel_review"]
        brief_data = generate_mock_brief_data("fanduel_review", scenario)
        results = run_regression_test("fanduel_review", scenario, brief_data)

        all_passed = all(c["passed"] for c in results["checks"])
        assert all_passed, f"Some checks failed: {[c for c in results['checks'] if not c['passed']]}"

    def test_check_names_match_criteria(self):
        scenario = TEST_SCENARIOS["fanduel_review"]
        brief_data = generate_mock_brief_data("fanduel_review", scenario)
        results = run_regression_test("fanduel_review", scenario, brief_data)

        expected_names = {c["name"] for c in REGRESSION_CRITERIA}
        actual_names = {c["name"] for c in results["checks"]}
        assert expected_names == actual_names

    def test_fails_with_bad_data(self):
        scenario = TEST_SCENARIOS["fanduel_review"]
        brief_data = {}  # No data
        results = run_regression_test("fanduel_review", scenario, brief_data)

        all_failed = all(not c["passed"] for c in results["checks"])
        assert all_failed


# ===========================================================================
# compare_regression_results
# ===========================================================================

class TestCompareRegressionResults:
    def _make_all_results(self):
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = generate_mock_brief_data(scenario_name, scenario)
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)
        return all_results

    def test_passes_with_all_good_data(self):
        all_results = self._make_all_results()
        comparison = compare_regression_results(all_results)
        assert comparison["overall_status"] == "PASSED"
        assert len(comparison["critical_failures"]) == 0

    def test_consistency_analysis_has_all_criteria(self):
        all_results = self._make_all_results()
        comparison = compare_regression_results(all_results)
        for criterion in REGRESSION_CRITERIA:
            assert criterion["name"] in comparison["consistency_analysis"]

    def test_fails_with_critical_failures(self):
        # Create data where brand positioning fails for all scenarios
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = {}  # Empty data - all checks fail
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)

        comparison = compare_regression_results(all_results)
        assert comparison["overall_status"] == "FAILED"
        assert len(comparison["critical_failures"]) > 0

    def test_advisory_warnings_detected(self):
        # Create data that passes critical but fails advisory (DOCX)
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = generate_mock_brief_data(scenario_name, scenario)
            # Remove output files (docx advisory)
            brief_data["output_files"] = ["brief.md"]
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)

        comparison = compare_regression_results(all_results)
        assert len(comparison["advisory_warnings"]) > 0

    def test_pass_rate_calculation(self):
        all_results = self._make_all_results()
        comparison = compare_regression_results(all_results)

        # With good data, all criteria should have 100% pass rate
        for criterion, consistency in comparison["consistency_analysis"].items():
            assert consistency["pass_rate"] == 100.0

    def test_scenario_counts(self):
        all_results = self._make_all_results()
        comparison = compare_regression_results(all_results)
        assert comparison["total_scenarios"] == 3


# ===========================================================================
# generate_regression_report
# ===========================================================================

class TestGenerateRegressionReport:
    def _make_comparison(self, all_results=None):
        if all_results is None:
            all_results = []
            for scenario_name, scenario in TEST_SCENARIOS.items():
                brief_data = generate_mock_brief_data(scenario_name, scenario)
                results = run_regression_test(scenario_name, scenario, brief_data)
                all_results.append(results)
        comparison = compare_regression_results(all_results)
        return all_results, comparison

    def test_report_has_required_keys(self):
        all_results, comparison = self._make_comparison()
        report = generate_regression_report(all_results, comparison)
        assert "test_run_timestamp" in report
        assert "test_type" in report
        assert "summary" in report
        assert "test_scenarios" in report
        assert "regression_comparisons" in report
        assert "recommendations" in report

    def test_report_summary_counts(self):
        all_results, comparison = self._make_comparison()
        report = generate_regression_report(all_results, comparison)
        assert report["summary"]["total_scenarios_tested"] == 3
        assert report["summary"]["overall_status"] == "PASSED"
        assert report["summary"]["critical_failures_count"] == 0

    def test_report_has_all_scenarios(self):
        all_results, comparison = self._make_comparison()
        report = generate_regression_report(all_results, comparison)
        assert "fanduel_review" in report["test_scenarios"]
        assert "best_betting_sites" in report["test_scenarios"]
        assert "betmgm_bonus_code" in report["test_scenarios"]

    def test_report_adds_critical_recommendations(self):
        # Make all checks fail
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = {}
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)
        comparison = compare_regression_results(all_results)
        report = generate_regression_report(all_results, comparison)

        assert any("CRITICAL" in r for r in report["recommendations"])

    def test_report_scenario_details(self):
        all_results, comparison = self._make_comparison()
        report = generate_regression_report(all_results, comparison)

        for scenario_name in ["fanduel_review", "best_betting_sites", "betmgm_bonus_code"]:
            scenario_data = report["test_scenarios"][scenario_name]
            assert "checks_passed" in scenario_data
            assert "checks_failed" in scenario_data
            assert "checks_detail" in scenario_data

    def test_report_includes_improvement_recommendations_on_fail(self):
        # Make only advisory fail (docx)
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = generate_mock_brief_data(scenario_name, scenario)
            brief_data["output_files"] = ["brief.md"]  # No docx
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)
        comparison = compare_regression_results(all_results)
        report = generate_regression_report(all_results, comparison)

        assert len(report["recommendations"]) > 0
        assert any("DOCX Conversion Works" in r or "consistency" in r.lower() for r in report["recommendations"])


# ===========================================================================
# print_summary
# ===========================================================================

class TestPrintSummary:
    def _make_report(self):
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = generate_mock_brief_data(scenario_name, scenario)
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)
        comparison = compare_regression_results(all_results)
        return generate_regression_report(all_results, comparison)

    def test_print_summary_runs_without_error(self, capsys):
        report = self._make_report()
        print_summary(report)
        captured = capsys.readouterr()
        assert "PHASE 3 REGRESSION TEST SUMMARY" in captured.out
        assert "PASSED" in captured.out

    def test_print_summary_shows_scenarios(self, capsys):
        report = self._make_report()
        print_summary(report)
        captured = capsys.readouterr()
        assert "fanduel_review" in captured.out
        assert "best_betting_sites" in captured.out
        assert "betmgm_bonus_code" in captured.out

    def test_print_summary_shows_recommendations_when_present(self, capsys):
        # Create report with recommendations
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = {}
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)
        comparison = compare_regression_results(all_results)
        report = generate_regression_report(all_results, comparison)
        print_summary(report)
        captured = capsys.readouterr()
        assert "RECOMMENDATIONS" in captured.out

    def test_print_summary_with_failed_scenarios(self, capsys):
        all_results = []
        for scenario_name, scenario in TEST_SCENARIOS.items():
            brief_data = {}
            results = run_regression_test(scenario_name, scenario, brief_data)
            all_results.append(results)
        comparison = compare_regression_results(all_results)
        report = generate_regression_report(all_results, comparison)
        print_summary(report)
        captured = capsys.readouterr()
        assert "CONSISTENCY ANALYSIS" in captured.out


# ===========================================================================
# main()
# ===========================================================================

class TestMain:
    def test_main_returns_0_on_success(self, tmp_path):
        with patch("phase3_regression_test.Path.cwd", return_value=tmp_path):
            with patch("builtins.print"):
                result = main()
        assert result == 0

    def test_main_creates_report_file(self, tmp_path):
        with patch("phase3_regression_test.Path.cwd", return_value=tmp_path):
            with patch("builtins.print"):
                main()
        report_file = tmp_path / "PHASE3-REGRESSION-TEST-REPORT.json"
        assert report_file.exists()

    def test_main_report_is_valid_json(self, tmp_path):
        with patch("phase3_regression_test.Path.cwd", return_value=tmp_path):
            with patch("builtins.print"):
                main()
        report_file = tmp_path / "PHASE3-REGRESSION-TEST-REPORT.json"
        with open(report_file, encoding='utf-8') as f:
            data = json.load(f)
        assert data["summary"]["overall_status"] == "PASSED"

    def test_main_returns_1_on_failure(self, tmp_path):
        """main() should return 1 when overall status is FAILED."""
        def run_regression_test_bad(scenario_name, scenario, brief_data):
            results = run_regression_test(scenario_name, scenario, brief_data)
            # Force all checks to fail
            for check in results["checks"]:
                check["passed"] = False
            return results

        with patch("phase3_regression_test.Path.cwd", return_value=tmp_path):
            with patch("phase3_regression_test.run_regression_test", side_effect=run_regression_test_bad):
                with patch("builtins.print"):
                    result = main()
        assert result == 1

    def test_main_prints_output(self, tmp_path, capsys):
        with patch("phase3_regression_test.Path.cwd", return_value=tmp_path):
            main()
        captured = capsys.readouterr()
        assert "Phase 3 Regression Testing" in captured.out


# ===========================================================================
# TEST_SCENARIOS and REGRESSION_CRITERIA structure
# ===========================================================================

class TestConstants:
    def test_test_scenarios_has_3_entries(self):
        assert len(TEST_SCENARIOS) == 3

    def test_test_scenarios_required_keys(self):
        for name, scenario in TEST_SCENARIOS.items():
            assert "type" in scenario
            assert "description" in scenario
            assert "url" in scenario
            assert "keyword" in scenario
            assert "expected" in scenario

    def test_regression_criteria_has_7_entries(self):
        assert len(REGRESSION_CRITERIA) == 7

    def test_regression_criteria_required_keys(self):
        for criterion in REGRESSION_CRITERIA:
            assert "name" in criterion
            assert "check" in criterion
            assert "critical" in criterion
            assert callable(criterion["check"])
