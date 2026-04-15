import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/prembly-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"File {package_json_path} does not exist."

def test_app_jsx_exists():
    app_jsx_path = os.path.join(PROJECT_DIR, "src", "App.jsx")
    assert os.path.isfile(app_jsx_path), f"File {app_jsx_path} does not exist."

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_installed():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."
