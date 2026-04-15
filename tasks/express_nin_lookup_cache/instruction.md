# Prembly NIN Lookup Cache

## Background
Create a Node.js Express server that implements a cached NIN lookup using the Prembly API. It should check an in-memory cache before calling the API to save costs and reduce latency.

## Requirements
- Create an Express server listening on port 3000.
- Implement a `GET /nin/:number` endpoint.
- On request, check an in-memory cache (e.g., a simple JavaScript object or Map) for the given NIN.
- If found in cache, return the cached result immediately.
- If not found, call the Prembly NIN verification endpoint via POST to `${PREMBLY_BASE_URL}/verification/nin` with body `{"number": "<NIN>"}`.
- Use the `PREMBLY_BASE_URL` environment variable for the API base URL (default to `https://api.prembly.com` if not set).
- Store the successful result in the cache before returning it.
- Handle errors gracefully.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/prembly_cache`.
2. Install `express` and `axios`.
3. Create an `index.js` file with the Express server and cache logic.
4. Use the following headers for the Prembly API call:
   - `app-id`: `TEST_APP_ID`
   - `x-api-key`: `TEST_API_KEY`
5. Ensure the server listens on port 3000.

## Constraints
- Project path: `/home/user/prembly_cache`
- Start command: `node index.js`
- Port: 3000
