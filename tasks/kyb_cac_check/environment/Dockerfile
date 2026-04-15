FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        ffmpeg ripgrep libxcb-shm0 libx11-xcb1 libx11-6 libxcb1 libxext6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libgtk-3-0t64 libpangocairo-1.0-0 libpango-1.0-0 libatk1.0-0t64 libcairo-gobject2 libcairo2 libgdk-pixbuf-2.0-0 libxrender1 libasound2t64 libfreetype6 libfontconfig1 libdbus-1-3 libnss3 libnspr4 libatk-bridge2.0-0t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 libcups2t64 libxshmfence1 libgbm1 && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @getpochi/cli agent-browser && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN agent-browser install

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Prembly KYB CAC Verification App with Node.js v24 and browser verification environment."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    npm init -y && \
    npm install express axios cors

RUN cat > /home/user/mock_server.js <<'EOF'
const express = require('express');
const app = express();
app.use(express.json());

app.post('/verification/cac', (req, res) => {
    if (req.headers['x-api-key'] !== 'test_key' || req.headers['app-id'] !== 'test_id') {
        return res.status(401).json({status: false, detail: "Unauthorized"});
    }
    if (req.body.rc_number === '092932') {
        res.json({
            status: true,
            data: { rc_number: "092932", company_name: "TEST COMPANY", company_status: "Active" }
        });
    } else {
        res.status(404).json({status: false, detail: "Not Found"});
    }
});

app.listen(8080, () => {
    console.log('Mock Prembly server listening on port 8080');
});
EOF

RUN cd /home/user/project && \
    sed -i 's/"test": "echo \\"Error: no test specified\\" && exit 1"/"start": "node server.js"/g' package.json

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the task environment
#   - browser verification dependencies: Pochi CLI, agent-browser, ffmpeg, ripgrep, and more
#   - /home/user/project: base directory for the project, with express and axios installed
#   - /home/user/mock_server.js: mock server for Prembly API

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
