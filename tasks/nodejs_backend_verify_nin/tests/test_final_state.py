import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "verify_nin.js")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_verify_nin_functionality():
    test_runner = os.path.join(PROJECT_DIR, "test_runner.js")
    with open(test_runner, "w") as f:
        f.write("""
const Module = require('module');
const originalRequire = Module.prototype.require;

Module.prototype.require = function(path) {
    if (path === 'axios') {
        return {
            post: async function(url, data, config) {
                console.log(JSON.stringify({ url, data, config }));
                return { data: { status: "success" } };
            }
        };
    }
    return originalRequire.apply(this, arguments);
};

const { verifyNIN } = require('./verify_nin.js');

(async () => {
    try {
        const result = await verifyNIN('12345678901');
        console.log("RESULT:", JSON.stringify(result));
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
})();
""")
    
    env = os.environ.copy()
    env["PREMBLY_APP_ID"] = "test_app_id"
    env["PREMBLY_API_KEY"] = "test_api_key"
    
    result = subprocess.run(
        ["node", "test_runner.js"],
        cwd=PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Test runner failed: {result.stderr}\\n{result.stdout}"
    
    output = result.stdout
    assert "https://api.prembly.com/verification/nin" in output, "Did not call correct URL."
    assert "12345678901" in output, "Did not pass correct NIN number."
    assert "test_app_id" in output, "Did not pass correct app-id header."
    assert "test_api_key" in output, "Did not pass correct x-api-key header."
    assert "RESULT: {\\"status\\":\\"success\\"}" in output, "Did not return correct data."
