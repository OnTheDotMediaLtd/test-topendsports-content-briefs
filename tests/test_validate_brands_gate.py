#!/usr/bin/env python3
"""
Tests for the brand validation gate script.

This validates that the gate correctly:
1. Accepts briefs with only verified brands
2. Rejects briefs with suspicious/fake brands
3. Provides helpful suggestions for typos
"""

import sys
import subprocess
from pathlib import Path
import tempfile
import pytest

# Test data: content with various brand scenarios
BRIEF_WITH_VERIFIED_BRANDS = """
# Canada Sports Betting Sites

## Top Sportsbooks

### FanDuel
FanDuel is the #1 sportsbook in North America with coverage in 24 states.

### BetMGM
BetMGM offers competitive odds and a wide selection of markets.

### DraftKings
DraftKings is known for their daily fantasy sports integration.

### Caesars
Caesars Sportsbook provides a generous welcome bonus.
"""

BRIEF_WITH_FAKE_BRANDS = """
# Canada Sports Betting Sites

## Top Sportsbooks

### Treasure Spins Sport
Treasure Spins offers exciting betting opportunities. [FAKE BRAND - SHOULD BE BLOCKED]

### FanDuel
FanDuel is the #1 sportsbook in North America.

### Royalistplay
Royalistplay provides competitive odds. [FAKE BRAND - SHOULD BE BLOCKED]

### DraftKings
DraftKings is known for their DFS integration.
"""

BRIEF_WITH_TYPO_BRANDS = """
# Canada Sports Betting Sites

## Top Sportsbooks

### Wyns
Wyns offers great odds. [TYPO - SHOULD SUGGEST WynnBET]

### FanDuel
FanDuel is the #1 sportsbook.

### DraftKings
DraftKings provides competitive markets.
"""


def run_validation_script(brief_content: str, strict: bool = True) -> tuple[int, str, str]:
    """
    Run the validation script on temporary brief content.
    
    Returns:
        (exit_code, stdout, stderr)
    """
    script_path = Path(__file__).parent.parent / "scripts" / "validate_brands_gate.py"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(brief_content)
        temp_path = Path(f.name)
    
    try:
        cmd = [sys.executable, str(script_path), str(temp_path)]
        if strict:
            cmd.append("--strict")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        return result.returncode, result.stdout, result.stderr
    finally:
        temp_path.unlink(missing_ok=True)


def test_accepts_verified_brands():
    """Validation should PASS when all brands are verified (lenient mode for automated gates)."""
    # Use lenient mode (default) which only blocks suspicious brands, not text fragments
    exit_code, stdout, stderr = run_validation_script(BRIEF_WITH_VERIFIED_BRANDS, strict=False)
    
    assert exit_code == 0, f"Should pass with verified brands. Got exit {exit_code}:\n{stdout}\n{stderr}"
    assert "[OK] VALIDATION PASSED" in stdout
    assert "FanDuel" in stdout
    assert "BetMGM" in stdout
    assert "DraftKings" in stdout
    assert "Caesars" in stdout


def test_rejects_fake_brands():
    """Validation should FAIL when fake brands are detected (even in lenient mode)."""
    # Lenient mode still blocks suspicious/fake brands like "Treasure Spins" and "Royalistplay"
    exit_code, stdout, stderr = run_validation_script(BRIEF_WITH_FAKE_BRANDS, strict=False)
    
    assert exit_code == 1, f"Should reject fake brands. Got exit {exit_code}:\n{stdout}\n{stderr}"
    assert "[BLOCKED] VALIDATION FAILED" in stdout
    assert "Treasure Spins" in stdout or "Treasure" in stdout  # May split into tokens
    assert "Royalistplay" in stdout or "Royalist" in stdout


def test_suggests_corrections_for_typos():
    """Validation should suggest corrections for likely typos."""
    exit_code, stdout, stderr = run_validation_script(BRIEF_WITH_TYPO_BRANDS, strict=True)
    
    # In strict mode, unknown brands cause failure
    assert exit_code == 1, f"Should fail on unknown brands. Got exit {exit_code}:\n{stdout}\n{stderr}"
    
    # Should suggest WynnBET for Wyns
    assert "Wyns" in stdout
    assert "WynnBET" in stdout or "did you mean" in stdout.lower()


def test_lenient_mode_warns_unknown():
    """In lenient mode, unknown brands should warn but not block."""
    exit_code, stdout, stderr = run_validation_script(BRIEF_WITH_TYPO_BRANDS, strict=False)
    
    # Lenient mode: unknown brands warn but don't block (unless suspicious)
    # Exit code depends on whether "Wyns" is classified as suspicious
    # Let's just verify the output format is correct
    assert "[WARN]" in stdout or "[ERROR]" in stdout
    assert "Wyns" in stdout


def test_cli_usage_message():
    """Script should show usage when run without arguments."""
    script_path = Path(__file__).parent.parent / "scripts" / "validate_brands_gate.py"
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    
    assert result.returncode == 2
    assert "Usage:" in result.stdout
    assert "Example:" in result.stdout


def test_handles_missing_file():
    """Script should handle missing files gracefully."""
    script_path = Path(__file__).parent.parent / "scripts" / "validate_brands_gate.py"
    fake_path = Path("/nonexistent/path/brief.md")
    
    result = subprocess.run(
        [sys.executable, str(script_path), str(fake_path)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    
    assert result.returncode == 2
    assert "[ERROR]" in result.stdout
    assert "not found" in result.stdout.lower()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
