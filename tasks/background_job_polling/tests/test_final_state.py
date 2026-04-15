import os
import subprocess
import json

def test_poll_js_fetches_pending_sessions():
    project_dir = "/home/user/project"
    poll_js_path = os.path.join(project_dir, "poll.js")
    
    assert os.path.exists(poll_js_path), "poll.js was not created."
    
    # We will create a test wrapper to intercept the HTTPS request using nock
    wrapper_js = """
const nock = require('nock');
const fs = require('fs');

const mockResponse = {
  "status": true,
  "message": "Sessions retrieved successfully",
  "data": {
    "sessions": [
      {
        "id": "1",
        "session_id": "sess_1_in_progress",
        "status": "in_progress"
      },
      {
        "id": "2",
        "session_id": "sess_2_completed",
        "status": "completed"
      },
      {
        "id": "3",
        "session_id": "sess_3_in_progress",
        "status": "in_progress"
      }
    ],
    "pagination": { "total": 3, "page": 1, "page_size": 10, "total_pages": 1 }
  }
};

const scope = nock('https://api.prembly.com')
  .get('/api/v1/checker-widget/sdk/sessions/')
  .reply(function(uri, requestBody) {
    if (this.req.headers['x-api-key'] !== 'test_api_key') {
      return [401, { error: 'Invalid x-api-key' }];
    }
    if (this.req.headers['app-id'] !== 'test_app_id') {
      return [401, { error: 'Invalid app-id' }];
    }
    return [200, mockResponse];
  });

// Run the user's script
require('./poll.js');

// Set a timeout to ensure we don't exit too early if something hangs
setTimeout(() => {
    if (!scope.isDone()) {
        console.error('Nock scope was not called. Did the script make the right request?');
        process.exit(1);
    }
}, 2000);
"""
    
    wrapper_path = os.path.join(project_dir, "test_wrapper.js")
    with open(wrapper_path, "w") as f:
        f.write(wrapper_js)
        
    # Remove existing pending_sessions.txt if any
    output_file = os.path.join(project_dir, "pending_sessions.txt")
    if os.path.exists(output_file):
        os.remove(output_file)
        
    env = os.environ.copy()
    env["PREMBLY_API_KEY"] = "test_api_key"
    env["PREMBLY_APP_ID"] = "test_app_id"
    
    # Run the wrapper
    result = subprocess.run(["node", "test_wrapper.js"], cwd=project_dir, env=env, capture_output=True, text=True)
    
    assert os.path.exists(output_file), f"pending_sessions.txt was not created. Output: {result.stdout} {result.stderr}"
    
    with open(output_file, "r") as f:
        content = f.read()
        
    assert "sess_1_in_progress" in content, f"Missing first in_progress session. File content: {content}"
    assert "sess_3_in_progress" in content, f"Missing second in_progress session. File content: {content}"
    assert "sess_2_completed" not in content, f"Included a completed session, which should be filtered out. File content: {content}"
