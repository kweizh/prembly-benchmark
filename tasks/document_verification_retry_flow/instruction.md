# Prembly Document Verification Retry Flow

## Background
You are building an onboarding flow for a fintech application using React and the `prembly-pass` SDK. You need to implement a document verification step that allows a maximum of 3 retries if the verification fails.

## Requirements
- Create a simple React application that integrates the `prembly-pass` SDK.
- The application should have a button "Start Verification" that launches the Prembly widget.
- If the verification fails (the `error` event is triggered), the user should be allowed to retry up to 3 times.
- Keep track of the retry count. Display the current number of attempts remaining on the screen (e.g., "Attempts remaining: 3").
- If the verification succeeds (`success` event), display a success message: "Verification successful!".
- If the user fails 3 times, disable the "Start Verification" button and display an error message: "Maximum retries exceeded. Please contact support.".

## Implementation Guide
1. Initialize a React project in `/home/user/app` using Vite.
2. Install the `prembly-pass` SDK (`npm install prembly-pass`).
3. In `src/App.jsx`, implement the retry logic.
4. Initialize `PremblyPass` with `app_id: import.meta.env.VITE_PREMBLY_APP_ID`, `x_api_key: import.meta.env.VITE_PREMBLY_API_KEY`, and `environment: "test"`. You can also configure the base URL to `https://api.prembly.com` if needed.
5. Use `import.meta.env.VITE_PREMBLY_CONFIG_ID` for the `config_id` when calling `launch()`.

## Constraints
- Project path: /home/user/app
- Start command: npm run dev -- --port 3000
- Port: 3000
- The environment variables will be provided at runtime.

## Integrations
- None