# Prembly Driver's License Verification API

## Background
You need to implement a backend API endpoint that verifies a driver's license using the Prembly API. This is a common requirement for ride-hailing apps or gig economy platforms to ensure the driver's identity is legitimate.

## Requirements
- Create an Express.js server that exposes a `POST /verify-license` endpoint.
- The endpoint should accept a JSON body with a `license_number` field.
- The endpoint must call the Prembly Driver's License verification API to verify the license.
- Return the verification result to the client.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/app`.
2. Install `express` and `axios`.
3. Create an `index.js` file that sets up the Express server.
4. Implement the `POST /verify-license` endpoint.
5. In the endpoint, make a POST request to `https://api.prembly.com/verification/drivers_license` with the payload `{"number": "DXG100"}`.
6. Set the headers `app-id` and `x-api-key` for the Prembly API request using the environment variables `PREMBLY_APP_ID` and `PREMBLY_API_KEY` respectively.
7. Return the data received from Prembly back to the client.
8. Start the server on port 3000.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: 3000
- The server must read `PREMBLY_APP_ID` and `PREMBLY_API_KEY` from the environment.
