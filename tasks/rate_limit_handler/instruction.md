# Prembly Rate Limit Handler

## Background
Prembly provides identity verification APIs. To prevent abuse and manage costs, you need to implement a rate limit handler for a Node.js Express application that calls the Prembly NIN verification API.

## Requirements
- Build an Express.js server that exposes a `POST /api/verify` endpoint.
- The endpoint accepts a JSON body with `user_id` and `nin` (e.g., `{ "user_id": "user123", "nin": "12345678901" }`).
- Implement a rate limiter that allows a maximum of 3 verification attempts per `user_id` within a 15-minute window.
- If the limit is exceeded, the endpoint must return an HTTP 429 Too Many Requests status code with a JSON response `{"error": "Too many verification attempts"}`.
- If the limit is not exceeded, the endpoint should call the Prembly API at `http://localhost:3001/verification/nin` (a local mock server provided in the environment) using a POST request with the `number` field in the body (`{"number": "..."}`) and the headers `app-id: test-app` and `x-api-key: test-key`. It should then return the Prembly API response to the client.

## Implementation
1. The project is located at `/home/user/prembly-app`.
2. The project has already been initialized with `package.json` and dependencies (`express`, `axios`).
3. Create or modify `server.js` to implement the requirements.
4. The Express server must listen on port 3000.

## Constraints
- Project path: `/home/user/prembly-app`
- Start command: `node server.js`
- Port: 3000
- Mock Prembly API URL: `http://localhost:3001`