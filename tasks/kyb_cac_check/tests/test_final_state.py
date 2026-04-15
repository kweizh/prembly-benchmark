import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/project"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the mock server
    mock_process = subprocess.Popen(
        ["node", "/home/user/mock_server.js"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(8080):
        import signal
        os.killpg(os.getpgid(mock_process.pid), signal.SIGTERM)
        pytest.fail("Mock server failed to start on port 8080.")

    # Start the app
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        os.killpg(os.getpgid(mock_process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")

    yield

    # Shut down the app and mock server
    import signal
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except Exception:
        pass
    try:
        os.killpg(os.getpgid(mock_process.pid), signal.SIGTERM)
    except Exception:
        pass
    
    try:
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        pass
    try:
        mock_process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        pass

def test_cac_verification(start_app):
    reason = "The application should feature a form to input an RC number and verify it against the Prembly API."
    truth = "Navigate to http://localhost:3000. Verify that an input field with id 'rc-input' and a select dropdown with id 'type-select' are visible. Type '092932' into the input field and select 'RC'. Click the button with id 'verify-btn'. Verify that the company name 'TEST COMPANY' appears in the element with id 'result-name', and the status 'Active' appears in the element with id 'result-status'."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_cac_verification"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
