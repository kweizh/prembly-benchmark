import os
import shutil
import pytest

PROJECT_DIR = "/home/user/prembly-app"

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}."

def test_mock_server_exists():
    mock_server_path = "/home/user/mock-server.js"
    assert os.path.isfile(mock_server_path), f"Mock server file not found at {mock_server_path}."
