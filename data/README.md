# Shared synthetic data

All records are fictional and generated with seed `20260826`. No personal, company, identity-document, bank-account, or production-system data is used.

| File / table | Grain | Purpose |
|---|---|---|
| `merchant_onboarding_raw.csv` | One row per merchant | Lead attributes and latest onboarding outcome |
| `funnel_events.csv` | One row per merchant-stage event | Ordered funnel movement and time-to-stage analysis |
| `merchant_monthly_activity.csv` | One row per merchant-month | 30/60/90-day retention and order activity |
| `merchant_onboarding.db` | SQLite database | Reproducible SQL analysis across all source tables |

Regenerate everything with `python scripts/generate_data.py`. The deliberate casing/whitespace issues in a small number of raw segment and channel values support the cleaning exercise; `merchants_clean` standardises them.
