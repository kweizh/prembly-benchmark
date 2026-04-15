# Prembly SDK Session Polling

## Background
Prembly handles identity verifications. Sometimes, webhooks for the widget verification might not be received or processed correctly. To ensure no verification is missed, you need to implement a background job that polls the SDK Session Retrieval endpoint to find pending verifications.

## Requirements
- Create a Node.js script `poll.js` in `/home/user/project`.
- The script should fetch data from the Prembly SDK Session Retrieval endpoint: `https://api.prembly.com/api/v1/checker-widget/sdk/sessions/`.
- It must use the `PREMBLY_APP_ID` environment variable for the `app-id` header and `PREMBLY_API_KEY` for the `x-api-key` header.
- The script should fetch the first page of sessions.
- For every session where `status` is `"in_progress"`, write the `session_id` to a file named `/home/user/project/pending_sessions.txt`, one per line.
- The script should run once and exit (no need for `setInterval` for this evaluation).

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project` if not already done.
2. Install `axios` or use the native `fetch` API.
3. Write the `poll.js` script to make a GET request to the endpoint.
4. Parse the JSON response (`response.data.data.sessions`).
5. Filter the sessions where `status === 'in_progress'`.
6. Append each matching `session_id` to `/home/user/project/pending_sessions.txt`.

## Constraints
- Project path: `/home/user/project`
- Start command: `node poll.js`
- Do not hardcode the API keys; read them from `process.env`.