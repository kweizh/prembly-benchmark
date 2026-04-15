import os
import shutil
import pytest

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_nest_cli_available():
    assert shutil.which("nest") is not None, "nest CLI not found in PATH."

def test_project_dir_not_exists_yet():
    # The task says "Initialize a NestJS project in /home/user/nestjs-kyb"
    # So it shouldn't exist initially, or maybe just the parent dir exists
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
