# MANDATORY Testing Rules for All Agents

**CRITICAL: Read and follow these rules for every code change.**

---

## Rule 1: ALWAYS Update Tests When You Change Code

If you modify ANY source file in `scripts/`, you MUST:
1. Run the existing tests FIRST to see what passes
2. Make your code change
3. Run tests again to see what broke
4. Fix ALL broken tests before committing
5. NEVER commit code changes that break existing tests

**Anti-pattern (NEVER DO THIS):**
```
# BAD: Changed source code, committed without running tests
git add scripts/validator.py
git commit -m "refactor: change operators from set to dict"
# Tests now fail because they expect set, not dict
```

**Correct pattern:**
```
# GOOD: Change code, verify tests, fix tests, commit together
python -m pytest tests/ --tb=short -q
# ... make code change ...
python -m pytest tests/ --tb=short -q
# ... fix any broken tests ...
git add scripts/validator.py tests/test_validator.py
git commit -m "refactor: change operators from set to dict (update tests)"
```

---

## Rule 2: Python 3.14 Mock Compatibility

This environment runs **Python 3.14**. The mock library changed behavior.

**NEVER use this pattern:**
```python
# BAD - breaks on Python 3.14
printed_calls = [call[0][0] for call in mock_print.call_args_list]
```

**ALWAYS use this pattern:**
```python
# GOOD - works on Python 3.14
printed_calls = [call.args[0] if call.args else '' for call in mock_print.call_args_list]
```

**For checking if print was called with specific text:**
```python
# GOOD
output = '\n'.join(str(call) for call in mock_print.call_args_list)
assert "expected text" in output
```

---

## Rule 3: Windows Encoding (cp1252)

This runs on Windows where the default encoding is cp1252, not UTF-8.

**NEVER use emoji or Unicode special chars in:**
- Print statements
- Error messages
- Log output
- Test assertions

**Use ASCII alternatives:**
```python
# BAD
print("✅ Test passed")
print("❌ Test failed")

# GOOD
print("[OK] Test passed")
print("[FAIL] Test failed")
```

**For file operations, always specify encoding:**
```python
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
```

---

## Rule 4: Import Everything You Use

Always verify your test files import all needed modules.

**Common missing imports:**
```python
import os          # for os.path, os.utime, os.environ
import sys         # for sys.exit, sys.argv
import json        # for json.dumps, json.loads
import tempfile    # for tempfile.mkdtemp
from pathlib import Path
from unittest.mock import patch, MagicMock, call
```

---

## Rule 5: Match Actual Code API

Before writing or updating tests, ALWAYS read the source file first.

**Check for:**
- Current class names (they may have been renamed)
- Current method signatures (parameters may have changed)
- Current return types (set vs dict, list vs tuple)
- Current exception types
- Current import paths

**Anti-pattern:**
```python
# BAD - importing a class that was renamed
from validate_csv_config_tiered import ValidationResult  # was renamed to ValidationLevel
```

**Correct:**
```python
# GOOD - read the source file first, use current name
from validate_csv_config_tiered import ValidationLevel
```

---

## Rule 6: Skip Tests for Missing Dependencies

If a test requires an optional dependency (like Playwright), add a skip decorator:

```python
import pytest

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

@pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright not installed")
def test_browser_interaction():
    ...
```

---

## Rule 7: Always Push to GitHub

After committing changes to any repo:
```bash
git push origin <branch>
```

NEVER leave commits unpushed. All work must be synced to GitHub.

---

## Rule 8: Test Before AND After

**Before any code change:** `python -m pytest tests/ --tb=short -q`
**After any code change:** `python -m pytest tests/ --tb=short -q`
**Before committing:** `python -m pytest tests/ --tb=short -q`

If tests fail after your change, fix them. If they failed before your change, note which ones and don't make them worse.

---

## Rule 9: Commit Tests Together With Code

When you change source code AND update tests, commit them together in a single commit:

```bash
git add scripts/changed_file.py tests/test_changed_file.py
git commit -m "refactor: description of change (update tests)"
git push origin <branch>
```

---

## Rule 10: Use `;` Not `&&` in Shell Commands

PowerShell does not support `&&`. Use `;` to chain commands:

```bash
# BAD
cd path && python test.py

# GOOD - use full paths
python C:/Users/AndreBorg\clawd\repos-test\REPO\tests\test_file.py

# GOOD - if you must chain
cd path; python test.py
```

---

## Quick Reference: Common Test Failures and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| `TypeError: unsupported operand type(s)` | Source changed data structure | Read source, update test expectations |
| `IndexError: tuple index out of range` on mock | Python 3.14 mock change | Use `call.args[0]` not `call[0][0]` |
| `ImportError: cannot import name 'X'` | Class/function renamed | Read source, use current name |
| `NameError: name 'os' is not defined` | Missing import | Add `import os` to test file |
| `UnicodeDecodeError: 'charmap' codec` | Unicode on Windows | Use ASCII, specify encoding='utf-8' |
| `assert False is True` | Validation logic changed | Read source to understand new behavior |
| `AttributeError: module has no attribute` | Optional dependency missing | Add `@pytest.mark.skipif` |
| `KeyError: 'expected_key'` | Return dict structure changed | Read source, update expected keys |
