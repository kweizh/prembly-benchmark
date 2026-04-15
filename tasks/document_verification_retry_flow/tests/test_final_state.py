import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/app"

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
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)

    # Start the app
    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "3000"],
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
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_document_verification_retry_flow(start_app):
    reason = "The application should allow exactly 3 attempts for document verification before disabling the button and showing an error message."
    truth = "Navigate to http://localhost:3000. Verify that 'Attempts remaining: 3' is visible. Click the 'Start Verification' button to launch the widget. Simulate an error event 3 times (or let the widget fail 3 times). Verify that the 'Start Verification' button is disabled and 'Maximum retries exceeded. Please contact support.' is displayed."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_document_verification_retry_flow"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
