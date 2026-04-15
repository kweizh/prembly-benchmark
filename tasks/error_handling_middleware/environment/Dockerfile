FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash jq && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js project with Express installed for Prembly webhook middleware task."

RUN mkdir -p /home/user/app && \
    cd /home/user/app && \
    npm init -y && \
    npm install express && \
    jq '.scripts.start = "node index.js"' package.json > package.json.tmp && mv package.json.tmp package.json && \
    cat >index.js <<'EOF'
const express = require('express');
const app = express();
const port = 3000;

// TODO: Import and use the Prembly webhook middleware
// const premblyMiddleware = require('./middleware');
// app.post('/webhook', premblyMiddleware, (req, res) => {
//   res.json({ status: "received" });
// });

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
EOF

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/app - Node.js project directory.
#   - express installed in /home/user/app.
#   - index.js with a basic Express server setup.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]