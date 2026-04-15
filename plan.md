# Prembly (Identitypass) Evaluation Dataset Research
Prembly (formerly Identitypass) is a leading compliance and security infrastructure provider specializing in identity verification, KYC (Know Your Customer), and KYB (Know Your Business) for emerging markets (Africa, APAC, LATAM, EMEA).
### 1. Library Overview
*   **Description**: Prembly provides a suite of APIs and SDKs to verify individuals, businesses, and documents. It abstracts the complexity of connecting to various government databases and performing biometric checks.
*   **Ecosystem Role**: It acts as the "Stripe for Identity" in its target regions, offering a unified interface for diverse verification needs (e.g., NIN in Nigeria, KRA in Kenya, BVN, etc.).
*   **Project Setup**:
    1.  **Dashboard**: Create an account at [Prembly Dashboard](https://dashboard.prembly.com/) to obtain an `app-id` and `x-api-key`.
    2.  **SDK Installation (React/Web)**: `npm install prembly-pass`
    3.  **SDK Configuration**: Create a "New SDK" on the dashboard to generate a `config_id` for the widget/browser-based validation.
    4.  **Environment**: Use `https://api.prembly.com` for api calls.
### 2. Core Primitives & APIs
*   **Data Verification**: Direct lookup of government IDs (NIN, BVN, Drivers License, etc.).
*   **Document Verification**: OCR and authenticity checks on uploaded ID images.
*   **Biometrics (Face Liveliness)**: Ensuring the user is a real person via browser-based camera capture.
*   **Business Verification**: Verifying company registration details (CAC, BRS, etc.).
*   **Webhooks**: Asynchronous notifications for verification results.
#### Basic API Usage (Backend/Node.js)
```javascript
const axios = require('axios');
const verifyNIN = async (ninNumber) => {
  const response = await axios.post('https://api.prembly.com/verification/nin', {
    number: ninNumber
  }, {
    headers: {
      'app-id': 'YOUR_APP_ID',
      'x-api-key': 'YOUR_SECRET_KEY'
    }
  });
  return response.data;
};
```
#### Browser Validation (The Widget/SDK)
The "Prembly Pass" widget handles the UI for liveness and document capture.
```javascript
import { PremblyPass } from "prembly-pass";
const prembly = new PremblyPass({
  app_id: "YOUR_APP_ID",
  x_api_key: "YOUR_PUBLIC_KEY", // Use public/sandbox key for frontend
  environment: "test"
});
prembly.on("success", (data) => {
  console.log("Verification successful:", data.verification.reference);
});
prembly.on("error", (error) => {
  console.error("Verification failed:", error);
});
// Trigger the widget
prembly.launch({
  config_id: "YOUR_CONFIG_ID_FROM_DASHBOARD",
  user_ref: "unique_user_id_123"
});
```
*   **Documentation**: [Prembly SDK Guide](https://docs.prembly.com/docs/new-sdk.md)
### 3. Real-World Use Cases & Templates
*   **Fintech Onboarding**: Verifying user identity (NIN/BVN) and performing a face liveliness check before allowing wallet creation.
*   **Gig Economy Verification**: Verifying driver's licenses and vehicle plate numbers for ride-hailing apps.
*   **Corporate Compliance (KYB)**: Verifying business registration and UBO (Ultimate Beneficial Owner) details during B2B onboarding.
*   **Integration Pattern**: Frontend triggers the Widget -> User completes verification -> Prembly sends Webhook to Backend -> Backend updates user status.
### 4. Developer Friction Points
1.  **Webhook Verification**: Developers often struggle to securely verify that incoming webhooks are legitimately from Prembly, leading to security vulnerabilities.
2.  **Sandbox Data Limitations**: The sandbox environment requires specific "test data" (e.g., specific NIN numbers) to return successful results; using random numbers often leads to confusing "Not Found" errors. [Sandbox Docs](https://docs.prembly.com/docs/environment.md)
3.  **Config ID Dependency**: The browser widget requires a `config_id` created via the dashboard UI, which is a manual step that can't be easily automated in CI/CD pipelines.
### 5. Evaluation Ideas
*   **Implementation**: Create a React component that triggers the Prembly Widget and handles the `success` callback.
*   **Integration**: Build a Node.js Express server that receives Prembly webhooks and verifies their signature.
*   **Logic**: Implement a "Retry Verification" flow that only allows a user to retry 3 times if the document verification fails.
*   **System Design**: Set up a background job that polls the `SDK Session Retrieval` endpoint for pending verifications that haven't sent a webhook.
*   **Security**: Implement a secure backend proxy that hides the `x-api-key` from the frontend while still allowing the widget to function.
*   **Complex Flow**: Build a multi-step onboarding where the user first provides a phone number (verified via API) and then performs a Face Liveliness check (verified via Widget).
### 6. Sources
1.  [Prembly Official Documentation](https://docs.prembly.com/): Primary source for API and SDK details.
2.  [Prembly llms.txt](https://docs.prembly.com/llms.txt): Structured overview of all documentation pages.
3.  [NPM: prembly-pass](https://www.npmjs.com/package/prembly-pass): Official React/Web SDK package details.
4.  [GitHub: prembly-java](https://github.com/prembly/prembly_java): Reference for backend SDK patterns and sandbox URLs.
5.  [Prembly Face Liveliness Docs](https://docs.prembly.com/docs/face-livelinness-check): Details on biometric verification.
6.  [Prembly Webhooks Guide](https://docs.prembly.com/docs/webhooks): Details on asynchronous response handling.
