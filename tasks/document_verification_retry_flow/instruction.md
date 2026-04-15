# Prembly Verification Retry Flow

## Background
When integrating identity verification with Prembly, users might fail verification due to incorrect data or poor image quality. To prevent abuse and manage costs, you need to limit the number of times a user can attempt verification.

## Requirements
Build an Express.js REST API that enforces a strict 3-retry limit for Prembly NIN verification.

- **Endpoint**: `POST /verify`
- **Payload**: JSON `{ "nin": "string", "userId": "string" }`
- **Logic**:
  1. Call the Prembly NIN verification API at `https://sandbox.myidentitypay.com/verification/nin`.
  2. Pass headers `app-id: process.env.PREMBLY_APP_ID` and `x-api-key: process.env.PREMBLY_API_KEY`.
  3. If the Prembly API call fails (e.g., returns 404 or 400), increment the failure count for that `userId`.
  4. If a `userId` reaches 3 failed attempts, any further requests for that `userId` must immediately return HTTP 403 with JSON `{ "error": "Max retries exceeded" }` and MUST NOT call the Prembly API.
  5. If the Prembly API call succeeds (HTTP 200), reset the failure count for that `userId` and return the success data.

## Implementation Guide
1. A basic Express app is provided in `/home/user/prembly-retry-app/index.js`.
2. Implement the in-memory store for tracking retries per `userId`.
3. Implement the `POST /verify` endpoint using `axios`.

## Constraints
- **Project path**: `/home/user/prembly-retry-app`
- **Start command**: `npm start`
- **Port**: 3000
