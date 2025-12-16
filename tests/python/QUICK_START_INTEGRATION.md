# Quick Start: Integration Tests

## TL;DR - Run All Tests

```bash
# Run all 26 integration tests
python3 -m pytest tests/python/test_integration.py -v

# Expected output: 26 passed in ~1.5s
```

## One-Command Test Scenarios

### Test Error Tracking Integration

```bash
python3 -m pytest tests/python/test_integration.py::TestErrorTrackerPromptMonitorIntegration -v
```

**What it tests**: Error tracker and prompt monitor working together

**Output**: 3 tests showing coordinated logging, pattern detection, and recommendations

---

### Test Automation Orchestration

```bash
python3 -m pytest tests/python/test_integration.py::TestAutomationOrchestration -v
```

**What it tests**: Automation script coordinating all components

**Output**: 6 tests showing command execution, report generation, and error analysis

---

### Test End-to-End Lesson Generation

```bash
python3 -m pytest tests/python/test_integration.py::TestLessonGenerationIntegration::test_end_to_end_lesson_generation -v
```

**What it tests**: Complete workflow: log error → detect pattern → generate lesson → update file

**Output**: Single comprehensive test showing the full lesson generation workflow

---

### Test Pytest Plugin

```bash
python3 -m pytest tests/python/test_integration.py::TestPytestPluginIntegration -v --error-tracking
```

**What it tests**: Pytest plugin automatically capturing test failures

**Output**: 4 tests showing plugin initialization and failure capture

---

### Test Real-World Workflow

```bash
python3 -m pytest tests/python/test_integration.py::TestEndToEndWorkflow::test_full_workflow_brief_generation_failure -v
```

**What it tests**: Simulates user generating brief, encountering failures, system learning from them

**Output**: Complete user scenario with error tracking, pattern detection, and lesson generation

---

## Understanding Test Output

### Successful Test Run

```
tests/python/test_integration.py::TestLessonGenerationIntegration::test_end_to_end_lesson_generation PASSED [38%]
```

✅ **PASSED** = Test verified the component works correctly

### Test with Captured Output

```
----------------------------- Captured stdout call -----------------------------
[LOGGED] HIGH error from test_ahrefs: HTTP 403 Forbidden from Ahrefs API
[PATTERN] Recurring error detected (3 times): HTTP 403 Forbidden
[OK] Added 1 lessons to /tmp/pytest-123/lessons-learned.md
```

This shows the system:
1. Logged an error
2. Detected a pattern after 3 occurrences
3. Successfully created a lesson

---

## Quick Validation Commands

### Check Test Count

```bash
python3 -m pytest tests/python/test_integration.py --collect-only | grep "test session starts" -A 5
```

**Expected**: `collected 26 items`

### Run Fastest Tests Only

```bash
# Run tests that complete in < 0.2s
python3 -m pytest tests/python/test_integration.py -v -k "plugin or coordinated"
```

### Run Most Important Tests

```bash
# Run critical end-to-end workflows
python3 -m pytest tests/python/test_integration.py -v -k "end_to_end or full_workflow"
```

---

## What Each Test Verifies

### 🔗 Integration Tests (3 tests)

| Test | Verifies |
|------|----------|
| `test_coordinated_logging` | Both systems log related events |
| `test_cross_system_pattern_detection` | Patterns detected across systems |
| `test_recommendations_based_on_errors` | Recommendations align with errors |

### 🤖 Automation Tests (6 tests)

| Test | Verifies |
|------|----------|
| `test_automation_runner_initialization` | Runner initializes correctly |
| `test_run_command_success` | Successful command execution |
| `test_run_command_failure` | Failed command handling |
| `test_run_command_timeout` | Timeout handling |
| `test_generate_report_format` | Report formatting |
| `test_analyze_errors_with_tracker` | Error analysis integration |

### 📚 Lesson Generation Tests (5 tests)

| Test | Verifies |
|------|----------|
| `test_end_to_end_lesson_generation` | **Full workflow** |
| `test_lesson_generation_threshold` | Only generates when threshold met |
| `test_multiple_category_lessons` | Multiple categories handled |
| `test_lesson_file_format` | Correct markdown format |
| `test_lesson_persistence` | No duplicate generation |

### 🔌 Pytest Plugin Tests (4 tests)

| Test | Verifies |
|------|----------|
| `test_plugin_options_added` | Command line options work |
| `test_plugin_captures_failures` | Failures are captured |
| `test_plugin_categorizes_test_failures` | Correct categorization |
| `test_plugin_dry_run` | Graceful degradation |

### 🌊 End-to-End Tests (4 tests)

| Test | Verifies |
|------|----------|
| `test_full_workflow_brief_generation_failure` | **Complete user scenario** |
| `test_workflow_with_recovery` | Recovery after fixes |
| `test_multiple_error_sources` | Multiple error types |
| `test_data_persistence_across_sessions` | Data persists |

### 🛡️ Error Recovery Tests (4 tests)

| Test | Verifies |
|------|----------|
| `test_corrupted_data_recovery` | Handles corrupted files |
| `test_missing_lessons_file` | Handles missing files |
| `test_large_dataset_performance` | Scales to 100+ errors |
| `test_concurrent_access_safety` | Multiple instances safe |

---

## Interpreting Coverage Reports

### Run with Coverage

```bash
python3 -m pytest tests/python/test_integration.py --cov=scripts --cov-report=term-missing
```

### Understanding Coverage Output

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
scripts/error_tracker.py  440    191    57%   160, 168-170, ...
scripts/prompt_monitor.py 503    298    41%   130, 132, ...
scripts/automation.py     143     81    43%   58, 71-72, ...
```

- **Stmts**: Total lines of code
- **Miss**: Lines not executed by tests
- **Cover**: Percentage covered
- **Missing**: Specific line numbers not covered

**Current Status**: ~40-57% coverage for integration testing

**Target**: 70%+ coverage

---

## Common Issues and Fixes

### Issue: Import Errors

```
ImportError: No module named 'error_tracker'
```

**Fix**: Tests automatically add scripts to path, but verify with:

```bash
python3 -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path.cwd() / 'scripts')); import error_tracker; print('OK')"
```

### Issue: Permission Errors

```
PermissionError: [Errno 13] Permission denied
```

**Fix**: Tests use temp directories. Check:

```bash
# Verify write access
python3 -c "from pathlib import Path; import tempfile; td = Path(tempfile.mkdtemp()); print(f'Temp: {td}'); (td / 'test.txt').write_text('ok'); print('OK')"
```

### Issue: Slow Tests

```
tests/python/test_integration.py::test_large_dataset_performance PASSED [96%]  5.23s
```

**Expected**: < 5s for performance test with 100 errors

**If slower**: Check system I/O performance

---

## CI/CD Integration

### Quick CI Test

```bash
# Minimal CI test (for faster feedback)
python3 -m pytest tests/python/test_integration.py -v -x --tb=short
```

**Flags**:
- `-v`: Verbose output
- `-x`: Stop on first failure
- `--tb=short`: Short traceback

### Full CI Test

```bash
# Complete test with coverage and error tracking
python3 -m pytest tests/python/test_integration.py -v \
  --cov=scripts \
  --cov-report=xml \
  --error-tracking \
  --junit-xml=test-results.xml
```

**Outputs**:
- `coverage.xml`: Coverage report for Codecov
- `test-results.xml`: JUnit format for CI systems

---

## Next Steps

1. **Run the tests**: `python3 -m pytest tests/python/test_integration.py -v`
2. **Check coverage**: Add `--cov=scripts --cov-report=html`
3. **Open coverage report**: `open htmlcov/index.html`
4. **Identify gaps**: Look for uncovered code paths
5. **Add tests**: Write new tests for uncovered scenarios

---

## Quick Test During Development

### Watch Mode (requires pytest-watch)

```bash
# Install
pip install pytest-watch

# Run
ptw tests/python/test_integration.py -- -v
```

Auto-runs tests when files change.

### Test Specific Scenario

```bash
# Test only lesson generation
python3 -m pytest tests/python/test_integration.py -v -k lesson

# Test only automation
python3 -m pytest tests/python/test_integration.py -v -k automation

# Test only end-to-end
python3 -m pytest tests/python/test_integration.py -v -k "end_to_end or workflow"
```

---

## Performance Expectations

| Operation | Expected Time |
|-----------|---------------|
| All 26 tests | ~1.5s |
| Single test | ~0.05s |
| End-to-end test | ~0.15s |
| Performance test (100 errors) | < 5s |

**If slower**: Check for:
- Slow disk I/O
- Network calls (should be mocked)
- Infinite loops
- Large data operations

---

## Success Checklist

✅ All 26 tests pass

✅ Tests complete in < 2s

✅ Coverage > 40% (target: 70%)

✅ No import errors

✅ No permission errors

✅ Tests isolated (can run in any order)

✅ Temp directories used (no pollution)

---

## Getting Help

**Test failures**: Check test output and error messages

**Coverage gaps**: Review `htmlcov/index.html` for details

**Performance issues**: Run with `pytest-benchmark`

**Questions**: See full README_INTEGRATION_TESTS.md

---

**Last Updated**: 2025-12-11

**Test Suite Version**: 1.0.0

**Python Version**: 3.11+

**Pytest Version**: 9.0+
