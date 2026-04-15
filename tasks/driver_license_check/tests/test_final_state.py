import os
import subprocess
import time
import socket
import json
import pytest
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/ride_app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_server():
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
    # Start the server with dummy environment variables
    env = os.environ.copy()
    env["PREMBLY_APP_ID"] = "dummy_app_id"
    env["PREMBLY_API_KEY"] = "dummy_api_key"
    
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Server failed to start and listen on port 3000.")

    yield

    # Shut down the server
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_verify_endpoint_returns_error(start_server):
    """Priority 3: Verify the endpoint using urllib, expecting a 400 or 401 error from Prembly."""
    url = "http://localhost:3000/verify"
    data = json.dumps({
        "number": "ABC12345YZ00",
        "first_name": "john",
        "last_name": "doe"
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        response = urllib.request.urlopen(req)
        pytest.fail("Expected an HTTP error due to dummy credentials, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code in [400, 401, 403], f"Expected 400, 401, or 403 error from Prembly proxy, got {e.code}"
        
        # Read the response body from the error
        body = e.read().decode("utf-8")
        try:
            error_data = json.loads(body)
            # Just verify it's a JSON response, we don't know the exact format Prembly returns for auth errors
            assert isinstance(error_data, dict), "Expected JSON error response from the proxy."
        except json.JSONDecodeError:
            pytest.fail(f"Expected a JSON response body, got: {body}")
