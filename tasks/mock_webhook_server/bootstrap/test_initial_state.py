import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/prembly-webhook"

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_working_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Working directory {PROJECT_DIR} does not exist."
