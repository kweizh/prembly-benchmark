# Prembly Webhook Signature Verification Middleware

## Background
Prembly (Identitypass) sends asynchronous webhook events when verifications complete. To ensure these webhooks are legitimately from Prembly and haven't been tampered with, you need to verify the webhook signature.

## Requirements
Create an Express.js middleware function that verifies incoming Prembly webhooks.
- The middleware should check for the `x-identitypass-signature` header.
- It must compute the HMAC SHA256 hash of the raw request body using the `PREMBLY_SECRET_KEY` environment variable.
- The computed hash must be compared against the `x-identitypass-signature` header.
- If the signature matches, call `next()` to proceed to the route handler.
- If the signature is missing or does not match, return a `401 Unauthorized` status with a JSON response `{"error": "Invalid signature"}`.

## Implementation Guide
1. Project path: `/home/user/app`
2. The project already has `express` installed and a basic server setup in `index.js`.
3. Create the middleware in a file named `middleware.js` and export it.
4. Apply the middleware to a POST endpoint `/webhook` in `index.js` that responds with `200 OK` and `{"status": "received"}` if successful.
5. Start command: `npm start`
6. Port: 3000

## Constraints
- Ensure you capture the raw body for HMAC computation. If using `express.json()`, you may need to configure it to preserve the raw body or compute the hash before JSON parsing alters it.
- Use the `crypto` module built into Node.js.