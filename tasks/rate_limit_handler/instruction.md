# Prembly API Rate Limit Handler

## Background
You are building a Node.js backend that integrates with Prembly (Identitypass) to verify National Identity Numbers (NIN). The Prembly API may occasionally return a `429 Too Many Requests` status code when rate limits are exceeded. You need to implement an exponential backoff retry mechanism to handle this gracefully.

## Requirements
- Initialize a Node.js Express application in `/home/user/app`.
- Create a `POST /verify-nin` endpoint that accepts a JSON body with a `nin` string (e.g., `{"nin": "12345678901"}`).
- The endpoint must call the Prembly NIN API using the base URL from the `PREMBLY_BASE_URL` environment variable (defaulting to `https://api.prembly.com`) and the path `/verification/nin`.
- Pass the `app-id` and `x-api-key` headers using the `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables.
- Implement an exponential backoff retry mechanism for the Prembly API call: if the API returns a 429 status code, retry the request up to 3 times. Wait 100ms before the first retry, 200ms before the second, and 400ms before the third.
- If the request succeeds, return the Prembly API response with a 200 status code.
- If the request still fails with a 429 after 3 retries, return a 429 status code to the client with the message `"Rate limit exceeded, please try again later"`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/app`.
2. Install `express` and `axios`.
3. Create an `index.js` that sets up the Express server on `process.env.PORT` or port 3000.
4. Implement the `POST /verify-nin` endpoint with the retry logic.
5. Ensure the server parses JSON request bodies.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: `process.env.PORT` or 3000
- Log file: `/home/user/app/output.log`
- Use `axios` for HTTP requests.