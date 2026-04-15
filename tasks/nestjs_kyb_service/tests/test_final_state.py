import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/prembly-kyb"
SERVICE_FILE = os.path.join(PROJECT_DIR, "src/prembly/prembly.service.ts")

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

def test_service_file_exists():
    assert os.path.isfile(SERVICE_FILE), f"Service file not found at {SERVICE_FILE}"

def test_service_url():
    with open(SERVICE_FILE) as f:
        content = f.read()
    assert "https://sandbox.myidentitypay.com/api/v2/biometrics/merchant/data/verification/cac" in content or "myidentitypay.com" in content or "prembly.com" in content, "Expected Prembly sandbox URL in prembly.service.ts"

def test_service_headers():
    with open(SERVICE_FILE) as f:
        content = f.read()
    assert "PREMBLY_APP_ID" in content, "Expected PREMBLY_APP_ID in prembly.service.ts"
    assert "PREMBLY_API_KEY" in content, "Expected PREMBLY_API_KEY in prembly.service.ts"
    assert "app-id" in content or "app_id" in content.lower(), "Expected app-id header in prembly.service.ts"
    assert "x-api-key" in content or "x_api_key" in content.lower(), "Expected x-api-key header in prembly.service.ts"

@pytest.fixture(scope="module")
def start_app():
    env = os.environ.copy()
    env["PREMBLY_APP_ID"] = "test_app_id"
    env["PREMBLY_API_KEY"] = "test_api_key"

    process = subprocess.Popen(
        ["npm", "run", "start"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")

    yield process

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_api_endpoint(start_app):
    result = subprocess.run(
        ["curl", "-s", "-i", "http://localhost:3000/verify-cac?rcNumber=123456&companyName=TEST"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl request failed: {result.stderr}"
    assert "HTTP/1.1 200" in result.stdout or "HTTP/1.1 201" in result.stdout or "HTTP/1.1 500" in result.stdout or "HTTP/1.1 400" in result.stdout, f"Expected HTTP response, got: {result.stdout}"
