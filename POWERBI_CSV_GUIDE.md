# 🎯 Power BI Dashboard - CSV Import Guide

## ✅ Your CSV Files are Ready!

All database tables have been exported to CSV format. Just import them into Power BI - super simple!

📁 Files in `powerbi_data/` folder:
- `stocks.csv` (3 rows)
- `portfolios.csv` (1 row)
- `holdings.csv` (3 rows)
- `transactions.csv` (5 rows)
- `price_history.csv` (35 rows)
- `portfolio_metrics.csv` (8 rows)

---

## 🚀 Quick Start - 3 Steps to Dashboard

### Step 1: Install & Open Power BI (5 min)
1. Go to https://powerbi.microsoft.com/downloads/
2. Download **Power BI Desktop** (free)
3. Install & launch

### Step 2: Import CSV Files (10 min)

**In Power BI Desktop:**

1. **Home** → **Get Data** → **Text/CSV**
2. Navigate to: `C:\Users\annie\OneDrive\Documents\StockPortfolioProject\powerbi_data\`
3. Select **`stocks.csv`** → **Load**
4. Repeat steps 1-3 for each file:
   - `portfolios.csv`
   - `holdings.csv`
   - `transactions.csv`
   - `price_history.csv`
   - `portfolio_metrics.csv`

**All 6 tables are now in Power BI!** ✅

### Step 3: Create Relationships (5 min)

1. **Model** tab (left panel)
2. Drag relationships to connect:
   - `holdings[portfolio_id]` → `portfolios[portfolio_id]`
   - `holdings[stock_id]` → `stocks[stock_id]`
   - `transactions[portfolio_id]` → `portfolios[portfolio_id]`
   - `transactions[stock_id]` → `stocks[stock_id]`
   - `price_history[stock_id]` → `stocks[stock_id]`
   - `portfolio_metrics[portfolio_id]` → `portfolios[portfolio_id]`

**Done! Ready to build dashboard.** ✅

---

## 📊 Build Dashboard - Complete Instructions

### PAGE 1: OVERVIEW

**Create new page:** Right-click tab → New page → Name: "Overview"

#### Row 1: KPI Cards

**Add 4 KPI Cards (drag to top row):**

1. **Portfolio Value**
   - Visualization: **Card**
   - Value: `portfolio_metrics[total_value]` (use MAX aggregation)
   - Format as: **Currency**
   - Title: "Portfolio Value"
   - Font size: 32pt

2. **Total Invested**
   - Visualization: **Card**
   - Value: `portfolios[total_invested]`
   - Format as: **Currency**
   - Title: "Total Invested"

3. **Gain/Loss**
   - Visualization: **Card**
   - Value: Create DAX measure:
   ```dax
   Total Gain = MAX(portfolio_metrics[total_value]) - MAX(portfolios[total_invested])
   ```
   - Format as: **Currency**
   - Title: "Total Gain/Loss"

4. **Sharpe Ratio**
   - Visualization: **Card**
   - Value: `portfolio_metrics[sharpe_ratio]` (use MAX)
   - Format: **2 decimals**
   - Title: "Sharpe Ratio"

#### Row 2: Charts

**Portfolio Allocation (Pie Chart)**
- Visualization: **Pie Chart**
- Legend (Colors): `stocks[ticker]`
- Values: 
  - Create measure: `Holdings Value = SUM(holdings[shares]) * SUM(holdings[current_price])`
  - Or manually: `holdings[shares]` × `holdings[current_price]`
- Title: "Portfolio Allocation"
- Font: 14pt

**Portfolio Value Trend (Line Chart)**
- Visualization: **Line Chart**
- X-axis: `portfolio_metrics[metric_date]`
- Y-axis: `portfolio_metrics[total_value]` (as line)
- Title: "Value Over Time"
- Format: Currency on Y-axis, smooth line

---

### PAGE 2: RISK ANALYSIS

**Create new page:** Name: "Risk Analysis"

#### Row 1: Risk KPI Cards

1. **Annual Volatility**
   - Visualization: **Card**
   - Measure:
   ```dax
   Volatility % = MAX(portfolio_metrics[annual_volatility]) * 100
   ```
   - Format: **1 decimal, add % symbol**
   - Title: "Annual Volatility"

2. **Max Drawdown**
   - Visualization: **Card**
   - Measure:
   ```dax
   Max Drawdown % = MIN(portfolio_metrics[max_drawdown]) * 100
   ```
   - Format: **1 decimal, add % symbol**
   - Title: "Max Drawdown"

3. **Annual Return**
   - Visualization: **Card**
   - Value: `portfolio_metrics[annual_return]` (MAX)
   - Measure:
   ```dax
   Return % = MAX(portfolio_metrics[annual_return]) * 100
   ```
   - Format: **1 decimal, add % symbol**
   - Title: "Annual Return"

4. **Sharpe Ratio**
   - Visualization: **Card**
   - Value: `portfolio_metrics[sharpe_ratio]` (MAX)
   - Format: **2 decimals**
   - Title: "Sharpe Ratio"

#### Row 2: Risk Charts

**Volatility Trend (Line Chart)**
- X-axis: `portfolio_metrics[metric_date]`
- Y-axis: Create measure:
```dax
Vol Trend = MAX(portfolio_metrics[annual_volatility]) * 100
```
- Title: "Volatility Over Time"
- Format: Orange/warning color, smooth line

**Return Trend (Line Chart)**
- X-axis: `portfolio_metrics[metric_date]`
- Y-axis: Create measure:
```dax
Return Trend = MAX(portfolio_metrics[annual_return]) * 100
```
- Title: "Return Over Time"
- Format: Green color, smooth line

---

### PAGE 3: HOLDINGS

**Create new page:** Name: "Holdings"

#### Holdings Table
- Visualization: **Table**
- Columns (drag in order):
  - `stocks[ticker]`
  - `stocks[company_name]`
  - `stocks[sector]`
  - `holdings[shares]` (format: whole number)
  - `holdings[purchase_price]` (format: currency)
  - `holdings[current_price]` (format: currency)
  - Create column: `Holdings Value = [shares] × [current_price]` (format: currency)
  - Create column: `Gain/Loss = ([current_price] - [purchase_price]) × [shares]` (format: currency)
  - Create column: `Return % = (([current_price] - [purchase_price]) / [purchase_price]) × 100` (format: 2 decimals)

#### Stock Performance Chart (Column Chart)
- X-axis: `stocks[ticker]`
- Y-axis: Create measure:
```dax
Stock Return % = 
DIVIDE(
    (MAX(holdings[current_price]) - MAX(holdings[purchase_price])),
    MAX(holdings[purchase_price])
) * 100
```
- Title: "Stock Performance"
- **Data colors:** Green if positive, red if negative
  - Right-click bar → Conditional formatting → Color scale

#### Sector Allocation (Pie Chart)
- Legend: `stocks[sector]`
- Values: Sum of holding values (create measure as above)
- Title: "Sector Breakdown"

---

### PAGE 4: TRANSACTIONS

**Create new page:** Name: "Transactions"

#### Transaction History Table
- Visualization: **Table**
- Columns:
  - `transactions[transaction_date]` (format: MM/DD/YYYY)
  - `stocks[ticker]`
  - `transactions[action]` (BUY/SELL)
  - `transactions[shares]` (whole number)
  - `transactions[price]` (currency)
  - `transactions[total_value]` (currency)
- Sort: By date, newest first

#### Transaction Activity (Column Chart)
- Create column: Extract month from `transaction_date`
  ```
  Month = FORMAT([transaction_date], "YYYY-MM")
  ```
- X-axis: `Month`
- Y-axis: Count of transactions
- Title: "Monthly Activity"
- Format: Blue bars

---

## 🎛️ Add Interactivity - Slicers

### Slicer 1: Date Range (All Pages)
1. Add **Slicer** visual
2. Field: `portfolio_metrics[metric_date]`
3. Type: **Between** (Range slider)
4. Title: "Date Range"
5. **Edit Interactions**: 
   - Click each chart/table
   - Set to **Filter** mode

### Slicer 2: Stock Ticker (Holdings Page)
1. Add **Slicer**
2. Field: `stocks[ticker]`
3. Type: **List** (allow multi-select)
4. Title: "Select Stock"
5. Edit Interactions: Filter holdings table

### Slicer 3: Action Filter (Transactions Page)
1. Add **Slicer**
2. Field: `transactions[action]`
3. Type: **List**
4. Title: "Transaction Type"
5. Edit Interactions: Filter transaction table

---

## 🎨 Design & Formatting

### Color Scheme
```
Primary Blue:     #1a73e8  (charts, titles)
Positive Green:   #27ae60  (gains, good metrics)
Negative Red:     #e74c3c  (losses, warnings)
Warning Orange:   #f39c12  (volatility)
Background:       White   (clean look)
Text Dark:        #2c3e50 (high contrast)
```

### Apply to All Pages:
1. **View** → **Themes** → Choose professional theme
2. Apply color palette above
3. Format titles:
   - Size: 24pt, bold, #1a3a52
   - Subtitles: 12pt, gray

### Layout:
1. **View** → **Page View** → **Fit to page** width
2. Arrange:
   - Row 1: All KPI cards (equal width)
   - Row 2: Charts side-by-side
   - Row 3: Tables (full width)
3. Slicers: Top of each page

---

## 💾 Save & Share

### Save Locally
1. **File** → **Save As**
2. Name: `Stock Portfolio Dashboard.pbix`
3. Location: `C:\Users\annie\OneDrive\Documents\`

### Deploy to Web (Power BI Service)

**If you have Power BI Pro:**
1. **Home** → **Publish**
2. Select workspace
3. Dashboard gets public URL
4. Share link with anyone

**If you have Power BI Free (or no account):**
1. Just save the `.pbix` file
2. Share file directly with stakeholders
3. They open in Power BI Desktop

---

## 📋 Final Checklist

### Dashboard Complete?
- [ ] Overview page: 4 KPIs + 2 charts
- [ ] Risk page: 4 KPIs + 2 charts
- [ ] Holdings page: table + 2 charts
- [ ] Transactions page: table + 1 chart
- [ ] All slicers working
- [ ] Color scheme applied
- [ ] Saved as `.pbix`

### Ready to Present?
- [ ] Tested all interactions
- [ ] Numbers look correct
- [ ] Charts display properly
- [ ] No errors/warnings
- [ ] Looks professional
- [ ] Exported or published

---

## 🎯 Present Your Dashboard

1. **Start with Overview** → Shows portfolio health at a glance
2. **Click to Risk Analysis** → Demonstrate risk management
3. **Show Holdings** → Detail individual positions
4. **Demonstrate Transactions** → Show trading history
5. **Use Slicers** → Filter by date, stock, action to show flexibility

---

## ✅ You're Ready!

All data is exported and waiting. 

**Next:** Follow steps 1-3 above (Install → Import CSVs → Create Relationships)

Then build dashboard using the detailed instructions.

**Result:** Professional multi-page Power BI dashboard in ~1 hour! 📊

---

*Created: February 7, 2026*
*Format: CSV Import (No database server needed)*
*Status: Production Ready ✅*
