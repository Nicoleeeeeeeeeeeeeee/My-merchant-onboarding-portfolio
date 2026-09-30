"""Generate deterministic synthetic data for the three portfolio projects."""

from __future__ import annotations

import csv
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB = DATA / "merchant_onboarding.db"
SEED = 20260826
N_MERCHANTS = 1200

SEGMENTS = ("Micro", "SME", "Enterprise")
CHANNELS = ("Direct", "Partner", "Paid Search", "Referral")
BUSINESS_TYPES = ("Retail", "Food & Beverage", "Professional Services", "E-commerce")
COUNTRIES = ("Hong Kong", "Singapore", "United Kingdom", "Australia")
STAGES = ("Lead", "Qualified", "Approved", "Activated")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def weighted_choice(rng: random.Random, items: tuple[str, ...], weights: tuple[int, ...]) -> str:
    return rng.choices(items, weights=weights, k=1)[0]


def generate() -> tuple[list[dict], list[dict], list[dict]]:
    rng = random.Random(SEED)
    merchants: list[dict] = []
    events: list[dict] = []
    monthly: list[dict] = []
    start = date(2025, 1, 1)

    for index in range(1, N_MERCHANTS + 1):
        merchant_id = f"M{index:05d}"
        segment = weighted_choice(rng, SEGMENTS, (55, 35, 10))
        channel = weighted_choice(rng, CHANNELS, (35, 25, 25, 15))
        business_type = weighted_choice(rng, BUSINESS_TYPES, (30, 25, 20, 25))
        country = weighted_choice(rng, COUNTRIES, (82, 7, 6, 5))
        lead_date = start + timedelta(days=rng.randrange(365))

        qualify_p = {"Direct": 0.77, "Partner": 0.82, "Paid Search": 0.61, "Referral": 0.86}[channel]
        approve_p = {"Micro": 0.73, "SME": 0.82, "Enterprise": 0.88}[segment]
        activate_p = {"Retail": 0.82, "Food & Beverage": 0.86, "Professional Services": 0.70, "E-commerce": 0.79}[business_type]
        qualified = rng.random() < qualify_p
        approved = qualified and rng.random() < approve_p
        activated = approved and rng.random() < activate_p

        stage_dates = {"Lead": lead_date}
        if qualified:
            stage_dates["Qualified"] = lead_date + timedelta(days=max(1, round(rng.lognormvariate(1.0, 0.55))))
        if approved:
            delay = max(1, round(rng.lognormvariate(1.35 if segment != "Enterprise" else 1.8, 0.55)))
            stage_dates["Approved"] = stage_dates["Qualified"] + timedelta(days=delay)
        if activated:
            delay = max(1, round(rng.lognormvariate(1.45 if channel != "Partner" else 1.15, 0.65)))
            stage_dates["Activated"] = stage_dates["Approved"] + timedelta(days=delay)

        current_stage = list(stage_dates)[-1]
        activation_date = stage_dates.get("Activated")
        base_orders = {"Micro": 42, "SME": 135, "Enterprise": 430}[segment]
        orders = round(max(0, rng.gauss(base_orders, base_orders * 0.35))) if activated else 0
        churn_p = 0.08 + (0.09 if channel == "Paid Search" else 0) + (0.04 if business_type == "Professional Services" else 0)
        churn_flag = int(activated and rng.random() < churn_p)

        # A few deliberate raw-data quality issues are corrected by 02_cleaning.sql.
        raw_channel = channel
        if index % 97 == 0:
            raw_channel = "paid search "
        raw_segment = segment
        if index % 131 == 0:
            raw_segment = "sme"

        merchants.append({
            "merchant_id": merchant_id,
            "lead_date": lead_date.isoformat(),
            "segment": raw_segment,
            "channel": raw_channel,
            "business_type": business_type,
            "country": country,
            "onboarding_stage": current_stage,
            "activation_date": activation_date.isoformat() if activation_date else "",
            "monthly_orders": orders,
            "churn_flag": churn_flag,
        })

        for sequence, (stage, event_date) in enumerate(stage_dates.items(), start=1):
            events.append({
                "merchant_id": merchant_id,
                "stage": stage,
                "stage_date": event_date.isoformat(),
                "stage_sequence": sequence,
            })

        if activated and activation_date:
            churn_month = rng.choice((1, 2, 3)) if churn_flag else None
            for month_number in range(0, 4):
                month_start = (activation_date.replace(day=1) + timedelta(days=32 * month_number)).replace(day=1)
                active = int(churn_month is None or month_number < churn_month)
                month_orders = round(max(0, rng.gauss(base_orders * (1 + 0.08 * month_number), base_orders * 0.25))) if active else 0
                monthly.append({
                    "merchant_id": merchant_id,
                    "activity_month": month_start.isoformat(),
                    "months_since_activation": month_number,
                    "orders": month_orders,
                    "active_flag": active,
                })

    return merchants, events, monthly


def build_database(merchants: list[dict], events: list[dict], monthly: list[dict]) -> None:
    if DB.exists():
        DB.unlink()
    connection = sqlite3.connect(DB)
    schema = (ROOT / "p1-funnel-diagnostics" / "sql" / "01_schema.sql").read_text(encoding="utf-8")
    connection.executescript(schema)
    connection.executemany(
        "INSERT INTO merchant_onboarding_raw VALUES (:merchant_id,:lead_date,:segment,:channel,:business_type,:country,:onboarding_stage,:activation_date,:monthly_orders,:churn_flag)",
        merchants,
    )
    connection.executemany(
        "INSERT INTO funnel_events VALUES (:merchant_id,:stage,:stage_date,:stage_sequence)",
        events,
    )
    connection.executemany(
        "INSERT INTO merchant_monthly_activity VALUES (:merchant_id,:activity_month,:months_since_activation,:orders,:active_flag)",
        monthly,
    )
    connection.executescript((ROOT / "p1-funnel-diagnostics" / "sql" / "02_cleaning.sql").read_text(encoding="utf-8"))
    connection.commit()
    connection.close()


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    merchants, events, monthly = generate()
    write_csv(DATA / "merchant_onboarding_raw.csv", merchants, list(merchants[0]))
    write_csv(DATA / "funnel_events.csv", events, list(events[0]))
    write_csv(DATA / "merchant_monthly_activity.csv", monthly, list(monthly[0]))
    build_database(merchants, events, monthly)
    print(f"Generated {len(merchants)} merchants, {len(events)} events, {len(monthly)} monthly rows")
    print(f"SQLite database: {DB}")


if __name__ == "__main__":
    main()
