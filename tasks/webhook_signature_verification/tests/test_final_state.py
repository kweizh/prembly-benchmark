import os
import subprocess
import time
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import signal
import pytest

PROJECT_DIR = "/home/user/prembly-webhook"
MOCK_API_PORT = 8080
NODE_SERVER_PORT = 3000

class MockPremblyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/verification/valid_ref/status"):
            api_key = self.headers.get("x-api-key")
            if api_key != "test_secret_key":
                self.send_response(401)
                self.end_headers()
                return
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": True,
                "data": {
                    "verification_status": "VERIFIED"
                }
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith("/verification/invalid_ref/status"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": True,
                "data": {
                    "verification_status": "FAILED"
                }
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_mock_server():
    server = HTTPServer(('localhost', MOCK_API_PORT), MockPremblyHandler)
    server.serve_forever()

def test_webhook_verification():
    # Start mock server
    mock_server_thread = threading.Thread(target=run_mock_server, daemon=True)
    mock_server_thread.start()

    # Start Node server
    env = os.environ.copy()
    env["PREMBLY_SECRET_KEY"] = "test_secret_key"
    env["PREMBLY_API_URL"] = f"http://localhost:{MOCK_API_PORT}"
    
    # Remove previous verified_webhooks.json if it exists
    verified_file = os.path.join(PROJECT_DIR, "verified_webhooks.json")
    if os.path.exists(verified_file):
        os.remove(verified_file)

    node_process = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)  # Wait for server to start

    try:
        # Test 1: Valid Webhook
        req = urllib.request.Request(
            f"http://localhost:{NODE_SERVER_PORT}/webhook",
            data=json.dumps({"verification": {"reference": "valid_ref", "status": "VERIFIED"}}).encode(),
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, f"Expected 200 OK, got {response.status}"
        except urllib.error.HTTPError as e:
            pytest.fail(f"Valid webhook failed with {e.code}")

        # Check if file was written
        assert os.path.exists(verified_file), "verified_webhooks.json was not created"
        with open(verified_file, "r") as f:
            content = f.read()
            assert "valid_ref" in content, "valid_ref not found in verified_webhooks.json"

        # Test 2: Invalid Webhook
        req_invalid = urllib.request.Request(
            f"http://localhost:{NODE_SERVER_PORT}/webhook",
            data=json.dumps({"verification": {"reference": "invalid_ref", "status": "VERIFIED"}}).encode(),
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req_invalid) as response:
                pytest.fail("Expected 403 Forbidden, but got 200 OK")
        except urllib.error.HTTPError as e:
            assert e.code == 403, f"Expected 403 Forbidden, got {e.code}"

    finally:
        node_process.send_signal(signal.SIGTERM)
        node_process.wait(timeout=5)
