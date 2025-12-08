# Shell Script Tests

This directory contains bats-core tests for shell scripts in the topendsports-content-briefs project.

## Overview

We use [bats-core](https://github.com/bats-core/bats-core) (Bash Automated Testing System) to test shell scripts. The test suite provides comprehensive coverage of validation logic, error handling, and edge cases.

## Test Structure

```
tests/shell/
├── README.md                    # This file
├── run-shell-tests.sh          # Wrapper script to run all tests
├── setup.bash                  # Test setup/teardown helpers
├── basic.bats                  # Basic sanity tests (file existence, permissions)
├── validate-phase.bats         # Comprehensive tests for validate-phase.sh
└── fixtures/                   # Test data files
    ├── valid-phase1.json
    ├── invalid-phase1-missing-keywords.json
    ├── valid-phase2.json
    ├── invalid-phase2-few-faqs.json
    ├── valid-control-sheet.md
    ├── valid-writer-brief.md
    ├── valid-ai-enhancement.md
    └── invalid-ai-enhancement.md
```

## Prerequisites

### Install bats-core

**macOS:**
```bash
brew install bats-core
```

**Ubuntu/Debian:**
```bash
sudo apt-get install bats
```

**Fedora/RHEL:**
```bash
sudo dnf install bats
```

**From source:**
```bash
git clone https://github.com/bats-core/bats-core.git
cd bats-core
sudo ./install.sh /usr/local
```

**npm (if you have Node.js):**
```bash
npm install -g bats
```

## Running Tests

### Run all shell tests (recommended)
```bash
./tests/shell/run-shell-tests.sh
```

This wrapper script:
- Checks if bats is installed
- Provides installation instructions if needed
- Runs all .bats files in the directory
- Reports results with timing

### Run specific test file
```bash
bats tests/shell/validate-phase.bats
```

### Run specific test by name
```bash
bats tests/shell/validate-phase.bats -f "Phase 1: validation passes"
```

### Run tests with verbose output
```bash
bats -x tests/shell/validate-phase.bats
```

### Run all tests from project root
```bash
bats tests/shell/
```

## Test Files

### basic.bats
Sanity tests that verify:
- All required scripts exist
- Scripts have correct permissions
- Scripts have proper shebangs
- Directory structure is correct
- Required documentation exists

**Run:** `bats tests/shell/basic.bats`

### validate-phase.bats
Comprehensive tests for `content-briefs-skill/scripts/validate-phase.sh`:

**Argument Validation (3 tests)**
- Missing phase argument
- Missing page-name argument
- Invalid phase number

**Phase 1 Validation (8 tests)**
- Valid data passes
- Missing JSON file fails
- Missing primaryKeyword fails
- Insufficient secondary keywords fails
- Missing volume data fails
- Insufficient brands fails
- Missing control sheet fails
- Missing KEYWORD CLUSTER section fails

**Phase 2 Validation (6 tests)**
- Valid data passes
- Phase 1 not completed fails
- Missing phase2.json fails
- Insufficient FAQs fails
- Missing writer-brief.md fails
- Missing required sections fails

**Phase 3 Validation (7 tests)**
- Valid data passes
- Phase 1 not completed fails
- Phase 2 not completed fails
- Missing ai-enhancement.md fails
- Missing schema markup fails
- Missing comparison table fails
- Missing T&Cs section fails
- Placeholders present fails

**All Phases Validation (2 tests)**
- Runs all three phase validations
- Does not exit early on failures

**Output Format (3 tests)**
- Header format
- Success footer
- Failure footer

**Total: 29 comprehensive tests**

**Run:** `bats tests/shell/validate-phase.bats`

## Test Fixtures

Fixtures are sample data files used by tests. They are located in `fixtures/`:

### Valid Fixtures
- `valid-phase1.json` - Complete Phase 1 data with 8 secondary keywords, real volume data, 5 brands
- `valid-phase2.json` - Complete Phase 2 data with 8 FAQs
- `valid-control-sheet.md` - Complete control sheet with KEYWORD CLUSTER section
- `valid-writer-brief.md` - Complete writer brief with all required sections
- `valid-ai-enhancement.md` - Complete AI enhancement with schema.org, no placeholders

### Invalid Fixtures
- `invalid-phase1-missing-keywords.json` - Only 3 secondary keywords (need 8+)
- `invalid-phase2-few-faqs.json` - Only 3 FAQs (need 7+)
- `invalid-ai-enhancement.md` - Contains "..." and "[Insert]" placeholders

## Helper Functions

The `setup.bash` file provides test helpers:

### Setup/Teardown
- `setup()` - Creates temporary test directories, copies validation script
- `teardown()` - Cleans up temporary files

### Fixture Helpers
- `copy_to_active(fixture, target)` - Copy fixture to active/ directory
- `copy_to_output(fixture, target)` - Copy fixture to output/ directory
- `setup_valid_phase1()` - Set up complete Phase 1 files
- `setup_valid_phase2()` - Set up complete Phase 1 + Phase 2 files
- `setup_valid_phase3()` - Set up complete Phase 1 + Phase 2 + Phase 3 files

### Validation Helper
- `run_validation(phase, page_name)` - Run validation script with proper environment

### Assertions
- `assert_file_exists(file)` - Assert file exists
- `assert_file_not_exists(file)` - Assert file does not exist

## Writing New Tests

### Test Template
```bash
@test "description of what is being tested" {
  # Arrange: Set up test data
  setup_valid_phase1

  # Act: Run the command
  cd "$TEST_SCRIPTS_DIR"
  run ./validate-phase.sh 1 "$TEST_PAGE"

  # Assert: Check the results
  [ "$status" -eq 0 ]
  [[ "$output" =~ "PASS: expected message" ]]
}
```

### Bats Assertions
- `[ "$status" -eq 0 ]` - Exit code is 0 (success)
- `[ "$status" -eq 1 ]` - Exit code is 1 (failure)
- `[[ "$output" =~ "pattern" ]]` - Output matches pattern
- `[ -f "$file" ]` - File exists
- `[ ! -f "$file" ]` - File does not exist

### Test Organization
1. Group related tests together
2. Use descriptive test names
3. Follow Arrange-Act-Assert pattern
4. Clean up after tests (handled by teardown)
5. Use fixtures for test data

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Install bats
  run: sudo apt-get install -y bats

- name: Run shell tests
  run: ./tests/shell/run-shell-tests.sh
```

## Troubleshooting

### Tests fail with "command not found: bats"
Install bats-core (see Prerequisites section above)

### Tests fail with "No such file or directory"
Ensure you're running tests from the project root or using the wrapper script

### Tests timeout or hang
Check that the validation script is executable:
```bash
chmod +x content-briefs-skill/scripts/validate-phase.sh
```

### Individual test fails but passes when run alone
Check for test isolation issues - ensure each test cleans up properly

### Python validation errors in tests
Ensure Python 3 is installed and available in PATH:
```bash
python3 --version
```

## Best Practices

1. **Run tests before committing** - Ensure all tests pass
2. **Add tests for new features** - When adding validation logic, add tests
3. **Test edge cases** - Include tests for error conditions
4. **Keep fixtures minimal** - Only include data needed for the test
5. **Use descriptive names** - Test names should explain what they verify
6. **Test one thing per test** - Each test should verify a single behavior
7. **Make tests independent** - Tests should not depend on execution order

## Coverage

Current test coverage for `validate-phase.sh`:

- ✅ Argument validation
- ✅ Phase 1 validation (all checks)
- ✅ Phase 2 validation (all checks)
- ✅ Phase 3 validation (all checks)
- ✅ "all" phases validation
- ✅ Error messages
- ✅ Success messages
- ✅ Exit codes

## Future Enhancements

Potential additions to the test suite:

- [ ] Tests for other shell scripts (mcp-ahrefs.sh, mcp-topendsports.sh)
- [ ] Performance tests (validation time limits)
- [ ] Integration tests with actual Ahrefs API
- [ ] Tests for error recovery scenarios
- [ ] Tests for concurrent validation runs

## Resources

- [bats-core documentation](https://bats-core.readthedocs.io/)
- [Bash testing tutorial](https://github.com/bats-core/bats-core#tutorial)
- [Shell scripting best practices](https://google.github.io/styleguide/shellguide.html)

## Questions?

If you encounter issues or have questions about the test suite:

1. Check this README for answers
2. Review existing tests for examples
3. Run tests with `-x` flag for verbose output
4. Check bats-core documentation for assertion syntax
