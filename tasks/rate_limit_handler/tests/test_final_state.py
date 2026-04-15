import os
import subprocess
import time
import pytest

# We can't import requests if it's not installed in the test environment (standard python environment).
# Wait, let's use urllib.request instead to be safe, since standard library is preferred.

import urllib.request
import urllib.error
import json

def test_rate_limit_handler():
    # Start mock server
    mock_server = subprocess.Popen(["node", "/home/user/mock-server.js"])
    
    # Start app server
    app_server = subprocess.Popen(["node", "server.js"], cwd="/home/user/prembly-app")
    
    try:
        # Wait for servers to start
        time.sleep(3)
        
        def make_request(user_id, nin):
            data = json.dumps({"user_id": user_id, "nin": nin}).encode("utf-8")
            req = urllib.request.Request(
                "http://localhost:3000/api/verify",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req) as response:
                    return response.status, json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                return e.code, json.loads(e.read().decode("utf-8"))
        
        # Test Case 1: Successful Verification
        status, body = make_request("user1", "11111111111")
        assert status == 200, f"Expected 200 OK, got {status}"
        
        # Test Case 2: Rate Limit Enforcement
        for _ in range(3):
            status, body = make_request("user2", "22222222222")
            assert status == 200, f"Expected 200 OK within limit, got {status}"
            
        status4, body4 = make_request("user2", "22222222222")
        assert status4 == 429, f"Expected 429 Too Many Requests, got {status4}"
        assert body4.get("error") == "Too many verification attempts", "Expected specific error message"
        
        # Test Case 3: Independent Limits
        status5, body5 = make_request("user3", "33333333333")
        assert status5 == 200, f"Expected 200 OK for new user, got {status5}"
        
    finally:
        mock_server.terminate()
        app_server.terminate()
