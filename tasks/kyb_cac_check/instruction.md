# Prembly KYB CAC Verification App

## Background
Create a simple web application to verify Nigerian business registration (CAC) details using the Prembly Identitypass API.

## Requirements
- **Backend**: An Express.js server that exposes a `POST /api/verify` endpoint.
- **Frontend**: A simple HTML page served at `/` with a form to input an RC number and select a company type.
- **Integration**: The backend must call the Prembly API (mocked locally) to perform the verification.

## Implementation
1. You have a Node.js project initialized at `/home/user/project`.
2. In `server.js`, set up an Express app to serve static files from a `public` directory.
3. Create `public/index.html` with:
   - An input field with `id="rc-input"` for the RC number.
   - A select dropdown with `id="type-select"` containing options `RC`, `BN`, and `IT`.
   - A button with `id="verify-btn"` to trigger the check.
   - Divs with `id="result-name"` and `id="result-status"` to display the company name and status.
4. Write frontend JavaScript to send a POST request to your backend `/api/verify` when the button is clicked, sending `{ "rc_number": "...", "company_type": "..." }`.
5. In your backend `/api/verify` endpoint, make a POST request to the local Prembly mock API at `http://localhost:8080/verification/cac`.
   - Send the `rc_number` and `company_type` in the request body.
   - Include headers: `x-api-key: test_key` and `app-id: test_id`.
6. Return the `data.company_name` and `data.company_status` from the Prembly response to the frontend, which then populates the `result-name` and `result-status` divs.

## Constraints
- **Project path**: `/home/user/project`
- **Start command**: `npm start` (which should run `node server.js`)
- **Port**: 3000
- **Prembly Mock URL**: `http://localhost:8080/verification/cac`