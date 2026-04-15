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

RUN mkdir -p /home/user/vue-prembly-app/src && chmod -R 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Vue 3 task environment with Node.js v24 installed, including the browser verification environment."

RUN cd /home/user/vue-prembly-app && \
    cat > package.json <<'PKG'
{
  "name": "vue-prembly-app",
  "version": "0.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
PKG

RUN cd /home/user/vue-prembly-app && \
    cat > vite.config.js <<'VITE'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()]
})
VITE

RUN cd /home/user/vue-prembly-app && \
    cat > index.html <<'HTML'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
HTML

RUN cd /home/user/vue-prembly-app && \
    cat > src/main.js <<'MAIN'
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
MAIN

RUN cd /home/user/vue-prembly-app && \
    cat > src/App.vue <<'APP'
<template>
  <div>
    <h1>Prembly Widget Setup</h1>
  </div>
</template>

<script setup>
</script>
APP

RUN cd /home/user/vue-prembly-app && npm install

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the Vue task environment
#   - browser verification dependencies: Pochi CLI, agent-browser, ffmpeg, ripgrep, and more
#   - /home/user/vue-prembly-app: initialized Vue 3 project

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
