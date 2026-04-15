import os
import shutil
import pytest

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_installed():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_npx_installed():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_home_user_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
