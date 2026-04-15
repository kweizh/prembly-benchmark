FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Prembly Rate Limit Handler Express.js Environment"

RUN mkdir -p /home/user/prembly-app && \
    cd /home/user/prembly-app && \
    npm init -y && \
    npm install express axios

RUN cat << 'EOF' > /home/user/mock-server.js
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/verification/nin') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'success', message: 'NIN verified' }));
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

server.listen(3001, () => {
  console.log('Mock server listening on port 3001');
});
EOF

RUN cat << 'EOF' > /home/user/prembly-app/server.js
const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// TODO: Implement /api/verify endpoint with rate limiting

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
EOF

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
