# Bats-Core Test Setup - Complete Summary

## What Was Created

### Core Test Files
1. **validate-phase.bats** (30 comprehensive tests)
   - Tests all validation logic for Phase 1, 2, and 3
   - Covers error conditions, edge cases, and success scenarios
   - Tests argument validation and output formatting

2. **basic.bats** (10 sanity tests)
   - Existing file - validates file existence and permissions
   - Checks project structure integrity

3. **setup.bash**
   - Test helper functions for setup/teardown
   - Fixture copying utilities
   - Validation runner helper

4. **run-shell-tests.sh**
   - Wrapper script to run all tests
   - Checks for bats installation
   - Provides installation instructions
   - Reports results with timing

5. **README.md**
   - Comprehensive documentation
   - Installation instructions
   - Usage examples
   - Troubleshooting guide

### Test Fixtures (8 files)

**Valid Fixtures:**
- `valid-phase1.json` - Complete Phase 1 with 8 keywords, volume data, 5 brands
- `valid-phase2.json` - Complete Phase 2 with 8 FAQs
- `valid-control-sheet.md` - Complete control sheet with required sections
- `valid-writer-brief.md` - Complete writer brief with all sections
- `valid-ai-enhancement.md` - Complete AI enhancement with schema.org, no placeholders

**Invalid Fixtures:**
- `invalid-phase1-missing-keywords.json` - Only 3 secondary keywords
- `invalid-phase2-few-faqs.json` - Only 3 FAQs
- `invalid-ai-enhancement.md` - Contains "..." and "[Insert]" placeholders

## Test Coverage

### Total: 40 Tests

#### validate-phase.bats (30 tests)

**Argument Validation (3 tests)**
- Requires phase argument
- Requires page-name argument
- Rejects invalid phase numbers

**Phase 1 Validation (8 tests)**
- ✅ Valid data passes
- ❌ Missing JSON file
- ❌ Missing primaryKeyword
- ❌ Insufficient secondary keywords (< 8)
- ❌ Keywords lacking volume data
- ❌ Insufficient brands (< 5)
- ❌ Missing control sheet
- ❌ Control sheet missing KEYWORD CLUSTER section

**Phase 2 Validation (6 tests)**
- ✅ Valid data passes
- ❌ Phase 1 not completed
- ❌ Missing phase2.json
- ❌ Insufficient FAQs (< 7)
- ❌ Missing writer-brief.md
- ❌ Writer brief missing required sections

**Phase 3 Validation (7 tests)**
- ✅ Valid data passes
- ❌ Phase 1 not completed
- ❌ Phase 2 not completed
- ❌ Missing ai-enhancement.md
- ❌ Missing schema markup
- ❌ Missing comparison table
- ❌ Missing T&Cs section
- ❌ Placeholders present (... or [Insert])

**All Phases (2 tests)**
- Runs validation for all three phases
- Does not exit early on failures

**Output Format (3 tests)**
- Header format validation
- Success footer validation
- Failure footer validation

#### basic.bats (10 tests)
- File existence checks
- Permission checks
- Shebang validation
- Directory structure validation
- Documentation existence

## How to Use

### Installation

First, install bats-core:

```bash
# Ubuntu/Debian
sudo apt-get install bats

# macOS
brew install bats-core

# From source
git clone https://github.com/bats-core/bats-core.git
cd bats-core
sudo ./install.sh /usr/local
```

### Running Tests

**Run all tests (recommended):**
```bash
./tests/shell/run-shell-tests.sh
```

**Run specific test file:**
```bash
bats tests/shell/validate-phase.bats
```

**Run specific test by name:**
```bash
bats tests/shell/validate-phase.bats -f "Phase 1: validation passes"
```

**Run with verbose output:**
```bash
bats -x tests/shell/validate-phase.bats
```

**Run from project root:**
```bash
bats tests/shell/
```

## Example Output

### When bats is not installed:
```
==========================================
  Shell Script Test Runner
==========================================

ERROR: bats-core is not installed

bats-core is required to run these tests.

To install bats-core:

  macOS:
    brew install bats-core

  Ubuntu/Debian:
    sudo apt-get install bats
  ...
```

### When tests pass:
```
 ✓ validation script requires phase argument
 ✓ validation script requires page-name argument
 ✓ validation script rejects invalid phase number
 ✓ Phase 1: validation passes with valid data
 ✓ Phase 1: validation fails when JSON file is missing
 ...

30 tests, 0 failures

==========================================
✓ All tests passed!
Duration: 3s
==========================================
```

### When tests fail:
```
 ✓ validation script requires phase argument
 ✗ Phase 1: validation passes with valid data
   (in test file tests/shell/validate-phase.bats, line 25)
     Expected output to contain "PASS: phase1.json exists"
     Got: "FAIL: Missing active/test-betting-apps-phase1.json"
...

30 tests, 1 failure

==========================================
✗ Some tests failed
Duration: 3s
==========================================

Tips:
  • Review failed test output above
  • Run individual test files: bats tests/shell/validate-phase.bats
  • Run specific test: bats tests/shell/validate-phase.bats -f 'test name'
  • Add -x flag for verbose output: bats -x tests/shell/validate-phase.bats
```

## File Structure

```
tests/shell/
├── README.md                              # Full documentation
├── TEST-SETUP-SUMMARY.md                  # This file
├── run-shell-tests.sh                     # Test runner wrapper
├── setup.bash                             # Test helpers
├── basic.bats                             # Basic sanity tests (10)
├── validate-phase.bats                    # Comprehensive tests (30)
└── fixtures/                              # Test data
    ├── valid-phase1.json
    ├── invalid-phase1-missing-keywords.json
    ├── valid-phase2.json
    ├── invalid-phase2-few-faqs.json
    ├── valid-control-sheet.md
    ├── valid-writer-brief.md
    ├── valid-ai-enhancement.md
    └── invalid-ai-enhancement.md
```

## Key Features

### Test Isolation
- Each test runs in a clean temporary directory
- Automatic setup and teardown
- No cross-test contamination

### Comprehensive Coverage
- All validation checks tested
- Both success and failure paths
- Edge cases and error conditions
- Output format validation

### Helper Functions
```bash
setup_valid_phase1()    # Set up valid Phase 1 files
setup_valid_phase2()    # Set up valid Phase 1 + Phase 2 files
setup_valid_phase3()    # Set up valid Phase 1 + Phase 2 + Phase 3 files
copy_to_active()        # Copy fixture to active/ directory
copy_to_output()        # Copy fixture to output/ directory
run_validation()        # Run validation with proper environment
```

### Realistic Fixtures
All fixtures contain realistic data:
- Real keyword structure from Ahrefs
- Actual brand positioning (FanDuel, BetMGM, DraftKings, etc.)
- Complete schema.org markup
- Proper T&Cs format
- Valid comparison tables

## What Gets Tested

### Phase 1 Validation
- ✅ JSON file exists
- ✅ Primary keyword present with volume data
- ✅ 8+ secondary keywords with volume data
- ✅ 5+ brands selected
- ✅ Control sheet exists
- ✅ KEYWORD CLUSTER section present

### Phase 2 Validation
- ✅ Phase 1 completed (prerequisite)
- ✅ JSON file exists
- ✅ 7+ FAQs present
- ✅ Writer brief exists
- ✅ Required sections: FAQ, Source Requirements, KEYWORD, BRANDS

### Phase 3 Validation
- ✅ Phase 1 & 2 completed (prerequisites)
- ✅ AI enhancement file exists
- ✅ Schema markup present (schema.org)
- ✅ Comparison table present
- ✅ T&Cs section present
- ✅ No placeholders ("..." or "[Insert]")

### Edge Cases
- ✅ Missing arguments
- ✅ Invalid phase numbers
- ✅ Missing prerequisite phases
- ✅ Incomplete data structures
- ✅ Missing required sections
- ✅ Malformed JSON
- ✅ All phases validation mode

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Shell Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install bats
        run: sudo apt-get install -y bats

      - name: Run shell tests
        run: ./tests/shell/run-shell-tests.sh
```

### GitLab CI Example
```yaml
test:shell:
  stage: test
  script:
    - apt-get update && apt-get install -y bats
    - ./tests/shell/run-shell-tests.sh
```

## Best Practices

1. **Run tests before committing**
   ```bash
   ./tests/shell/run-shell-tests.sh
   ```

2. **Add tests for new validation logic**
   - Follow existing test patterns
   - Test both success and failure cases
   - Use descriptive test names

3. **Keep fixtures minimal**
   - Only include data needed for the test
   - Use helper functions to set up complex scenarios

4. **Test one thing per test**
   - Each test should verify a single behavior
   - Makes failures easier to diagnose

5. **Make tests independent**
   - Don't rely on test execution order
   - Each test should be runnable in isolation

## Troubleshooting

### Problem: "command not found: bats"
**Solution:** Install bats-core (see Installation section)

### Problem: Tests fail with Python errors
**Solution:** Ensure Python 3 is installed
```bash
python3 --version
```

### Problem: Permission denied
**Solution:** Make scripts executable
```bash
chmod +x tests/shell/*.sh tests/shell/*.bats
chmod +x content-briefs-skill/scripts/validate-phase.sh
```

### Problem: Tests hang or timeout
**Solution:** Check if validation script has infinite loops or missing error handling

### Problem: "No such file or directory"
**Solution:** Run tests from project root or use the wrapper script

## Next Steps

1. **Install bats-core** if not already installed
2. **Run the tests** to verify everything works:
   ```bash
   ./tests/shell/run-shell-tests.sh
   ```
3. **Review test output** to ensure all 40 tests pass
4. **Add to CI/CD pipeline** for automated testing
5. **Add more tests** as new shell scripts are created

## Resources

- [bats-core documentation](https://bats-core.readthedocs.io/)
- [Bash testing tutorial](https://github.com/bats-core/bats-core#tutorial)
- [Shell scripting best practices](https://google.github.io/styleguide/shellguide.html)
- Project README: `/home/user/topendsports-content-briefs/tests/shell/README.md`

## Questions?

For detailed information, see:
- **README.md** - Comprehensive documentation with examples
- **setup.bash** - Available helper functions
- **validate-phase.bats** - Test implementation examples

---

**Created:** December 8, 2025
**Tests:** 40 (30 comprehensive + 10 sanity)
**Coverage:** Complete validation script coverage
**Status:** Ready to use
