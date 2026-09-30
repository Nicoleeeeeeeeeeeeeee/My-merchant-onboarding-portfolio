# One-page requirements: Merchant Onboarding Validation Tool

## Objective

Provide a small, deterministic prototype that checks whether an onboarding application is complete before it is routed to an authorised reviewer. It is a simulated learning project, not a production onboarding or KYC system.

## User and workflow

An onboarding coordinator enters merchant details, selects the available document checklist items, and submits the form. The tool shows missing required fields, field-format errors, outstanding checklist items, and one of three statuses.

## Rules and acceptance criteria

1. Registered name, business registration number, business type, country, contact name, email, and expected monthly volume are required.
2. Email must match a basic `name@domain` pattern.
3. Business registration number must be exactly eight digits.
4. Expected monthly volume must be a positive number.
5. All three checklist items are required for `READY_FOR_COMPLETENESS_REVIEW`.
6. Missing fields or format errors produce `INCOMPLETE`.
7. Complete fields with missing checklist items produce `DOCUMENTS_OUTSTANDING`.
8. The tool never approves/rejects a merchant and does not assess suspicious activity.
9. No values are persisted or sent to a server.

## Out of scope

Identity verification, beneficial-owner determination, sanctions screening, transaction monitoring, document upload, authentication, production integrations, and any real customer data.
