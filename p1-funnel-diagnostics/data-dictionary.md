# Data dictionary

## merchant_onboarding_raw / merchants_clean

| Field | Type | Definition | Quality rule |
|---|---|---|---|
| merchant_id | TEXT | Synthetic unique merchant key | Required; trimmed and upper-case |
| lead_date | DATE | Date the merchant entered the funnel | Required; valid ISO date |
| segment | TEXT | Commercial size: Micro, SME, Enterprise | Standardised controlled value |
| channel | TEXT | Acquisition source | Standardised controlled value |
| business_type | TEXT | Synthetic operating category | Required |
| country | TEXT | Country of registration | Synthetic; not a risk decision |
| onboarding_stage | TEXT | Furthest stage reached | Lead, Qualified, Approved, Activated |
| activation_date | DATE | Date activation completed | Null unless activated; not before lead date |
| monthly_orders | INTEGER | Illustrative first-month order count | Non-negative |
| churn_flag | INTEGER | Synthetic churn indicator | 0 or 1 |

## funnel_events

| Field | Type | Definition |
|---|---|---|
| merchant_id | TEXT | Foreign key to merchant |
| stage | TEXT | Lead, Qualified, Approved, or Activated |
| stage_date | DATE | Date the stage was first reached |
| stage_sequence | INTEGER | Expected stage order, 1 to 4 |

## merchant_monthly_activity

| Field | Type | Definition |
|---|---|---|
| merchant_id | TEXT | Foreign key to merchant |
| activity_month | DATE | Calendar month of the observation |
| months_since_activation | INTEGER | 0, 1, 2, or 3 |
| orders | INTEGER | Synthetic orders in that month |
| active_flag | INTEGER | 1 when merchant placed orders; otherwise 0 |

`30/60/90-day retention` is approximated by activity in months 1, 2, and 3 after activation. This limitation is stated because the dataset is monthly, not daily.
