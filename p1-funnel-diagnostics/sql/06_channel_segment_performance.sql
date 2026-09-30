WITH outcomes AS (
    SELECT
        m.merchant_id,
        m.channel,
        m.segment,
        m.monthly_orders,
        MAX(CASE WHEN e.stage = 'Activated' THEN 1 ELSE 0 END) AS activated,
        CAST(JULIANDAY(m.activation_date) - JULIANDAY(m.lead_date) AS INTEGER) AS days_to_activate
    FROM merchants_clean m
    LEFT JOIN funnel_events e USING (merchant_id)
    GROUP BY m.merchant_id
)
SELECT
    channel,
    segment,
    COUNT(*) AS leads,
    SUM(activated) AS activated_merchants,
    ROUND(100.0 * SUM(activated) / COUNT(*), 1) AS activation_rate_pct,
    ROUND(AVG(days_to_activate), 1) AS avg_days_to_activate,
    ROUND(AVG(CASE WHEN activated = 1 THEN monthly_orders END), 1) AS avg_monthly_orders
FROM outcomes
GROUP BY channel, segment
ORDER BY activation_rate_pct DESC, leads DESC;
