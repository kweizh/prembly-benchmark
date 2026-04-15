import os
import subprocess
import time
import socket
import pytest
import urllib.request
import json
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/onboarding"

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
        ["node", "server.js"],
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

def test_api_verify_phone(start_app):
    """Test the backend API endpoint for phone verification."""
    data = json.dumps({"phone": "08012345678"}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:3000/api/verify-phone",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to call API: {e}")

def test_frontend_loads(start_app):
    """Test that the frontend HTML page loads."""
    try:
        with urllib.request.urlopen("http://localhost:3000", timeout=10) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            html = response.read().decode('utf-8')
            assert "form" in html.lower(), "Expected a form on the HTML page"
            assert "prembly" in html.lower() or "identitypass" in html.lower(), "Expected Prembly widget script on the HTML page"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to load frontend: {e}")

def test_browser_verification(start_app):
    """Test browser interaction using PochiVerifier."""
    reason = "The application should display a form for phone number input and load the Prembly widget."
    truth = "Navigate to http://localhost:3000. Verify that the page contains a form for phone number input and can load the Prembly widget."
    
    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_verification"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
