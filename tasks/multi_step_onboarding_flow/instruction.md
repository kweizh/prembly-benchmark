# Multi-Step Onboarding with Prembly

## Background
Build a multi-step onboarding flow using Prembly (Identitypass). The user first provides a phone number which is verified via the Prembly backend API, and then performs a Face Liveliness check using the Prembly Pass widget on the frontend.

## Requirements
1. Initialize a Node.js project in `/home/user/onboarding_app`.
2. Install `express`, `axios`, and `prembly-pass`.
3. Create an Express server (`server.js`) that serves static files from a `public` directory.
4. Implement a `POST /api/verify-phone` endpoint in `server.js` that accepts `{"phone": "number"}` and calls the Prembly API at `https://sandbox.myidentitypay.com/verification/phone` with headers `app-id` and `x-api-key` (use environment variables `PREMBLY_APP_ID` and `PREMBLY_SECRET_KEY`). Return success if the API returns a 200 status.
5. Create `public/index.html` with a form to submit the phone number. On success from `/api/verify-phone`, use the `prembly-pass` SDK to launch the widget for Face Liveliness with `config_id` from `PREMBLY_CONFIG_ID` and the public key from `PREMBLY_PUBLIC_KEY`.

## Constraints
- Project path: `/home/user/onboarding_app`
- Start command: `node server.js`
- Port: 3000