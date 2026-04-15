FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/prembly-webhook && chmod 0755 /home/user /home/user/prembly-webhook

LABEL Author="any-task-builder"
LABEL Description="Prembly Webhook Fastify Server environment with Node.js v24 installed."

# Container contents:
#   - Node.js v24 installed
#   - /home/user/prembly-webhook empty directory created for project initialization

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
