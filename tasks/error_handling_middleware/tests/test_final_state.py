import os
import subprocess
import time
import socket
import json
import hmac
import hashlib
import urllib.request
from urllib.error import HTTPError
import pytest

PROJECT_DIR = "/home/user/app"
PORT = 3000
SECRET = "test_secret"

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
    # Start the app with the secret key environment variable
    env = os.environ.copy()
    env["PREMBLY_SECRET_KEY"] = SECRET
    
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
    )

    # Wait for the app to be ready
    if not wait_for_port(PORT):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required port.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_missing_signature(start_app):
    data = json.dumps({"event":"test"}).encode('utf-8')
    req = urllib.request.Request(f"http://localhost:{PORT}/webhook", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 401 HTTPError but request succeeded.")
    except HTTPError as e:
        assert e.code == 401, f"Expected status code 401, got {e.code}"
        response_body = e.read().decode('utf-8')
        assert "Invalid signature" in response_body, f"Expected 'Invalid signature' in response, got {response_body}"

def test_invalid_signature(start_app):
    data = json.dumps({"event":"test"}).encode('utf-8')
    req = urllib.request.Request(f"http://localhost:{PORT}/webhook", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-identitypass-signature", "invalid_hash")
    
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 401 HTTPError but request succeeded.")
    except HTTPError as e:
        assert e.code == 401, f"Expected status code 401, got {e.code}"
        response_body = e.read().decode('utf-8')
        assert "Invalid signature" in response_body, f"Expected 'Invalid signature' in response, got {response_body}"

def test_valid_signature(start_app):
    data = json.dumps({"event":"test"}).encode('utf-8')
    # Compute valid signature
    signature = hmac.new(SECRET.encode('utf-8'), data, hashlib.sha256).hexdigest()
    
    req = urllib.request.Request(f"http://localhost:{PORT}/webhook", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-identitypass-signature", signature)
    
    try:
        response = urllib.request.urlopen(req)
        assert response.code == 200, f"Expected status code 200, got {response.code}"
        response_body = response.read().decode('utf-8')
        assert "received" in response_body, f"Expected 'received' in response, got {response_body}"
    except HTTPError as e:
        pytest.fail(f"Expected 200 OK, got HTTPError {e.code}: {e.read().decode('utf-8')}")

def test_middleware_file_exists():
    middleware_path = os.path.join(PROJECT_DIR, "middleware.js")
    assert os.path.isfile(middleware_path), f"File {middleware_path} does not exist."
