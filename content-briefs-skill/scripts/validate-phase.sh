#!/bin/bash
# VALIDATION SCRIPT - Must pass before proceeding to next phase
# Usage: ./validate-phase.sh <phase> <page-name>

set -euo pipefail

PHASE="${1:-}"
PAGE_NAME="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$PHASE" ] || [ -z "$PAGE_NAME" ]; then
    echo "Usage: $0 <phase> <page-name>"
    echo "Example: $0 1 best-sports-betting-apps"
    exit 1
fi

echo "=========================================="
echo "VALIDATING PHASE $PHASE: $PAGE_NAME"
echo "=========================================="

validate_phase1() {
    local errors=0

    # Check JSON file exists
    if [ ! -f "$BASE_DIR/active/${PAGE_NAME}-phase1.json" ]; then
        echo "FAIL: Missing active/${PAGE_NAME}-phase1.json"
        errors=$((errors + 1))
    else
        echo "PASS: phase1.json exists"

        # Check required keys in JSON
        if ! python3 -c "
import json
import sys
data = json.load(open('$BASE_DIR/active/${PAGE_NAME}-phase1.json'))

# Check primary keyword
if 'primaryKeyword' not in data:
    print('FAIL: Missing primaryKeyword')
    sys.exit(1)
print('PASS: primaryKeyword present')

# Check secondary keywords count
secondary = data.get('secondaryKeywords', [])
if len(secondary) < 8:
    print(f'FAIL: Only {len(secondary)} secondary keywords (need 8+)')
    sys.exit(1)
print(f'PASS: {len(secondary)} secondary keywords')

# Check for real volume data
has_volume = all(kw.get('volume', 0) > 0 for kw in secondary)
if not has_volume:
    print('FAIL: Some keywords missing volume data')
    sys.exit(1)
print('PASS: All keywords have volume data')

# Check brands
brands = data.get('brands', [])
if len(brands) < 5:
    print(f'FAIL: Only {len(brands)} brands (need 5+)')
    sys.exit(1)
print(f'PASS: {len(brands)} brands selected')
" 2>/dev/null; then
            echo "FAIL: JSON validation failed"
            errors=$((errors + 1))
        fi
    fi

    # Check control sheet exists
    if [ ! -f "$BASE_DIR/output/${PAGE_NAME}-brief-control-sheet.md" ]; then
        echo "FAIL: Missing output/${PAGE_NAME}-brief-control-sheet.md"
        errors=$((errors + 1))
    else
        echo "PASS: brief-control-sheet.md exists"

        # Check control sheet has required sections
        if ! grep -q "KEYWORD CLUSTER" "$BASE_DIR/output/${PAGE_NAME}-brief-control-sheet.md"; then
            echo "FAIL: Control sheet missing KEYWORD CLUSTER section"
            errors=$((errors + 1))
        else
            echo "PASS: KEYWORD CLUSTER section present"
        fi
    fi

    return $errors
}

validate_phase2() {
    local errors=0

    # First, validate Phase 1 exists
    if [ ! -f "$BASE_DIR/active/${PAGE_NAME}-phase1.json" ]; then
        echo "FAIL: Phase 1 not completed - cannot validate Phase 2"
        exit 1
    fi

    # Check JSON file exists
    if [ ! -f "$BASE_DIR/active/${PAGE_NAME}-phase2.json" ]; then
        echo "FAIL: Missing active/${PAGE_NAME}-phase2.json"
        errors=$((errors + 1))
    else
        echo "PASS: phase2.json exists"

        # Check FAQs
        if ! python3 -c "
import json
import sys
data = json.load(open('$BASE_DIR/active/${PAGE_NAME}-phase2.json'))

faqs = data.get('faqs', [])
if len(faqs) < 7:
    print(f'FAIL: Only {len(faqs)} FAQs (need 7+)')
    sys.exit(1)
print(f'PASS: {len(faqs)} FAQs')
" 2>/dev/null; then
            echo "FAIL: JSON validation failed"
            errors=$((errors + 1))
        fi
    fi

    # Check writer brief exists
    if [ ! -f "$BASE_DIR/output/${PAGE_NAME}-writer-brief.md" ]; then
        echo "FAIL: Missing output/${PAGE_NAME}-writer-brief.md"
        errors=$((errors + 1))
    else
        echo "PASS: writer-brief.md exists"

        # Check required sections
        for section in "FAQ" "Source Requirements" "KEYWORD" "BRANDS"; do
            if ! grep -qi "$section" "$BASE_DIR/output/${PAGE_NAME}-writer-brief.md"; then
                echo "FAIL: Writer brief missing $section section"
                errors=$((errors + 1))
            else
                echo "PASS: $section section present"
            fi
        done
    fi

    return $errors
}

validate_phase3() {
    local errors=0

    # First, validate Phase 1 and 2 exist
    if [ ! -f "$BASE_DIR/active/${PAGE_NAME}-phase1.json" ]; then
        echo "FAIL: Phase 1 not completed - cannot validate Phase 3"
        exit 1
    fi
    if [ ! -f "$BASE_DIR/active/${PAGE_NAME}-phase2.json" ]; then
        echo "FAIL: Phase 2 not completed - cannot validate Phase 3"
        exit 1
    fi

    # Check AI enhancement exists
    if [ ! -f "$BASE_DIR/output/${PAGE_NAME}-ai-enhancement.md" ]; then
        echo "FAIL: Missing output/${PAGE_NAME}-ai-enhancement.md"
        errors=$((errors + 1))
    else
        echo "PASS: ai-enhancement.md exists"

        # Check for schema markup
        if ! grep -q "schema.org" "$BASE_DIR/output/${PAGE_NAME}-ai-enhancement.md"; then
            echo "FAIL: Missing schema markup"
            errors=$((errors + 1))
        else
            echo "PASS: Schema markup present"
        fi

        # Check for comparison table
        if ! grep -qi "comparison" "$BASE_DIR/output/${PAGE_NAME}-ai-enhancement.md"; then
            echo "FAIL: Missing comparison table"
            errors=$((errors + 1))
        else
            echo "PASS: Comparison table present"
        fi

        # Check for T&Cs
        if ! grep -qi "Terms" "$BASE_DIR/output/${PAGE_NAME}-ai-enhancement.md"; then
            echo "FAIL: Missing T&Cs section"
            errors=$((errors + 1))
        else
            echo "PASS: T&Cs section present"
        fi

        # Check for placeholders (should have NONE)
        if grep -q "\.\.\." "$BASE_DIR/output/${PAGE_NAME}-ai-enhancement.md" || \
           grep -qi "\[insert" "$BASE_DIR/output/${PAGE_NAME}-ai-enhancement.md"; then
            echo "FAIL: Found placeholders (... or [Insert]) - code must be complete"
            errors=$((errors + 1))
        else
            echo "PASS: No placeholders found"
        fi
    fi

    return $errors
}

case "$PHASE" in
    1)
        validate_phase1
        result=$?
        ;;
    2)
        validate_phase2
        result=$?
        ;;
    3)
        validate_phase3
        result=$?
        ;;
    all)
        echo ""
        echo "=== Validating Phase 1 ==="
        validate_phase1 || true
        echo ""
        echo "=== Validating Phase 2 ==="
        validate_phase2 || true
        echo ""
        echo "=== Validating Phase 3 ==="
        validate_phase3 || true
        result=0
        ;;
    *)
        echo "Unknown phase: $PHASE"
        echo "Valid phases: 1, 2, 3, all"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
if [ ${result:-0} -eq 0 ]; then
    echo "VALIDATION PASSED - Phase $PHASE complete"
    echo "=========================================="
    exit 0
else
    echo "VALIDATION FAILED - $result errors found"
    echo "FIX ERRORS BEFORE PROCEEDING"
    echo "=========================================="
    exit 1
fi
