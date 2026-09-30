DROP VIEW IF EXISTS merchants_clean;

CREATE VIEW merchants_clean AS
SELECT
    UPPER(TRIM(merchant_id)) AS merchant_id,
    DATE(lead_date) AS lead_date,
    CASE LOWER(TRIM(segment))
        WHEN 'micro' THEN 'Micro'
        WHEN 'sme' THEN 'SME'
        WHEN 'enterprise' THEN 'Enterprise'
        ELSE 'Unknown'
    END AS segment,
    CASE LOWER(TRIM(channel))
        WHEN 'direct' THEN 'Direct'
        WHEN 'partner' THEN 'Partner'
        WHEN 'paid search' THEN 'Paid Search'
        WHEN 'referral' THEN 'Referral'
        ELSE 'Unknown'
    END AS channel,
    TRIM(business_type) AS business_type,
    TRIM(country) AS country,
    onboarding_stage,
    CASE WHEN activation_date = '' THEN NULL ELSE DATE(activation_date) END AS activation_date,
    CASE WHEN monthly_orders < 0 THEN 0 ELSE monthly_orders END AS monthly_orders,
    CASE WHEN churn_flag = 1 THEN 1 ELSE 0 END AS churn_flag
FROM merchant_onboarding_raw
WHERE merchant_id IS NOT NULL
  AND DATE(lead_date) IS NOT NULL;

-- Quality checks: each query should return zero rows.
SELECT merchant_id, COUNT(*) AS row_count
FROM merchants_clean
GROUP BY merchant_id
HAVING COUNT(*) > 1;

SELECT merchant_id
FROM merchants_clean
WHERE activation_date < lead_date;

SELECT e.merchant_id, e.stage, e.stage_date
FROM funnel_events e
JOIN merchants_clean m USING (merchant_id)
WHERE DATE(e.stage_date) < m.lead_date;
