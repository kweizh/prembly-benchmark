import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_public_index_html_exists():
    html_path = os.path.join(PROJECT_DIR, "public", "index.html")
    assert os.path.isfile(html_path), f"Frontend HTML file {html_path} does not exist."
