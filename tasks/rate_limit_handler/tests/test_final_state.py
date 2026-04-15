import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def mock_server():
    mock_script = os.path.join(PROJECT_DIR, "mock_server.js")
    with open(mock_script, "w") as f:
        f.write("""
const http = require('http');
let count = 0;
const server = http.createServer((req, res) => {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
        try {
            const data = JSON.parse(body);
            if (data.nin === '11111111111') {
                count++;
                if (count <= 2) {
                    res.writeHead(429, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'Too Many Requests' }));
                } else {
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success: true, message: 'Verified' }));
                }
            } else if (data.nin === '22222222222') {
                res.writeHead(429, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Too Many Requests' }));
            } else {
                res.writeHead(400);
                res.end();
            }
        } catch (e) {
            res.writeHead(400);
            res.end();
        }
    });
});
server.listen(4000);
""")
    
    process = subprocess.Popen(
        ["node", "mock_server.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(4000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Mock server failed to start on port 4000")
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

@pytest.fixture(scope="module")
def express_app_mock():
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR)
    
    env = os.environ.copy()
    env["PREMBLY_BASE_URL"] = "http://localhost:4000"
    env["PREMBLY_APP_ID"] = "test_app_id"
    env["PREMBLY_API_KEY"] = "test_api_key"
    
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Express app failed to start on port 3000")
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

@pytest.fixture(scope="module")
def express_app_real():
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR)
    
    env = os.environ.copy()
    env["PREMBLY_BASE_URL"] = "https://api.prembly.com"
    env["PREMBLY_APP_ID"] = os.environ.get("PREMBLY_APP_ID", "test_app_id")
    env["PREMBLY_API_KEY"] = os.environ.get("PREMBLY_API_KEY", "test_api_key")
    env["PORT"] = "3001"
    
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(3001):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Express app failed to start on port 3001")
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

def test_rate_limit_retry_success(mock_server, express_app_mock):
    req = urllib.request.Request(
        "http://localhost:3000/verify-nin",
        data=json.dumps({"nin": "11111111111"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200 after retries, got {response.status}"
            data = json.loads(response.read().decode())
            assert data.get("success") is True, "Expected success: true in response"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Request failed with status {e.code}: {e.read().decode()}")

def test_rate_limit_exhausted(mock_server, express_app_mock):
    req = urllib.request.Request(
        "http://localhost:3000/verify-nin",
        data=json.dumps({"nin": "22222222222"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            pytest.fail(f"Expected 429 error, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 429, f"Expected status 429 after exhausting retries, got {e.code}"
        body = e.read().decode()
        assert "Rate limit exceeded" in body, "Expected 'Rate limit exceeded, please try again later' message"

def test_real_api_integration(express_app_real):
    # Test with the real API sandbox using a valid or invalid NIN
    # According to Prembly sandbox docs, specific test data is needed,
    # but we can just check that it doesn't return 404 or 500
    req = urllib.request.Request(
        "http://localhost:3001/verify-nin",
        data=json.dumps({"nin": "12345678901"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
    except urllib.error.HTTPError as e:
        # 400 Bad Request or 404 Not Found is acceptable if the NIN is invalid in sandbox
        # But we want to make sure the API is actually reached
        assert e.code in [400, 404, 422], f"Expected 400/404/422 from real API for invalid NIN, got {e.code}"
