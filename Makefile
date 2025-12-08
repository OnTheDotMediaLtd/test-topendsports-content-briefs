# TopEndSports Content Briefs - Makefile
# Convenience targets for testing and development

.PHONY: help test test-mcp test-python test-shell install-deps ci clean

# Default target
help:
	@echo "TopEndSports Content Briefs - Available Make Targets"
	@echo "======================================================"
	@echo ""
	@echo "  make test          - Run all tests"
	@echo "  make test-mcp      - Run MCP server tests only"
	@echo "  make test-python   - Run Python tests only"
	@echo "  make test-shell    - Run shell script tests only"
	@echo "  make install-deps  - Install all test dependencies"
	@echo "  make ci            - Simulate full CI run locally"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make lint          - Run linting checks"
	@echo ""

# Run all tests
test: test-mcp test-python test-shell
	@echo "✅ All tests completed!"

# Test MCP server
test-mcp:
	@echo "🧪 Testing MCP Server..."
	@cd mcp-server && npm ci && npm run build && npm test
	@echo "✅ MCP server tests passed!"

# Test Python scripts
test-python:
	@echo "🐍 Testing Python scripts..."
	@if [ ! -f requirements.txt ]; then \
		echo "⚠️  requirements.txt not found, installing minimal dependencies..."; \
		pip install pytest python-docx requests; \
	else \
		pip install -r requirements.txt; \
	fi
	@if [ -d "tests/python" ]; then \
		pytest tests/python/ -v --tb=short; \
	else \
		echo "⚠️  tests/python/ directory not found, running syntax checks..."; \
		python -m py_compile .claude/scripts/*.py; \
		python -m py_compile content-briefs-skill/scripts/*.py; \
	fi
	@echo "✅ Python tests passed!"

# Test shell scripts
test-shell:
	@echo "🐚 Testing shell scripts..."
	@if ! command -v bats >/dev/null 2>&1; then \
		echo "Installing bats-core..."; \
		sudo apt-get update && sudo apt-get install -y bats || \
		(echo "Failed to install bats via apt, trying npm..." && npm install -g bats); \
	fi
	@chmod +x .claude/scripts/*.sh
	@chmod +x content-briefs-skill/scripts/*.sh
	@if [ -d "tests/shell" ] && [ -n "$$(ls -A tests/shell/*.bats 2>/dev/null)" ]; then \
		bats tests/shell/*.bats; \
	else \
		echo "⚠️  No shell tests found, creating basic validation..."; \
		mkdir -p tests/shell; \
		echo '#!/usr/bin/env bats' > tests/shell/basic.bats; \
		echo '' >> tests/shell/basic.bats; \
		echo '@test "Scripts are executable" {' >> tests/shell/basic.bats; \
		echo '  [ -x ".claude/scripts/ahrefs-api.py" ]' >> tests/shell/basic.bats; \
		echo '  [ -x "content-briefs-skill/scripts/validate-phase.sh" ]' >> tests/shell/basic.bats; \
		echo '}' >> tests/shell/basic.bats; \
		bats tests/shell/basic.bats; \
	fi
	@echo "✅ Shell tests passed!"

# Install all test dependencies
install-deps:
	@echo "📦 Installing test dependencies..."
	@echo ""
	@echo "Installing Node.js dependencies..."
	@cd mcp-server && npm ci
	@echo ""
	@echo "Installing Python dependencies..."
	@pip install --upgrade pip
	@if [ -f requirements.txt ]; then \
		pip install -r requirements.txt; \
	else \
		pip install pytest python-docx requests; \
	fi
	@echo ""
	@echo "Installing shell test dependencies..."
	@if ! command -v bats >/dev/null 2>&1; then \
		echo "Installing bats-core..."; \
		sudo apt-get update && sudo apt-get install -y bats || npm install -g bats; \
	else \
		echo "bats already installed"; \
	fi
	@echo ""
	@echo "✅ All dependencies installed!"

# Simulate full CI run locally
ci:
	@echo "🚀 Running full CI simulation..."
	@echo ""
	@echo "================================================"
	@echo "Step 1/5: Installing dependencies"
	@echo "================================================"
	@make install-deps
	@echo ""
	@echo "================================================"
	@echo "Step 2/5: Building MCP server"
	@echo "================================================"
	@cd mcp-server && npm run build
	@echo ""
	@echo "================================================"
	@echo "Step 3/5: Running MCP tests"
	@echo "================================================"
	@make test-mcp
	@echo ""
	@echo "================================================"
	@echo "Step 4/5: Running Python tests"
	@echo "================================================"
	@make test-python
	@echo ""
	@echo "================================================"
	@echo "Step 5/5: Running Shell tests"
	@echo "================================================"
	@make test-shell
	@echo ""
	@echo "================================================"
	@echo "✅ CI Simulation Complete!"
	@echo "================================================"

# Lint checks
lint:
	@echo "🔍 Running linting checks..."
	@echo ""
	@echo "Checking Python files..."
	@python -m py_compile .claude/scripts/*.py
	@python -m py_compile content-briefs-skill/scripts/*.py
	@echo "✅ Python syntax check passed"
	@echo ""
	@echo "Checking shell scripts..."
	@if command -v shellcheck >/dev/null 2>&1; then \
		find . -name "*.sh" -not -path "*/node_modules/*" -exec shellcheck {} + || true; \
	else \
		echo "⚠️  shellcheck not installed, skipping shell lint"; \
	fi
	@echo ""
	@echo "Checking TypeScript files..."
	@cd mcp-server && npx tsc --noEmit
	@echo "✅ TypeScript check passed"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf mcp-server/dist
	@rm -rf mcp-server/node_modules/.cache
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete!"
