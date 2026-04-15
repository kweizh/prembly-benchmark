# Multi-Step Onboarding with Prembly

## Background
You need to implement a multi-step onboarding flow for a fintech application using Prembly (Identitypass). The flow consists of a phone number verification API call followed by a Face Liveliness check using the Prembly browser widget.

## Requirements
- Create a Node.js Express server that serves a static HTML page.
- **Step 1: Phone Verification API**: Implement a `POST /api/verify-phone` endpoint that accepts a phone number and uses the Prembly API (`https://api.prembly.com/verification/phone`) to verify it. Return the API response.
- **Step 2: Face Liveliness Widget**: On the frontend (HTML page), provide a form to input a phone number. After successful verification via the backend endpoint, display the Prembly Pass widget (`prembly-pass`) to perform a Face Liveliness check.
- Use the `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables for backend API calls.
- Use the provided `config_id` for the widget initialization on the frontend.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/onboarding`.
2. Install `express`, `axios`, and `prembly-pass`.
3. Create an `server.js` that sets up the Express server on port 3000 and serves static files from a `public` directory.
4. Create `public/index.html` with the onboarding UI.
5. Implement the backend route to call the Prembly API.

## Constraints
- Project path: `/home/user/onboarding`
- Start command: `node server.js`
- Port: 3000
- The frontend should initialize the widget using a placeholder `config_id` if one is not provided.

## Integrations
- Prembly API and Widget