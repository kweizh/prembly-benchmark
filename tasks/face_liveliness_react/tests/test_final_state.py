import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/app"

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
    # Pass necessary environment variables to the app, mapping them to REACT_APP_ prefix
    # just in case the user relied on the environment rather than a .env file.
    env = os.environ.copy()
    env["REACT_APP_PREMBLY_APP_ID"] = env.get("PREMBLY_APP_ID", "")
    env["REACT_APP_PREMBLY_API_KEY"] = env.get("PREMBLY_API_KEY", "")
    env["REACT_APP_PREMBLY_CONFIG_ID"] = env.get("PREMBLY_CONFIG_ID", "")

    # Start the app
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        env=env,
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
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_face_liveliness_react(start_app):
    reason = "The React application should have a button that launches the Prembly Pass widget."
    truth = "Navigate to http://localhost:3000. Verify that a button with id `verify-btn` is visible. Click the `verify-btn` button. Verify that the Prembly Pass widget iframe or modal is added to the document."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_face_liveliness_react"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
