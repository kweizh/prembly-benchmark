# Fintech Wallet Creation with Prembly

## Background
You are building a fintech onboarding flow. To create a wallet, a user must verify their identity using Prembly (Identitypass). The flow involves verifying a National Identity Number (NIN) and performing a face liveliness check before allowing wallet creation.

## Requirements
- Implement a Node.js backend to handle the wallet creation API.
- Create an endpoint `POST /api/wallet/create` that accepts `ninNumber` and `faceLivelinessRef`.
- The endpoint must first verify the NIN using Prembly's `POST https://api.prembly.com/verification/nin` (use `https://api.prembly.com/verification/nin` for testing).
- If the NIN is valid, it should verify the face liveliness session using Prembly's SDK Session Retrieval or a mock endpoint if not available in sandbox, but let's assume the NIN verification is the primary backend check. For this task, only implement the NIN verification on the backend.
- Use the `PREMBLY_APP_ID` and `PREMBLY_API_KEY` from environment variables.
- If verification succeeds, return `201 Created` with `{"wallet_id": "new_wallet_123"}`. If it fails, return `400 Bad Request`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/fintech-app`.
2. Install `express` and `axios`.
3. Create `index.js` that sets up the Express server on port 3000.
4. Implement the `POST /api/wallet/create` endpoint.
5. Call the Prembly sandbox API: `POST https://api.prembly.com/verification/nin` with the `number` from the request body. Pass `app-id` and `x-api-key` headers.
6. Start the server using `npm start`.

## Constraints
- Project path: /home/user/fintech-app
- Start command: npm start
- Port: 3000
- The server must read `PREMBLY_APP_ID` and `PREMBLY_API_KEY` from the environment.

## Integrations
- Prembly