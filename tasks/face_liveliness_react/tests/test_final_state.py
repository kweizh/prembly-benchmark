import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/prembly-app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "3000", "--host"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")

    yield

    # Shut down the app
    import signal
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=30)
    except Exception:
        pass

def test_code_implementation():
    app_jsx_path = os.path.join(PROJECT_DIR, "src", "App.jsx")
    with open(app_jsx_path, 'r') as f:
        content = f.read()
    
    assert "PremblyPass" in content, "PremblyPass is not imported or used in App.jsx."
    assert "test_app_id" in content, "test_app_id is missing in the configuration."
    assert "test_public_key" in content, "test_public_key is missing in the configuration."
    assert "test_config_id" in content, "test_config_id is missing in the configuration."
    assert "user_123" in content, "user_123 is missing in the configuration."

def test_browser_rendering(start_app):
    reason = "The application should render a button to verify identity."
    truth = "Navigate to http://localhost:3000. Verify that a button with the text 'Verify Identity' exists on the page."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_rendering"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
