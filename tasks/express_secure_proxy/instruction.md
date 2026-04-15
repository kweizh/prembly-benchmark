# Prembly Secure Backend Proxy

## Background
Prembly provides identity verification widgets. To securely integrate the widget without exposing sensitive API keys in the frontend code, we need a backend proxy that serves the configuration to the frontend dynamically.

## Requirements
Create a Node.js Express secure backend proxy that hides the `x-api-key` from the frontend while still allowing the Prembly widget to function by securely returning a `config_id` to the frontend.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/proxy`.
2. Install `express` and `cors`.
3. Create `server.js` that sets up an Express server.
4. Create a `GET /api/config` endpoint that returns a JSON object with `app_id` and `config_id` from environment variables `PREMBLY_APP_ID` and `PREMBLY_CONFIG_ID`.
5. Ensure the server listens on port 3000.

## Constraints
- Project path: `/home/user/proxy`
- Start command: `node server.js`
- Port: 3000