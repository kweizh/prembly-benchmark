import os
import subprocess
import time
import requests
import hmac
import hashlib
import base64
import pytest
import json

PROJECT_DIR = "/home/user/prembly-webhook"
PORT = 3000
API_KEY = os.environ.get("PREMBLY_API_KEY", "test_api_key_123")
SANDBOX_URL = "https://api.prembly.com"

@pytest.fixture(scope="module", autouse=True)
def setup_server():
    # Setup step 1: Run npm install
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
    # Setup step 2: Start server
    env = os.environ.copy()
    env["PREMBLY_API_KEY"] = API_KEY
    server_process = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    for _ in range(30):
        try:
            response = requests.get(f"http://localhost:{PORT}")
            break
        except requests.ConnectionError:
            time.sleep(0.5)
            
    yield
    
    # Teardown: Stop server
    server_process.terminate()
    server_process.wait()

def generate_signature(payload_str, secret):
    hmac_obj = hmac.new(secret.encode('utf-8'), payload_str.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode('utf-8')

def test_valid_signature():
    payload = {"event": "verification.success", "data": {"id": "123"}}
    payload_str = json.dumps(payload)
    
    # Ensure exact string is sent
    signature = generate_signature(payload_str, API_KEY)
    
    headers = {
        "Content-Type": "application/json",
        "x-prembly-signature": signature
    }
    
    response = requests.post(f"http://localhost:{PORT}/webhook", data=payload_str, headers=headers)
    
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    assert response.json() == {"status": "success"}, f"Expected success JSON, got {response.text}"

def test_invalid_signature():
    payload = {"event": "verification.success", "data": {"id": "123"}}
    payload_str = json.dumps(payload)
    
    headers = {
        "Content-Type": "application/json",
        "x-prembly-signature": "invalid_signature_here"
    }
    
    response = requests.post(f"http://localhost:{PORT}/webhook", data=payload_str, headers=headers)
    
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"
    assert response.json() == {"error": "Invalid signature"}, f"Expected error JSON, got {response.text}"

def test_missing_signature():
    payload = {"event": "verification.success", "data": {"id": "123"}}
    payload_str = json.dumps(payload)
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"http://localhost:{PORT}/webhook", data=payload_str, headers=headers)
    
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"
    assert response.json() == {"error": "Invalid signature"}, f"Expected error JSON, got {response.text}"
