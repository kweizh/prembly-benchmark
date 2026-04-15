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
LABEL Description="Next.js environment for Prembly API route proxy task."

RUN cd /home/user && \
    npx create-next-app@14 prembly-app --javascript --no-eslint --no-tailwind --app --no-src-dir --import-alias "@/*" --use-npm

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 installed
#   - /home/user/prembly-app: initialized Next.js application

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
