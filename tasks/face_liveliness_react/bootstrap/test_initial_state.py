import os
import shutil
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}"

def test_src_dir_exists():
    src_dir = os.path.join(PROJECT_DIR, "src")
    assert os.path.isdir(src_dir), f"src directory not found at {src_dir}"

def test_node_modules_installed():
    node_modules_dir = os.path.join(PROJECT_DIR, "node_modules")
    assert os.path.isdir(node_modules_dir), f"node_modules not found at {node_modules_dir}"
