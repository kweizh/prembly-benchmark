# Prembly Webhook Server

## Background
You need to build a Node.js Express server that can securely receive webhooks from Prembly. Developers often struggle to securely verify that incoming webhooks are legitimately from Prembly, leading to security vulnerabilities.

## Requirements
- Create an Express.js server that listens for POST requests on `/webhook`.
- The server must verify the webhook signature using the `x-prembly-signature` header.
- Prembly generates the signature by computing the HMAC-SHA256 of the raw request payload using your API key, and then Base64 encodes it.
- Implement a middleware that computes the HMAC-SHA256 (Base64 encoded) of the raw request body using the API key from the `PREMBLY_API_KEY` environment variable and compares it to the `x-prembly-signature` header.
- If the signature is valid, respond with HTTP status 200 and a JSON body `{"status": "success"}`.
- If the signature is invalid or missing, respond with HTTP status 401 and a JSON body `{"error": "Invalid signature"}`.

## Implementation Guide
1. You have a directory at `/home/user/prembly-webhook`. Initialize a Node.js project in it.
2. Install `express`.
3. Create `server.js` that sets up the Express app and the `/webhook` endpoint.
4. Ensure the raw request body is used for signature verification.

## Constraints
- Project path: `/home/user/prembly-webhook`
- Start command: `node server.js`
- Port: 3000
- Use `PREMBLY_API_KEY` from the environment for signature verification.
- Assume the Prembly sandbox URL is in `PREMBLY_SANDBOX_URL` (https://api.prembly.com) for any future API call needs.