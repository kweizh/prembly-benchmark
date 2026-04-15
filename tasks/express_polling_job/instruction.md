# Prembly Express Polling Job

## Background
Prembly (formerly Identitypass) provides identity verification APIs. In some workflows, you need to poll their SDK Session Retrieval endpoint to check the status of a verification session if webhooks are not available.

## Requirements
Create an Express.js application that runs a background job using `setInterval` (every 2 seconds) to poll the Prembly SDK Session Retrieval endpoint for a specific session ID.
- **Endpoint to poll**: `http://localhost:8080/api/v1/sdk/session-retrieval` (A mock server is provided at `/home/user/mock_server`).
- **Headers required**: `app-id: test-app-id` and `x-api-key: test-api-key`.
- **Query Parameters/Body**: Pass `session_id=12345` in the request.
- **Action**: When the background job receives a response with `status: "completed"`, it should append the `verification_data` to a file named `results.json` in the project root and stop polling for that session.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/app`.
2. Install `express` and `axios`.
3. Create `index.js` that sets up a basic Express server on port 3000.
4. Implement the `setInterval` polling logic in `index.js`.

## Constraints
- Project path: `/home/user/app`
- Start command: `node index.js`
- Port: 3000