import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/prembly-widget"
INDEX_HTML = os.path.join(PROJECT_DIR, "index.html")

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
        ["python3", "-m", "http.server", "3000"],
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
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"Expected index.html to exist at {INDEX_HTML}."

def test_index_html_content():
    with open(INDEX_HTML) as f:
        content = f.read()
    assert "PremblyPass" in content, "Expected 'PremblyPass' in index.html."
    assert "YOUR_APP_ID" in content, "Expected 'YOUR_APP_ID' in index.html."
    assert "YOUR_PUBLIC_KEY" in content, "Expected 'YOUR_PUBLIC_KEY' in index.html."
    assert "YOUR_CONFIG_ID_FROM_DASHBOARD" in content, "Expected 'YOUR_CONFIG_ID_FROM_DASHBOARD' in index.html."

def test_browser_widget_button(start_app):
    reason = "The application must display a 'Verify Identity' button with id 'verify-btn'. Clicking the button must attempt to launch the Prembly widget."
    truth = "Navigate to http://localhost:3000. Verify that a button with id 'verify-btn' is visible. Click the button and verify that the page attempts to load the Prembly iframe or shows a Prembly-related error/modal, indicating the widget launch logic was triggered."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_widget_button"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
