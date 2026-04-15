# NestJS KYB Verification Service with Prembly

## Background
Create a NestJS service that implements a Know Your Business (KYB) verification flow using Prembly's API. The service needs to verify business registration details (e.g., CAC in Nigeria) and handle asynchronous verification results via webhooks.

## Requirements
- POST `/kyb/verify`: Accept business registration number and company type, then call Prembly's Business Verification API.
- POST `/webhook/prembly`: Receive and process Prembly webhooks for verification status updates.
- Securely verify the signature of incoming webhooks to ensure they are genuinely from Prembly.
- Use the `PREMBLY_API_KEY` environment variable for authentication.
- Use the sandbox environment: `https://api.prembly.com`.

## Implementation Guide
1. Initialize a NestJS project in `/home/user/nestjs-kyb`.
2. Install required dependencies like `@nestjs/axios`, `axios`, and any crypto libraries for webhook signature verification.
3. Implement a `KybService` that calls the Prembly API endpoint for business verification.
4. Implement a `WebhookController` that listens for POST requests on `/webhook/prembly`.
5. Implement webhook signature verification using the `x-prembly-signature` header and your webhook secret (which in sandbox is often the same as the API key or a specific webhook secret).

## Constraints
- Project path: /home/user/nestjs-kyb
- Start command: npm run start
- Port: 3000
- The API key should be read from the `PREMBLY_API_KEY` environment variable.
- The Prembly App ID should be read from the `PREMBLY_APP_ID` environment variable.
- The webhook secret should be read from the `PREMBLY_WEBHOOK_SECRET` environment variable (if not set, fallback to `PREMBLY_API_KEY`).

## Integrations
- Prembly