# Prembly Face Liveliness Integration in React

## Background
Prembly (formerly Identitypass) provides identity verification APIs and SDKs. You need to integrate their Face Liveliness widget into a React application.

## Requirements
- You have a React application at `/home/user/prembly-app`.
- Install the `prembly-pass` library.
- Add a button with the text `Verify Identity` to the main component (`App.jsx`).
- When the button is clicked, it should initialize and launch the `PremblyPass` widget.
- The widget should be configured with:
  - `app_id`: `test_app_id`
  - `x_api_key`: `test_public_key`
  - `environment`: `test`
- The launch configuration should use:
  - `config_id`: `test_config_id`
  - `user_ref`: `user_123`
- When the `success` event is fired, the application should display a success message containing the text `Verification successful: ` followed by the verification reference.
- When the `error` event is fired, the application should display an error message containing the text `Verification failed: ` followed by the error.

## Implementation Guide
1. Go to `/home/user/prembly-app`.
2. Install the `prembly-pass` package.
3. Edit `src/App.jsx` to include the button and the `PremblyPass` logic.
4. Ensure the component renders correctly and listens to `success` and `error` events from `PremblyPass`.
5. Start the application on port 3000.

## Constraints
- Project path: `/home/user/prembly-app`
- Start command: `npm run dev -- --port 3000 --host`
- Port: 3000