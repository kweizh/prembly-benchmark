# Secure Prembly Webhook Verification

## Background
Prembly sends webhooks to notify your application of asynchronous verification results. Because Prembly webhooks do not currently include a cryptographic signature header, developers must securely verify the authenticity of the webhook payload to prevent spoofing attacks.

## Requirements
Create an Express.js server that:
1. Exposes a `POST /webhook` endpoint to receive Prembly webhooks.
2. Extracts the `verification.reference` from the incoming webhook payload.
3. Makes a secure server-to-server `GET` request to Prembly's `Get Verification Status` API (`<PREMBLY_API_URL>/verification/{reference}/status`) using the `x-api-key` header to confirm the webhook is legitimate.
4. If the API returns `status: true` and the `verification_status` matches the webhook's `verification.status`, respond with `200 OK` and write the verified data to `verified_webhooks.json`.
5. If the API call fails or the status does not match, respond with `403 Forbidden`.

## Implementation Guide
1. The project is located at `/home/user/prembly-webhook`.
2. Install `express` and `axios`.
3. Create `server.js` with the Express app listening on port 3000.
4. Read the Prembly API key from the `PREMBLY_SECRET_KEY` environment variable.
5. Read the Prembly API URL from the `PREMBLY_API_URL` environment variable (default to `https://api.prembly.com`).
6. Implement the `/webhook` endpoint as described.

## Constraints
- Project path: `/home/user/prembly-webhook`
- Start command: `node server.js`
- Port: 3000