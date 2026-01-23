# Integration Tests for Error Tracking and Prompt Monitoring

## Overview

The integration tests in `test_integration.py` verify that all components of the error tracking and prompt monitoring system work together correctly. These tests ensure:

1. **Component Integration**: Error tracker and prompt monitor coordinate properly
2. **Automation Orchestration**: The automation script successfully manages all components
3. **Lesson Generation**: Errors are detected, patterns analyzed, and lessons created
4. **Pytest Plugin**: Test failures are automatically captured and logged
5. **End-to-End Workflows**: Complete user scenarios work from start to finish

## Test Coverage

### Test Classes

| Test Class | Tests | Purpose |
|------------|-------|---------|
| **TestErrorTrackerPromptMonitorIntegration** | 3 | Verify tracker and monitor work together |
| **TestAutomationOrchestration** | 6 | Test automation script coordination |
| **TestLessonGenerationIntegration** | 5 | Verify lesson generation workflow |
| **TestPytestPluginIntegration** | 4 | Test pytest plugin integration |
| **TestEndToEndWorkflow** | 4 | Complete user scenarios |
| **TestErrorRecoveryAndCleanup** | 4 | Error handling and cleanup |

**Total: 26 integration tests**

## Running the Tests

### Run All Integration Tests

```bash
# Standard run
python3 -m pytest tests/python/test_integration.py -v

# With coverage report
python3 -m pytest tests/python/test_integration.py -v --cov=scripts --cov-report=html

# Show detailed output
python3 -m pytest tests/python/test_integration.py -vv --tb=long
```

### Run Specific Test Classes

```bash
# Test error tracker + prompt monitor integration
python3 -m pytest tests/python/test_integration.py::TestErrorTrackerPromptMonitorIntegration -v

# Test automation orchestration
python3 -m pytest tests/python/test_integration.py::TestAutomationOrchestration -v

# Test lesson generation
python3 -m pytest tests/python/test_integration.py::TestLessonGenerationIntegration -v

# Test pytest plugin
python3 -m pytest tests/python/test_integration.py::TestPytestPluginIntegration -v

# Test end-to-end workflows
python3 -m pytest tests/python/test_integration.py::TestEndToEndWorkflow -v

# Test error recovery
python3 -m pytest tests/python/test_integration.py::TestErrorRecoveryAndCleanup -v
```

### Run Individual Tests

```bash
# Test coordinated logging
python3 -m pytest tests/python/test_integration.py::TestErrorTrackerPromptMonitorIntegration::test_coordinated_logging -v

# Test end-to-end lesson generation
python3 -m pytest tests/python/test_integration.py::TestLessonGenerationIntegration::test_end_to_end_lesson_generation -v

# Test full workflow with brief generation failure
python3 -m pytest tests/python/test_integration.py::TestEndToEndWorkflow::test_full_workflow_brief_generation_failure -v
```

### Run with Error Tracking Plugin

```bash
# Enable error tracking for the test run
python3 -m pytest tests/python/test_integration.py -v --error-tracking

# With verbose tracking output
python3 -m pytest tests/python/test_integration.py -v --error-tracking --verbose-tracking
```

## Key Test Scenarios

### 1. Coordinated System Logging

**Test**: `test_coordinated_logging`

Verifies that when a command fails, both the prompt monitor and error tracker log the event:

```python
# Monitor logs command failure
monitor.log_usage(command="/generate-brief", status="failure")

# Tracker logs error details
tracker.add_error(source="generate-brief", error_message="HTTP 403")

# Both systems have the event recorded
assert len(monitor.entries) == 1
assert len(tracker.errors) == 1
```

### 2. Cross-System Pattern Detection

**Test**: `test_cross_system_pattern_detection`

Verifies that recurring failures are detected across both systems:

```python
# Simulate 5 Ahrefs failures
for i in range(5):
    monitor.log_usage(command="ahrefs", status="failure")
    tracker.add_error(source="ahrefs", error_message="403")

# Pattern detected in tracker
assert pattern["count"] == 5

# Failures tracked in monitor
assert stats["by_status"]["failure"] == 5
```

### 3. End-to-End Lesson Generation

**Test**: `test_end_to_end_lesson_generation`

Complete workflow from error logging to lesson creation:

```python
# 1. Log recurring errors (5 times)
for i in range(5):
    tracker.add_error(source="test_ahrefs", error_message="HTTP 403")

# 2. Pattern detected
assert pattern["count"] == 5

# 3. Generate lessons
lessons = tracker.generate_lessons(min_occurrences=3)

# 4. Verify lesson created
assert len(lessons) == 1
assert lesson["category"] == "api"

# 5. Verify file updated
assert "Auto-Generated Lessons" in lessons_file.read_text()

# 6. Pattern marked as processed
assert pattern["lesson_generated"] == True
```

### 4. Pytest Plugin Captures Failures

**Test**: `test_plugin_captures_failures`

Verifies the pytest plugin automatically logs test failures:

```python
# Simulate test failure
mock_call.excinfo.value = Exception("Test assertion failed")

# Plugin captures the failure
plugin.pytest_runtest_makereport(mock_item, mock_call)

# Failure is recorded
assert len(plugin.failures) == 1
assert "assertion failed" in failure["error"].lower()
```

### 5. Full Brief Generation Workflow

**Test**: `test_full_workflow_brief_generation_failure`

Simulates a real user scenario where brief generation fails multiple times:

```python
# 1. Brief generation fails 5 times
for attempt in range(5):
    monitor.log_usage(command="/generate-brief", status="failure")
    tracker.add_error(source="generate-brief", error_message="HTTP 403")

# 2. Pattern detected
assert stats["patterns_needing_attention"] > 0

# 3. Recommendations generated
recommendations = monitor.get_recommendations()
assert len(ahrefs_recs) > 0

# 4. Lessons created
lessons = tracker.generate_lessons(min_occurrences=3)
assert len(lessons) >= 1

# 5. Lessons file updated
assert "Auto-Generated Lessons" in lessons_file.read_text()
```

### 6. Automation Runner Coordination

**Test**: `test_automation_runner_initialization` and others

Verifies the automation script properly coordinates all components:

```python
runner = AutomationRunner(verbose=True)

# Run tests
runner.run_tests(with_tracking=True)

# Analyze errors
runner.analyze_errors()

# Process feedback
runner.process_feedback()

# Generate lessons
runner.generate_lessons()

# Create report
report = runner.generate_report()
```

## Testing Best Practices

### 1. Temporary Directories

All tests use temporary directories to avoid polluting real data:

```python
@pytest.fixture
def integrated_system(self, tmp_path, monkeypatch):
    error_dir = tmp_path / "logs" / "errors"
    error_dir.mkdir(parents=True)

    # Patch paths to use temp directories
    monkeypatch.setattr(et, 'ERROR_LOG_DIR', error_dir)
```

### 2. Proper Mocking

Tests use mocking where needed to avoid external dependencies:

```python
with patch('automation.subprocess.run') as mock_run:
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=1)
    code, stdout, stderr = runner.run_command(["sleep", "1000"])
```

### 3. Isolation

Each test is independent and doesn't rely on state from other tests:

```python
@pytest.fixture
def cleanup_system(self, tmp_path, monkeypatch):
    """Fresh system for each test."""
    # Clean setup for every test
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-mock

      - name: Run integration tests
        run: |
          python3 -m pytest tests/python/test_integration.py -v --cov=scripts --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

## Troubleshooting

### Tests Fail Due to Import Errors

**Problem**: `ImportError: No module named 'error_tracker'`

**Solution**: Ensure scripts are in Python path:

```python
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts"))
```

### Tests Fail with Path Issues

**Problem**: Tests can't find files in expected locations

**Solution**: Check that monkeypatch is correctly applied:

```python
# Verify in test
import error_tracker as et
print(et.ERROR_LOG_DIR)  # Should be temp path
```

### Concurrent Test Failures

**Problem**: Tests interfere with each other when run in parallel

**Solution**: Use unique temp directories per test:

```python
@pytest.fixture
def unique_system(self, tmp_path):
    # tmp_path is unique for each test
    return tmp_path
```

## Performance Benchmarks

Expected test execution times:

| Test Class | Tests | Typical Duration |
|------------|-------|------------------|
| Integration | 3 | ~0.2s |
| Automation | 6 | ~0.3s |
| Lesson Generation | 5 | ~0.3s |
| Plugin | 4 | ~0.1s |
| End-to-End | 4 | ~0.4s |
| Recovery | 4 | ~0.1s |
| **Total** | **26** | **~1.5s** |

## Code Coverage

Current coverage for integration tests:

- `error_tracker.py`: ~57%
- `prompt_monitor.py`: ~41%
- `automation.py`: ~43%

**Coverage Goal**: 70%+ for all integration components

## Contributing

When adding new integration tests:

1. **Use fixtures** for setup and teardown
2. **Mock external dependencies** (API calls, file systems)
3. **Test both success and failure paths**
4. **Use temporary directories** to avoid pollution
5. **Document test purpose** in docstring
6. **Keep tests fast** (< 0.5s per test)
7. **Ensure tests are isolated** and can run in any order

### Example Template

```python
class TestMyFeature:
    """Test integration of my new feature."""

    @pytest.fixture
    def my_system(self, tmp_path, monkeypatch):
        """Set up test environment."""
        # Setup code
        return {"component": component}

    def test_feature_integration(self, my_system):
        """Test that my feature integrates correctly.

        Workflow:
        1. Setup initial state
        2. Trigger feature
        3. Verify integration
        4. Check side effects
        """
        # Test implementation
        assert expected_behavior
```

## Related Documentation

- [Error Tracker Documentation](../../scripts/error_tracker.py) - Main error tracking system
- [Prompt Monitor Documentation](../../scripts/prompt_monitor.py) - Command usage monitoring
- [Automation Documentation](../../scripts/automation.py) - Unified automation runner
- [Pytest Plugin](./conftest_error_tracking.py) - Automatic test failure tracking
- [Unit Tests](./test_error_tracker.py) - Unit tests for error tracker
- [Unit Tests](./test_prompt_monitor.py) - Unit tests for prompt monitor

## Support

For issues or questions about integration tests:

1. Check this documentation first
2. Review test output for specific errors
3. Check GitHub Issues for known problems
4. Create a new issue with test output and environment details

## Version History

- **v1.0.0** (2025-12-11): Initial comprehensive integration test suite
  - 26 tests covering all major workflows
  - Full pytest plugin integration
  - Temporary directory isolation
  - Mock-based external dependency handling
