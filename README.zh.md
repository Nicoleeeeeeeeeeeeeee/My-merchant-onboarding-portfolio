# Merchant onboarding operations portfolio

這是一個虛構商戶 onboarding 流程的實務分析作品集。流程由 lead intake 開始，經過 qualification、approval 和 activation，再觀察 activation 後的早期 activity。這個專案想展示的是：如何把一個營運問題整理成可核對的分析、可使用的報表，以及一套小型 validation workflow。

所有資料都是 synthetic data，以固定 seed 產生。內容不包括客戶資料、身分證明文件、銀行帳戶資料、僱主內部資料或 production system 匯出檔。

## 業務背景

Onboarding team 需要回答幾個實際問題：

1. 商戶在哪一個 funnel stage 流失？
2. 哪些 acquisition channel 或 merchant group 值得跟進？
3. 從 lead 到 activation 平均需要多久？
4. 文件完整度、handoff 和 escalation 是否足夠清楚，讓營運團隊可以處理？

這個專案定位為 operational diagnostic。Dashboard 可以幫助團隊找到問題，但不能單獨證明因果關係，也不能代替 KYC 決定或 authorised compliance process。

## 業務需求

我把上述問題轉成以下 outputs：

- 使用 distinct merchant ID 計算每個 funnel stage 的商戶數量。
- 以 acquisition channel、merchant segment、business type 和 lead-date cohort 比較 activation。
- 使用 median lead-to-activation time，避免只看容易受極端值影響的 average。
- 以 activation 後的 monthly activity 作為 retention proxy。
- 讓使用者以 lead date、channel、segment 和 business type 篩選報表。
- 用 SQL outputs 和 source-level quality checks 核對報表數字。
- 在不作 approval 或 rejection 的前提下，檢查 onboarding application 是否完整。
- 清楚記錄 handoff owner、SLA miss 後的處理方式，以及何時需要 authorised review。

## 完成的工作

### P1：Funnel diagnostics

資料模型由一張 merchant-level table 和兩張 event/activity tables 組成：

- `Merchants`：lead attributes 和最新 onboarding outcome
- `FunnelEvents`：每個 merchant-stage event 一行
- `MonthlyActivity`：activation 後每個 merchant 每月一行

分析涵蓋 1,200 個 leads。這份 sample 中有 562 個 merchants 完成 activation，lead-to-activation rate 為 46.8%，median time to activate 為 12 天。Paid Search + Micro 的 activation rate 是 36.3%，Partner + Micro 則是 52.0%。

我把這個差異當作 prioritisation signal，而不是 channel 導致結果的證明。合理的下一步是為較低 activation 的 group 加入 assisted qualification，再用 controlled comparison 檢驗效果，同時維持原有 approval controls。

技術工作包括：

- 建立 SQL schema 和 data-quality checks
- 清理 raw channel、segment 中不一致的大小寫和空白
- Funnel conversion queries
- 使用 CTE 和 window functions 計算 activation time
- 以 cohort 分析 monthly retention proxy
- 比較 channel 和 segment
- 匯出 CSV 作 reconciliation
- 建立 Excel review workbook
- 在 Power BI Desktop 建立 DAX measures、兩個 pages 和四個 slicers

四個 slicers 是 lead date、acquisition channel、merchant segment 和 business type。它們讓 reviewer 可以由 overall funnel 進一步查看指定 operating segment，同時保留同一個 data model。

### P2：Simulated UAT validation tool

第二個專案處理另一種營運風險：資料不完整的 application 被錯誤交給下一位 reviewer。

Browser prototype 會檢查 required fields、email format、registration-number format、positive expected monthly volume，以及三項 required checklist items。結果分為 `INCOMPLETE`、`DOCUMENTS_OUTSTANDING` 和 `READY_FOR_COMPLETENESS_REVIEW`。

工具在 completeness check 停止，不會 approval 或 reject merchant，也不會做 suspicious-activity assessment、identity verification 或資料儲存。Package 內包含 requirements、test cases、defect records、simulated feedback 和 automated rule tests。

### P3：Client lifecycle learning case

第三個專案整理一個虛構 corporate onboarding case 的 operating boundary。它把 intake 和 completeness work，與 authorised compliance review 分開。Tracker 涵蓋文件缺漏、completeness review、compliance review、activation pending 和 periodic review due。

SLA breach 或 non-standard ownership structure 會形成 escalation reason，而不是非正式 override。在受控的 onboarding 流程中，operations team 可以記錄 evidence 和 route exception，但 regulated decision 必須由 authorised reviewer 作出。

## 技術棧和工作方式

| 範圍 | 工具和方法 |
|---|---|
| Data generation | Python standard library、deterministic seed |
| Data storage | 分析期間使用 CSV 和 SQLite |
| Data analysis | SQL、CTEs、window functions、cohort logic |
| Reporting | Power BI Desktop、DAX、Excel review workbook |
| Validation | HTML、CSS、vanilla JavaScript、Node rule tests |
| Process design | Mermaid、CSV case tracker、Markdown control memo |
| Quality control | Reproducible scripts、row-count checks、data-quality assertions、reconciliation outputs |

工作方式很直接：先定義 data grain，再驗證 source，計算 metrics，核對結果，最後把結論寫成有 owner、measure 和 guardrail 的營運建議。這樣每個建議都能追溯到可檢查的資料。

## 證據和結果

Package 內有 source CSV、SQL files、generated outputs、Power BI report、Excel workbook、validation prototype 和 lifecycle case。主要數字可以和 `p1-funnel-diagnostics/outputs/` 對照，不需要只相信圖表上的顯示值。

在 package root 執行：

```powershell
python scripts/verify_project.py
node p2-validation-tool/tests/validation.test.js
```

如需重新產生 synthetic source data 和 analysis outputs：

```powershell
python scripts/generate_data.py
python scripts/export_analysis.py
```

使用 Power BI Desktop 開啟 `p1-funnel-diagnostics/power-bi/merchant-onboarding-diagnostics.pbix`。如果 package 被移到其他位置，請在 Data source settings 更新三個 CSV source paths。

## 限制和工作邊界

資料是 synthetic 及 observational。Monthly activity 只是 30、60、90 日 retention 的 proxy，不是 daily retention measure。小型 subgroup 的結果需要更多資料和進一步測試，才適合用於業務決策。Dashboard 是作品集 report，UAT feedback 是 simulated。本專案不代表 production KYC、AML、payment operations 或 authorised compliance decision 的實務經驗。

## Package 內容

`data/` 放置 synthetic source files。`p1-funnel-diagnostics/` 是主要分析。`p2-validation-tool/` 是 validation prototype 和 evidence。`p3-client-lifecycle-case/` 是 process case。`scripts/` 是用來產生和驗證結果的 scripts。
