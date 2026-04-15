# Next.js API Route Proxy for Prembly

## Background
Create a Next.js API route that acts as a secure proxy to the Prembly NIN verification API, hiding the API key from the frontend.

## Requirements
- Initialize a Next.js project in `/home/user/app`.
- Create an API route `POST /api/verify-nin` that accepts a JSON body with a `number` field.
- The route should call the Prembly NIN verification API (`https://api.prembly.com/api/v1/verification/nin` or `https://api.prembly.com/verification/nin` according to the documentation) using the `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables.
- Set the headers `app-id` and `x-api-key` appropriately.
- Return the JSON response from Prembly to the client.
- The API route must handle errors appropriately.

## Implementation Guide
1. Initialize a Next.js project in `/home/user/app` using `npx create-next-app@latest app --javascript --eslint --tailwind --app --src-dir --use-npm`.
2. Create the API route in `src/app/api/verify-nin/route.js`.
3. Implement the POST handler to read the `number` from the request body.
4. Make a POST request to the Prembly sandbox API using `fetch` or `axios`.
5. Return the response to the client.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm run build && npm start`
- Port: 3000
- Use `https://api.prembly.com` as the base URL for the Prembly API.

## Integrations
- Prembly