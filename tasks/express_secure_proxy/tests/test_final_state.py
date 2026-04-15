import os
import subprocess
import time
import socket
import pytest
import urllib.request
import urllib.error
import json

PROJECT_DIR = "/home/user/proxy-app"

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
    process = subprocess.Popen(
        ["node", "index.js"],
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
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_proxy_injects_credentials(start_app):
    """Priority 3: Send request to the proxy and verify it forwards correctly."""
    url = "http://localhost:3000/api/prembly/api/v2/biometrics/merchant/data/verification/nin"
    data = json.dumps({"number": "11111111111"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        response = urllib.request.urlopen(req)
        status = response.getcode()
        body = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect to proxy server: {e}")
    
    # If the proxy didn't inject the credentials, Prembly returns 401
    assert status != 401, \
        f"Expected credentials to be injected, but received 401 Unauthorized from Prembly. Response: {body}"
    
    # It should either be 200 (if sandbox data matches) or another error like 400/404
    assert status in [200, 400, 404], \
        f"Expected proxy to forward the request to Prembly, but received unexpected status {status}. Response: {body}"
