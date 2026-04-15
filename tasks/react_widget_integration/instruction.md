# Prembly React Widget Integration

## Background
Prembly (Identitypass) provides a browser-based widget to verify individuals via a face liveliness check and document capture. You need to integrate the `prembly-pass` SDK into a React application to launch the verification widget.

## Requirements
- Initialize a React application using Vite.
- Install the `prembly-pass` SDK.
- Create a component `PremblyWidget.jsx` that initializes `PremblyPass` with specific credentials.
- The component should have a button with the text `Verify Identity` that triggers the widget launch.
- The widget must be configured to handle `success` and `error` events, logging the results to the console.

## Implementation
1. Initialize a React project in `/home/user/prembly-app` using Vite (e.g., `npm create vite@latest . -- --template react`).
2. Install `prembly-pass`.
3. Create `src/PremblyWidget.jsx`.
4. In `PremblyWidget.jsx`, instantiate `PremblyPass` with:
   - `app_id`: `test_app_id`
   - `x_api_key`: `test_public_key`
   - `environment`: `test`
5. Add event listeners for `success` (logging `Verification successful: <data.verification.reference>`) and `error` (logging `Verification failed: <error>`).
6. Add a button that calls `prembly.launch()` with:
   - `config_id`: `test_config_id`
   - `user_ref`: `user_123`
7. Render `PremblyWidget` in `src/App.jsx`.

## Output
- Project path: `/home/user/prembly-app`
- Start command: `npm run dev`
- Port: 5173