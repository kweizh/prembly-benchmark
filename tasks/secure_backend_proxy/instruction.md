# Secure Backend Proxy for Prembly

## Background
When integrating Prembly (Identitypass) APIs, using the secret `x-api-key` on the frontend exposes it to users. To secure the integration, we need a backend proxy that safely stores the API key and handles requests to Prembly APIs.

## Requirements
- Create an Express REST API with an endpoint `POST /api/verify/nin`.
- The endpoint should accept `ninNumber` in the request body.
- It should make a POST request to the Prembly sandbox API (`https://sandbox.myidentitypay.com/api/v2/biometrics/merchant/data/verification/nin`) with the `app-id` and `x-api-key` headers attached.
- The backend should return the Prembly API response to the client.
- The frontend (already provided in `/home/user/app/public/index.html`) should call this backend endpoint instead of calling Prembly directly.

## Implementation
1. Initialize an Express application in `/home/user/app`.
2. Install `express`, `cors`, and `axios`.
3. Create `server.js` that listens on port 3000.
4. Define the `POST /api/verify/nin` endpoint.
5. Read the `PREMBLY_APP_ID` and `PREMBLY_SECRET_KEY` from environment variables.
6. Serve static files from the `public` directory.

## Constraints
- **Project path**: /home/user/app
- **Start command**: npm start
- **Port**: 3000