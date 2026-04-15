# Fintech Wallet Creation Verification

## Background
In a fintech application, before a user can create a wallet, they must verify their identity using their National Identity Number (NIN). You need to implement a backend endpoint that integrates with the Prembly (Identitypass) API to perform this verification.

## Requirements
- Create an Express server with a `POST /api/verify-nin` endpoint.
- The endpoint should accept a JSON body with a `nin` field (e.g., `{"nin": "12345678901"}`).
- It must call the Prembly sandbox API at `https://sandbox.myidentitypay.com/verification/nin` using the `axios` library.
- The Prembly API requires the following headers:
  - `app-id`: `test_app_id`
  - `x-api-key`: `test_api_key`
- The endpoint should return the data received from Prembly API to the client.
- The server must listen on port 3000.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project`.
2. Install `express` and `axios`.
3. Create an `index.js` file and set up the Express server.
4. Implement the `POST /api/verify-nin` endpoint. Make sure to parse the JSON body.
5. Start the server on port 3000.

## Constraints
- Project path: `/home/user/project`
- Start command: `node index.js`
- Port: 3000