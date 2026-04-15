FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js environment with a mock Prembly API server for testing SDK Session Retrieval polling."

RUN mkdir -p /home/user/app && \
    mkdir -p /home/user/mock_server && \
    cd /home/user/mock_server && \
    cat >package.json <<'EOF'
{
  "name": "mock-server",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.19.2"
  }
}
EOF

RUN cd /home/user/mock_server && \
    cat >index.js <<'EOF'
const express = require('express');
const app = express();
const port = 8080;

app.use(express.json());

let requestCount = 0;

app.get('/api/v1/sdk/session-retrieval', (req, res) => {
  const appId = req.headers['app-id'];
  const apiKey = req.headers['x-api-key'];
  const sessionId = req.query.session_id;

  if (appId !== 'test-app-id' || apiKey !== 'test-api-key') {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (sessionId !== '12345') {
    return res.status(404).json({ error: 'Session not found' });
  }

  requestCount++;
  
  if (requestCount < 3) {
    return res.json({ status: 'pending' });
  } else {
    return res.json({ status: 'completed', verification_data: { document: 'verified', name: 'John Doe' } });
  }
});

app.listen(port, () => {
  console.log(`Mock server listening on port ${port}`);
});
EOF

RUN cd /home/user/mock_server && npm install

# Container contents:
#   - Node.js v24 installed
#   - /home/user/app: Empty directory for the task
#   - /home/user/mock_server: Mock API server configured to return pending then completed status

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]