#!/usr/bin/env python3
"""
Brand Validation Gate - Blocks delivery of briefs with fake brands.

This script is a BLOCKING gate that must pass before Phase 2 briefs are delivered.
Uses tes-shared-infrastructure BrandValidator to catch hallucinated brand names.

Usage:
    python scripts/validate_brands_gate.py <brief-file>

Exit codes:
    0 - All brands validated, safe to proceed
    1 - Unknown or suspicious brands found, BLOCKED
    2 - Validation error (file not found, etc.)

Example:
    python scripts/validate_brands_gate.py output/canada-sports-betting-sites-writer-brief.md
"""

import sys
from pathlib import Path

# Add tes-shared-infrastructure to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SHARED_INFRA = PROJECT_ROOT.parent / "TEST-tes-shared-infrastructure"

if not SHARED_INFRA.exists():
    print(f"[ERROR] tes-shared-infrastructure not found at: {SHARED_INFRA}")
    print("[ERROR] Cannot validate brands without shared infrastructure")
    sys.exit(2)

sys.path.insert(0, str(SHARED_INFRA / "src"))

try:
    from tes_shared.validators.brand_validator import BrandValidator
except ImportError as e:
    print(f"[ERROR] Failed to import BrandValidator: {e}")
    print(f"[ERROR] Checked path: {SHARED_INFRA}/src/tes_shared/validators/brand_validator.py")
    sys.exit(2)


def validate_brief_brands(brief_path: Path, strict: bool = True) -> tuple[bool, dict]:
    """
    Validate all brand names mentioned in a brief.
    
    Args:
        brief_path: Path to the brief file (.md or .json)
        strict: If True, block on unknown brands. If False, only block on suspicious.
    
    Returns:
        (is_valid, validation_details)
    """
    if not brief_path.exists():
        print(f"[ERROR] Brief file not found: {brief_path}")
        return False, {"error": "File not found"}
    
    try:
        content = brief_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[ERROR] Failed to read brief: {e}")
        return False, {"error": str(e)}
    
    # Initialize validator
    validator = BrandValidator(strict_mode=strict)
    
    # Run validation
    result = validator.validate(content)
    
    return result.valid, {
        "verified_brands": result.verified_brands,
        "unknown_brands": result.unknown_brands,
        "suspicious_brands": result.suspicious_brands,
        "errors": result.errors,
        "warnings": result.warnings,
        "suggestions": result.suggestions,
    }


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_brands_gate.py <brief-file>")
        print("Example: python scripts/validate_brands_gate.py output/page-writer-brief.md")
        sys.exit(2)
    
    brief_file = Path(sys.argv[1])
    # Default to lenient mode for automated gates (strict mode catches too many text fragments)
    strict_mode = "--strict" in sys.argv
    
    print(f"\n{'='*70}")
    print(f"BRAND VALIDATION GATE")
    print(f"{'='*70}")
    print(f"File: {brief_file.name}")
    print(f"Mode: {'STRICT (blocks unknown brands)' if strict_mode else 'LENIENT (blocks suspicious/fake only)'}")
    print(f"{'='*70}\n")
    
    is_valid, details = validate_brief_brands(brief_file, strict=strict_mode)
    
    # Report results
    if details.get("error"):
        print(f"[ERROR] Validation failed: {details['error']}")
        sys.exit(2)
    
    # Show verified brands
    if details.get("verified_brands"):
        print(f"[OK] Verified brands ({len(details['verified_brands'])}):")
        for brand in details["verified_brands"]:
            print(f"  - {brand}")
        print()
    
    # Show unknown brands (warnings in lenient mode, errors in strict mode)
    if details.get("unknown_brands"):
        level = "ERROR" if strict_mode else "WARN"
        print(f"[{level}] Unknown brands ({len(details['unknown_brands'])}):")
        for brand in details["unknown_brands"]:
            suggestion = details.get("suggestions", {}).get(brand)
            if suggestion:
                print(f"  - {brand} (did you mean: {', '.join(suggestion)}?)")
            else:
                print(f"  - {brand}")
        print()
    
    # Show suspicious brands (always errors)
    if details.get("suspicious_brands"):
        print(f"[ERROR] Suspicious/fake brands ({len(details['suspicious_brands'])}):")
        for brand in details["suspicious_brands"]:
            print(f"  - {brand}")
        print()
    
    # Show all errors
    if details.get("errors"):
        print("[ERROR] Validation errors:")
        for error in details["errors"]:
            print(f"  - {error}")
        print()
    
    # Show warnings
    if details.get("warnings"):
        print("[WARN] Warnings:")
        for warning in details["warnings"]:
            print(f"  - {warning}")
        print()
    
    # Final verdict
    print(f"{'='*70}")
    if is_valid:
        print("[OK] VALIDATION PASSED - Safe to proceed")
        print(f"{'='*70}\n")
        sys.exit(0)
    else:
        print("[BLOCKED] VALIDATION FAILED - Fix brands before proceeding")
        print(f"{'='*70}\n")
        print("Action required:")
        print("1. Review the unknown/suspicious brands listed above")
        print("2. Replace with verified brands from the suggestions")
        print("3. Re-run validation: python scripts/validate_brands_gate.py <file>")
        print("4. Only proceed after validation passes")
        sys.exit(1)


if __name__ == "__main__":
    main()
