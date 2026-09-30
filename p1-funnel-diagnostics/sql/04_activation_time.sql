WITH stage_times AS (
    SELECT
        merchant_id,
        MIN(CASE WHEN stage = 'Lead' THEN DATE(stage_date) END) AS lead_date,
        MIN(CASE WHEN stage = 'Activated' THEN DATE(stage_date) END) AS activation_date
    FROM funnel_events
    GROUP BY merchant_id
), activation_times AS (
    SELECT
        merchant_id,
        CAST(JULIANDAY(activation_date) - JULIANDAY(lead_date) AS INTEGER) AS days_to_activate,
        ROW_NUMBER() OVER (ORDER BY JULIANDAY(activation_date) - JULIANDAY(lead_date)) AS row_number,
        COUNT(*) OVER () AS total_rows
    FROM stage_times
    WHERE activation_date IS NOT NULL
)
SELECT
    ROUND(AVG(CASE
        WHEN row_number IN ((total_rows + 1) / 2, (total_rows + 2) / 2)
        THEN days_to_activate
    END), 1) AS median_days_to_activate,
    MIN(days_to_activate) AS fastest_days,
    MAX(days_to_activate) AS slowest_days
FROM activation_times;
