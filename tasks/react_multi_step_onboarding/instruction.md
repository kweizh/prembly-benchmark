# React Multi-Step Onboarding with Prembly

## Background
Create a React multi-step onboarding flow where the user first provides a phone number (verified via API) and then performs a Face Liveliness check (verified via Prembly Widget).

## Requirements
- Step 1: A form to input a phone number. Upon submission, it should make a POST request to `/api/verify-phone` (which you must implement as a mock API endpoint returning a success response).
- Step 2: Upon successful phone verification, display the Prembly Pass widget for a Face Liveliness check.
- The widget should be configured with `app_id: "MOCK_APP_ID"`, `x_api_key: "MOCK_PUBLIC_KEY"`, and `config_id: "MOCK_CONFIG_ID"`.
- Upon successful verification from the widget, display a success message: "Verification successful: [reference]".

## Implementation Guide
1. Initialize a React project (e.g., using Vite or Next.js) in `/home/user/onboarding-app`.
2. Install `prembly-pass`.
3. Implement the multi-step flow in the main component.
4. Create the mock API endpoint (if using Next.js) or mock the API call (if using Vite).

## Constraints
- Project path: `/home/user/onboarding-app`
- Start command: `npm run dev`
- Port: `3000`
- The app must handle the `success` event from the Prembly widget and display the reference.