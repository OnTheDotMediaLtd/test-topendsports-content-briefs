#!/bin/bash
# Test setup and helper functions for bats tests

# Setup function - run before each test
setup() {
  # Create a temporary test directory
  export TEST_TEMP_DIR="$(mktemp -d -t bats-test-XXXXXX)"

  # Set up directory structure mimicking the real structure
  export TEST_BASE_DIR="$TEST_TEMP_DIR/content-briefs-skill"
  export TEST_ACTIVE_DIR="$TEST_BASE_DIR/active"
  export TEST_OUTPUT_DIR="$TEST_BASE_DIR/output"
  export TEST_SCRIPTS_DIR="$TEST_BASE_DIR/scripts"

  mkdir -p "$TEST_ACTIVE_DIR"
  mkdir -p "$TEST_OUTPUT_DIR"
  mkdir -p "$TEST_SCRIPTS_DIR"

  # Copy the validation script to test location
  cp "${BATS_TEST_DIRNAME}/../../content-briefs-skill/scripts/validate-phase.sh" "$TEST_SCRIPTS_DIR/"
  chmod +x "$TEST_SCRIPTS_DIR/validate-phase.sh"

  # Get fixtures directory
  export FIXTURES_DIR="${BATS_TEST_DIRNAME}/fixtures"

  # Set test page name
  export TEST_PAGE="test-betting-apps"
}

# Teardown function - run after each test
teardown() {
  # Clean up temporary directory
  if [ -n "$TEST_TEMP_DIR" ] && [ -d "$TEST_TEMP_DIR" ]; then
    rm -rf "$TEST_TEMP_DIR"
  fi
}

# Helper function to copy fixture to active directory
copy_to_active() {
  local fixture_file="$1"
  local target_name="$2"
  cp "$FIXTURES_DIR/$fixture_file" "$TEST_ACTIVE_DIR/$target_name"
}

# Helper function to copy fixture to output directory
copy_to_output() {
  local fixture_file="$1"
  local target_name="$2"
  cp "$FIXTURES_DIR/$fixture_file" "$TEST_OUTPUT_DIR/$target_name"
}

# Helper function to set up valid Phase 1 files
setup_valid_phase1() {
  copy_to_active "valid-phase1.json" "${TEST_PAGE}-phase1.json"
  copy_to_output "valid-control-sheet.md" "${TEST_PAGE}-brief-control-sheet.md"
}

# Helper function to set up valid Phase 2 files
setup_valid_phase2() {
  # Phase 2 requires Phase 1 to exist
  setup_valid_phase1
  copy_to_active "valid-phase2.json" "${TEST_PAGE}-phase2.json"
  copy_to_output "valid-writer-brief.md" "${TEST_PAGE}-writer-brief.md"
}

# Helper function to set up valid Phase 3 files
setup_valid_phase3() {
  # Phase 3 requires Phase 1 and 2 to exist
  setup_valid_phase2
  copy_to_output "valid-ai-enhancement.md" "${TEST_PAGE}-ai-enhancement.md"
}

# Helper function to run validation script
run_validation() {
  local phase="$1"
  local page_name="${2:-$TEST_PAGE}"

  # Change to scripts directory and run validation
  cd "$TEST_SCRIPTS_DIR"

  # Override BASE_DIR to point to our test directory
  # The script calculates BASE_DIR from SCRIPT_DIR, so we need to be in the right place
  ./validate-phase.sh "$phase" "$page_name"
}

# Assert helpers
assert_file_exists() {
  local file="$1"
  [ -f "$file" ]
}

assert_file_not_exists() {
  local file="$1"
  [ ! -f "$file" ]
}
