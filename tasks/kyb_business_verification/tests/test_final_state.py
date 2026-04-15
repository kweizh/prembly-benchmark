import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def test_script_execution():
    """Priority 1: Run the script and verify output."""
    env = os.environ.copy()
    if "PREMBLY_APP_ID" not in env:
        env["PREMBLY_APP_ID"] = "dummy_app_id"
    if "PREMBLY_API_KEY" not in env:
        env["PREMBLY_API_KEY"] = "dummy_api_key"

    result = subprocess.run(
        ["node", "verify_business.js", "1234567"],
        capture_output=True, text=True, cwd=PROJECT_DIR, env=env
    )
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"

def test_output_file_exists():
    """Priority 3: Check if output file was created."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

def test_output_file_contains_json():
    """Priority 3: Check if output is valid JSON."""
    with open(OUTPUT_FILE, "r") as f:
        content = f.read()
    
    try:
        data = json.loads(content)
        assert isinstance(data, dict), "Output JSON should be an object."
    except json.JSONDecodeError:
        pytest.fail(f"Output file does not contain valid JSON: {content}")
