# Python Tests for TopEndSports Content Briefs

This directory contains pytest-based tests for the Python scripts in the project.

## Test Structure

```
tests/python/
├── conftest.py              # Shared fixtures for all tests
├── test_convert_docx.py     # Tests for markdown to DOCX conversion
├── test_ahrefs_api.py       # Tests for Ahrefs API wrapper
├── test_validate_feedback.py # Tests for feedback validation
├── fixtures/                 # Sample test files
│   ├── sample.md            # Sample markdown for conversion tests
│   ├── sample-feedback.md   # Complete feedback file
│   └── incomplete-feedback.md # Incomplete feedback for error testing
└── README.md                # This file
```

## Scripts Under Test

1. **content-briefs-skill/scripts/convert_to_docx.py**
   - Markdown to DOCX conversion
   - Handles headings, lists, code blocks, tables
   - Test coverage: heading parsing, list parsing, table parsing, error handling

2. **.claude/scripts/ahrefs-api.py**
   - Ahrefs API wrapper with caching and retry logic
   - Test coverage: cache operations, parameter validation, API mocking, retry logic

3. **content-briefs-skill/scripts/validate_feedback.py**
   - Feedback file validation
   - Test coverage: required fields, placeholders, warnings, edge cases

## Installation

Install test dependencies:

```bash
# Using pip
pip install -e ".[dev]"

# Or install pytest directly
pip install pytest pytest-mock pytest-cov pytest-timeout
```

## Running Tests

### Run all tests:
```bash
pytest tests/python/
```

### Run with verbose output:
```bash
pytest tests/python/ -v
```

### Run specific test file:
```bash
pytest tests/python/test_convert_docx.py
pytest tests/python/test_ahrefs_api.py
pytest tests/python/test_validate_feedback.py
```

### Run specific test class or function:
```bash
# Run specific class
pytest tests/python/test_convert_docx.py::TestParseMarkdownToDocx

# Run specific test
pytest tests/python/test_convert_docx.py::TestParseMarkdownToDocx::test_parse_simple_heading_h1
```

### Run with coverage report:
```bash
pytest tests/python/ --cov --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view detailed coverage.

### Run only fast tests (skip slow tests):
```bash
pytest tests/python/ -m "not slow"
```

### Run with output from print statements:
```bash
pytest tests/python/ -s
```

## Test Markers

Tests are marked with the following markers:

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (may be slower)
- `@pytest.mark.slow` - Slow-running tests

Use markers to run specific test categories:
```bash
pytest tests/python/ -m unit
pytest tests/python/ -m integration
```

## Writing New Tests

### Use Shared Fixtures

Fixtures are defined in `conftest.py`. Common fixtures include:

- `temp_dir` - Temporary directory for test files
- `sample_markdown` - Sample markdown content
- `sample_feedback` - Complete feedback file content
- `incomplete_feedback` - Incomplete feedback for testing validation
- `ahrefs_mock_response` - Mock Ahrefs API response

Example:
```python
def test_my_function(temp_dir, sample_markdown):
    """Test description."""
    # Use the fixtures
    file_path = temp_dir / "test.md"
    file_path.write_text(sample_markdown)
    # ... rest of test
```

### Mocking External Dependencies

Use `unittest.mock` or `pytest-mock` to mock external calls:

```python
from unittest.mock import patch

@patch('module.external_function')
def test_with_mock(mock_function):
    """Test with mocked external dependency."""
    mock_function.return_value = "mocked value"
    # ... rest of test
```

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use descriptive names that explain what is being tested

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_something():
    """Test description."""
    # Arrange - set up test data
    input_data = "test input"

    # Act - call the function being tested
    result = function_under_test(input_data)

    # Assert - verify the results
    assert result == expected_output
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. The configuration in `pyproject.toml` ensures:

- Tests timeout after 30 seconds
- Coverage reports are generated
- Warnings are filtered appropriately

## Troubleshooting

### Import Errors

If you get import errors, ensure the scripts directory is in the Python path:
```python
import sys
from pathlib import Path
SCRIPT_DIR = Path(__file__).parent.parent.parent / "content-briefs-skill" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
```

### Path Issues

Tests use temporary directories to avoid conflicts. Always use the `temp_dir` fixture for test files.

### Mock Not Working

Ensure you're mocking at the right level. Mock where the function is used, not where it's defined:
```python
# If module A imports function from module B
# Mock it in module A's namespace
@patch('module_a.function_from_b')
```

## Code Coverage Goals

Target coverage levels:
- Overall: 80%+
- Critical functions: 90%+
- Edge cases: 100%

View current coverage:
```bash
pytest tests/python/ --cov --cov-report=term-missing
```

## Adding New Test Files

1. Create test file: `test_new_module.py`
2. Add imports and path setup
3. Create test classes for logical grouping
4. Write test functions with docstrings
5. Add fixtures to `conftest.py` if reusable
6. Run tests to ensure they pass

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Mock Documentation](https://pytest-mock.readthedocs.io/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
