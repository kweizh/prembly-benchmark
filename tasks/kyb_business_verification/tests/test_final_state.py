import os
import subprocess
import time
import socket
import json
import pytest
import urllib.request
import urllib.error
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

PROJECT_DIR = "/home/user/onboarding_api"
MOCK_PORT = 8080
API_PORT = 3000

class MockPremblyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/v1/verification/cac':
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length))
            
            app_id = self.headers.get('app-id')
            api_key = self.headers.get('x-api-key')
            
            if app_id != "test_app" or api_key != "test_key":
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"status": "error", "message": "Unauthorized"}')
                return
                
            if body.get('company_number') == "RC123456":
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success", "data": {"company_name": "Test Company"}}')
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"status": "error", "message": "Not found"}')
        else:
            self.send_response(404)
            self.end_headers()

def run_mock_server():
    server = HTTPServer(('localhost', MOCK_PORT), MockPremblyHandler)
    server.serve_forever()

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
    # Check if project exists
    assert os.path.exists(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
    assert os.path.exists(os.path.join(PROJECT_DIR, "index.js")), "index.js not found."

    # Start mock server
    mock_thread = Thread(target=run_mock_server, daemon=True)
    mock_thread.start()
    assert wait_for_port(MOCK_PORT), "Mock server failed to start."

    # Start the user's API
    env = os.environ.copy()
    env["PREMBLY_BASE_URL"] = f"http://localhost:{MOCK_PORT}"
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

    if not wait_for_port(API_PORT, timeout=10):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("User API failed to start on port 3000.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

def test_verify_business_endpoint(setup_environment):
    req_data = json.dumps({"registration_number": "RC123456"}).encode('utf-8')
    req = urllib.request.Request(
        f"http://localhost:{API_PORT}/verify-business",
        data=req_data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            resp_data = json.loads(response.read().decode('utf-8'))
            assert resp_data.get("status") == "success", "Expected status 'success' from Prembly mock."
            assert "Test Company" in json.dumps(resp_data), "Expected 'Test Company' in response data."
    except urllib.error.HTTPError as e:
        pytest.fail(f"API request failed with HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        pytest.fail(f"API request failed: {e}")
