#!/usr/bin/env bats
# Basic tests for shell scripts

setup() {
    # Get the project root directory
    PROJECT_ROOT="$BATS_TEST_DIRNAME/../.."
}

@test "ahrefs-api.py exists and is executable" {
    [ -f "$PROJECT_ROOT/.claude/scripts/ahrefs-api.py" ]
    [ -x "$PROJECT_ROOT/.claude/scripts/ahrefs-api.py" ]
}

@test "validate-phase.sh exists and is executable" {
    [ -f "$PROJECT_ROOT/content-briefs-skill/scripts/validate-phase.sh" ]
    [ -x "$PROJECT_ROOT/content-briefs-skill/scripts/validate-phase.sh" ]
}

@test "mcp-ahrefs.sh exists and is executable" {
    [ -f "$PROJECT_ROOT/.claude/scripts/mcp-ahrefs.sh" ]
    [ -x "$PROJECT_ROOT/.claude/scripts/mcp-ahrefs.sh" ]
}

@test "mcp-topendsports.sh exists and is executable" {
    [ -f "$PROJECT_ROOT/.claude/scripts/mcp-topendsports.sh" ]
    [ -x "$PROJECT_ROOT/.claude/scripts/mcp-topendsports.sh" ]
}

@test "Shell scripts have proper shebang" {
    grep -q "#!/bin/bash" "$PROJECT_ROOT/.claude/scripts/mcp-ahrefs.sh"
    grep -q "#!/bin/bash" "$PROJECT_ROOT/.claude/scripts/mcp-topendsports.sh"
}

@test "validate-phase.sh accepts arguments" {
    run "$PROJECT_ROOT/content-briefs-skill/scripts/validate-phase.sh" --help
    # Should exit with 0 or 1 (help message), not crash
    [ "$status" -le 1 ]
}

@test "Python scripts have shebang" {
    grep -q "#!/usr/bin/env python3" "$PROJECT_ROOT/.claude/scripts/ahrefs-api.py"
}

@test "MCP server directory exists" {
    [ -d "$PROJECT_ROOT/mcp-server" ]
    [ -f "$PROJECT_ROOT/mcp-server/package.json" ]
}

@test "Test directory structure exists" {
    [ -d "$PROJECT_ROOT/tests" ]
    [ -d "$PROJECT_ROOT/tests/python" ]
    [ -d "$PROJECT_ROOT/tests/shell" ]
}

@test "Required documentation exists" {
    [ -f "$PROJECT_ROOT/README.md" ]
    [ -f "$PROJECT_ROOT/CLAUDE.md" ]
}
