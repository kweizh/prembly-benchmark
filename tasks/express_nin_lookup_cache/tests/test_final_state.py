import os
import subprocess
import time
import socket
import json
import pytest

PROJECT_DIR = "/home/user/nin-cache"
PORT = 3000

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
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(PORT):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_api_verify_nin(start_app):
    """Test that the /api/verify-nin endpoint works and caches the result."""
    import urllib.request
    import urllib.error

    url = f"http://localhost:{PORT}/api/verify-nin"
    data = json.dumps({"nin": "11111111111"}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    # First request
    req1 = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req1) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            res1_data = json.loads(response.read().decode())
    except urllib.error.URLError as e:
        pytest.fail(f"First request failed: {e}")

    # Second request (should be cached)
    req2 = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req2) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            res2_data = json.loads(response.read().decode())
    except urllib.error.URLError as e:
        pytest.fail(f"Second request failed: {e}")

    assert res1_data == res2_data, "Expected second request to return identical data from cache."
    # We could also verify that it contains expected structure from Prembly API
    # But since it's a sandbox, we just ensure it didn't crash and returned JSON
