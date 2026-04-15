# Express NIN Lookup Cache

## Background
You need to build a simple Express.js API that verifies National Identity Numbers (NIN) using the Prembly API. To reduce API costs and improve response times, you must implement an in-memory cache for the verification results.

## Requirements
- Create an Express.js server with a POST endpoint at `/api/verify-nin`.
- The endpoint should accept a JSON body with a `nin` field.
- Make a POST request to the Prembly sandbox API: `https://api.prembly.com/verification/nin` with a JSON body `{"number": "<nin>"}`.
- The Prembly API requires `app-id` and `x-api-key` headers. Use the environment variables `PREMBLY_APP_ID` and `PREMBLY_API_KEY` for these.
- If the `nin` has been verified previously, return the cached result immediately.
- Cache the successful response data and return it to the client.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/nin-cache`.
2. Install `express` and `axios`.
3. Create an `index.js` that sets up the Express server.
4. Implement the `/api/verify-nin` endpoint with the caching logic and Prembly API integration.
5. The server should listen on port 3000.

## Constraints
- Project path: /home/user/nin-cache
- Start command: node index.js
- Port: 3000

## Integrations
- Prembly