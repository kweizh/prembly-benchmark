import os
import subprocess
import time
import socket
import json
import hmac
import hashlib
import base64
import urllib.request
import urllib.error
import signal
import pytest

PROJECT_DIR = "/home/user/prembly-webhook"
TEST_SECRET = os.environ.get("PREMBLY_API_KEY", "test_secret_key_123")
PORT = 3000

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_server():
    env = os.environ.copy()
    env["PREMBLY_API_KEY"] = TEST_SECRET
    env["PREMBLY_API_URL"] = "https://api.prembly.com"
    
    # Start the app
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(PORT):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Server failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_valid_signature(start_server):
    payload = json.dumps({
        "status": True,
        "detail": "Verification Successful",
        "response_code": "00",
        "data": {"id": "12345"}
    }).encode('utf-8')
    
    signature = base64.b64encode(
        hmac.new(TEST_SECRET.encode('utf-8'), payload, hashlib.sha256).digest()
    ).decode('utf-8')
    
    req = urllib.request.Request(
        f"http://localhost:{PORT}/webhook",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-prembly-signature": signature
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            res_body = json.loads(response.read().decode('utf-8'))
            assert res_body.get("status") == "success", f"Expected success status, got {res_body}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Valid signature request failed with HTTP {e.code}: {e.read().decode('utf-8')}")

def test_invalid_signature(start_server):
    payload = json.dumps({
        "status": True,
        "detail": "Verification Successful",
        "response_code": "00",
        "data": {"id": "12345"}
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"http://localhost:{PORT}/webhook",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-prembly-signature": "invalid_signature_here"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            pytest.fail(f"Expected HTTP 401, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected HTTP 401, got {e.code}"
        res_body = json.loads(e.read().decode('utf-8'))
        assert res_body.get("error") == "Invalid signature", f"Expected invalid signature error, got {res_body}"
