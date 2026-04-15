# Prembly BVN Verification API

## Background
Prembly provides identity verification APIs. You need to create an Express.js REST API that acts as a proxy to Prembly's BVN (Bank Verification Number) validation endpoint.

## Requirements
- Create an Express server listening on port 3000.
- Implement a `POST /verify-bvn` endpoint that accepts a JSON body: `{"bvn": "string"}`.
- The endpoint must call Prembly's BVN verification API: `POST {PREMBLY_BASE_URL}/verification/bvn_validation`
- The request to Prembly must include the following headers:
  - `app-id`: value from the `PREMBLY_APP_ID` environment variable.
  - `x-api-key`: value from the `PREMBLY_API_KEY` environment variable.
- The request body to Prembly must be: `{"number": "<the_bvn_from_client>"}`.
- Return the exact JSON response received from Prembly back to the client.
- If `PREMBLY_BASE_URL` is not set in the environment, default it to `https://api.prembly.com`.

## Implementation
1. Initialize a Node.js project in `/home/user/prembly_bvn`.
2. Install `express` and `axios`.
3. Create `index.js` implementing the server and endpoint.

## Constraints
- **Project path**: `/home/user/prembly_bvn`
- **Start command**: `node index.js`
- **Port**: 3000
