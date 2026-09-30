WITH activated AS (
    SELECT merchant_id, SUBSTR(activation_date, 1, 7) AS activation_cohort
    FROM merchants_clean
    WHERE activation_date IS NOT NULL
), cohort_activity AS (
    SELECT
        a.activation_cohort,
        m.months_since_activation,
        COUNT(DISTINCT CASE WHEN m.active_flag = 1 THEN m.merchant_id END) AS retained_merchants,
        COUNT(DISTINCT a.merchant_id) AS cohort_merchants
    FROM activated a
    JOIN merchant_monthly_activity m USING (merchant_id)
    WHERE m.months_since_activation IN (1, 2, 3)
    GROUP BY a.activation_cohort, m.months_since_activation
)
SELECT
    activation_cohort,
    months_since_activation * 30 AS retention_day,
    retained_merchants,
    cohort_merchants,
    ROUND(100.0 * retained_merchants / cohort_merchants, 1) AS retained_pct
FROM cohort_activity
ORDER BY activation_cohort, months_since_activation;
