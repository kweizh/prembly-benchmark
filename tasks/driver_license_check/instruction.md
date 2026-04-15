# Prembly Driver License Verification API

## Background
We are building a ride-hailing application and need to verify the driver's license of our drivers using the Prembly API.

## Requirements
Create an Express REST API that acts as a proxy to the Prembly Drivers License V2 API.
- Endpoint: `POST /verify`
- Request Body: JSON object containing `number`, `first_name`, and `last_name`.
- Action: The endpoint should make a POST request to the Prembly sandbox API (`https://sandbox.myidentitypay.com/verification/drivers_license/advance/v2`) with the provided data.
- Headers: The request to Prembly must include the `app-id` and `x-api-key` headers, which should be read from the `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables respectively.
- Response: The endpoint should return the exact JSON response received from the Prembly API with the same HTTP status code.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/ride_app`.
2. Install `express` and `axios`.
3. Create an `index.js` file that sets up the Express server and implements the `/verify` endpoint.
4. Ensure the server listens on port 3000.
5. Add a `start` script to `package.json` that runs `node index.js`.

## Constraints
- Project path: `/home/user/ride_app`
- Start command: `npm start`
- Port: 3000