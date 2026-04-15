# Prembly Widget Integration in Vue 3

## Background
Prembly provides a browser-based widget for identity verification (e.g., Face Liveliness, Document Verification). You need to integrate the `prembly-pass` SDK into a Vue 3 application.

## Requirements
- Initialize a Vue 3 project using Vite.
- Install the `prembly-pass` SDK.
- Create a Vue component that initializes `PremblyPass` with the provided credentials and environment.
- Add a button with the id `launch-widget` that triggers `prembly.launch()`.
- The component should listen for `success` and `error` events and log the result to the console.

## Implementation Guide
1. Initialize a Vue 3 project in `/home/user/app` using Vite (e.g., `npm create vite@latest app -- --template vue` inside `/home/user`, or similar, but the project path must be exactly `/home/user/app`).
2. Install `prembly-pass`.
3. In `src/App.vue`, import `PremblyPass` and initialize it with:
   - `app_id`: `'dummy_app_id'`
   - `x_api_key`: `import.meta.env.VITE_PREMBLY_API_KEY`
   - `environment`: `'test'` (which connects to the sandbox URL https://api.prembly.com)
4. Add a button `<button id="launch-widget">Launch Prembly</button>` that calls the `launch` method with `config_id: 'dummy_config_id'` and a random `user_ref`.
5. Run the app on port 3000.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm run dev -- --port 3000`
- Port: 3000
- You must use the `VITE_PREMBLY_API_KEY` environment variable for the API key.