import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

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
        preexec_fn=os.setsid,
        env=os.environ.copy()
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

def test_verify_license_endpoint(start_app):
    url = "http://localhost:3000/verify-license"
    data = json.dumps({"license_number": "DXG100"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8')
            json_response = json.loads(body)
            # We don't know the exact structure of the sandbox response, but it should be a valid JSON object
            assert isinstance(json_response, dict), "Response should be a JSON object"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTPError: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        pytest.fail(f"Failed to make request: {e}")

def test_app_files_exist():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "index.js")), "index.js not found"
    assert os.path.isfile(os.path.join(PROJECT_DIR, "package.json")), "package.json not found"
