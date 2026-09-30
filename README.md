# Merchant onboarding operations portfolio

This project is a practical review of a fictional merchant-onboarding process. It follows a merchant from lead intake through qualification, approval and activation, then looks at early activity after activation. The purpose is to show how I would turn an operational question into a traceable analysis, a usable report and a small validation workflow.

All records are synthetic. They were generated with a fixed seed and contain no customer, identity-document, bank-account, employer-internal or production-system data.

## Business context

An onboarding team needs to answer four straightforward questions:

1. Where do merchants leave the funnel?
2. Which acquisition or merchant groups need attention?
3. How long does it take to reach activation?
4. Are the hand-offs and completeness checks clear enough for operations to act on?

The work is intentionally framed as an operational diagnostic. It does not pretend that a dashboard alone can explain causality, make a KYC decision or replace an authorised compliance process.

## Business requirements

The project translates the questions above into measurable outputs:

- Count merchants at each funnel stage using distinct merchant IDs.
- Compare activation by acquisition channel, merchant segment, business type and lead-date cohort.
- Measure median lead-to-activation time instead of relying only on averages.
- Track monthly activity after activation as a retention proxy.
- Let a user filter the report by lead date, channel, segment and business type.
- Make the numbers auditable against SQL outputs and source-level quality checks.
- Validate onboarding completeness without approving or rejecting a merchant.
- Show who owns a hand-off, what happens when an SLA is missed and when an authorised review is required.

## What I built

### P1: Funnel diagnostics

The data model has one merchant-level table and two event/activity tables:

- `Merchants`: lead attributes and the latest onboarding outcome
- `FunnelEvents`: one row per merchant-stage event
- `MonthlyActivity`: one row per merchant-month after activation

The analysis produces a 1,200-lead funnel. In the current sample, 562 merchants activate, giving a 46.8% lead-to-activation rate. Median time to activate is 12 days. Paid Search plus Micro merchants have a 36.3% activation rate, compared with 52.0% for Partner plus Micro merchants.

I treat that last comparison as a prioritisation signal. It is not a causal claim. A sensible next step would be assisted qualification for the lower-performing group, followed by a controlled comparison with approval controls unchanged.

The technical work includes:

- SQL schema creation and data-quality checks
- Cleaning inconsistent casing and whitespace in raw channel and segment values
- Funnel conversion queries
- CTE and window-function analysis for activation time
- Cohort retention analysis using monthly activity
- Channel and segment comparisons
- CSV extracts for reconciliation
- An Excel review workbook for quick inspection
- A Power BI report with DAX measures, two pages and four slicers

The four slicers are lead date, acquisition channel, merchant segment and business type. They allow an interviewer or reviewer to move from the overall funnel to a specific operating segment without changing the underlying model.

### P2: Simulated UAT validation tool

The second project addresses a different operational risk: an incomplete application being routed to the next reviewer.

The browser prototype checks required fields, email format, registration-number format, positive expected monthly volume and three required checklist items. It returns `INCOMPLETE`, `DOCUMENTS_OUTSTANDING` or `READY_FOR_COMPLETENESS_REVIEW`.

The tool deliberately stops at completeness. It does not approve or reject merchants, assess suspicious activity, perform identity verification or persist data. The repository includes requirements, test cases, defect records, simulated feedback and automated rule tests.

### P3: Client lifecycle learning case

The third project maps the operating boundary around a hypothetical corporate onboarding case. It separates intake and completeness work from authorised compliance review. The tracker covers document gaps, completeness review, compliance review, activation pending and periodic review due.

An SLA breach or non-standard ownership structure creates an escalation reason. It does not create an informal override. This distinction matters in a controlled onboarding process: the operations team can record evidence and route an exception, while an authorised reviewer makes the regulated decision.

## Technology and working method

| Area | Tools and approach |
|---|---|
| Data generation | Python standard library, deterministic seed |
| Data storage | CSV and SQLite during analysis |
| Data analysis | SQL, CTEs, window functions and cohort logic |
| Reporting | Power BI Desktop and DAX; Excel review workbook |
| Validation | HTML, CSS and vanilla JavaScript; Node-based rule tests |
| Process design | Mermaid, CSV case tracker and Markdown control memo |
| Quality control | Reproducible scripts, row-count checks, data-quality assertions and reconciliation outputs |

The working pattern is simple: define the grain, validate the source, calculate metrics, reconcile results, then write an operational recommendation with an owner, measure and guardrail. This keeps the business conclusion tied to something that can be checked.

## Evidence and results

The repository contains the source CSVs, SQL files, generated outputs, Power BI report, Excel workbook, validation prototype and lifecycle case. The main figures can be checked against `p1-funnel-diagnostics/outputs/` rather than taken from a chart on trust.

Run the checks from the package root:

```powershell
python scripts/verify_project.py
node p2-validation-tool/tests/validation.test.js
```

To regenerate the synthetic source data and analysis outputs:

```powershell
python scripts/generate_data.py
python scripts/export_analysis.py
```

Open `p1-funnel-diagnostics/power-bi/merchant-onboarding-diagnostics.pbix` with Power BI Desktop. If the package is moved, update the three CSV source paths in Data source settings.

## Limits and professional boundaries

The data is synthetic and observational. Monthly activity is a proxy for 30-, 60- and 90-day retention, not a daily retention measure. Small subgroup results should be tested with more data before a business decision is made. The dashboard is a portfolio report, and the UAT feedback is simulated. No part of this project represents production KYC, AML, payment operations or an authorised compliance decision.

## Package contents

`data/` contains the synthetic source files. `p1-funnel-diagnostics/` contains the main analysis. `p2-validation-tool/` contains the validation prototype and evidence. `p3-client-lifecycle-case/` contains the process case. `scripts/` contains the scripts used to generate and verify the work.
