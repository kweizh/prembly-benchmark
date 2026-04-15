# Prembly Webhook Handler with Fastify

## Background
Prembly (Identitypass) sends asynchronous webhooks to notify your backend when an identity verification completes. You need to create a Fastify server that receives these webhooks securely and updates a mock database.

## Requirements
- Create a Fastify server in `/home/user/prembly-webhook`.
- Implement a `POST /webhook` endpoint.
- **Signature Verification**: Prembly sends an `x-identitypass-signature` header with each webhook. This header contains the base64 encoded value of your webhook secret. You must verify that this header exactly matches the base64 encoded value of the `WEBHOOK_SECRET` environment variable. If the header is missing or invalid, return HTTP 401 Unauthorized.
- **Webhook Processing**: If the signature is valid, parse the JSON body. The body will have a `data.verification_id` field. You must update an in-memory mock database (a simple JavaScript object) to mark that `verification_id` as `{ verified: true }`.
- Return HTTP 200 OK after successful processing.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/prembly-webhook`.
2. Install `fastify`.
3. Create an `index.js` file that sets up the Fastify server on port 3000.
4. Define the mock database variable in memory: `const db = {};`
5. Implement the `POST /webhook` route.
6. Add a `GET /status/:id` route to retrieve the verification status from the mock database, returning `{ verified: true }` or `{ verified: false }`.

## Constraints
- Project path: `/home/user/prembly-webhook`
- Start command: `node index.js`
- Port: 3000
- The environment variable `WEBHOOK_SECRET` will be provided.