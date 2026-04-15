FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/prembly-webhook && chmod -R 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js environment for Prembly webhook signature verification task."

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the Express.js task environment
#   - /home/user/prembly-webhook: empty project directory

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]