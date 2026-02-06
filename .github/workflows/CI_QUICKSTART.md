# CI Quick Start Guide

Get your CI up and running in 5 minutes!

## Prerequisites

Ensure you have:
- Node.js 18+ installed
- Python 3.10+ installed
- Git installed

## Step 1: Install Dependencies (2 minutes)

```bash
# From project root
make install-deps
```

This installs:
- Node.js packages for MCP server
- Python packages (pytest, python-docx, requests)
- Bats (shell test framework)

## Step 2: Run Tests Locally (1 minute)

```bash
# Run all tests
make test

# Or run individual test suites
make test-mcp      # MCP server tests
make test-python   # Python tests
make test-shell    # Shell tests
```

## Step 3: Commit and Push (1 minute)

```bash
git add .
git commit -m "Add CI workflow"
git push
```

## Step 4: Check GitHub Actions (1 minute)

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see your workflow running!

## That's It!

Your CI is now running automatically on every:
- Push to main/master/develop
- Pull request to main/master/develop

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make test` | Run all tests |
| `make ci` | Simulate full CI locally |
| `make lint` | Run linting checks |
| `make clean` | Clean build artifacts |
| `make install-deps` | Install all dependencies |

## Troubleshooting

### Tests fail locally?

```bash
# Make sure all scripts are executable
chmod +x .claude/scripts/*.sh
chmod +x content-briefs-skill/scripts/*.sh

# Clean and reinstall
make clean
make install-deps
```

### CI fails but tests pass locally?

1. Check Node.js/Python versions match CI (see `.github/workflows/test.yml`)
2. Ensure all dependencies are listed in `package.json` / `requirements.txt`
3. Run `make ci` to simulate CI locally

### Need help?

- Check `CI_SETUP.md` for detailed documentation
- Check `tests/README.md` for test-specific help
- Look at workflow logs in GitHub Actions tab

## Next Steps

- Add status badges to your README.md
- Configure code coverage reporting
- Add more tests for your features
- Set up branch protection rules requiring CI to pass

See `CI_SETUP.md` for comprehensive documentation.
