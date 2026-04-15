# Prembly React Document Verification Retry

## Background
Prembly (formerly Identitypass) provides a widget for document verification. You need to create a React component that triggers the Prembly Widget and implements a retry flow that only allows a user to retry 3 times if the verification fails.

## Requirements
- Create a React component that imports and uses `PremblyPass` from `prembly-pass`.
- The component should have a button "Start Verification" that launches the widget.
- When the widget triggers an `error` event, increment a retry counter.
- The user should be allowed to retry up to 3 times.
- If the user fails 3 times, disable the button and show a message "Maximum retries reached".
- If the verification succeeds (`success` event), show a message "Verification successful" and hide the button.

## Implementation Guide
1. The project is located at `/home/user/prembly-app`.
2. The project is a React application (created with Vite).
3. You need to implement the logic in `/home/user/prembly-app/src/App.jsx`.
4. Use dummy credentials for PremblyPass:
   ```javascript
   import { PremblyPass } from "prembly-pass";
   // Inside your component:
   const startVerification = () => {
     const prembly = new PremblyPass({
       app_id: "dummy_app_id",
       x_api_key: "dummy_api_key",
       environment: "test"
     });
     prembly.on("success", (data) => { /* handle success */ });
     prembly.on("error", (error) => { /* handle error */ });
     prembly.launch({
       config_id: "dummy_config_id",
       user_ref: "dummy_user_ref"
     });
   };
   ```

## Constraints
- Project path: `/home/user/prembly-app`
- Start command: `npm run dev`
- Port: 5173