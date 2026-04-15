import os
import shutil
import subprocess
import pytest

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_nestjs_cli_available():
    assert shutil.which("nest") is not None, "nest CLI binary not found in PATH."
