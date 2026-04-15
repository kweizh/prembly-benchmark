# Prembly Webhook Verification Server

## Background
Prembly sends asynchronous webhooks to notify your backend about verification results (e.g., when a document verification is completed). To ensure these webhooks are legitimately from Prembly and haven't been tampered with, you must verify the webhook signature.

## Requirements
Create a Node.js Express server that listens for Prembly webhooks and verifies their HMAC SHA512 signatures.
- **Endpoint**: POST `/webhook`
- **Signature Header**: `x-prembly-signature`
- **Secret Key**: `test_secret_key_123`
- **Logic**:
  - Compute the HMAC SHA512 hash of the raw request body using the secret key.
  - Compare the computed hash to the `x-prembly-signature` header.
  - If valid, return HTTP 200 with JSON `{"status": "success"}`.
  - If invalid or missing, return HTTP 401 with JSON `{"status": "error", "message": "Invalid signature"}`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/prembly-webhook`.
2. Install `express`.
3. Create `index.js` setting up the Express server.
4. Ensure you parse the raw body correctly to compute the HMAC SHA512 signature using Node's built-in `crypto` module.
5. Add a `start` script to `package.json` that runs `node index.js`.

## Constraints
- Project path: `/home/user/prembly-webhook`
- Start command: `npm start`
- Port: 3000