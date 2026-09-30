# P1: Merchant Onboarding Funnel Diagnostics

An independent diagnostic using synthetic data, SQLite SQL, Excel-compatible CSV outputs, and a completed Power BI report. It demonstrates a complete analysis loop: define the funnel, clean the data, measure conversion and activation time, compare segments, and turn findings into operational hypotheses.

## Run

```powershell
cd merchant-onboarding-portfolio
python scripts/generate_data.py
python scripts/export_analysis.py
```

Open `data/merchant_onboarding.db` in DB Browser for SQLite, run the SQL files in order, or import `p1-funnel-diagnostics/outputs/*.csv` into Excel/Power BI. The SQL quality checks in `02_cleaning.sql` should return zero rows.

## Deliverables

- `data/README.md` and `data-dictionary.md`: source grain, field definitions, and quality rules.
- `sql/01_schema.sql` through `sql/06_channel_segment_performance.sql`: DDL, cleaning, funnel conversion, CTE/window activation-time calculation, cohort retention, and channel/segment comparison.
- `outputs/`: reproducible CSV extracts used to validate dashboard totals.
- `merchant-onboarding-analysis.xlsx`: formatted Excel review workbook with funnel and retention charts.
- `power-bi/model-and-dax.md`: relationships, five measures, two-page layout, and the explicit `.pbix` save step.
- `power-bi/slicer-completion-guide-zh.md`: four slicer setup, interaction checks, visual QA, and interview walkthrough.
- `insights-and-recommendations.md`: findings, prioritised interventions, owners, measures, and limitations.

## Current status

- Completed: synthetic data generation, SQLite data model, SQL cleaning and analysis, CSV outputs, Excel review workbook, dashboard preview, recommendations memo.
- Completed: the PBIX was edited with the four slicers and saved as `power-bi/merchant-onboarding-diagnostics.pbix`. It remains a portfolio report, not production reporting experience.

## Portfolio wording after PBIX validation

> Built an independent merchant-onboarding funnel diagnostic using synthetic data, SQL and Power BI; analysed conversion, activation time and retention, then proposed prioritised operational interventions.
