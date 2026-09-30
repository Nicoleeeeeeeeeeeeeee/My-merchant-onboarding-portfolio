PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS merchant_monthly_activity;
DROP TABLE IF EXISTS funnel_events;
DROP TABLE IF EXISTS merchant_onboarding_raw;

CREATE TABLE merchant_onboarding_raw (
    merchant_id TEXT PRIMARY KEY,
    lead_date TEXT NOT NULL,
    segment TEXT NOT NULL,
    channel TEXT NOT NULL,
    business_type TEXT NOT NULL,
    country TEXT NOT NULL,
    onboarding_stage TEXT NOT NULL,
    activation_date TEXT,
    monthly_orders INTEGER NOT NULL,
    churn_flag INTEGER NOT NULL CHECK (churn_flag IN (0, 1))
);

CREATE TABLE funnel_events (
    merchant_id TEXT NOT NULL,
    stage TEXT NOT NULL CHECK (stage IN ('Lead', 'Qualified', 'Approved', 'Activated')),
    stage_date TEXT NOT NULL,
    stage_sequence INTEGER NOT NULL,
    PRIMARY KEY (merchant_id, stage),
    FOREIGN KEY (merchant_id) REFERENCES merchant_onboarding_raw (merchant_id)
);

CREATE TABLE merchant_monthly_activity (
    merchant_id TEXT NOT NULL,
    activity_month TEXT NOT NULL,
    months_since_activation INTEGER NOT NULL,
    orders INTEGER NOT NULL CHECK (orders >= 0),
    active_flag INTEGER NOT NULL CHECK (active_flag IN (0, 1)),
    PRIMARY KEY (merchant_id, months_since_activation),
    FOREIGN KEY (merchant_id) REFERENCES merchant_onboarding_raw (merchant_id)
);

CREATE INDEX idx_events_stage_date ON funnel_events(stage, stage_date);
CREATE INDEX idx_activity_cohort ON merchant_monthly_activity(months_since_activation, active_flag);
