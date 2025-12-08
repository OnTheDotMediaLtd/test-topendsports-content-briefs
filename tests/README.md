# Tests Directory

This directory contains all tests for the TopEndSports Content Briefs project.

## Structure

```
tests/
├── python/          # Python unit tests (pytest)
│   └── test_scripts.py
└── shell/           # Shell script tests (bats)
    └── basic.bats
```

## Running Tests

### All Tests

```bash
make test
```

### Individual Test Suites

```bash
# Python tests only
make test-python

# Shell tests only
make test-shell

# MCP server tests only
make test-mcp
```

### Direct Test Commands

```bash
# Run Python tests with pytest
pytest tests/python/ -v

# Run shell tests with bats
bats tests/shell/*.bats

# Run MCP server tests
cd mcp-server && npm test
```

## Test Requirements

### Python Tests

Requires:
- Python 3.10+
- pytest
- python-docx
- requests

Install with:

```bash
pip install -r requirements.txt
```

### Shell Tests

Requires:
- bats-core

Install with:

```bash
# Ubuntu/Debian
sudo apt-get install bats

# Or via npm
npm install -g bats
```

### MCP Server Tests

Requires:
- Node.js 18+
- npm

Install with:

```bash
cd mcp-server
npm ci
```

## Writing New Tests

### Python Tests

Add test files to `tests/python/` with the naming convention `test_*.py`:

```python
def test_something():
    assert True
```

### Shell Tests

Add bats test files to `tests/shell/` with `.bats` extension:

```bash
@test "description" {
    [ -f "some-file.sh" ]
}
```

### MCP Server Tests

Add test files to `mcp-server/src/__tests__/` with `.test.ts` extension (if using vitest).

## CI/CD

Tests run automatically on:
- Push to main/master/develop branches
- Pull requests to main/master/develop branches

See `.github/workflows/test.yml` for CI configuration.

## Continuous Improvement

As the project grows, add tests for:
- Brief generation logic
- Content validation
- Keyword research functions
- Data transformation utilities
- API integrations
- File operations
