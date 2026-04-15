# Prembly Webhook Idempotency

## Background
Prembly (Identitypass) sends asynchronous webhooks to notify your backend of verification results. In distributed systems, webhooks can sometimes be delivered more than once. It is critical to implement idempotency to ensure that a single verification result does not trigger duplicate business logic (e.g., updating a user's verification status multiple times).

## Requirements
- Create a Node.js Express server that listens for POST requests on `/webhook/prembly`.
- The webhook payload will contain a `webhook_id` (string) and `verification_status` (string).
- Implement an SQLite database to store processed `webhook_id`s.
- When a webhook is received, check if the `webhook_id` has already been processed.
- If it has, return a `200 OK` immediately without processing it again.
- If it has not, save the `webhook_id` to the database, process it (e.g., update a mock user status), and return a `200 OK`.
- The server must handle concurrent duplicate requests gracefully.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/prembly-webhook`.
2. Install `express` and `sqlite3`.
3. Create `server.js` and set up the Express app and SQLite database (e.g., a table `processed_webhooks` with `webhook_id` as PRIMARY KEY).
4. Implement the POST `/webhook/prembly` endpoint with the idempotency logic.
5. Ensure the server listens on port 3000.

## Constraints
- Project path: `/home/user/prembly-webhook`
- Start command: `node server.js`
- Port: 3000