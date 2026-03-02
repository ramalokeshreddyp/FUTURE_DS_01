<div align="center">

<img src="https://img.shields.io/badge/Task-1%20%7C%20Business%20Sales%20Analytics-blueviolet?style=for-the-badge&logo=databricks" />
<img src="https://img.shields.io/badge/Tools-Python%20%7C%20Pandas%20%7C%20Matplotlib%20%7C%20Chart.js-orange?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge" />

# 📊 Business Sales Performance Analytics

**Future Interns – Data Science & Analytics Internship · Task 1 · 2026**

> *Transforming 5,000 orders of raw sales data into actionable business intelligence — revenue trends, product rankings, category breakdowns, and regional performance — presented in a fully interactive dashboard.*

</div>

---

## 🗂️ Project Structure

```
DS1/
├── data/
│   └── superstore_sales.csv          ← 5,000-row generated dataset (708 KB)
├── scripts/
│   ├── generate_dataset.py           ← Dataset generation (seed=42, reproducible)
│   └── analysis.py                   ← Full Python EDA + 10 chart exports
├── output/                           ← 10 PNG charts + kpi_summary.csv
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_yearly_revenue_vs_profit.png
│   ├── 03_quarterly_heatmap.png
│   ├── 04_top10_products.png
│   ├── 05_category_performance.png
│   ├── 06_regional_performance.png
│   ├── 07_segment_analysis.png
│   ├── 08_discount_impact.png
│   ├── 09_shipmode_revenue.png
│   ├── 10_margin_trend_by_category.png
│   └── kpi_summary.csv
├── dashboard/
│   ├── index.html                    ← ⭐ Interactive single-file dashboard
│   └── data.json                     ← Pre-computed chart data
├── notebooks/
│   └── task1_business_sales_analysis.ipynb
├── reports/
│   └── insights_report.md            ← Written insights & recommendations
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### 2 — (Re)generate the dataset
```bash
python scripts/generate_dataset.py
```

### 3 — Run the full analysis (exports 10 charts to `/output`)
```bash
python scripts/analysis.py
```

### 4 — Open the interactive dashboard
```bash
# Simply open in any browser:
start dashboard/index.html
```

---

## 📈 Key KPIs

| Metric | Value |
|---|---|
| 💰 Total Revenue | **$3.32M** (2021–2024) |
| 📈 Total Profit | **$534.7K** |
| 📊 Avg Profit Margin | **18.26%** |
| 🛒 Total Orders | **5,000** |
| 💳 Avg Order Value | **$663.73** |
| 🏷️ Avg Discount Applied | **11.7%** |
| 👥 Unique Customers | **3,836** |

---

## 🎨 Dashboard Features

The **`dashboard/index.html`** is a single-file interactive dashboard with:

| Tab | Contents |
|---|---|
| 🏠 **Overview** | KPI cards, category donut, YoY bar chart, region + segment breakdowns |
| 📈 **Revenue Trends** | Monthly area chart (2021–2024), quarterly grouped bars, discount impact |
| 🏆 **Products** | Top-10 revenue & profit horizontal bars, product performance table |
| 📦 **Categories** | Revenue share donut, revenue vs profit bar, margin %, sub-category bars |
| 🌍 **Regions** | Region revenue/profit bars, grouped comparison, regional KPI table |
| 💡 **Insights** | 6 insight cards with business recommendations + executive KPI summary table |

---

## 💡 Key Business Insights

1. **Technology leads at 35.5% revenue share** with a 20.2% profit margin — the strongest category.
2. **Q4 seasonality is consistent** — revenue peaks every November–December across all 4 years.
3. **East region outperforms** with $1.02M revenue; Central lags and needs strategic attention.
4. **Discounts ≥ 25% sharply erode profits** — average profit drops below $70 per order.
5. **Furniture's 10.1% margin** is far below the 18% portfolio average — a margin improvement opportunity.
6. **Corporate segment** has the highest AOV — a high-value B2B retention opportunity.

---

## 🛠️ Tools & Stack

- **Python 3.x** — Data generation, cleaning, EDA
- **Pandas** — Data manipulation and aggregation
- **Matplotlib + Seaborn** — Static chart generation
- **Chart.js 4.4** — Interactive web dashboard
- **HTML / CSS / JavaScript** — Single-file dashboard (no build step required)

---

## 📤 Deliverables

- [x] ✅ Clean, reproducible synthetic dataset (`data/superstore_sales.csv`)
- [x] ✅ Python analysis script with 10 analytical sections
- [x] ✅ 10 PNG static charts exported to `/output`
- [x] ✅ Interactive HTML dashboard (`dashboard/index.html`)
- [x] ✅ Written insights report (`reports/insights_report.md`)
- [x] ✅ Jupyter notebook (`notebooks/task1_business_sales_analysis.ipynb`)

---

<div align="center">

Made with ❤️ for **Future Interns** · DS1 Task 1 · March 2026

</div>
