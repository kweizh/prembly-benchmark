import os
import subprocess
import time
import socket
import pytest
import json

PROJECT_DIR = "/home/user/fintech-app"

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
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_valid_nin_returns_201(start_app):
    """Priority 1: Send a POST request to API with valid NIN."""
    import urllib.request
    import urllib.error

    data = json.dumps({"ninNumber": "11111111111"}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:3000/api/wallet/create",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        response = urllib.request.urlopen(req)
        assert response.getcode() == 201, f"Expected 201 Created, got {response.getcode()}"
        res_body = json.loads(response.read().decode('utf-8'))
        assert "wallet_id" in res_body, "Expected 'wallet_id' in response"
        assert res_body["wallet_id"] == "new_wallet_123", f"Expected 'new_wallet_123', got {res_body['wallet_id']}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Request failed with HTTP {e.code}: {e.read().decode('utf-8')}")

def test_invalid_nin_returns_400(start_app):
    """Priority 1: Send a POST request to API with invalid NIN."""
    import urllib.request
    import urllib.error

    data = json.dumps({"ninNumber": "invalid_nin"}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:3000/api/wallet/create",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        response = urllib.request.urlopen(req)
        pytest.fail(f"Expected 400 Bad Request, but request succeeded with {response.getcode()}")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected 400 Bad Request, got {e.code}"
