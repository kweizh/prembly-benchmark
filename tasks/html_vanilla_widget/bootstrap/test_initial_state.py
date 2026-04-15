import os
import pytest

PROJECT_DIR = "/home/user/prembly-widget"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
