import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_node_and_npm_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"File {package_json_path} does not exist."

def test_express_installed():
    node_modules_express = os.path.join(PROJECT_DIR, "node_modules", "express")
    assert os.path.isdir(node_modules_express), f"Express is not installed in {node_modules_express}."

def test_index_js_exists():
    index_js_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index_js_path), f"File {index_js_path} does not exist."
