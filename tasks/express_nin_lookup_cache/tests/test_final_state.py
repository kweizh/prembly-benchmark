import os
import subprocess
import time
import socket
import pytest
import urllib.request
import json
import signal

PROJECT_DIR = "/home/user/prembly_cache"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
    return False

@pytest.fixture(scope="module")
def mock_server():
    mock_code = """
const http = require('http');
let requestCount = 0;
const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/verification/nin') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            requestCount++;
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'success', data: { nin: '11111111111', requestCount } }));
        });
    } else if (req.url === '/count') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ count: requestCount }));
    } else {
        res.writeHead(404);
        res.end();
    }
});
server.listen(4000);
"""
    mock_path = "/tmp/mock_server.js"
    with open(mock_path, "w") as f:
        f.write(mock_code)
    
    process = subprocess.Popen(
        ["node", mock_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(4000):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Mock server failed to start on port 4000.")
        
    yield
    
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

@pytest.fixture(scope="module")
def user_server(mock_server):
    env = os.environ.copy()
    env["PREMBLY_BASE_URL"] = "http://localhost:4000"
    
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(3000):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("User server failed to start on port 3000.")
        
    yield
    
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_cache_logic(mock_server, user_server):
    # 1. Send first request
    req1 = urllib.request.Request("http://localhost:3000/nin/11111111111")
    try:
        with urllib.request.urlopen(req1) as response:
            res1 = json.loads(response.read().decode())
    except Exception as e:
        pytest.fail(f"First request failed: {e}")

    # Verify mock server got 1 request
    req_count = urllib.request.Request("http://localhost:4000/count")
    with urllib.request.urlopen(req_count) as response:
        count_data = json.loads(response.read().decode())
    assert count_data["count"] == 1, f"Expected 1 request to mock server, got {count_data['count']}"

    # 2. Send second request
    req2 = urllib.request.Request("http://localhost:3000/nin/11111111111")
    try:
        with urllib.request.urlopen(req2) as response:
            res2 = json.loads(response.read().decode())
    except Exception as e:
        pytest.fail(f"Second request failed: {e}")

    # Verify mock server STILL has only 1 request
    with urllib.request.urlopen(req_count) as response:
        count_data = json.loads(response.read().decode())
    assert count_data["count"] == 1, f"Cache failed! Expected 1 request to mock server, got {count_data['count']}. The user server called the API again."
