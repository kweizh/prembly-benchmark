# Prembly Face Liveliness with React

## Background
You have a basic React application initialized at `/home/user/app`. You need to integrate the Prembly Pass widget to perform a Face Liveliness check.

## Requirements
- Install the `prembly-pass` library.
- Create a `FaceLiveliness` React component in `src/FaceLiveliness.js`.
- The component should have a button with the id `verify-btn` that, when clicked, launches the Prembly Pass widget.
- Initialize `PremblyPass` with `app_id` from the environment variable `PREMBLY_APP_ID`, `x_api_key` from `PREMBLY_API_KEY`, and set `environment` to `'test'` (or the sandbox URL `https://api.prembly.com` if required by the SDK).
- Launch the widget with `config_id` from `PREMBLY_CONFIG_ID` and `user_ref` as `'user_123'`.
- On successful verification, the component should render a `div` with the id `success-message` containing the text 'Verification successful'.
- Update `src/App.js` to render the `FaceLiveliness` component.
- Ensure the environment variables are correctly passed to your React app (e.g., by creating a `.env` file with `REACT_APP_PREMBLY_APP_ID`, etc., if using Create React App).

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: 3000

## Integrations
- Prembly