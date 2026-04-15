import os
import shutil
import subprocess
import pytest

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir("/home/user/onboarding"), "Project directory /home/user/onboarding does not exist."
