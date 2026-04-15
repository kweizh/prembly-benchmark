# Prembly Pass Vanilla HTML Widget

## Background
You need to integrate the Prembly Pass widget into a vanilla web application to handle identity verification.

## Requirements
- Initialize a vanilla JS project using Vite in `/home/user/app`.
- Install `prembly-pass`.
- Create a simple UI with a button to launch the Prembly verification widget.
- Initialize `PremblyPass` with `app_id` as `test_app_id` and `x_api_key` from the `PREMBLY_API_KEY` environment variable. Ensure the environment is set to `test` and uses the Prembly sandbox URL (`https://api.prembly.com`).
- Configure it with `config_id` as `test_config_id` and a unique `user_ref`.
- Listen for `success` and `error` events, and log the results to the console or display them on the screen.

## Implementation Guide
1. Run `npm create vite@latest /home/user/app -- --template vanilla`.
2. `cd /home/user/app` and `npm install`.
3. Install the SDK: `npm install prembly-pass`.
4. Edit `main.js` to import and configure `PremblyPass`.
5. Add a button in `index.html` to trigger the widget launch.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm run dev -- --host 0.0.0.0 --port 3000`
- Port: 3000
- Read the API key from the environment variable `PREMBLY_API_KEY`.

## Integrations
- None