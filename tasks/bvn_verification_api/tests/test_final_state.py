import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

PROJECT_DIR = "/home/user/prembly_bvn"

class MockPremblyHandler(BaseHTTPRequestHandler):
    request_data = None
    request_headers = None
    request_path = None

    def do_POST(self):
        MockPremblyHandler.request_path = self.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        if post_data:
            try:
                MockPremblyHandler.request_data = json.loads(post_data.decode('utf-8'))
            except:
                MockPremblyHandler.request_data = post_data.decode('utf-8')
                
        MockPremblyHandler.request_headers = self.headers

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": True,
            "detail": "Verification Successfull",
            "response_code": "00",
            "data": {
                "firstName": "John",
                "lastName": "Doe"
            }
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        
    def log_message(self, format, *args):
        pass

def start_mock_server():
    server = HTTPServer(('localhost', 4000), MockPremblyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def setup_environment():
    mock_server = start_mock_server()
    
    env = os.environ.copy()
    env["PREMBLY_BASE_URL"] = "http://localhost:4000"
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
        pytest.fail("Express app failed to start and listen on port 3000.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)
    mock_server.shutdown()

def test_verify_bvn_endpoint(setup_environment):
    url = "http://localhost:3000/verify-bvn"
    data = json.dumps({"bvn": "12345678901"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        response = urllib.request.urlopen(req, timeout=10)
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        pytest.fail(f"Request to {url} failed with status {e.code}: {body}")
    except Exception as e:
        pytest.fail(f"Request to {url} failed: {e}")

    # Verify mock server received the correct request
    assert MockPremblyHandler.request_path == "/verification/bvn_validation", \
        f"Expected Prembly request path to be '/verification/bvn_validation', got {MockPremblyHandler.request_path}"
        
    assert MockPremblyHandler.request_data is not None, "Mock Prembly server did not receive any request."
    assert isinstance(MockPremblyHandler.request_data, dict), "Expected request data to be JSON."
    assert MockPremblyHandler.request_data.get("number") == "12345678901", \
        f"Expected Prembly request body to contain 'number': '12345678901', got {MockPremblyHandler.request_data}"
    
    assert MockPremblyHandler.request_headers.get("app-id") == "test_app", \
        "Expected 'app-id' header to be 'test_app' in request to Prembly."
    assert MockPremblyHandler.request_headers.get("x-api-key") == "test_key", \
        "Expected 'x-api-key' header to be 'test_key' in request to Prembly."

    # Verify Express app returned the correct response
    assert response_json.get("status") is True, \
        f"Expected Express app to return the proxy response from Prembly, got {response_json}"
    assert response_json.get("data", {}).get("firstName") == "John", \
        "Expected Express app to return the Prembly data containing 'firstName': 'John'."
