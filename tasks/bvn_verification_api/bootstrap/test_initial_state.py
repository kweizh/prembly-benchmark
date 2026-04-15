import os
import shutil

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_installed():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir("/home/user/prembly_bvn"), "Project directory /home/user/prembly_bvn does not exist."
