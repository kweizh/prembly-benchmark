# Secure Backend Proxy for Prembly

## Background
Prembly (Identitypass) provides APIs for identity verification. To secure our integration, we need to implement a backend proxy using Express.js that hides our API credentials (`app-id` and `x-api-key`) from the frontend while forwarding requests to the Prembly sandbox.

## Requirements
- Create an Express server that acts as a proxy.
- All requests to `/api/prembly/*` should be forwarded to `https://api.prembly.com/*`.
- The proxy must automatically inject the `app-id` and `x-api-key` headers from the `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables.
- The proxy must forward the request method, body, and query parameters correctly.
- The server must listen on port 3000.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/proxy-app`.
2. Install `express` and any necessary proxy middleware (like `http-proxy-middleware` or `axios`).
3. Create an `index.js` file that sets up the Express server.
4. Implement the proxy logic for the `/api/prembly/*` route.

## Constraints
- Project path: /home/user/proxy-app
- Start command: `node index.js`
- Port: 3000

## Integrations
- None