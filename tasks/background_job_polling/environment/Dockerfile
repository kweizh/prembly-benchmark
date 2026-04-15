FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project && chmod 0755 /home/user /home/user/project

# Pre-install nock for tests
RUN cd /home/user/project && \
    npm init -y && \
    npm install nock axios

LABEL Author="any-task-builder"
LABEL Description="Node.js environment for Prembly API polling script."

# Container contents:
#   - Node.js v24 installed
#   - /home/user/project directory created with nock pre-installed

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
