import os
import subprocess
import time
import socket
import pytest
import sqlite3
import urllib.request
import json
import glob

PROJECT_DIR = "/home/user/prembly-webhook"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_server():
    process = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Server failed to start and listen on port 3000.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_webhook_idempotency(start_server):
    url = "http://localhost:3000/webhook/prembly"
    data = json.dumps({"webhook_id": "test_123", "verification_status": "success"}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    # First request
    req1 = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req1) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
    except Exception as e:
        pytest.fail(f"First request failed: {e}")

    # Second request
    req2 = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req2) as response:
            assert response.status == 200, f"Expected 200 OK for duplicate request, got {response.status}"
    except Exception as e:
        pytest.fail(f"Second request failed: {e}")

def test_database_contains_only_one_entry(start_server):
    db_files = glob.glob(os.path.join(PROJECT_DIR, "*.db")) + glob.glob(os.path.join(PROJECT_DIR, "*.sqlite"))
    assert len(db_files) > 0, "Could not find any SQLite database file (.db or .sqlite) in the project directory."
    
    found_entry = False
    for db_file in db_files:
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                try:
                    cursor.execute(f"SELECT * FROM {table_name};")
                    rows = cursor.fetchall()
                    for row in rows:
                        if 'test_123' in row:
                            found_entry = True
                            # Check how many times it appears
                            count = sum(1 for r in rows if 'test_123' in r)
                            assert count == 1, f"Expected exactly 1 entry for 'test_123' in table {table_name}, but found {count}."
                except sqlite3.OperationalError:
                    pass
            conn.close()
        except Exception:
            pass

    assert found_entry, "Could not find the processed webhook_id 'test_123' in any database table."
