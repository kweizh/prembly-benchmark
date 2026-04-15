import os
import subprocess
import pytest
import json

PROJECT_DIR = "/home/user/project"

def test_verify_js_exists():
    verify_js = os.path.join(PROJECT_DIR, "verify.js")
    assert os.path.isfile(verify_js), f"verify.js not found at {verify_js}"

def test_verify_function_works():
    # We will write a small script to test the verifyNIN function
    test_script_path = os.path.join(PROJECT_DIR, "test_verify.js")
    test_script_content = """
const { verifyNIN } = require('./verify');

async function test() {
    try {
        const result = await verifyNIN('11111111111');
        console.log(JSON.stringify(result));
    } catch (error) {
        console.error(error);
        process.exit(1);
    }
}

test();
"""
    with open(test_script_path, "w") as f:
        f.write(test_script_content)

    # Use real API keys from environment
    env = os.environ.copy()
    
    # Run the test script
    result = subprocess.run(
        ["node", "test_verify.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )
    
    assert result.returncode == 0, f"Running verifyNIN failed: {result.stderr}"
    
    # Check if we got a valid JSON response
    try:
        data = json.loads(result.stdout)
        # We don't strictly check the response content as it might be 'Not Found' or 'Success' depending on sandbox data
        # but it should be a parsed JSON response from the API.
        assert isinstance(data, dict), "Response data should be an object"
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse response as JSON: {result.stdout}")
