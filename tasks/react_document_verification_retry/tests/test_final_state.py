import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/prembly-app"

def test_app_jsx_logic():
    app_jsx = os.path.join(PROJECT_DIR, "src", "App.jsx")
    assert os.path.isfile(app_jsx), f"{app_jsx} does not exist."
    
    with open(app_jsx, "r") as f:
        content = f.read()
        
    assert "PremblyPass" in content, "PremblyPass should be imported and used."
    assert "Maximum retries reached" in content, "Should contain the maximum retries reached message."
    assert "Verification successful" in content, "Should contain the success message."
    assert "disabled" in content.lower(), "Should contain logic to disable the button."
    
    # Check if a counter or retry logic is present (looking for common state variables)
    assert "useState" in content, "Should use React state for the retry counter."