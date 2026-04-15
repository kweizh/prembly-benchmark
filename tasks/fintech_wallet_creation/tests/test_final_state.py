import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/project"

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Express server failed to start on port 3000.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

def test_api_endpoint(start_app):
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:3000/api/verify-nin", 
         "-H", "Content-Type: application/json", 
         "-d", '{"nin": "11111111111"}'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl request failed: {result.stderr}"
    assert result.stdout.strip() != "", "Expected a non-empty response from the server."

def test_code_contains_required_elements():
    index_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index_path), f"index.js not found at {index_path}"
    
    with open(index_path) as f:
        content = f.read()
    
    assert "https://sandbox.myidentitypay.com/verification/nin" in content, "Expected Prembly sandbox URL in index.js."
    assert "test_app_id" in content, "Expected 'test_app_id' in index.js."
    assert "test_api_key" in content, "Expected 'test_api_key' in index.js."
