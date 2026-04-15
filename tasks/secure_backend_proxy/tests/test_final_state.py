import os
import subprocess
import time
import socket
import json
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
    # Start the app
    env = os.environ.copy()
    env["PREMBLY_APP_ID"] = "test_app_id"
    env["PREMBLY_SECRET_KEY"] = "test_secret_key"
    
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
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

def test_static_html_served(start_app):
    """Priority 1: Test that the static HTML is served correctly."""
    result = subprocess.run(
        ["curl", "-s", "http://localhost:3000/"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to fetch HTML: {result.stderr}"
    assert "Prembly Verification" in result.stdout, "Expected HTML title 'Prembly Verification' not found in response."

def test_proxy_endpoint(start_app):
    """Priority 1: Test the POST /api/verify/nin endpoint."""
    payload = json.dumps({"ninNumber": "12345678901"})
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:3000/api/verify/nin",
         "-H", "Content-Type: application/json", "-d", payload],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to call proxy endpoint: {result.stderr}"
    # Even with dummy credentials, it should return a JSON response (likely an error from Prembly)
    try:
        response_json = json.loads(result.stdout)
        # We expect it to successfully parse as JSON, meaning it successfully proxied the response.
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response from proxy endpoint, got: {result.stdout}")

def test_browser_verification(start_app):
    """Priority 2: Browser verification to ensure the button click makes the API call."""
    reason = "The frontend should be able to click the verify button and receive a response."
    truth = "Navigate to http://localhost:3000/. Click the 'Verify' button. The console should log an object (likely containing an error from Prembly due to dummy credentials)."
    
    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_verification"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
