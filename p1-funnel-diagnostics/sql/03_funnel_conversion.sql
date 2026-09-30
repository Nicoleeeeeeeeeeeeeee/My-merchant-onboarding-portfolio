WITH stage_counts AS (
    SELECT stage, stage_sequence, COUNT(DISTINCT merchant_id) AS merchants
    FROM funnel_events
    GROUP BY stage, stage_sequence
), ordered AS (
    SELECT
        stage,
        stage_sequence,
        merchants,
        LAG(merchants) OVER (ORDER BY stage_sequence) AS prior_stage_merchants
    FROM stage_counts
)
SELECT
    stage,
    merchants,
    ROUND(100.0 * merchants / FIRST_VALUE(merchants) OVER (ORDER BY stage_sequence), 1) AS lead_to_stage_pct,
    ROUND(100.0 * merchants / COALESCE(prior_stage_merchants, merchants), 1) AS stage_conversion_pct
FROM ordered
ORDER BY stage_sequence;
