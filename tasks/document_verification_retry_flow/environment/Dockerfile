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
LABEL Description="Node.js environment for building a Prembly retry flow API."

RUN mkdir -p /home/user/prembly-retry-app && \
    cd /home/user/prembly-retry-app && \
    npm init -y && \
    npm install express axios && \
    cat >index.js <<'EOF'
const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

app.post('/verify', async (req, res) => {
    // Implement logic here
    res.status(501).json({ error: "Not implemented" });
});

app.listen(3000, () => console.log('Server running on port 3000'));
EOF
    
# Container contents:
#   - Node.js v24 installed
#   - /home/user/prembly-retry-app - Express project with axios installed
#   - Boilerplate index.js

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
