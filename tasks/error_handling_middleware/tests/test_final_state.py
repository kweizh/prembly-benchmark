import os
import subprocess
import time
import socket
import json
import pytest
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
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
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_error_handling_middleware(start_app):
    """Test that the Express server correctly intercepts Prembly API errors and formats them using the global error handling middleware."""
    url = "http://localhost:3000/verify-nin"
    data = json.dumps({"number": "invalid_nin_123"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        response = urllib.request.urlopen(req)
        pytest.fail("Expected a 400 error response, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected status code 400, got {e.code}"
        body = e.read().decode('utf-8')
        try:
            res_json = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Expected JSON response, got: {body}")
        
        assert res_json.get("error") is True, f"Expected 'error': true in response, got: {res_json}"
        assert res_json.get("message") == "Verification failed", f"Expected 'message': 'Verification failed' in response, got: {res_json}"
        assert "details" in res_json, f"Expected 'details' in response, got: {res_json}"

def test_package_json_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(os.path.join(PROJECT_DIR, "package.json")), "package.json not found in /home/user/app"

def test_index_js_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(os.path.join(PROJECT_DIR, "index.js")), "index.js not found in /home/user/app"
