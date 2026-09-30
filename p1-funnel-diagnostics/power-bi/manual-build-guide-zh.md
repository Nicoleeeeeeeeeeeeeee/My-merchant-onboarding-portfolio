# Power BI Desktop 手动构建指南

目标文件：`merchant-onboarding-diagnostics.pbix`

以下菜单名以 Power BI Desktop 英文界面为准，中文界面通常位于相同位置。

## 1. 导入三张表

1. 打开 Power BI Desktop，选择 **Blank report**。
2. 依次选择 **Home > Get data > Text/CSV**，导入：
   - `p1-funnel-diagnostics/outputs/merchants_clean.csv`
   - `data/funnel_events.csv`
   - `data/merchant_monthly_activity.csv`
3. 每次在预览窗口选择 **Transform Data**，在左侧查询列表中重命名：
   - `merchants_clean` → `Merchants`
   - `funnel_events` → `FunnelEvents`
   - `merchant_monthly_activity` → `MonthlyActivity`
4. 在 Power Query 中设置字段类型：
   - `Merchants[lead_date]`、`Merchants[activation_date]`：**Date**。
   - `FunnelEvents[stage_date]`：**Date**。
   - `MonthlyActivity[activity_month]`：**Date**。
   - `monthly_orders`、`churn_flag`、`stage_sequence`、`months_since_activation`、`orders`、`active_flag`：**Whole Number**。
   - 其余字段保持 **Text**。
5. 选择 **Home > Close & Apply**。

## 2. 建立模型关系

1. 左侧选择 **Model view**。
2. 将 `Merchants[merchant_id]` 拖到 `FunnelEvents[merchant_id]`。
3. 设置 Cardinality 为 **One to many (1:*)**，Cross-filter direction 为 **Single**，并勾选 active relationship。
4. 将 `Merchants[merchant_id]` 拖到 `MonthlyActivity[merchant_id]`，使用相同设置。
5. 最终应只有两条关系，`Merchants` 位于 “1” 端。

## 3. 设置阶段顺序

1. 左侧选择 **Table view**，打开 `FunnelEvents`。
2. 单击 `stage` 列。
3. 选择顶部 **Column tools > Sort by column > stage_sequence**。

## 4. 新建辅助列

在 Fields/Data pane 中右键 `MonthlyActivity`，选择 **New column**：

```DAX
Retention Day = MonthlyActivity[months_since_activation] * 30
```

右键 `Merchants`，选择 **New column**：

```DAX
Activation Cohort =
IF(
    ISBLANK(Merchants[activation_date]),
    BLANK(),
    DATE(YEAR(Merchants[activation_date]), MONTH(Merchants[activation_date]), 1)
)
```

选中 `Activation Cohort`，在 **Column tools** 中设置 Format 为 `YYYY-MM`。

## 5. 新建 measures

右键 `Merchants`，依次选择 **New measure**，粘贴：

```DAX
Total Leads =
CALCULATE(
    DISTINCTCOUNT(FunnelEvents[merchant_id]),
    FunnelEvents[stage] = "Lead"
)

Activated Merchants =
CALCULATE(
    DISTINCTCOUNT(FunnelEvents[merchant_id]),
    FunnelEvents[stage] = "Activated"
)

Activation Rate =
DIVIDE([Activated Merchants], [Total Leads])

Median Time to Activate =
MEDIANX(
    FILTER(Merchants, NOT ISBLANK(Merchants[activation_date])),
    DATEDIFF(Merchants[lead_date], Merchants[activation_date], DAY)
)

Retained Merchant Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(MonthlyActivity[merchant_id]),
        MonthlyActivity[active_flag] = 1
    ),
    DISTINCTCOUNT(MonthlyActivity[merchant_id])
)
```

将 `Activation Rate` 和 `Retained Merchant Rate` 设为 Percentage、1 位小数；`Median Time to Activate` 设为 Whole number。

## 6. 创建 Page 1：Funnel Diagnostics

将页面重命名为 `Funnel Diagnostics`，Canvas settings 设为 **16:9**。

### 四个 KPI cards

分别插入四个 **Card**，字段为 `[Total Leads]`、`[Activation Rate]`、`[Median Time to Activate]`、`[Retained Merchant Rate]`。

对第 4 张 Card，在 **Filters on this visual** 中加入 `MonthlyActivity[months_since_activation]`，只勾选 `3`。标题改为 `90-day Retained Merchant Rate`。

核对结果：`1,200`、`46.8%`、`12`、`88.4%`。

### Funnel

1. 插入 **Funnel chart**。
2. Category/Group：`FunnelEvents[stage]`。
3. Values：`FunnelEvents[merchant_id]`，汇总方式改为 **Distinct count**。
4. 核对：Lead `1,200`、Qualified `884`、Approved `696`、Activated `562`。

### Retention line chart

1. 插入 **Line chart**。
2. X-axis：`Merchants[Activation Cohort]`。
3. Y-axis：`[Retained Merchant Rate]`。
4. Legend：`MonthlyActivity[Retention Day]`。
5. Visual filter：`Retention Day` 只保留 `30`、`60`、`90`。
6. X-axis Type 设为 **Categorical**。

### Channel performance bar chart

1. 插入 **Clustered bar chart**。
2. Y-axis：`Merchants[channel]`。
3. X-axis：`[Activation Rate]`。
4. Small multiples：`Merchants[segment]`；若画布过小，可把 segment 改为 slicer。
5. 按 Activation Rate 降序排列。

### Channel × segment matrix

1. 插入 **Matrix**。
2. Rows：`Merchants[channel]`。
3. Columns：`Merchants[segment]`。
4. Values：`[Activation Rate]`。
5. 在 Conditional formatting 中对低值使用浅红色背景。

### Slicers

加入 `Merchants[lead_date]`（Between）、`Merchants[channel]`、`Merchants[segment]`、`Merchants[business_type]`。选择 **Format > Edit interactions**，确认 slicers 会过滤所有视觉对象。

## 7. 创建 Page 2：Recommendations

1. 点击页面标签旁的 `+`，重命名为 `Recommendations`。
2. 插入三组 Text box，内容来自 `insights-and-recommendations.md` 的 P0、P1、P2。
3. 每组保留 Evidence、Hypothesis、Action、Owner、Success measure。
4. 页脚加入：`Synthetic observational data; recommendations require controlled testing and do not change approval controls.`

## 8. 最终核对和保存

1. 清除所有 slicer 选择。
2. 对照 `outputs/funnel_conversion.csv` 和 `power-bi/dashboard-preview.png` 检查总数。
3. 检查 90-day Card 的 visual-level filter 仍为 `months_since_activation = 3`。
4. 选择 **File > Save As**，保存到：
   `E:\resume\merchant-onboarding-portfolio\p1-funnel-diagnostics\power-bi\merchant-onboarding-diagnostics.pbix`
5. 关闭后重新打开 `.pbix`，确认没有找不到 CSV 的错误。若路径变化，选择 **File > Options and settings > Data source settings > Change Source** 更新三张 CSV 的位置。
