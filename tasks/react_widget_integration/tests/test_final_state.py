import os
import json
import subprocess
import time
import pytest

PROJECT_DIR = "/home/user/prembly-app"

def test_project_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), "package.json not found."
    with open(pkg_path) as f:
        pkg = json.load(f)
    deps = pkg.get("dependencies", {})
    assert "prembly-pass" in deps, "prembly-pass is not in package.json dependencies."

def test_prembly_widget_source():
    widget_path = os.path.join(PROJECT_DIR, "src", "PremblyWidget.jsx")
    if not os.path.isfile(widget_path):
        widget_path = os.path.join(PROJECT_DIR, "src", "PremblyWidget.tsx")
    assert os.path.isfile(widget_path), "PremblyWidget component file not found."
    
    with open(widget_path) as f:
        content = f.read()
    
    # Check for imports and initialization
    assert "PremblyPass" in content, "PremblyPass is not imported or used."
    assert "app_id" in content and "test_app_id" in content, "test_app_id not found in initialization."
    assert "x_api_key" in content and "test_public_key" in content, "test_public_key not found in initialization."
    assert "environment" in content and "test" in content, "environment: 'test' not found in initialization."
    
    # Check for event listeners
    assert "success" in content, "success event listener not found."
    assert "error" in content, "error event listener not found."
    
    # Check for launch
    assert "launch" in content, "launch() method not called."
    assert "config_id" in content and "test_config_id" in content, "test_config_id not found in launch."
    assert "user_ref" in content and "user_123" in content, "user_123 not found in launch."

def test_browser_verification():
    # Start the server
    p = subprocess.Popen(["npm", "run", "dev"], cwd=PROJECT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # wait for vite to start
    
    try:
        # Use agent-browser to check the page
        subprocess.run(["agent-browser", "open", "http://localhost:5173"], check=True)
        result = subprocess.run(["agent-browser", "eval", "document.body.innerText"], capture_output=True, text=True, check=True)
        assert "Verify Identity" in result.stdout, "Button with 'Verify Identity' not found on the page."
    finally:
        p.terminate()
