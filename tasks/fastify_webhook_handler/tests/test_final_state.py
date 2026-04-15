import os
import subprocess
import time
import socket
import json
import urllib.request
import urllib.error
import pytest

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=30):
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
    env = os.environ.copy()
    # Use real API key if available, otherwise fallback to test key
    api_key = env.get("PREMBLY_API_KEY", "test_api_key")
    env["PREMBLY_API_KEY"] = api_key
    
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
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
    process.wait(timeout=10)

def test_missing_signature(start_app):
    url = "http://localhost:3000/webhook"
    data = json.dumps({"status": True, "response_code": "00"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 401 Unauthorized, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected HTTP 401, got {e.code}"

def test_invalid_signature(start_app):
    url = "http://localhost:3000/webhook"
    data = json.dumps({"status": True, "response_code": "00"}).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'x-prembly-signature': 'invalid_signature_base64='
    }
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 401 Unauthorized, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected HTTP 401, got {e.code}"

def test_valid_signature(start_app):
    url = "http://localhost:3000/webhook"
    data = b'{"status":true,"response_code":"00"}'
    
    import hmac
    import hashlib
    import base64
    
    api_key = os.environ.get("PREMBLY_API_KEY", "test_api_key")
    
    # Compute the signature dynamically using the actual key
    sig = hmac.new(api_key.encode('utf-8'), data, hashlib.sha256).digest()
    valid_signature = base64.b64encode(sig).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'x-prembly-signature': valid_signature
    }
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        response = urllib.request.urlopen(req)
        assert response.getcode() == 200, f"Expected HTTP 200, got {response.getcode()}"
        
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)
        assert response_json.get("status") == "received", f"Expected {{'status': 'received'}}, got {response_json}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200, but got {e.code}: {e.read().decode('utf-8')}")
