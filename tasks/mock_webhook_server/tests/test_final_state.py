import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error
import hmac
import hashlib

PROJECT_DIR = "/home/user/prembly-webhook"
SECRET_KEY = b"test_secret_key_123"

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
    # Ensure the directory exists
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

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

def test_valid_signature(start_app):
    url = "http://localhost:3000/webhook"
    data = json.dumps({"event": "verification.success", "reference": "12345"}).encode('utf-8')
    signature = hmac.new(SECRET_KEY, data, hashlib.sha512).hexdigest()

    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'x-prembly-signature': signature
    })

    try:
        response = urllib.request.urlopen(req, timeout=5)
        assert response.getcode() == 200, f"Expected 200 OK, got {response.getcode()}"
        resp_data = json.loads(response.read().decode('utf-8'))
        assert resp_data.get("status") == "success", f"Expected status success, got {resp_data}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Request failed with HTTP {e.code}: {e.read().decode('utf-8')}")

def test_invalid_signature(start_app):
    url = "http://localhost:3000/webhook"
    data = json.dumps({"event": "verification.success", "reference": "12345"}).encode('utf-8')
    signature = "invalid_signature_hash"

    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'x-prembly-signature': signature
    })

    try:
        urllib.request.urlopen(req, timeout=5)
        pytest.fail("Expected 401 Unauthorized, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401, got {e.code}"
        resp_data = json.loads(e.read().decode('utf-8'))
        assert resp_data.get("status") == "error", f"Expected status error, got {resp_data}"
        assert resp_data.get("message") == "Invalid signature", f"Expected message 'Invalid signature', got {resp_data}"

def test_missing_signature(start_app):
    url = "http://localhost:3000/webhook"
    data = json.dumps({"event": "verification.success", "reference": "12345"}).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json'
    })

    try:
        urllib.request.urlopen(req, timeout=5)
        pytest.fail("Expected 401 Unauthorized, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401, got {e.code}"
