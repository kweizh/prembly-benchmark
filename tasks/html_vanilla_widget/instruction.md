# Prembly Pass Widget in Vanilla JS

## Background
Implement the Prembly Pass widget in a plain HTML/Vanilla JS file, handling success and error callbacks.

## Requirements
- Create an `index.html` file that includes a button with id `verify-btn`.
- Import and initialize the `PremblyPass` widget (e.g., via CDN like `https://esm.sh/prembly-pass` or a bundler if you prefer).
- Initialize it with `app_id: "YOUR_APP_ID"`, `x_api_key: "YOUR_PUBLIC_KEY"`, and `environment: "test"`.
- Add an event listener to the `verify-btn` to call `prembly.launch()` with `config_id: "YOUR_CONFIG_ID_FROM_DASHBOARD"` and `user_ref: "unique_user_id_123"`.
- Handle the `success` callback by setting the innerText of a div with id `result` to "Verification successful".
- Handle the `error` callback by setting the innerText of the same div to "Verification failed".

## Implementation Guide
1. Work in `/home/user/prembly-widget`.
2. Create `index.html`.
3. Make sure to serve the directory on port 3000.

## Constraints
- Project path: `/home/user/prembly-widget`
- Start command: `python3 -m http.server 3000`
- Port: 3000