import os
import subprocess
import time
import socket
import json
import pytest

PROJECT_DIR = "/home/user/prembly-retry-app"

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
    env = os.environ.copy()
    env["PREMBLY_APP_ID"] = "test_app"
    env["PREMBLY_API_KEY"] = "test_key"
    
    process = subprocess.Popen(
        ["node", "index.js"],
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

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_retry_limit_logic(start_app):
    """Test that after 3 failed attempts, the 4th attempt returns 403 Max retries exceeded."""
    
    # Send 3 requests for user1
    for i in range(3):
        payload = json.dumps({"nin": "00000000000", "userId": "user1"})
        result = subprocess.run(
            ["curl", "-s", "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json", "-d", payload, "http://localhost:3000/verify"],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Curl failed: {result.stderr}"
        # The API should return an error code from Prembly, not 403 yet
        assert result.stdout.endswith("403") == False, f"Expected non-403 error on attempt {i+1}, got {result.stdout}"

    # 4th request for user1 should be 403
    payload = json.dumps({"nin": "00000000000", "userId": "user1"})
    result = subprocess.run(
        ["curl", "-s", "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json", "-d", payload, "http://localhost:3000/verify"],
        capture_output=True, text=True
    )
    assert result.stdout.endswith("403"), f"Expected 403 on 4th attempt, got: {result.stdout}"
    
    # Parse the JSON body from curl output (everything before the last 3 chars which is http_code)
    body = result.stdout[:-3]
    try:
        data = json.loads(body)
        assert data.get("error") == "Max retries exceeded", f"Expected error message 'Max retries exceeded', got: {data}"
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse JSON response: {body}")

    # Request for user2 should not be 403
    payload = json.dumps({"nin": "00000000000", "userId": "user2"})
    result = subprocess.run(
        ["curl", "-s", "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json", "-d", payload, "http://localhost:3000/verify"],
        capture_output=True, text=True
    )
    assert result.stdout.endswith("403") == False, f"Expected non-403 for new user2, got: {result.stdout}"
