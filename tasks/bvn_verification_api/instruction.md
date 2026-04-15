# BVN Verification API with Prembly

## Background
You need to build a Node.js Express server that verifies a Bank Verification Number (BVN) using Prembly's API.

## Requirements
- Initialize a Node.js project in `/home/user/app`.
- Create an Express server with a POST endpoint at `/verify-bvn`.
- The endpoint should accept a JSON body with a `bvn` field.
- It must call Prembly's BVN verification API using the sandbox environment (`https://api.prembly.com/verification/bvn`).
- Provide the `app-id` and `x-api-key` headers using the environment variables `PREMBLY_APP_ID` and `PREMBLY_API_KEY`.
- The endpoint should return the data received from Prembly.
- Implement proper error handling.

## Implementation Guide
1. `cd /home/user/app` and run `npm init -y`.
2. Install `express` and `axios`.
3. Create an `index.js` file that sets up the Express server.
4. Implement the POST `/verify-bvn` endpoint to forward requests to the Prembly BVN verification API.
5. Ensure the server listens on port 3000.

## Constraints
- Project path: /home/user/app
- Start command: `npm start` (ensure this is defined in package.json to run `node index.js`)
- Port: 3000
- Use `https://api.prembly.com` as the base URL.

## Integrations
- None