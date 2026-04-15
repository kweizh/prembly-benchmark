import os
import shutil
import pytest

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_mock_server_dir_exists():
    assert os.path.isdir("/home/user/mock_server"), "Mock server directory not found."

def test_app_dir_exists():
    assert os.path.isdir("/home/user/app"), "App directory not found."