# Prembly Webhook Signature Verification

## Background
Create an Express.js server that receives Prembly webhooks and securely verifies their signature. Prembly sends webhooks with an `x-prembly-signature` header containing a Base64 encoded HMAC-SHA256 hash of the request body, using your API key as the secret. Verifying this signature is critical to ensure the webhook is legitimately from Prembly and hasn't been tampered with.

## Requirements
- Initialize a Node.js project and install `express`.
- Create a POST `/webhook` endpoint that accepts JSON payloads.
- The endpoint must capture the raw request body to verify the signature.
- Compute the HMAC-SHA256 hash of the raw request body using the `PREMBLY_API_KEY` environment variable as the secret key.
- Base64 encode the computed hash.
- Compare the computed signature with the `x-prembly-signature` header.
- If the signatures match, respond with `200 OK` and `{"status": "success"}`.
- If the signatures do NOT match or the header is missing, respond with `401 Unauthorized` and `{"error": "Invalid signature"}`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/prembly-webhook`.
2. Install `express`.
3. Create an `index.js` file.
4. Use `express.raw({ type: 'application/json' })` middleware for the `/webhook` route to ensure you have the exact raw body for signature verification.
5. Implement the signature computation using Node's built-in `crypto` module (`crypto.createHmac('sha256', process.env.PREMBLY_API_KEY).update(req.body).digest('base64')`).
6. Compare the signatures securely.
7. Start the server on port 3000.

## Constraints
- Project path: `/home/user/prembly-webhook`
- Start command: `npm start` (ensure this is defined in package.json)
- Port: `3000`
- The server must read the secret key from the `PREMBLY_API_KEY` environment variable.

## Integrations
- None required for this specific task.