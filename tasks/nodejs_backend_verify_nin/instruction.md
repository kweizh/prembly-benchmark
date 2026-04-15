# Prembly NIN Verification

## Background
Prembly (formerly Identitypass) provides a suite of APIs for identity verification. We need a Node.js script to verify a Nigerian National Identity Number (NIN) using their backend API.

## Requirements
- Create a Node.js script `verify_nin.js` that exports an async function `verifyNIN(ninNumber)`.
- The function must use `axios` to make a POST request to `https://api.prembly.com/verification/nin`.
- It must pass the NIN number in the request body as `{ "number": ninNumber }`.
- It must include the headers `app-id` and `x-api-key`, reading them from the environment variables `PREMBLY_APP_ID` and `PREMBLY_API_KEY` respectively.
- It must return the `data` object from the response.

## Implementation
1. Initialize a Node.js project in `/home/user/myproject`.
2. Install `axios`.
3. Create `/home/user/myproject/verify_nin.js` with the required implementation.

## Constraints
- Project path: `/home/user/myproject`
- Start command: `node verify_nin.js`
- Port: N/A