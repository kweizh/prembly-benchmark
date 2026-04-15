# Prembly KYB Service with NestJS

## Background
Prembly provides identity verification APIs, including Business Verification (CAC) for Nigerian companies. You need to build a NestJS service that integrates with Prembly's API to verify company details.

## Requirements
- Create a NestJS application in `/home/user/prembly-kyb`.
- Create a `PremblyService` in a `prembly` module.
- Implement a method `verifyCAC(rcNumber: string, companyName: string)` in `PremblyService`.
- The method should make a POST request to `https://sandbox.myidentitypay.com/api/v2/biometrics/merchant/data/verification/cac` with the payload `{"rc_number": rcNumber, "company_name": companyName}`.
- It must include `app-id` and `x-api-key` headers, reading from `PREMBLY_APP_ID` and `PREMBLY_API_KEY` environment variables.
- Expose a GET endpoint `/verify-cac` in `PremblyController` that accepts `rcNumber` and `companyName` as query parameters and returns the verification result.

## Implementation Guide
1. Initialize a NestJS project in `/home/user/prembly-kyb` using `@nestjs/cli`.
2. Install `@nestjs/axios` and `axios` for making HTTP requests.
3. Generate a module, service, and controller for `prembly`.
4. Inject `HttpService` into `PremblyService` and implement the API call.
5. Use `process.env.PREMBLY_APP_ID` and `process.env.PREMBLY_API_KEY` for headers.

## Constraints
- **Project path**: `/home/user/prembly-kyb`
- **Start command**: `npm run start`
- **Port**: 3000