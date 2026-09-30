# Power BI build sheet

For click-by-click Chinese instructions, see `manual-build-guide-zh.md`.

## Import and model

Import these CSV files:

- `outputs/merchants_clean.csv` as `Merchants`
- `../../data/funnel_events.csv` as `FunnelEvents`
- `../../data/merchant_monthly_activity.csv` as `MonthlyActivity`

Create one-to-many relationships from `Merchants[merchant_id]` to each fact table. Set date fields to Date and numeric flags to Whole number. Sort `FunnelEvents[stage]` by `stage_sequence`.

## Measures

```DAX
Total Leads =
CALCULATE(
    DISTINCTCOUNT(FunnelEvents[merchant_id]),
    FunnelEvents[stage] = "Lead"
)

Activated Merchants =
CALCULATE(
    DISTINCTCOUNT(FunnelEvents[merchant_id]),
    FunnelEvents[stage] = "Activated"
)

Activation Rate =
DIVIDE([Activated Merchants], [Total Leads])

Median Time to Activate =
MEDIANX(
    FILTER(Merchants, NOT ISBLANK(Merchants[activation_date])),
    DATEDIFF(Merchants[lead_date], Merchants[activation_date], DAY)
)

Retained Merchant Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(MonthlyActivity[merchant_id]),
        MonthlyActivity[active_flag] = 1
    ),
    DISTINCTCOUNT(MonthlyActivity[merchant_id])
)
```

Format `Activation Rate` and `Retained Merchant Rate` as percentages with one decimal place. The required three measures are present; `Total Leads` and `Activated Merchants` make the first one auditable.

## Page 1: Funnel diagnostics

- KPI cards: Total Leads, Activation Rate, Median Time to Activate, 90-day Retained Merchant Rate.
- Funnel visual: stage and distinct merchant count.
- Line chart: activation cohort, retained rate; use retention day as legend.
- Clustered bar: channel by Activation Rate; segment as small multiple or slicer.
- Matrix: channel rows, segment columns, Activation Rate values.
- Slicers: lead-date range, channel, segment, business type. Configure all four on Page 1 and validate their cross-filter interactions using `slicer-completion-guide-zh.md`.

## Page 2: Recommendations

Use the evidence and priorities in `../insights-and-recommendations.md`. Keep each recommendation linked to a metric, owner, action, and success measure. This page describes hypotheses for operational testing, not causal conclusions.

Power BI Desktop step still required: import, lay out the visuals, check totals against `outputs/`, and save `merchant-onboarding-diagnostics.pbix`. A proprietary `.pbix` has deliberately not been fabricated.
