# Fastify Webhook Handler for Prembly

## Background
Prembly sends asynchronous webhook notifications when verifications are completed. To ensure the security of your endpoint, you must verify the `x-prembly-signature` header included in every webhook request. This signature is an HMAC-SHA256 hash of the raw request payload, generated using your Prembly Public Key.

## Requirements
- Create a Fastify server that listens on `POST /webhook`.
- The server must read the raw request body to compute the HMAC-SHA256 signature using the secret key provided in the `PREMBLY_API_KEY` environment variable.
- Compare the computed signature (base64 encoded) with the `x-prembly-signature` header.
- If the signature is missing, invalid, or does not match, respond with HTTP status `401 Unauthorized` and `{"error": "Invalid signature"}`.
- If the signature is valid, process the webhook (you can just respond with HTTP status `200 OK` and `{"status": "received"}`).

## Implementation Guide
1. Initialize a Node.js project in `/home/user/app`.
2. Install `fastify` and `fastify-raw-body` (or handle raw body manually) to ensure you have the exact raw payload for signature verification.
3. Create `server.js` that sets up the Fastify server and the `/webhook` route.
4. Implement the HMAC-SHA256 verification logic using Node's built-in `crypto` module.

## Constraints
- **Project path**: `/home/user/app`
- **Start command**: `npm start`
- **Port**: 3000
- You must use `fastify`.
- The signature must be computed as a Base64 encoded HMAC-SHA256 string of the raw payload using `PREMBLY_API_KEY`.

## Integrations
- None required for this specific webhook receiver task.