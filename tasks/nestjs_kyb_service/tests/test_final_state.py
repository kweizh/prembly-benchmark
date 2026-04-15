import os
import subprocess
import time
import socket
import json
import pytest
import hmac
import hashlib

PROJECT_DIR = "/home/user/nestjs-kyb"
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
    env = os.environ.copy()
    
    process = subprocess.Popen(
        ["npm", "run", "start"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(PORT):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_kyb_verify_endpoint(start_app):
    """Test POST /kyb/verify endpoint"""
    payload = json.dumps({"rc_number": "123456", "company_type": "RC"})
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST", f"http://localhost:{PORT}/kyb/verify",
            "-H", "Content-Type: application/json",
            "-d", payload
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    assert "404 Not Found" not in result.stdout, "Endpoint /kyb/verify not found"

def test_webhook_valid_signature(start_app):
    """Test POST /webhook/prembly with valid signature"""
    payload = json.dumps({"event": "verification.completed", "status": "success"})
    secret = os.environ.get("PREMBLY_WEBHOOK_SECRET", os.environ.get("PREMBLY_API_KEY", "test_secret"))
    signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha512).hexdigest()
    
    result = subprocess.run(
        [
            "curl", "-s", "-w", "%{http_code}", "-o", "/dev/null", "-X", "POST", f"http://localhost:{PORT}/webhook/prembly",
            "-H", "Content-Type: application/json",
            "-H", f"x-prembly-signature: {signature}",
            "-d", payload
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    http_code = result.stdout.strip()
    assert http_code in ["200", "201"], f"Expected 200 or 201 for valid webhook, got {http_code}"

def test_webhook_invalid_signature(start_app):
    """Test POST /webhook/prembly with invalid signature"""
    payload = json.dumps({"event": "verification.completed", "status": "success"})
    signature = "invalid_signature"
    
    result = subprocess.run(
        [
            "curl", "-s", "-w", "%{http_code}", "-o", "/dev/null", "-X", "POST", f"http://localhost:{PORT}/webhook/prembly",
            "-H", "Content-Type: application/json",
            "-H", f"x-prembly-signature: {signature}",
            "-d", payload
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    http_code = result.stdout.strip()
    assert http_code in ["400", "401", "403"], f"Expected 400, 401 or 403 for invalid webhook signature, got {http_code}"
