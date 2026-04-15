import os
import sys
import json
import time
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

PROJECT_DIR = "/home/user/prembly_poller"

received_webhooks = []

class MockPremblyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/v1/checker-widget/sdk/sessions/"):
            app_id = self.headers.get("app-id")
            api_key = self.headers.get("x-api-key")
            if app_id != "test_app_id" or api_key != "test_api_key":
                self.send_response(401)
                self.end_headers()
                return
            
            mock_sessions = {
                "status": True,
                "message": "Sessions retrieved successfully",
                "data": {
                    "sessions": [
                        {
                            "id": "1",
                            "status": "completed",
                            "is_used": False,
                            "full_name": "John Doe"
                        },
                        {
                            "id": "2",
                            "status": "completed",
                            "is_used": True,
                            "full_name": "Jane Doe"
                        },
                        {
                            "id": "3",
                            "status": "in_progress",
                            "is_used": False,
                            "full_name": "Jim Doe"
                        },
                        {
                            "id": "4",
                            "status": "completed",
                            "is_used": False,
                            "full_name": "Jill Doe"
                        }
                    ]
                }
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(mock_sessions).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

class MockWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/webhook":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
                received_webhooks.append(payload)
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run_server(server):
    server.serve_forever()

def test_poll_sessions():
    global received_webhooks
    received_webhooks.clear()

    prembly_server = HTTPServer(("localhost", 8080), MockPremblyHandler)
    webhook_server = HTTPServer(("localhost", 3000), MockWebhookHandler)
    
    t1 = threading.Thread(target=run_server, args=(prembly_server,), daemon=True)
    t2 = threading.Thread(target=run_server, args=(webhook_server,), daemon=True)
    t1.start()
    t2.start()
    
    try:
        time.sleep(1)
        
        env = os.environ.copy()
        env["APP_ID"] = "test_app_id"
        env["X_API_KEY"] = "test_api_key"
        env["PREMBLY_API_URL"] = "http://localhost:8080"
        
        subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=False)
        
        result = subprocess.run(
            ["node", "poll_sessions.js"], 
            cwd=PROJECT_DIR, 
            env=env, 
            capture_output=True, 
            text=True
        )
        
        assert result.returncode == 0, f"Node script failed with output: {result.stderr}\n{result.stdout}"
        assert len(received_webhooks) == 2, f"Expected 2 webhooks, got {len(received_webhooks)}"
        
        received_ids = [w.get("id") for w in received_webhooks]
        assert "1" in received_ids, "Session 1 was not sent to the webhook"
        assert "4" in received_ids, "Session 4 was not sent to the webhook"
        assert "2" not in received_ids, "Session 2 was sent to the webhook but it was already used"
        assert "3" not in received_ids, "Session 3 was sent to the webhook but it was not completed"
    finally:
        prembly_server.shutdown()
        webhook_server.shutdown()
        prembly_server.server_close()
        webhook_server.server_close()
