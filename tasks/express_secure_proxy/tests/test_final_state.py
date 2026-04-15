import os
import subprocess
import time
import socket
import json
import urllib.request
import pytest

PROJECT_DIR = "/home/user/proxy"

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
    env["PREMBLY_APP_ID"] = "test_app_id"
    env["PREMBLY_CONFIG_ID"] = "test_config_id"

    process = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Server failed to start and listen on port 3000.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_api_config_endpoint(start_server):
    try:
        req = urllib.request.Request("http://localhost:3000/api/config", method="GET")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("app_id") == "test_app_id", f"Expected app_id 'test_app_id', got {data.get('app_id')}"
            assert data.get("config_id") == "test_config_id", f"Expected config_id 'test_config_id', got {data.get('config_id')}"
    except Exception as e:
        pytest.fail(f"Failed to fetch /api/config: {str(e)}")
