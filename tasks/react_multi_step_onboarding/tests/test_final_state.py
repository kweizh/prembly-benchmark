import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/onboarding-app"

def test_project_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_contains_prembly():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), "package.json not found."
    with open(package_json_path) as f:
        content = f.read()
    assert "prembly-pass" in content, "prembly-pass is not installed in package.json."

def test_source_code_contains_prembly_usage():
    # Recursively check for PremblyPass usage in src or pages directory
    found = False
    for root, _, files in os.walk(PROJECT_DIR):
        if "node_modules" in root:
            continue
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                with open(os.path.join(root, file)) as f:
                    content = f.read()
                if "PremblyPass" in content or "prembly-pass" in content:
                    found = True
                    break
        if found:
            break
    assert found, "PremblyPass usage not found in source code."

def test_source_code_contains_mock_credentials():
    found = False
    for root, _, files in os.walk(PROJECT_DIR):
        if "node_modules" in root:
            continue
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                with open(os.path.join(root, file)) as f:
                    content = f.read()
                if "MOCK_APP_ID" in content and "MOCK_PUBLIC_KEY" in content:
                    found = True
                    break
        if found:
            break
    assert found, "Mock credentials (MOCK_APP_ID, MOCK_PUBLIC_KEY) not found in source code."
