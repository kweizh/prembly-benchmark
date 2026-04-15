# Secure Prembly API Proxy in Next.js

## Background
You are building a frontend application that needs to verify Nigerian National Identity Numbers (NIN) using the Prembly API. To avoid exposing your `app-id` and `x-api-key` to the client, you need to create a Next.js API route that proxies the request to Prembly.

## Requirements
- Create a Next.js API route at `app/api/verify-nin/route.js` (using App Router) that accepts a POST request with a JSON body containing `{ "number": "<NIN>" }`.
- The API route must forward this request to the Prembly NIN endpoint (`https://api.prembly.com/verification/nin`).
- The API route must attach the `app-id` and `x-api-key` headers to the Prembly request. These values must be read from the environment variables `PREMBLY_APP_ID` and `PREMBLY_API_KEY`.
- The API route must return the exact JSON response received from Prembly to the client.
- If `PREMBLY_BASE_URL` is set in the environment, use it instead of `https://api.prembly.com` for the base URL. This is useful for testing with a mock server.

## Constraints
- Project path: `/home/user/prembly-app`
- Start command: `npm run dev`
- Port: 3000