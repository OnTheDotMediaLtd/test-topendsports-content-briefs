"""
Basic tests for Python scripts
"""
import os
import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def test_ahrefs_script_exists():
    """Test that ahrefs-api.py script exists"""
    script_path = project_root / ".claude" / "scripts" / "ahrefs-api.py"
    assert script_path.exists(), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"


def test_validate_phase_script_exists():
    """Test that validate-phase.sh script exists"""
    script_path = project_root / "content-briefs-skill" / "scripts" / "validate-phase.sh"
    assert script_path.exists(), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"


def test_convert_to_docx_script_exists():
    """Test that convert_to_docx.py script exists"""
    script_path = project_root / "content-briefs-skill" / "scripts" / "convert_to_docx.py"
    assert script_path.exists(), f"Script not found: {script_path}"


def test_python_syntax():
    """Test that all Python scripts have valid syntax"""
    import py_compile

    scripts = [
        project_root / ".claude" / "scripts" / "ahrefs-api.py",
        project_root / "content-briefs-skill" / "scripts" / "convert_to_docx.py",
        project_root / "content-briefs-skill" / "scripts" / "ingest-feedback.py",
    ]

    for script in scripts:
        if script.exists():
            try:
                py_compile.compile(str(script), doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"Syntax error in {script}: {e}")


def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    requirements_path = project_root / "requirements.txt"
    assert requirements_path.exists(), "requirements.txt not found"


def test_mcp_server_exists():
    """Test that MCP server directory and files exist"""
    mcp_dir = project_root / "mcp-server"
    assert mcp_dir.exists(), "mcp-server directory not found"

    package_json = mcp_dir / "package.json"
    assert package_json.exists(), "package.json not found in mcp-server"

    src_dir = mcp_dir / "src"
    assert src_dir.exists(), "src directory not found in mcp-server"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
