import os
import subprocess
import time
import socket
import pytest

try:
    from pochi_verifier import PochiVerifier
except ImportError:
    PochiVerifier = None

PROJECT_DIR = "/home/user/vue-prembly-app"

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
        ["npm", "run", "dev", "--", "--port", "3000"],
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
        pytest.fail("App failed to start and listen on required ports.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_vue_code_implementation():
    app_vue_path = os.path.join(PROJECT_DIR, "src", "App.vue")
    assert os.path.isfile(app_vue_path), "src/App.vue does not exist."
    
    with open(app_vue_path, "r") as f:
        content = f.read()
        
    assert "prembly-pass" in content, "prembly-pass is not imported in App.vue."
    assert "PremblyPass" in content, "PremblyPass is not used in App.vue."
    assert "test_app_id" in content, "test_app_id is not configured."
    assert "test_public_key" in content, "test_public_key is not configured."
    assert "test_config_id" in content, "test_config_id is not passed to launch()."
    assert "user_123" in content, "user_123 is not passed to launch()."
    assert "id=\"result\"" in content or "id='result'" in content, "div with id 'result' is missing."

@pytest.mark.skipif(PochiVerifier is None, reason="pochi_verifier not available")
def test_browser_interaction(start_app):
    reason = "The Vue application should display a 'Verify Identity' button."
    truth = "Navigate to http://localhost:3000. Verify that a button with the text 'Verify Identity' is visible on the page. Click the button. Verify that a div with id 'result' exists on the page."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_interaction"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
