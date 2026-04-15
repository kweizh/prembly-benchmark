import os
import shutil
import subprocess
import pytest

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_vue_project_exists():
    assert os.path.isdir("/home/user/vue-prembly-app"), "Vue project directory does not exist."
    assert os.path.isfile("/home/user/vue-prembly-app/package.json"), "package.json not found in the Vue project."
