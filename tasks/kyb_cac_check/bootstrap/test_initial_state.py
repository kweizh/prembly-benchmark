import os
import shutil
import pytest

PROJECT_DIR = "/home/user/project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"File {package_json_path} does not exist."

def test_mock_server_exists():
    mock_server_path = "/home/user/mock_server.js"
    assert os.path.isfile(mock_server_path), f"File {mock_server_path} does not exist."

def test_node_installed():
    assert shutil.which("node") is not None, "Node.js is not installed."
