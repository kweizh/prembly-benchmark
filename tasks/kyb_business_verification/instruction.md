# Prembly KYB Verification API

## Background
Implement a B2B onboarding backend using Prembly to verify company registration details (CAC) in Nigeria.

## Requirements
- Create a Node.js project in `/home/user/onboarding_api`.
- Install `express` and `axios`.
- Create an `index.js` that sets up an Express server.
- Implement a `POST /verify-business` endpoint that accepts a JSON body with `registration_number`.
- The endpoint must call Prembly's API using the base URL provided in the `PREMBLY_BASE_URL` environment variable (default to `https://sandbox.myidentitypay.com`). The path is `/api/v1/verification/cac`.
- The request body to Prembly should be `{ "company_number": "<registration_number>" }`.
- Pass the `app-id` and `x-api-key` headers using `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables.
- Return the data from the Prembly API response to the client with the same HTTP status code.

## Implementation
1. `mkdir -p /home/user/onboarding_api && cd /home/user/onboarding_api`
2. `npm init -y`
3. `npm install express axios`
4. Write `index.js`.

## Constraints
- Project path: `/home/user/onboarding_api`
- Start command: `node index.js`
- Port: 3000