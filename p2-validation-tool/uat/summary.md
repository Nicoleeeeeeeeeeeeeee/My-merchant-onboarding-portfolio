# UAT summary

## Scope and evidence

The prototype was tested against 15 cases covering required fields, format validation, document completeness, reset behavior, keyboard access, and mobile layout. The automated rule suite is run with `node tests/validation.test.js` and currently passes 7 assertions. Three defects were found and fixed during self-testing; see `defect-log.csv`.

Three role-based simulated walkthroughs were also completed from the perspectives of an onboarding coordinator, an operations analyst, and a small-business applicant. These are recorded in `simulated-tester-feedback.csv` and are scenario simulations performed by the project author, not feedback from real people.

## Status

- Passed: 15/15 scripted cases in the current self-test run.
- Failed: none remaining after retest.
- Simulated walkthroughs: 3/3 completed; one usability issue maps to fixed defect D-003.
- Deferred: independent review by 2-3 real users. Use `real-tester-feedback-template.csv` if genuine testers become available.

## Honest boundary

This is an independent simulated UAT for a prototype, not production-system UAT. The simulated personas must not be described as real testers. No approval, rejection, suspicious-transaction assessment, or regulated KYC decision is made.

## Portfolio wording

> Conducted an independent simulated UAT for a merchant-onboarding validation prototype; documented requirements, test cases, defects and role-based simulated feedback. This was an independent project, not production-system UAT.
