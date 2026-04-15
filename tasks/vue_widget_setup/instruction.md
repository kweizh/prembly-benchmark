# Prembly Widget Setup in Vue

## Background
Integrate the Prembly (Identitypass) verification widget into a Vue 3 application to perform identity verification.

## Requirements
- Create a Vue 3 application.
- Install the `prembly-pass` SDK.
- Create a component with a button that launches the Prembly widget.
- Handle the `success` and `error` events from the widget by displaying the result on the screen.

## Implementation Guide
1. Initialize a Vue 3 project in `/home/user/vue-prembly-app`.
2. Install the `prembly-pass` package.
3. In `src/App.vue`, add a button with the text 'Verify Identity'.
4. When the button is clicked, instantiate `PremblyPass` with `app_id: 'test_app_id'`, `x_api_key: 'test_public_key'`, and `environment: 'test'`.
5. Call `.launch()` with `config_id: 'test_config_id'` and `user_ref: 'user_123'`.
6. Listen for the `success` event and set a data property `verificationResult` to the `data.verification.reference`. Display this reference in a `div` with id `result`.
7. Listen for the `error` event and set `verificationResult` to `error.message`. Display this in the same `div`.

## Constraints
- Project path: `/home/user/vue-prembly-app`
- Start command: `npm run dev -- --port 3000`
- Port: 3000