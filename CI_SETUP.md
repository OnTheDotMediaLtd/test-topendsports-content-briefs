# CI/CD Setup Documentation

This document describes the Continuous Integration (CI) setup for the TopEndSports Content Briefs project.

## Overview

The project uses GitHub Actions for CI/CD with three parallel test pipelines:
1. **MCP Server Tests** - Node.js/TypeScript tests using Vitest
2. **Python Tests** - Python script tests using pytest
3. **Shell Tests** - Bash script tests using bats-core

## GitHub Actions Workflows

### 1. Main CI Workflow (`.github/workflows/test.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches

**Jobs:**

#### test-mcp-server
- Sets up Node.js 18+
- Installs dependencies with npm ci (with caching)
- Builds the TypeScript code
- Runs Vitest tests
- Checks TypeScript compilation

#### test-python
- Sets up Python 3.10+
- Installs dependencies from `requirements.txt` (with caching)
- Runs pytest on `tests/python/`
- Validates Python syntax for all `.py` files

#### test-shell
- Installs bats-core
- Makes scripts executable
- Runs bats tests from `tests/shell/`
- Falls back to basic validation if no tests exist

#### all-tests-passed
- Depends on all three test jobs
- Confirms all tests passed
- Only runs if all previous jobs succeed

### 2. PR Check Workflow (`.github/workflows/pr-check.yml`)

**Triggers:**
- Pull requests only

**Jobs:**

#### pr-info
- Displays PR metadata (branch, author, etc.)
- Lists changed files

#### lint
- Runs syntax checks on JavaScript/TypeScript
- Runs syntax checks on Python
- Runs shellcheck on shell scripts (optional)

#### test
- Runs all tests via Makefile
- Ensures PR doesn't break existing functionality

#### status-check
- Final status check for PR
- Displays summary of all checks

### 3. Existing Workflows

#### markdown-lint.yml
- Lints all Markdown files
- Triggers on changes to `*.md` files

#### python-check.yml
- Validates Python syntax
- Triggers on changes to `*.py` files

## Local Development

### Makefile Targets

The project includes a comprehensive Makefile for local testing:

```bash
# Show available commands
make help

# Run all tests
make test

# Run specific test suites
make test-mcp      # MCP server tests only
make test-python   # Python tests only
make test-shell    # Shell tests only

# Install all test dependencies
make install-deps

# Simulate full CI run locally
make ci

# Run linting checks
make lint

# Clean build artifacts
make clean
```

### Installing Dependencies

```bash
# All dependencies at once
make install-deps

# Or individually:

# Node.js dependencies
cd mcp-server && npm ci

# Python dependencies
pip install -r requirements.txt

# Shell test dependencies
sudo apt-get install bats  # Ubuntu/Debian
# or
npm install -g bats        # Via npm
```

### Running Tests Locally

#### All Tests
```bash
make test
```

#### MCP Server Tests
```bash
cd mcp-server
npm test              # Run once
npm run test:watch    # Watch mode
npm run test:coverage # With coverage
npm run test:ui       # With UI
```

#### Python Tests
```bash
pytest tests/python/ -v              # Verbose output
pytest tests/python/ --tb=short      # Short traceback
pytest tests/python/ -k test_name    # Run specific test
```

#### Shell Tests
```bash
bats tests/shell/*.bats              # All shell tests
bats tests/shell/basic.bats          # Specific file
```

## Test Structure

```
topendsports-content-briefs/
├── .github/
│   └── workflows/
│       ├── test.yml              # Main CI workflow
│       ├── pr-check.yml          # PR-specific checks
│       ├── markdown-lint.yml     # Markdown linting
│       └── python-check.yml      # Python validation
├── mcp-server/
│   ├── src/
│   │   └── __tests__/
│   │       └── basic.test.ts     # Basic MCP tests
│   ├── vitest.config.ts          # Vitest configuration
│   └── package.json              # Contains test scripts
├── tests/
│   ├── python/
│   │   └── test_scripts.py       # Python unit tests
│   ├── shell/
│   │   └── basic.bats            # Shell script tests
│   └── README.md                 # Test documentation
├── Makefile                      # Build automation
├── requirements.txt              # Python dependencies
└── CI_SETUP.md                   # This file
```

## Dependencies

### Node.js (MCP Server)
- Node.js 18+
- TypeScript 5+
- Vitest 2.1+ (test runner)
- @vitest/ui (optional, for test UI)
- @vitest/coverage-v8 (optional, for coverage)

### Python
- Python 3.10+
- pytest 7.4+
- pytest-cov 4.1+ (for coverage)
- python-docx 0.8+
- requests 2.31+

### Shell
- bats-core (bash test framework)
- shellcheck (optional, for linting)

## Caching Strategy

The CI workflows use caching to speed up builds:

1. **NPM Cache**: Caches `node_modules` based on `package-lock.json`
2. **Pip Cache**: Caches Python packages based on `requirements.txt`

This reduces build times significantly for subsequent runs.

## Continuous Improvement

### Adding New Tests

#### MCP Server (TypeScript)
1. Create `*.test.ts` file in `mcp-server/src/` or `mcp-server/src/__tests__/`
2. Import `describe`, `it`, `expect` from vitest
3. Write tests
4. Run with `npm test`

Example:
```typescript
import { describe, it, expect } from 'vitest';

describe('Feature', () => {
  it('should work', () => {
    expect(true).toBe(true);
  });
});
```

#### Python
1. Create `test_*.py` file in `tests/python/`
2. Import pytest
3. Write tests
4. Run with `pytest`

Example:
```python
def test_something():
    assert True
```

#### Shell
1. Create `*.bats` file in `tests/shell/`
2. Use bats syntax
3. Run with `bats`

Example:
```bash
@test "description" {
    [ -f "file.sh" ]
}
```

### Monitoring CI Health

- Check the "Actions" tab on GitHub for workflow runs
- Failed workflows will show which job failed
- Click into failed jobs to see detailed logs
- Use `make ci` locally to reproduce CI issues

### Troubleshooting

#### Tests Pass Locally But Fail in CI

1. Check Node.js/Python versions match
2. Ensure all dependencies are in `package.json` / `requirements.txt`
3. Check for environment-specific issues (paths, permissions, etc.)
4. Run `make ci` to simulate full CI locally

#### Cache Issues

If you suspect cache issues:
1. Clear GitHub Actions cache (Settings → Actions → Caches)
2. Update dependency lock files (`package-lock.json`, `requirements.txt`)
3. Re-run workflow

#### Permission Issues

If scripts aren't executable:
```bash
chmod +x .claude/scripts/*.sh
chmod +x content-briefs-skill/scripts/*.sh
git add -u
git commit -m "Fix script permissions"
```

## Status Badges

Add these to your README.md:

```markdown
![CI Tests](https://github.com/YOUR_USERNAME/topendsports-content-briefs/workflows/CI%20Tests/badge.svg)
![PR Checks](https://github.com/YOUR_USERNAME/topendsports-content-briefs/workflows/PR%20Checks/badge.svg)
```

## Future Enhancements

Potential improvements:
- [ ] Add code coverage reporting (Codecov, Coveralls)
- [ ] Add integration tests for end-to-end brief generation
- [ ] Add performance benchmarks
- [ ] Add security scanning (Snyk, Dependabot)
- [ ] Add automatic PR labeling based on changed files
- [ ] Add deploy workflow for releases
- [ ] Add Docker container tests

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vitest Documentation](https://vitest.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Bats-core Documentation](https://github.com/bats-core/bats-core)
- [Makefile Tutorial](https://makefiletutorial.com/)
