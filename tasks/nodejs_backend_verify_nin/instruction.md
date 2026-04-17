# Node.js Backend Verification for NIN

## Background
Prembly provides identity verification APIs. You need to implement a Node.js function that verifies a National Identity Number (NIN) using their API.

## Requirements
- Create a Node.js script `verify.js` in `/home/user/project`.
- The script should export a function `verifyNIN(ninNumber)` that makes a POST request to the Prembly verification endpoint for NIN.
- Use the sandbox URL: `https://api.prembly.com/api/v1/verification/nin` (or similar depending on the exact Prembly sandbox path, but for this task, use `https://api.prembly.com/verification/vnin` as per documentation).
- Use the `axios` library to make the request.
- The function must use the `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables for the `app-id` and `x-api-key` headers respectively.
- The function should return the `data` object from the API response.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project`.
2. Install `axios`.
3. Create `verify.js` and implement the `verifyNIN` function as described.
4. Export the function using `module.exports = { verifyNIN };`.

## Constraints
- Project path: /home/user/project
- Use `axios` for HTTP requests.
