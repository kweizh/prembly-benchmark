import os
import subprocess
import time
import socket
import json
import pytest
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import urllib.request

PROJECT_DIR = "/home/user/prembly-app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

# Mock Prembly Server
class MockPremblyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/verification/nin':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Verify headers
            app_id = self.headers.get('app-id')
            api_key = self.headers.get('x-api-key')
            
            if app_id != 'test_app_id' or api_key != 'test_api_key':
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error": "Unauthorized"}')
                return
                
            try:
                body = json.loads(post_data)
                if body.get('number') == '12345678901':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "success", "message": "NIN verified successfully"}')
                    return
            except:
                pass
                
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Bad Request"}')
        else:
            self.send_response(404)
            self.end_headers()

@pytest.fixture(scope="module")
def mock_server():
    server = HTTPServer(('localhost', 4000), MockPremblyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield server
    server.shutdown()

@pytest.fixture(scope="module")
def start_app():
    env = os.environ.copy()
    env['PREMBLY_APP_ID'] = 'test_app_id'
    env['PREMBLY_API_KEY'] = 'test_api_key'
    env['PREMBLY_BASE_URL'] = 'http://localhost:4000'
    
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Next.js app failed to start and listen on port 3000.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_api_route_proxy(mock_server, start_app):
    """Priority 3: Verify the Next.js API route proxies the request correctly."""
    req = urllib.request.Request(
        'http://localhost:3000/api/verify-nin',
        data=json.dumps({"number": "12345678901"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = json.loads(response.read().decode('utf-8'))
            assert body.get('status') == 'success', f"Expected success status from proxy, got: {body}"
            assert body.get('message') == 'NIN verified successfully', f"Expected specific message, got: {body}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"API route returned HTTPError: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        pytest.fail(f"Failed to call API route: {e}")
