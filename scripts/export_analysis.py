"""Run portfolio SQL files and export reviewable CSV results."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "merchant_onboarding.db"
SQL_DIR = ROOT / "p1-funnel-diagnostics" / "sql"
OUTPUT = ROOT / "p1-funnel-diagnostics" / "outputs"

QUERIES = {
    "funnel_conversion.csv": "03_funnel_conversion.sql",
    "activation_time.csv": "04_activation_time.sql",
    "cohort_retention.csv": "05_cohort_retention.sql",
    "channel_segment_performance.csv": "06_channel_segment_performance.sql",
}


def export_query(connection: sqlite3.Connection, sql_file: str, output_file: str) -> None:
    cursor = connection.execute((SQL_DIR / sql_file).read_text(encoding="utf-8"))
    rows = cursor.fetchall()
    with (OUTPUT / output_file).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([column[0] for column in cursor.description])
        writer.writerows(rows)


def export_table(connection: sqlite3.Connection, query: str, output_file: Path) -> None:
    cursor = connection.execute(query)
    with output_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([column[0] for column in cursor.description])
        writer.writerows(cursor.fetchall())


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB)
    for output_file, sql_file in QUERIES.items():
        export_query(connection, sql_file, output_file)
    export_table(connection, "SELECT * FROM merchants_clean", OUTPUT / "merchants_clean.csv")
    connection.close()
    print(f"Exported {len(QUERIES) + 1} analysis files to {OUTPUT}")


if __name__ == "__main__":
    main()
