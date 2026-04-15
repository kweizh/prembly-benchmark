# Prembly SDK Session Poller

## Background
Prembly provides identity verification services. Sometimes, webhooks for verification results are missed or delayed. To ensure robustness, you need to create a background job that polls the Prembly SDK Session Retrieval endpoint to process pending verification sessions that have completed but haven't been processed yet.

## Requirements
Write a Node.js script `poll_sessions.js` in `/home/user/prembly_poller` that does the following:
1. Fetches sessions from the Prembly SDK Session Retrieval endpoint.
2. Filters the retrieved sessions for those where `status` is `"completed"` and `is_used` is `false`.
3. For each matching session, sends a POST request to a local webhook processor at `http://localhost:3000/webhook` with the session object as the JSON body.
4. The script should execute this logic once when run.

## Implementation Guide
1. Navigate to `/home/user/prembly_poller`.
2. Install `axios`.
3. Create `poll_sessions.js`.
4. Read `APP_ID` and `X_API_KEY` from environment variables.
5. Read the base API URL from the `PREMBLY_API_URL` environment variable, defaulting to `https://api.prembly.com` if not set. The endpoint path is `/api/v1/checker-widget/sdk/sessions/`.
6. Use `axios.get` to fetch the sessions with the headers `app-id` and `x-api-key`.
7. Parse the response (`response.data.data.sessions`), filter it, and send a `POST` request to `http://localhost:3000/webhook` for each valid session.

## Constraints
- Project path: `/home/user/prembly_poller`
- Start command: `node poll_sessions.js`
- Ensure you handle the request headers correctly as per Prembly documentation (`app-id` and `x-api-key`).