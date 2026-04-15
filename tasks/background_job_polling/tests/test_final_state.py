import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")

@pytest.fixture(scope="module", autouse=True)
def run_polling_script():
    # Install dependencies if package.json exists
    if os.path.exists(os.path.join(PROJECT_DIR, "package.json")):
        subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=False)
    
    # Run the script
    result = subprocess.run(
        ["node", "poll.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"
    yield

def test_log_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(LOG_FILE), f"Log file not found at {LOG_FILE}"

def test_log_file_format():
    """Priority 3 fallback: check log file contents format."""
    with open(LOG_FILE, "r") as f:
        content = f.read().strip()
    
    assert "Total sessions: " in content, f"Expected 'Total sessions: ' in log file, got: {content}"
    
    # Extract the part after "Total sessions: " to verify it's a number
    parts = content.split("Total sessions: ")
    assert len(parts) >= 2, "Failed to parse log file format"
    
    count_str = parts[1].strip()
    assert count_str.isdigit(), f"Expected a number after 'Total sessions: ', got: {count_str}"
