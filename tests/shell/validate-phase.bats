#!/usr/bin/env bats
# Tests for content-briefs-skill/scripts/validate-phase.sh

# Load test helpers
load setup

# ============================================================================
# ARGUMENT VALIDATION TESTS
# ============================================================================

@test "validation script requires phase argument" {
  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh
  [ "$status" -eq 1 ]
  [[ "$output" =~ "Usage:" ]]
}

@test "validation script requires page-name argument" {
  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1
  [ "$status" -eq 1 ]
  [[ "$output" =~ "Usage:" ]]
}

@test "validation script rejects invalid phase number" {
  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 99 test-page
  [ "$status" -eq 1 ]
  [[ "$output" =~ "Unknown phase: 99" ]]
  [[ "$output" =~ "Valid phases: 1, 2, 3, all" ]]
}

# ============================================================================
# PHASE 1 VALIDATION TESTS
# ============================================================================

@test "Phase 1: validation passes with valid data" {
  setup_valid_phase1

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 0 ]
  [[ "$output" =~ "PASS: phase1.json exists" ]]
  [[ "$output" =~ "PASS: primaryKeyword present" ]]
  [[ "$output" =~ "PASS: 8 secondary keywords" ]]
  [[ "$output" =~ "PASS: All keywords have volume data" ]]
  [[ "$output" =~ "PASS: 5 brands selected" ]]
  [[ "$output" =~ "PASS: brief-control-sheet.md exists" ]]
  [[ "$output" =~ "PASS: KEYWORD CLUSTER section present" ]]
  [[ "$output" =~ "VALIDATION PASSED" ]]
}

@test "Phase 1: validation fails when JSON file is missing" {
  # Don't set up any files

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing active/${TEST_PAGE}-phase1.json" ]]
  [[ "$output" =~ "VALIDATION FAILED" ]]
}

@test "Phase 1: validation fails when primaryKeyword is missing" {
  # Create a JSON file without primaryKeyword
  echo '{"secondaryKeywords": [], "brands": []}' > "$TEST_ACTIVE_DIR/${TEST_PAGE}-phase1.json"
  copy_to_output "valid-control-sheet.md" "${TEST_PAGE}-brief-control-sheet.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing primaryKeyword" ]]
}

@test "Phase 1: validation fails with insufficient secondary keywords" {
  copy_to_active "invalid-phase1-missing-keywords.json" "${TEST_PAGE}-phase1.json"
  copy_to_output "valid-control-sheet.md" "${TEST_PAGE}-brief-control-sheet.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Only 3 secondary keywords (need 8+)" ]]
}

@test "Phase 1: validation fails when keywords lack volume data" {
  # Create JSON with keywords but no volume
  cat > "$TEST_ACTIVE_DIR/${TEST_PAGE}-phase1.json" <<EOF
{
  "primaryKeyword": {"keyword": "test", "volume": 100},
  "secondaryKeywords": [
    {"keyword": "kw1", "volume": 0},
    {"keyword": "kw2", "volume": 0},
    {"keyword": "kw3", "volume": 0},
    {"keyword": "kw4", "volume": 0},
    {"keyword": "kw5", "volume": 0},
    {"keyword": "kw6", "volume": 0},
    {"keyword": "kw7", "volume": 0},
    {"keyword": "kw8", "volume": 0}
  ],
  "brands": [
    {"name": "Brand1"},
    {"name": "Brand2"},
    {"name": "Brand3"},
    {"name": "Brand4"},
    {"name": "Brand5"}
  ]
}
EOF
  copy_to_output "valid-control-sheet.md" "${TEST_PAGE}-brief-control-sheet.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Some keywords missing volume data" ]]
}

@test "Phase 1: validation fails with insufficient brands" {
  # Create JSON with only 3 brands
  cat > "$TEST_ACTIVE_DIR/${TEST_PAGE}-phase1.json" <<EOF
{
  "primaryKeyword": {"keyword": "test", "volume": 100},
  "secondaryKeywords": [
    {"keyword": "kw1", "volume": 100},
    {"keyword": "kw2", "volume": 100},
    {"keyword": "kw3", "volume": 100},
    {"keyword": "kw4", "volume": 100},
    {"keyword": "kw5", "volume": 100},
    {"keyword": "kw6", "volume": 100},
    {"keyword": "kw7", "volume": 100},
    {"keyword": "kw8", "volume": 100}
  ],
  "brands": [
    {"name": "Brand1"},
    {"name": "Brand2"},
    {"name": "Brand3"}
  ]
}
EOF
  copy_to_output "valid-control-sheet.md" "${TEST_PAGE}-brief-control-sheet.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Only 3 brands (need 5+)" ]]
}

@test "Phase 1: validation fails when control sheet is missing" {
  copy_to_active "valid-phase1.json" "${TEST_PAGE}-phase1.json"
  # Don't create control sheet

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing output/${TEST_PAGE}-brief-control-sheet.md" ]]
}

@test "Phase 1: validation fails when control sheet missing KEYWORD CLUSTER section" {
  copy_to_active "valid-phase1.json" "${TEST_PAGE}-phase1.json"
  echo "# Brief Control Sheet" > "$TEST_OUTPUT_DIR/${TEST_PAGE}-brief-control-sheet.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Control sheet missing KEYWORD CLUSTER section" ]]
}

# ============================================================================
# PHASE 2 VALIDATION TESTS
# ============================================================================

@test "Phase 2: validation passes with valid data" {
  setup_valid_phase2

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 2 "$TEST_PAGE"

  [ "$status" -eq 0 ]
  [[ "$output" =~ "PASS: phase2.json exists" ]]
  [[ "$output" =~ "PASS: 8 FAQs" ]]
  [[ "$output" =~ "PASS: writer-brief.md exists" ]]
  [[ "$output" =~ "PASS: FAQ section present" ]]
  [[ "$output" =~ "PASS: Source Requirements section present" ]]
  [[ "$output" =~ "PASS: KEYWORD section present" ]]
  [[ "$output" =~ "PASS: BRANDS section present" ]]
  [[ "$output" =~ "VALIDATION PASSED" ]]
}

@test "Phase 2: validation fails when Phase 1 not completed" {
  # Only create Phase 2 files, not Phase 1
  copy_to_active "valid-phase2.json" "${TEST_PAGE}-phase2.json"
  copy_to_output "valid-writer-brief.md" "${TEST_PAGE}-writer-brief.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 2 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Phase 1 not completed - cannot validate Phase 2" ]]
}

@test "Phase 2: validation fails when phase2.json is missing" {
  # Set up Phase 1 but not Phase 2 JSON
  setup_valid_phase1
  copy_to_output "valid-writer-brief.md" "${TEST_PAGE}-writer-brief.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 2 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing active/${TEST_PAGE}-phase2.json" ]]
}

@test "Phase 2: validation fails with insufficient FAQs" {
  setup_valid_phase1
  copy_to_active "invalid-phase2-few-faqs.json" "${TEST_PAGE}-phase2.json"
  copy_to_output "valid-writer-brief.md" "${TEST_PAGE}-writer-brief.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 2 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Only 3 FAQs (need 7+)" ]]
}

@test "Phase 2: validation fails when writer-brief.md is missing" {
  setup_valid_phase1
  copy_to_active "valid-phase2.json" "${TEST_PAGE}-phase2.json"
  # Don't create writer brief

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 2 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing output/${TEST_PAGE}-writer-brief.md" ]]
}

@test "Phase 2: validation fails when writer brief missing required sections" {
  setup_valid_phase1
  copy_to_active "valid-phase2.json" "${TEST_PAGE}-phase2.json"
  echo "# Writer Brief" > "$TEST_OUTPUT_DIR/${TEST_PAGE}-writer-brief.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 2 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Writer brief missing FAQ section" ]]
  [[ "$output" =~ "FAIL: Writer brief missing Source Requirements section" ]]
  [[ "$output" =~ "FAIL: Writer brief missing KEYWORD section" ]]
  [[ "$output" =~ "FAIL: Writer brief missing BRANDS section" ]]
}

# ============================================================================
# PHASE 3 VALIDATION TESTS
# ============================================================================

@test "Phase 3: validation passes with valid data" {
  setup_valid_phase3

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 0 ]
  [[ "$output" =~ "PASS: ai-enhancement.md exists" ]]
  [[ "$output" =~ "PASS: Schema markup present" ]]
  [[ "$output" =~ "PASS: Comparison table present" ]]
  [[ "$output" =~ "PASS: T&Cs section present" ]]
  [[ "$output" =~ "PASS: No placeholders found" ]]
  [[ "$output" =~ "VALIDATION PASSED" ]]
}

@test "Phase 3: validation fails when Phase 1 not completed" {
  # Only create Phase 3 files
  copy_to_output "valid-ai-enhancement.md" "${TEST_PAGE}-ai-enhancement.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Phase 1 not completed - cannot validate Phase 3" ]]
}

@test "Phase 3: validation fails when Phase 2 not completed" {
  # Set up Phase 1 but not Phase 2
  setup_valid_phase1
  copy_to_output "valid-ai-enhancement.md" "${TEST_PAGE}-ai-enhancement.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Phase 2 not completed - cannot validate Phase 3" ]]
}

@test "Phase 3: validation fails when ai-enhancement.md is missing" {
  setup_valid_phase2
  # Don't create ai-enhancement

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing output/${TEST_PAGE}-ai-enhancement.md" ]]
}

@test "Phase 3: validation fails when schema markup is missing" {
  setup_valid_phase2
  echo "# AI Enhancement\n\nSome content" > "$TEST_OUTPUT_DIR/${TEST_PAGE}-ai-enhancement.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing schema markup" ]]
}

@test "Phase 3: validation fails when comparison table is missing" {
  setup_valid_phase2
  echo "# AI Enhancement\n\nschema.org content" > "$TEST_OUTPUT_DIR/${TEST_PAGE}-ai-enhancement.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing comparison table" ]]
}

@test "Phase 3: validation fails when T&Cs section is missing" {
  setup_valid_phase2
  echo "# AI Enhancement\n\nschema.org\n\nComparison table here" > "$TEST_OUTPUT_DIR/${TEST_PAGE}-ai-enhancement.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Missing T&Cs section" ]]
}

@test "Phase 3: validation fails when placeholders are present" {
  setup_valid_phase2
  copy_to_output "invalid-ai-enhancement.md" "${TEST_PAGE}-ai-enhancement.md"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 3 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "FAIL: Found placeholders (... or [Insert]) - code must be complete" ]]
}

# ============================================================================
# ALL PHASES VALIDATION TEST
# ============================================================================

@test "Phase 'all': runs validation for all three phases" {
  setup_valid_phase3

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh all "$TEST_PAGE"

  [ "$status" -eq 0 ]
  [[ "$output" =~ "=== Validating Phase 1 ===" ]]
  [[ "$output" =~ "=== Validating Phase 2 ===" ]]
  [[ "$output" =~ "=== Validating Phase 3 ===" ]]
  [[ "$output" =~ "VALIDATION PASSED - Phase all complete" ]]
}

@test "Phase 'all': does not exit early on individual phase failures" {
  # Only set up Phase 1
  setup_valid_phase1

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh all "$TEST_PAGE"

  # Should not exit with error on "all" - it runs through all phases
  [ "$status" -eq 0 ]
  [[ "$output" =~ "=== Validating Phase 1 ===" ]]
  [[ "$output" =~ "=== Validating Phase 2 ===" ]]
  [[ "$output" =~ "=== Validating Phase 3 ===" ]]
}

# ============================================================================
# OUTPUT FORMAT TESTS
# ============================================================================

@test "validation outputs header with phase and page name" {
  setup_valid_phase1

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 0 ]
  [[ "$output" =~ "==========================================" ]]
  [[ "$output" =~ "VALIDATING PHASE 1: ${TEST_PAGE}" ]]
}

@test "validation outputs footer on success" {
  setup_valid_phase1

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 0 ]
  [[ "$output" =~ "VALIDATION PASSED - Phase 1 complete" ]]
}

@test "validation outputs footer on failure" {
  # Create incomplete Phase 1
  echo '{"primaryKeyword": {}}' > "$TEST_ACTIVE_DIR/${TEST_PAGE}-phase1.json"

  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  [ "$status" -eq 1 ]
  [[ "$output" =~ "VALIDATION FAILED" ]]
  [[ "$output" =~ "FIX ERRORS BEFORE PROCEEDING" ]]
}
