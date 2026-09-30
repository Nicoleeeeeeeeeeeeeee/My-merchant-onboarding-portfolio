"""Verify generated data, SQL outputs, and required portfolio artifacts."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "merchant_onboarding.db"

REQUIRED = [
    "README.md",
    "p1-funnel-diagnostics/data-dictionary.md",
    "p1-funnel-diagnostics/power-bi/model-and-dax.md",
    "p1-funnel-diagnostics/power-bi/dashboard-preview.html",
    "p1-funnel-diagnostics/power-bi/manual-build-guide-zh.md",
    "p1-funnel-diagnostics/merchant-onboarding-analysis.xlsx",
    "p2-validation-tool/app/index.html",
    "p2-validation-tool/requirements.md",
    "p2-validation-tool/uat/test-cases.csv",
    "p2-validation-tool/uat/defect-log.csv",
    "p2-validation-tool/uat/simulated-tester-feedback.csv",
    "p2-validation-tool/uat/real-tester-feedback-template.csv",
    "p3-client-lifecycle-case/process.mmd",
    "p3-client-lifecycle-case/case-tracker.csv",
    "p3-client-lifecycle-case/roles-and-controls-memo.md",
    "p3-client-lifecycle-case/sources.md",
]


def main() -> None:
    missing = [item for item in REQUIRED if not (ROOT / item).exists()]
    assert not missing, f"Missing deliverables: {missing}"

    connection = sqlite3.connect(DB)
    assert connection.execute("SELECT COUNT(*) FROM merchants_clean").fetchone()[0] == 1200
    assert connection.execute("SELECT COUNT(*) FROM funnel_events").fetchone()[0] == 3342
    assert connection.execute("SELECT COUNT(*) FROM merchant_monthly_activity").fetchone()[0] == 2248
    assert connection.execute("SELECT COUNT(*) FROM merchants_clean WHERE activation_date < lead_date").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM merchants_clean WHERE channel = 'Unknown' OR segment = 'Unknown'").fetchone()[0] == 0
    connection.close()

    with (ROOT / "p2-validation-tool" / "uat" / "test-cases.csv").open(encoding="utf-8") as handle:
        test_cases = list(csv.DictReader(handle))
    assert len(test_cases) == 15
    assert all(case["Status"] == "Pass" for case in test_cases)
    with (ROOT / "p2-validation-tool" / "uat" / "simulated-tester-feedback.csv").open(encoding="utf-8") as handle:
        simulated_feedback = list(csv.DictReader(handle))
    assert len(simulated_feedback) == 3
    assert all(row["Tester type"].startswith("Simulated") for row in simulated_feedback)
    print("Project verification passed: 16 deliverables, 3 table counts, 2 quality checks, 15 UAT rows, 3 simulated walkthroughs")


if __name__ == "__main__":
    main()
