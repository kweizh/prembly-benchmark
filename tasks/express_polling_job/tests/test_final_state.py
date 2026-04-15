import os
import subprocess
import time
import socket
import pytest
import json

APP_DIR = "/home/user/app"
MOCK_SERVER_DIR = "/home/user/mock_server"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def run_apps():
    # Start mock server
    mock_process = subprocess.Popen(
        ["node", "index.js"],
        cwd=MOCK_SERVER_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(8080):
        import signal
        os.killpg(os.getpgid(mock_process.pid), signal.SIGTERM)
        pytest.fail("Mock server failed to start on port 8080.")

    # Start user app
    app_process = subprocess.Popen(
        ["node", "index.js"],
        cwd=APP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(app_process.pid), signal.SIGTERM)
        os.killpg(os.getpgid(mock_process.pid), signal.SIGTERM)
        pytest.fail("User app failed to start on port 3000.")

    # Wait for the polling job to run a few times (2s interval, need at least 3 requests)
    time.sleep(10)

    yield

    # Shut down processes
    import signal
    os.killpg(os.getpgid(app_process.pid), signal.SIGTERM)
    os.killpg(os.getpgid(mock_process.pid), signal.SIGTERM)
    app_process.wait(timeout=10)
    mock_process.wait(timeout=10)

def test_results_file_exists(run_apps):
    results_path = os.path.join(APP_DIR, "results.json")
    assert os.path.isfile(results_path), f"results.json not found at {results_path}"

def test_results_contain_verification_data(run_apps):
    results_path = os.path.join(APP_DIR, "results.json")
    with open(results_path, 'r') as f:
        content = f.read()
    
    # We expect the mock server's verification_data to be present
    assert "John Doe" in content, f"Expected verification data to be written to results.json. Content found: {content}"
    assert "verified" in content, f"Expected verification status to be written to results.json. Content found: {content}"
