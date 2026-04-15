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
LABEL Description="Node.js environment for implementing a Prembly webhook verification server."

RUN mkdir -p /home/user/prembly-webhook && \
    cd /home/user/prembly-webhook && \
    npm init -y

# Container contents:
#   - curl, python3, pytest, git
#   - Node.js v24 installed
#   - /home/user/prembly-webhook initialized with package.json

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
