import os
import subprocess
import time
import socket
import pytest
import requests
import signal

PROJECT_DIR = "/home/user/app"

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
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_verify_bvn_endpoint(start_app):
    """Priority 3 fallback: HTTP API verification."""
    # Send a request to the locally running Express app
    url = "http://localhost:3000/verify-bvn"
    payload = {"bvn": "12345678901"}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /verify-bvn: {e}")
        
    # Prembly sandbox should return a response, even if it's an error due to mock data
    assert response.status_code in [200, 400], f"Expected status 200 or 400 from proxy, got {response.status_code}"
    assert response.headers.get("content-type", "").startswith("application/json"), "Expected JSON response from proxy"
    
    data = response.json()
    assert isinstance(data, dict), "Expected a JSON object from the response"

def test_index_js_exists_and_contains_headers():
    """Verify that the implementation file correctly uses the required headers."""
    index_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index_path), "index.js not found in project directory."
    
    with open(index_path, "r") as f:
        content = f.read()
        
    assert "PREMBLY_APP_ID" in content, "Expected to find PREMBLY_APP_ID in index.js"
    assert "PREMBLY_API_KEY" in content, "Expected to find PREMBLY_API_KEY in index.js"
    assert "api.prembly.com" in content, "Expected to find api.prembly.com in index.js"
