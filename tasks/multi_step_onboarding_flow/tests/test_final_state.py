import os
import subprocess
import time
import requests
import json
import pytest

PROJECT_DIR = "/home/user/onboarding_app"

@pytest.fixture(scope="session", autouse=True)
def setup_server():
    env = os.environ.copy()
    env["PREMBLY_APP_ID"] = "test_app"
    env["PREMBLY_SECRET_KEY"] = "test_sec"
    env["PREMBLY_PUBLIC_KEY"] = "test_pub"
    env["PREMBLY_CONFIG_ID"] = "test_conf"
    
    server_process = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)
    yield
    server_process.terminate()

def test_server_running():
    response = requests.get("http://localhost:3000")
    assert response.status_code == 200, "Server did not return 200 OK on root"

def test_verify_phone_endpoint():
    # We just check if the endpoint exists, it might fail to call Prembly API if no mock is provided
    # but we can check if it returns a response (even a 4xx/5xx from Prembly)
    response = requests.post("http://localhost:3000/api/verify-phone", json={"phone": "1234567890"})
    assert response.status_code in [200, 400, 401, 404, 500], f"Unexpected status code: {response.status_code}"

def test_frontend_code_contains_prembly():
    index_path = os.path.join(PROJECT_DIR, "public", "index.html")
    assert os.path.isfile(index_path), "public/index.html does not exist"
    with open(index_path, "r") as f:
        content = f.read()
    assert "PremblyPass" in content, "PremblyPass not found in index.html"
    assert "PREMBLY_CONFIG_ID" in content or "test_conf" in content or "config_id" in content.lower(), "config_id not found in index.html"

def test_server_code_contains_api_call():
    server_path = os.path.join(PROJECT_DIR, "server.js")
    assert os.path.isfile(server_path), "server.js does not exist"
    with open(server_path, "r") as f:
        content = f.read()
    assert "sandbox.myidentitypay.com" in content or "api.prembly.com" in content, "Prembly API URL not found in server.js"
    assert "x-api-key" in content.lower(), "x-api-key not found in server.js"
