import os
import subprocess
import time
import urllib.request
import json
import base64
from urllib.error import HTTPError

PROJECT_DIR = "/home/user/prembly-webhook"
PORT = 3000

def test_fastify_server_webhook_handling():
    # Set up environment
    env = os.environ.copy()
    env["WEBHOOK_SECRET"] = "my_super_secret"
    
    # Start the server
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for server to start
        time.sleep(3)
        
        # Test 1: Missing Signature
        req = urllib.request.Request(
            f"http://localhost:{PORT}/webhook",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            urllib.request.urlopen(req)
            assert False, "Expected 401 Unauthorized for missing signature"
        except HTTPError as e:
            assert e.code == 401, f"Expected 401, got {e.code}"
            
        # Test 2: Invalid Signature
        req = urllib.request.Request(
            f"http://localhost:{PORT}/webhook",
            data=b"{}",
            headers={
                "Content-Type": "application/json",
                "x-identitypass-signature": "invalid_base64"
            },
            method="POST"
        )
        try:
            urllib.request.urlopen(req)
            assert False, "Expected 401 Unauthorized for invalid signature"
        except HTTPError as e:
            assert e.code == 401, f"Expected 401, got {e.code}"
            
        # Test 3: Valid Signature
        valid_signature = base64.b64encode(b"my_super_secret").decode("utf-8")
        payload = json.dumps({"data": {"verification_id": "12345"}}).encode("utf-8")
        
        req = urllib.request.Request(
            f"http://localhost:{PORT}/webhook",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-identitypass-signature": valid_signature
            },
            method="POST"
        )
        try:
            response = urllib.request.urlopen(req)
            assert response.getcode() == 200, f"Expected 200 OK, got {response.getcode()}"
        except HTTPError as e:
            assert False, f"Expected 200 OK for valid signature, got {e.code}"
            
        # Test 4: Check Database Update
        req = urllib.request.Request(
            f"http://localhost:{PORT}/status/12345",
            method="GET"
        )
        try:
            response = urllib.request.urlopen(req)
            assert response.getcode() == 200, f"Expected 200 OK, got {response.getcode()}"
            
            data = json.loads(response.read().decode("utf-8"))
            assert data.get("verified") is True, "Expected verified status to be true"
        except HTTPError as e:
            assert False, f"Expected 200 OK for status check, got {e.code}"
            
    finally:
        process.terminate()
        process.wait(timeout=5)
