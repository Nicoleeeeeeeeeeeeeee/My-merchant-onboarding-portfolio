# Power BI 四个 Slicer 补齐与验收指南

目标文件：`merchant-onboarding-diagnostics.pbix`。本页处理 Funnel Diagnostics 页面上的四个 slicer：日期范围、渠道、客户规模、业务类型。它们必须改变同一页的 KPI、漏斗、留存图、渠道图和矩阵。

## 一、备份并确认模型

1. 复制一份 PBIX，命名为 `merchant-onboarding-diagnostics-before-slicer-qa.pbix`。
2. 确认模型中有 `Merchants`、`FunnelEvents`、`MonthlyActivity` 三张表。
3. 确认关系为 `Merchants[merchant_id]` 到两个事实表的 `1:*`、Single direction、Active。
4. 四个字段均来自 `Merchants`：`lead_date`、`channel`、`segment`、`business_type`。
5. `lead_date` 必须是 Date 类型；三个分类字段必须是 Text。不要用 `FunnelEvents[stage_date]` 替代 `lead_date`，这样才能清楚区分获客范围和漏斗事件日期。

## 二、添加四个 slicer

在 `Funnel Diagnostics` 页面依次选择 **Insert > Slicer**，从 Fields pane 拖入：

| 字段 | Slicer 设置 | 页面标题 | 用途 |
|---|---|---|---|
| `Merchants[lead_date]` | Style = Between | Lead date | 选择分析 cohort / 获客日期范围 |
| `Merchants[channel]` | Dropdown | Acquisition channel | 比较 Partner、Direct、Paid Search、Referral |
| `Merchants[segment]` | Dropdown | Merchant segment | 比较 Micro、SME、Enterprise |
| `Merchants[business_type]` | Dropdown | Business type | 检查业务类型是否造成结构差异 |

后三个 slicer 保持 `Single select = Off`，允许组合筛选；日期 slicer 保持 Between，便于演示 cohort 范围变化。给四个 slicer 使用完整标题，不要只显示字段名。

## 三、交互与布局

1. 使用 **View > Snap to grid**，把四个 slicer 放在页面顶部；窄屏时排成两行。
2. 依次选择每个 slicer，打开 **Format > Edit interactions**，对同页 KPI、漏斗、留存图、渠道图和矩阵选择 Filter 图标。若显示 None，改为 Filter。
3. Recommendations 页面不需要被这些 slicer 过滤时，不要强行同步过去；推荐文字是基于已审计结果的静态决策建议。
4. 保留清除筛选图标，并确认 slicer 不遮挡 KPI 卡或图表标题。

## 四、验收测试

每次测试前先清除全部筛选。

| 测试 | 操作 | 预期结果 |
|---|---|---|
| T1 | 清除全部筛选 | 回到 1,200 leads、46.8% activation rate、12 days；漏斗为 1,200 / 884 / 696 / 562 |
| T2 | Channel = Paid Search | 所有主要视觉对象同步变化；矩阵只保留 Paid Search 行 |
| T3 | Segment = Micro | KPI、漏斗、渠道图和矩阵均只反映 Micro merchants |
| T4 | Business type = E-commerce | 结果只反映 E-commerce；清除后恢复 T1 |
| T5 | 日期选择 2025-01-01 至 2025-06-30 | Total Leads 小于 1,200，且没有日期范围外的 lead cohort |
| T6 | 同时选择 Paid Search + Micro | 能复现重点诊断方向；activation rate 应接近 36.3%，以当前模型实际显示值为准 |
| T7 | 切换到 Recommendations | 推荐文字保持稳定，不把静态建议误认为动态因果结论 |

## 五、核对与保存

1. 将 T1 的漏斗数与 `outputs/funnel_conversion.csv` 对照。
2. 将 T6 的结果与 `insights-and-recommendations.md` 对照。若不同，先检查 slicer 是否使用错误表或字段，不要先修改分析结论。
3. 确认 90-day retained card 仍有 visual-level filter：`MonthlyActivity[months_since_activation] = 3`。
4. 用 **File > Save As** 保存为 `merchant-onboarding-diagnostics.pbix`，关闭后重新打开，确认四个 slicer 仍存在且 CSV 路径无错误。
5. 最终公开材料优先使用 `dashboard-preview.png` 和可复现文档；未经检查的 PBIX 不要直接提交到仓库。

## 面试 60 秒讲法

> 我把筛选器放在获客日期、渠道、客户规模和业务类型四个层级。日期用于限定 cohort，后三个维度用于拆解结构差异。完成配置后，我用清空筛选的基线值和 SQL 输出核对，再用 Paid Search + Micro 这个低激活组合复现分析结论。这样 slicer 不只是装饰，而是把总体漏斗变成可追问的运营诊断。数据是 synthetic，结论是描述性信号，不把相关性说成因果关系。
