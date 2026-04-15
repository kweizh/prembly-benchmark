import os
import subprocess
import time
import socket
import json
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory not found at {PROJECT_DIR}"

def test_build_succeeds():
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'npm run build' failed:\n{result.stderr}\n{result.stdout}"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
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
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_api_route_proxy(start_app):
    """Test the /api/verify-nin endpoint using curl."""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST", 
            "http://localhost:3000/api/verify-nin",
            "-H", "Content-Type: application/json",
            "-d", '{"number": "12345678901"}'
        ],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"curl request failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"API did not return valid JSON. Output: {result.stdout}")
        
    # The Prembly API might return success or error, but the proxy should forward it
    # We check if the response contains keys typical of Prembly responses
    assert "status" in data or "message" in data or "code" in data, \
        f"Response JSON does not look like a Prembly API response: {data}"
