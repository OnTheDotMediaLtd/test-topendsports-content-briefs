#!/bin/bash
# Wrapper script to run shell tests using bats-core

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "=========================================="
echo "  Shell Script Test Runner"
echo "=========================================="
echo ""

# Check if bats is installed
if ! command -v bats &> /dev/null; then
    echo -e "${RED}ERROR: bats-core is not installed${NC}"
    echo ""
    echo "bats-core is required to run these tests."
    echo ""
    echo "To install bats-core:"
    echo ""
    echo "  macOS:"
    echo -e "    ${BLUE}brew install bats-core${NC}"
    echo ""
    echo "  Ubuntu/Debian:"
    echo -e "    ${BLUE}sudo apt-get install bats${NC}"
    echo ""
    echo "  Fedora/RHEL:"
    echo -e "    ${BLUE}sudo dnf install bats${NC}"
    echo ""
    echo "  From source:"
    echo -e "    ${BLUE}git clone https://github.com/bats-core/bats-core.git${NC}"
    echo -e "    ${BLUE}cd bats-core${NC}"
    echo -e "    ${BLUE}sudo ./install.sh /usr/local${NC}"
    echo ""
    echo "  npm (if you have Node.js):"
    echo -e "    ${BLUE}npm install -g bats${NC}"
    echo ""
    exit 1
fi

# Check bats version
BATS_VERSION=$(bats --version | head -n1)
echo -e "${GREEN}Found: ${BATS_VERSION}${NC}"
echo ""

# Count test files
TEST_FILES=("$SCRIPT_DIR"/*.bats)
TEST_COUNT=${#TEST_FILES[@]}

if [ ${TEST_COUNT} -eq 0 ]; then
    echo -e "${YELLOW}WARNING: No .bats test files found in ${SCRIPT_DIR}${NC}"
    exit 0
fi

echo "Running ${TEST_COUNT} test file(s)..."
echo ""

# Run tests with timing
START_TIME=$(date +%s)

# Run bats with options:
# -r: recursive
# -t: tap output (can be piped to tap-prettify if available)
# --print-output-on-failure: only show output for failed tests
if command -v tap-prettify &> /dev/null; then
    # If tap-prettify is available, use it for prettier output
    bats --print-output-on-failure "$SCRIPT_DIR"/*.bats | tap-prettify
    RESULT=${PIPESTATUS[0]}
else
    # Otherwise use standard output
    bats --print-output-on-failure "$SCRIPT_DIR"/*.bats
    RESULT=$?
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "=========================================="

if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed${NC}"
fi

echo "Duration: ${DURATION}s"
echo "=========================================="
echo ""

# Provide helpful tips on failure
if [ $RESULT -ne 0 ]; then
    echo -e "${YELLOW}Tips:${NC}"
    echo "  • Review failed test output above"
    echo "  • Run individual test files: bats tests/shell/validate-phase.bats"
    echo "  • Run specific test: bats tests/shell/validate-phase.bats -f 'test name'"
    echo "  • Add -x flag for verbose output: bats -x tests/shell/validate-phase.bats"
    echo ""
fi

exit $RESULT
