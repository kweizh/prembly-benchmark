# Prembly KYB Business Verification

## Background
You need to implement a Node.js script that verifies a business registration using the Prembly API. The script should use the Prembly sandbox environment.

## Requirements
- Create a Node.js script `verify_business.js` in `/home/user/project`.
- The script should take a registration number as a command-line argument.
- It should make a POST request to the Prembly sandbox API (`https://api.prembly.com/api/v1/biometrics/merchant/data/verification/cac` - assuming this is the CAC endpoint, or use the appropriate endpoint if you know it, but let's assume `https://api.prembly.com/api/v1/biometrics/merchant/data/verification/cac` for CAC check, or just generic `https://api.prembly.com/api/v1/biometrics/merchant/data/verification/cac_advance`). Wait, let's keep it simpler: The task is to write a script that sends a POST request to `https://api.prembly.com/api/v1/biometrics/merchant/data/verification/cac` with the provided registration number.
- The request must include headers `app-id` and `x-api-key` read from environment variables `PREMBLY_APP_ID` and `PREMBLY_API_KEY` respectively.
- The body should be JSON containing `{"company_type": "RC", "rc_number": "<registration_number>"}`.
- The script should write the JSON response to `/home/user/project/output.json`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project` and install `axios`.
2. Write the `verify_business.js` script to read the registration number from `process.argv[2]`.
3. Make the axios POST request with the required headers and body to the sandbox URL.
4. Save the response data to `output.json`.

## Constraints
- Project path: `/home/user/project`
- Log file: `/home/user/project/output.json`
- Use `https://api.prembly.com` as the base URL.

## Integrations
- None