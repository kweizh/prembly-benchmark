FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="prembly-benchmark"
LABEL Description="Node.js environment for Prembly webhook signature verification task."

RUN mkdir -p /home/user/prembly-webhook

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24
#   - /home/user/prembly-webhook  — empty directory for the task

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
