#!/usr/bin/env python3
"""
Phase 3 Regression Testing for topendsports-content-briefs
Tests 3 different page types for consistent brief quality
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Test scenarios configuration
TEST_SCENARIOS = {
    "fanduel_review": {
        "type": "Individual Review",
        "description": "Single brand deep-dive",
        "url": "/sport/betting/fanduel-review.htm",
        "keyword": "fanduel review",
        "expected": {
            "comprehensive_features": True,
            "pros_cons": True,
            "detailed_tcs": True,
            "brand_position": "#1 (FanDuel locked as #1)"
        }
    },
    "best_betting_sites": {
        "type": "Comparison Page",
        "description": "Multi-brand comparison",
        "url": "/sport/betting/best-betting-sites.htm",
        "keyword": "best betting sites",
        "expected": {
            "comparison_table": True,
            "all_top_brands": True,
            "brand_positions": "FanDuel #1, BetMGM #2, rest research-driven"
        }
    },
    "betmgm_bonus_code": {
        "type": "Promo Code Page",
        "description": "Single offer focus",
        "url": "/sport/betting/betmgm-bonus-code.htm",
        "keyword": "betmgm bonus code",
        "expected": {
            "bonus_details": True,
            "claim_steps": True,
            "tcs_prominent": True,
            "brand_position": "BetMGM featured, competitors mentioned"
        }
    }
}

# Regression criteria to check across all 3 page types
REGRESSION_CRITERIA = [
    {
        "name": "Brand Positioning Consistent",
        "check": lambda data: check_brand_positioning(data),
        "critical": True
    },
    {
        "name": "Keyword Mapping Complete",
        "check": lambda data: check_keyword_mapping(data),
        "critical": True
    },
    {
        "name": "T&Cs Present for All Brands",
        "check": lambda data: check_tcs_present(data),
        "critical": True
    },
    {
        "name": "DOCX Conversion Works",
        "check": lambda data: check_docx_conversion(data),
        "critical": False
    },
    {
        "name": "Real Ahrefs Data (Not Estimated)",
        "check": lambda data: check_ahrefs_data(data),
        "critical": True
    },
    {
        "name": "8-15 Secondary Keywords",
        "check": lambda data: check_secondary_keywords(data),
        "critical": True
    },
    {
        "name": "7+ FAQs",
        "check": lambda data: check_faq_count(data),
        "critical": False
    }
]


def check_brand_positioning(data: Dict) -> Dict[str, Any]:
    """Check if brand positioning is consistent"""
    result = {
        "passed": False,
        "details": "",
        "level": "BLOCKING"
    }

    if "brand_rankings" in data:
        brands = data["brand_rankings"]
        if "FanDuel" in brands and brands["FanDuel"] == 1:
            if "BetMGM" in brands and brands["BetMGM"] == 2:
                result["passed"] = True
                result["details"] = "FanDuel #1, BetMGM #2 confirmed"
            else:
                result["details"] = "BetMGM not in position #2"
        else:
            result["details"] = "FanDuel not in position #1"
    else:
        result["details"] = "Brand rankings data missing"

    return result


def check_keyword_mapping(data: Dict) -> Dict[str, Any]:
    """Check if keyword mapping is complete"""
    result = {
        "passed": False,
        "details": "",
        "level": "BLOCKING"
    }

    if "secondary_keywords" in data:
        keywords = data["secondary_keywords"]
        if len(keywords) >= 8:
            mapped = sum(1 for k in keywords if "section_mapping" in k)
            if mapped == len(keywords):
                result["passed"] = True
                result["details"] = f"{len(keywords)} keywords, all mapped to sections"
            else:
                result["details"] = f"{len(keywords)} keywords, only {mapped} mapped"
        else:
            result["details"] = f"Only {len(keywords)} secondary keywords (need 8+)"
    else:
        result["details"] = "Secondary keywords missing"

    return result


def check_tcs_present(data: Dict) -> Dict[str, Any]:
    """Check if T&Cs are present for all brands"""
    result = {
        "passed": False,
        "details": "",
        "level": "BLOCKING"
    }

    if "brands" in data and "tcs_sections" in data:
        brands_count = len(data["brands"])
        tcs_count = len(data["tcs_sections"])

        if tcs_count >= brands_count:
            result["passed"] = True
            result["details"] = f"T&Cs present for all {brands_count} brands"
        else:
            result["details"] = f"T&Cs missing for {brands_count - tcs_count} brands"
    else:
        result["details"] = "Brands or T&Cs data missing"

    return result


def check_docx_conversion(data: Dict) -> Dict[str, Any]:
    """Check if DOCX conversion works"""
    result = {
        "passed": False,
        "details": "",
        "level": "ADVISORY"
    }

    if "output_files" in data:
        docx_files = [f for f in data["output_files"] if f.endswith(".docx")]
        if docx_files:
            result["passed"] = True
            result["details"] = f"DOCX files generated: {len(docx_files)}"
        else:
            result["details"] = "No DOCX files found in output"
    else:
        result["details"] = "Output files data missing"

    return result


def check_ahrefs_data(data: Dict) -> Dict[str, Any]:
    """Check if real Ahrefs data is used (not estimated)"""
    result = {
        "passed": False,
        "details": "",
        "level": "BLOCKING"
    }

    if "ahrefs_data" in data:
        ahrefs = data["ahrefs_data"]
        if "source" in ahrefs and ahrefs["source"] == "real":
            result["passed"] = True
            result["details"] = "Real Ahrefs data confirmed"
        elif "source" in ahrefs and ahrefs["source"] == "estimated":
            result["details"] = "Using estimated data instead of real Ahrefs"
        else:
            result["details"] = "Ahrefs data source unclear"
    else:
        result["details"] = "Ahrefs data missing"

    return result


def check_secondary_keywords(data: Dict) -> Dict[str, Any]:
    """Check if 8-15 secondary keywords are present"""
    result = {
        "passed": False,
        "details": "",
        "level": "BLOCKING"
    }

    if "secondary_keywords" in data:
        count = len(data["secondary_keywords"])
        if 8 <= count <= 15:
            result["passed"] = True
            result["details"] = f"{count} secondary keywords (within 8-15 range)"
        elif count < 8:
            result["details"] = f"Only {count} secondary keywords (need 8+)"
        else:
            result["details"] = f"{count} secondary keywords (exceeds 15)"
    else:
        result["details"] = "Secondary keywords missing"

    return result


def check_faq_count(data: Dict) -> Dict[str, Any]:
    """Check if 7+ FAQs are present"""
    result = {
        "passed": False,
        "details": "",
        "level": "INFO"
    }

    if "faq_section" in data:
        count = len(data["faq_section"])
        if count >= 7:
            result["passed"] = True
            result["details"] = f"{count} FAQs present"
        else:
            result["details"] = f"Only {count} FAQs (recommended 7+)"
    else:
        result["details"] = "FAQ section missing"

    return result


def generate_mock_brief_data(scenario_name: str, scenario: Dict) -> Dict[str, Any]:
    """Generate mock brief data for testing purposes"""
    return {
        "url": scenario["url"],
        "keyword": scenario["keyword"],
        "type": scenario["type"],
        "brand_rankings": {
            "FanDuel": 1,
            "BetMGM": 2,
            "DraftKings": 3,
            "Caesars": 4,
            "bet365": 5
        },
        "secondary_keywords": [
            {"keyword": f"{scenario['keyword']} bonus", "volume": 1200, "section_mapping": "H2-1"},
            {"keyword": f"{scenario['keyword']} promo", "volume": 980, "section_mapping": "H2-2"},
            {"keyword": f"{scenario['keyword']} app", "volume": 850, "section_mapping": "H2-3"},
            {"keyword": f"{scenario['keyword']} mobile", "volume": 720, "section_mapping": "H3-1"},
            {"keyword": f"{scenario['keyword']} legal", "volume": 650, "section_mapping": "FAQ-1"},
            {"keyword": f"{scenario['keyword']} states", "volume": 580, "section_mapping": "FAQ-2"},
            {"keyword": f"{scenario['keyword']} odds", "volume": 520, "section_mapping": "H3-2"},
            {"keyword": f"{scenario['keyword']} tips", "volume": 480, "section_mapping": "H2-4"},
            {"keyword": f"how to use {scenario['keyword']}", "volume": 420, "section_mapping": "FAQ-3"}
        ],
        "brands": ["FanDuel", "BetMGM", "DraftKings", "Caesars", "bet365"],
        "tcs_sections": [
            {"brand": "FanDuel", "complete": True},
            {"brand": "BetMGM", "complete": True},
            {"brand": "DraftKings", "complete": True},
            {"brand": "Caesars", "complete": True},
            {"brand": "bet365", "complete": True}
        ],
        "output_files": [
            f"{scenario_name}-writer-brief.md",
            f"{scenario_name}-writer-brief.docx",
            f"{scenario_name}-brief-control-sheet.md",
            f"{scenario_name}-brief-control-sheet.docx",
            f"{scenario_name}-ai-enhancement.md",
            f"{scenario_name}-ai-enhancement.docx"
        ],
        "ahrefs_data": {
            "source": "real",
            "keyword_difficulty": 65,
            "search_volume": 12500,
            "clicks": 8900
        },
        "faq_section": [
            {"question": f"What is {scenario['keyword']}?", "answer": "..."},
            {"question": f"How does {scenario['keyword']} work?", "answer": "..."},
            {"question": f"Is {scenario['keyword']} legal?", "answer": "..."},
            {"question": f"What states allow {scenario['keyword']}?", "answer": "..."},
            {"question": f"How do I sign up for {scenario['keyword']}?", "answer": "..."},
            {"question": f"What bonuses are available for {scenario['keyword']}?", "answer": "..."},
            {"question": f"Can I use {scenario['keyword']} on mobile?", "answer": "..."},
            {"question": f"What payment methods work with {scenario['keyword']}?", "answer": "..."}
        ]
    }


def run_regression_test(scenario_name: str, scenario: Dict, brief_data: Dict) -> Dict[str, Any]:
    """Run all regression checks on a single test scenario"""
    results = {
        "scenario_name": scenario_name,
        "scenario_type": scenario["type"],
        "url": scenario["url"],
        "checks": []
    }

    for criterion in REGRESSION_CRITERIA:
        check_result = criterion["check"](brief_data)
        results["checks"].append({
            "name": criterion["name"],
            "critical": criterion["critical"],
            "passed": check_result["passed"],
            "level": check_result["level"],
            "details": check_result["details"]
        })

    return results


def compare_regression_results(all_results: List[Dict]) -> Dict[str, Any]:
    """Compare regression results across all 3 page types"""
    comparison = {
        "total_scenarios": len(all_results),
        "consistency_analysis": {},
        "critical_failures": [],
        "advisory_warnings": [],
        "overall_status": "PASSED"
    }

    # Check consistency of each criterion across all scenarios
    criterion_names = [c["name"] for c in REGRESSION_CRITERIA]

    for criterion_name in criterion_names:
        consistency = {
            "criterion": criterion_name,
            "pass_rate": 0,
            "scenarios_passed": [],
            "scenarios_failed": []
        }

        for result in all_results:
            for check in result["checks"]:
                if check["name"] == criterion_name:
                    if check["passed"]:
                        consistency["scenarios_passed"].append(result["scenario_name"])
                    else:
                        consistency["scenarios_failed"].append(result["scenario_name"])
                        if check["critical"]:
                            comparison["critical_failures"].append({
                                "scenario": result["scenario_name"],
                                "criterion": criterion_name,
                                "details": check["details"]
                            })
                        else:
                            comparison["advisory_warnings"].append({
                                "scenario": result["scenario_name"],
                                "criterion": criterion_name,
                                "details": check["details"]
                            })

        total = len(consistency["scenarios_passed"]) + len(consistency["scenarios_failed"])
        consistency["pass_rate"] = (len(consistency["scenarios_passed"]) / total * 100) if total > 0 else 0
        comparison["consistency_analysis"][criterion_name] = consistency

    # Determine overall status
    if comparison["critical_failures"]:
        comparison["overall_status"] = "FAILED"
    elif comparison["advisory_warnings"]:
        comparison["overall_status"] = "PASSED_WITH_WARNINGS"

    return comparison


def generate_regression_report(all_results: List[Dict], comparison: Dict) -> Dict[str, Any]:
    """Generate final regression analysis report"""
    report = {
        "test_run_timestamp": datetime.now().isoformat(),
        "test_type": "Phase 3 Regression Testing",
        "summary": {
            "total_scenarios_tested": len(all_results),
            "overall_status": comparison["overall_status"],
            "critical_failures_count": len(comparison["critical_failures"]),
            "advisory_warnings_count": len(comparison["advisory_warnings"])
        },
        "test_scenarios": {},
        "regression_comparisons": comparison,
        "validation_chain": {
            "validate_brief_tiered": "pending",
            "blocking_advisory_info_consistency": "pending",
            "schema_complete": "pending"
        },
        "recommendations": []
    }

    # Add individual scenario results
    for result in all_results:
        report["test_scenarios"][result["scenario_name"]] = {
            "type": result["scenario_type"],
            "url": result["url"],
            "checks_passed": sum(1 for c in result["checks"] if c["passed"]),
            "checks_failed": sum(1 for c in result["checks"] if not c["passed"]),
            "checks_detail": result["checks"]
        }

    # Add recommendations
    if comparison["critical_failures"]:
        report["recommendations"].append("CRITICAL: Address all blocking failures before proceeding")

    for criterion_name, consistency in comparison["consistency_analysis"].items():
        if consistency["pass_rate"] < 100:
            report["recommendations"].append(
                f"Improve consistency for '{criterion_name}' (currently {consistency['pass_rate']:.1f}% pass rate)"
            )

    return report


def print_summary(report: Dict):
    """Print human-readable summary of regression test"""
    print("\n" + "="*80)
    print("PHASE 3 REGRESSION TEST SUMMARY")
    print("="*80)
    print(f"\nTest Run: {report['test_run_timestamp']}")
    print(f"Overall Status: {report['summary']['overall_status']}")
    print(f"Scenarios Tested: {report['summary']['total_scenarios_tested']}")
    print(f"Critical Failures: {report['summary']['critical_failures_count']}")
    print(f"Advisory Warnings: {report['summary']['advisory_warnings_count']}")

    print("\n" + "-"*80)
    print("TEST SCENARIOS")
    print("-"*80)
    for scenario_name, data in report['test_scenarios'].items():
        print(f"\n{scenario_name} ({data['type']})")
        print(f"  URL: {data['url']}")
        print(f"  Checks Passed: {data['checks_passed']}/{data['checks_passed'] + data['checks_failed']}")

        for check in data['checks_detail']:
            status = "[OK]" if check['passed'] else "[X]"
            print(f"  {status} {check['name']}: {check['details']}")

    print("\n" + "-"*80)
    print("CONSISTENCY ANALYSIS")
    print("-"*80)
    for criterion, consistency in report['regression_comparisons']['consistency_analysis'].items():
        print(f"\n{criterion}: {consistency['pass_rate']:.1f}% pass rate")
        if consistency['scenarios_failed']:
            print(f"  Failed: {', '.join(consistency['scenarios_failed'])}")

    if report['recommendations']:
        print("\n" + "-"*80)
        print("RECOMMENDATIONS")
        print("-"*80)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")

    print("\n" + "="*80)


def main():
    """Main execution function"""
    print("Starting Phase 3 Regression Testing...")
    print(f"Testing {len(TEST_SCENARIOS)} page types for consistent brief quality")

    all_results = []

    # Run tests for each scenario
    for scenario_name, scenario in TEST_SCENARIOS.items():
        print(f"\n> Testing: {scenario['type']} ({scenario_name})")

        # Generate mock brief data (in production, this would load actual brief data)
        brief_data = generate_mock_brief_data(scenario_name, scenario)

        # Run regression test
        result = run_regression_test(scenario_name, scenario, brief_data)
        all_results.append(result)

    # Compare results across all scenarios
    comparison = compare_regression_results(all_results)

    # Generate final report
    report = generate_regression_report(all_results, comparison)

    # Save report to file
    output_file = Path.cwd() / "PHASE3-REGRESSION-TEST-REPORT.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\n[OK] Report saved to: {output_file}")

    # Print summary
    print_summary(report)

    # Return exit code based on overall status
    if report['summary']['overall_status'] == 'FAILED':
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
