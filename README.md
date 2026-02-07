# Stock Portfolio Analyzer

A comprehensive Python application for tracking and analyzing stock portfolios with live market data, financial risk metrics, and PostgreSQL storage. Includes interactive Power BI dashboards for performance monitoring.

**Technologies**: Python, SQL, Power BI, yfinance API, PostgreSQL

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Financial Metrics](#financial-metrics)
- [Power BI Integration](#power-bi-integration)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Core Portfolio Management
- **Create and manage multiple portfolios** - Track different investment strategies
- **Add/update/remove holdings** - Manage stock positions in real-time
- **Transaction history** - Complete audit trail of all buy/sell activities
- **Portfolio snapshots** - Track portfolio values over time

### Market Data Integration
- **Live stock prices** - Real-time data from yfinance API
- **Historical data** - 365 days of price history with OHLCV data
- **Stock information** - Sector, industry, market cap, P/E ratio, beta
- **Automated price updates** - Scheduled market data synchronization

### Financial Risk Metrics
- **Returns Analysis**
  - Cumulative returns from inception
  - Daily, weekly, monthly, and annual returns
  - Portfolio-weighted composite returns

- **Volatility Metrics**
  - Daily volatility (standard deviation)
  - Annualized volatility
  - Risk assessment over time

- **Risk-Adjusted Returns**
  - Sharpe Ratio (return per unit of risk)
  - Portfolio optimization insights

- **Drawdown Analysis**
  - Maximum Drawdown - worst peak-to-trough decline
  - Drawdown duration tracking
  - Recovery analysis

### Data Storage
- **PostgreSQL database** - Scalable, reliable data persistence
- **Relational schema** - Normalized design for data integrity
- **Historical tracking** - Complete time-series data
- **Indexed queries** - Fast retrieval of large datasets

### Power BI Dashboards
- **Portfolio Overview** - KPIs, allocation, value trends
- **Risk Metrics** - Volatility, Sharpe ratio, drawdown visualization
- **Holdings Detail** - Individual position performance
- **Transaction Analysis** - Buy/sell activity tracking
- **Comparative Analysis** - Multi-stock performance comparison

---

## 📁 Project Structure

```
StockPortfolioProject/
├── src/
│   ├── market_data_fetcher.py      # Fetch live market data from yfinance
│   ├── risk_metrics.py              # Calculate financial risk metrics
│   └── portfolio_manager.py          # Portfolio management operations
├── database/
│   ├── db_connection.py             # PostgreSQL connection management
│   ├── schema.py                    # Database table creation
│   └── models.py                    # Data access layer (ORM-like)
├── config/
│   └── config.py                    # Configuration management
├── powerbi/
│   ├── POWERBI_SETUP_GUIDE.md      # Power BI integration guide
│   └── POWERBI_QUERIES.sql          # Pre-built SQL queries for Power BI
├── data/
│   └── (exported CSV files)
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
└── README.md                        # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- **Optional:** PostgreSQL 12+ (for production; SQLite used by default)

### Step 1: Clone Repository
```bash
cd StockPortfolioProject
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your database credentials
# Update: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
```

### Step 5: Verify Database Connection
```bash
python -c "from database.db_connection import DatabaseConnection; from config.config import config; db = DatabaseConnection(config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD, config.DB_PORT); print('Connected!' if db.connect() else 'Failed')"
```

---

## ⚙️ Configuration

### Database Options

**Default (SQLite)** - No additional setup required
```env
DB_TYPE=sqlite
```

**PostgreSQL** (optional) - For production use
```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_portfolio
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### Environment Variables (.env)

```env
# Database: 'sqlite' (default) or 'postgresql'
DB_TYPE=sqlite

# PostgreSQL (optional, only if using PostgreSQL)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_portfolio
DB_USER=postgres
DB_PASSWORD=your_password_here

# yfinance - Fetches LIVE stock prices (free, auto-enabled)
YFINANCE_API_KEY=default

# Financial Settings
RISK_FREE_RATE=0.02                  # Annual risk-free rate

# Logging
LOG_LEVEL=INFO
```

### Live Stock Prices

App automatically fetches **live market prices** from yfinance:
- Real-time AAPL, MSFT, GOOGL prices
- Free API (no keys needed)
- Portfolio updates dynamically

---

## 🎯 Usage

### Quick Start (Flask Dashboard)

```bash
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Run the Flask app
python app.py

# 3. Open http://localhost:5000 in your browser
```

**What you'll see:**
- Real-time portfolio dashboard with live stock prices
- 4 tabs: Overview, Risk Analysis, Holdings, Transactions
- Interactive charts showing portfolio performance
- KPI cards with gain/loss calculations

---

## 💻 Running the Application

### Deploy Flask Dashboard

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run Flask server
python app.py
```

Open http://localhost:5000 in browser

### Using PostgreSQL

Update `.env` to use PostgreSQL instead of SQLite:

```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_portfolio
DB_USER=postgres
DB_PASSWORD=your_secure_password
```

Then run `python app.py` - the app automatically switches to PostgreSQL.

---

## 🎯 Customization

### Add Custom Holdings

Edit the `HOLDINGS` list in `app.py`:

```python
HOLDINGS = [
    {"ticker": "TSLA", "shares": 5, "purchase_price": 250.00, "purchase_date": "2024-01-15"},
    {"ticker": "META", "shares": 10, "purchase_price": 350.00, "purchase_date": "2024-02-10"},
]
```

Prices auto-fetch from yfinance.

### Portfolio Value Calculation

Current implementation:
- Fetches real-time prices for each holding
- Calculates gain/loss vs. purchase price
- Computes total portfolio value
python main.py

# View logs
tail -f logs/application.log
```

### Using Portfolio Manager

```python
from src.portfolio_manager import PortfolioManager

pm = PortfolioManager()

# Create portfolio
pm.create_portfolio("Growth Portfolio", "Tech and growth stocks")

# Add holdings
pm.add_holding("Growth Portfolio", "AAPL", shares=10, purchase_price=150.00)

# Get summary
summary = pm.get_portfolio_summary("Growth Portfolio")
print(f"Total Value: ${summary['total_current_value']}")
print(f"Total Return: {summary['total_return_pct']:.2f}%")

# Export to CSV
pm.export_portfolio_to_csv("Growth Portfolio", "./data/portfolio.csv")
```

### Fetching Market Data

```python
from src.market_data_fetcher import MarketDataFetcher

fetcher = MarketDataFetcher()

# Get historical data
df = fetcher.fetch_stock_data("AAPL", start_date="2023-01-01", end_date="2024-12-31")

# Get current price
price = fetcher.get_current_price("AAPL")

# Get stock information
info = fetcher.get_stock_info("AAPL")
print(f"Company: {info['name']}")
print(f"Sector: {info['sector']}")
print(f"P/E Ratio: {info['pe_ratio']}")
```

### Calculating Risk Metrics

```python
from src.risk_metrics import RiskMetricsCalculator

calculator = RiskMetricsCalculator(risk_free_rate=0.02)

# Fetch price data
fetcher = MarketDataFetcher()
price_data = fetcher.fetch_stock_data("AAPL")

# Calculate returns
returns = calculator.calculate_returns(price_data)

# Calculate volatility
vol = calculator.calculate_volatility(returns)
print(f"Annual Volatility: {vol['annual_volatility']:.4f}")

# Calculate Sharpe Ratio
sharpe = calculator.calculate_sharpe_ratio(returns)
print(f"Sharpe Ratio: {sharpe:.4f}")

# Calculate max drawdown
max_dd, peak_date, trough_date = calculator.calculate_maximum_drawdown(price_data)
print(f"Maximum Drawdown: {max_dd:.4f} ({peak_date} to {trough_date})")

# Calculate cumulative returns
cum_return = calculator.calculate_cumulative_returns(price_data)
print(f"Total Return: {cum_return:.4f}")
```

---

## 📊 Database Schema

### Tables

#### `stocks`
Reference table for stock information
```sql
- stock_id (PK)
- ticker (UNIQUE)
- company_name
- sector
- industry
- market_cap
- pe_ratio
- dividend_yield
- beta
- created_date
- updated_date
```

#### `portfolios`
Portfolio master table
```sql
- portfolio_id (PK)
- portfolio_name (UNIQUE)
- description
- created_date
- updated_date
- total_invested
- current_value
```

#### `holdings`
Current stock positions in portfolios
```sql
- holding_id (PK)
- portfolio_id (FK)
- stock_id (FK)
- shares
- purchase_price
- purchase_value
- current_price
- current_value
- purchase_date
- updated_date
```

#### `transactions`
Buy/sell transaction history
```sql
- transaction_id (PK)
- portfolio_id (FK)
- stock_id (FK)
- action (BUY/SELL)
- shares
- price
- total_value
- transaction_date
- notes
```

#### `price_history`
Historical daily price data
```sql
- price_id (PK)
- stock_id (FK)
- price_date
- open_price
- high_price
- low_price
- close_price
- adj_close_price
- volume
- created_date
```

#### `portfolio_metrics`
Historical portfolio risk metrics
```sql
- metric_id (PK)
- portfolio_id (FK)
- metric_date
- total_value
- daily_return
- annual_return
- annual_volatility
- sharpe_ratio
- max_drawdown
- created_date
```

---

## 📈 Financial Metrics

### Returns
**Definition**: Percentage change in investment value

**Calculation**:
- Daily Returns: $(P_t - P_{t-1}) / P_{t-1}$
- Annualized Return: Mean Daily Return × 252 trading days

**Interpretation**: Positive returns indicate gains; negative indicate losses

---

### Volatility
**Definition**: Standard deviation of returns; measure of price fluctuation

**Calculation**:
- Daily Volatility: Standard deviation of daily returns
- Annualized Volatility: Daily Volatility × √252

**Interpretation**: Higher volatility = higher risk; typical stock: 15-30% annual

---

### Sharpe Ratio
**Definition**: Risk-adjusted return metric

**Formula**: 
$$\text{Sharpe Ratio} = \frac{\text{Mean Return} - \text{Risk-Free Rate}}{\text{Volatility}}$$

**Interpretation**:
- SR > 1: Good risk-adjusted return
- SR > 2: Excellent
- SR < 0: Returns worse than risk-free rate

---

### Maximum Drawdown
**Definition**: Largest peak-to-trough percentage decline

**Formula**: 
$$\text{Max Drawdown} = \frac{\text{Trough} - \text{Peak}}{\text{Peak}}$$

**Interpretation**: Shows worst-case loss scenario; used for risk assessment

---

## 📊 Power BI Integration

### Connection Setup
1. Open Power BI Desktop
2. Click **Get Data** → **PostgreSQL database**
3. Enter database credentials
4. Import tables

### Dashboard Pages Included

**Page 1: Portfolio Overview**
- Total value KPI
- Return percentage KPI
- Portfolio allocation pie chart
- Value trend line chart

**Page 2: Risk Metrics**
- Volatility gauge
- Sharpe ratio history
- Drawdown KPI
- Risk vs return scatter

**Page 3: Holdings Detail**
- Holdings table with performance
- Individual stock charts
- Gain/loss by position

**Page 4: Transactions**
- Transaction history
- Monthly activity
- Buy/sell analysis

### Pre-built Queries
SQL queries available in `powerbi/POWERBI_QUERIES.sql` for:
- Portfolio summary
- Holdings with performance
- Metrics history
- Price trends
- Transaction analysis

See [POWERBI_SETUP_GUIDE.md](powerbi/POWERBI_SETUP_GUIDE.md) for detailed setup instructions.

---

## 🔧 API Reference

### MarketDataFetcher

```python
fetch_stock_data(ticker, start_date, end_date)
  # Fetch historical OHLCV data
  
fetch_multiple_stocks(tickers, start_date, end_date)
  # Fetch data for multiple stocks
  
get_current_price(ticker)
  # Get latest stock price
  
get_stock_info(ticker)
  # Get company information
```

### RiskMetricsCalculator

```python
calculate_returns(price_data)
  # Calculate daily/weekly/monthly returns
  
calculate_volatility(returns)
  # Calculate standard deviation
  
calculate_sharpe_ratio(returns)
  # Calculate risk-adjusted return
  
calculate_maximum_drawdown(price_data)
  # Calculate worst drawdown
  
calculate_cumulative_returns(price_data)
  # Calculate total return
  
calculate_portfolio_metrics(weights, prices_dict)
  # Calculate all metrics for portfolio
```

### PortfolioManager

```python
create_portfolio(portfolio_name, description)
  # Create new portfolio
  
add_holding(portfolio_name, ticker, shares, purchase_price)
  # Add stock to portfolio
  
update_holding(portfolio_name, ticker, shares, current_price)
  # Update position size/price
  
remove_holding(portfolio_name, ticker)
  # Sell entire position
  
get_portfolio_summary(portfolio_name)
  # Get portfolio details and metrics
  
export_portfolio_to_csv(portfolio_name, filepath)
  # Export holdings to CSV
```

---

## 📚 Examples

### Example 1: Create and Analyze Portfolio

```python
from main import PortfolioAnalyzer

analyzer = PortfolioAnalyzer()
analyzer.initialize_database()

# Create portfolio
analyzer.portfolio_model.create_portfolio(
    "Dividend Portfolio",
    "High-yield dividend stocks"
)

# Add dividend stocks
stocks = [
    ("JNJ", 20, 160.00),    # Johnson & Johnson
    ("PG", 15, 130.00),     # Procter & Gamble
    ("KO", 25, 60.00)       # Coca-Cola
]

for ticker, shares, price in stocks:
    analyzer.add_stock_to_portfolio("Dividend Portfolio", ticker, shares, price)

# Update prices
analyzer.update_portfolio_prices("Dividend Portfolio")

# Calculate metrics
metrics = analyzer.calculate_portfolio_metrics("Dividend Portfolio")

print(f"Annual Return: {metrics['annual_return']:.2%}")
print(f"Volatility: {metrics['annual_volatility']:.2%}")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.4f}")

# Generate report
report = analyzer.generate_portfolio_report("Dividend Portfolio")
```

### Example 2: Track Multiple Portfolios

```python
from main import PortfolioAnalyzer

analyzer = PortfolioAnalyzer()
analyzer.initialize_database()

portfolios = {
    "Growth": ["AAPL", "MSFT", "GOOGL"],
    "Value": ["JNJ", "PG", "KO"],
    "Tech": ["NVDA", "AMD", "INTC"]
}

for portfolio_name, tickers in portfolios.items():
    analyzer.portfolio_model.create_portfolio(portfolio_name)
    
    for ticker in tickers:
        # Fetch current price
        price = analyzer.market_fetcher.get_current_price(ticker)
        analyzer.add_stock_to_portfolio(portfolio_name, ticker, shares=10, purchase_price=price)

# Compare all portfolios
all_portfolios = analyzer.portfolio_model.get_all_portfolios()
for p in all_portfolios:
    metrics = analyzer.calculate_portfolio_metrics(p['portfolio_name'])
    print(f"{p['portfolio_name']}: Sharpe = {metrics.get('sharpe_ratio', 0):.4f}")
```

### Example 3: Monitor Portfolio with Price Updates

```python
import schedule
import time
from main import PortfolioAnalyzer

analyzer = PortfolioAnalyzer()
analyzer.initialize_database()

def update_portfolio():
    """Update portfolio prices and metrics daily"""
    try:
        analyzer.update_portfolio_prices("My Portfolio")
        metrics = analyzer.calculate_portfolio_metrics("My Portfolio")
        print(f"Updated at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current Sharpe Ratio: {metrics['sharpe_ratio']:.4f}")
    except Exception as e:
        print(f"Error: {e}")

# Schedule updates for market close (4 PM EST)
schedule.every().day.at("16:00").do(update_portfolio)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🐛 Troubleshooting

### Database Connection Issues

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
1. Verify PostgreSQL is running: `pg_isready -h localhost`
2. Check credentials in `.env` file
3. Verify database exists: `psql -l` in psql
4. Check firewall allows port 5432

### yfinance Data Issues

**Error**: `No data found for ticker XXXX`

**Solutions**:
1. Verify ticker symbol is correct
2. Check ticker hasn't been delisted
3. Ensure internet connection is active
4. Try different date range

### Power BI Connection Issues

**Error**: `Gateway error` or `Connection timeout`

**Solutions**:
1. Install On-premises Data Gateway for PostgreSQL
2. Verify gateway is running and healthy
3. Check PostgreSQL credentials in gateway
4. Test connection with Query Editor

### Performance Issues

**Slow queries**:
1. Add indexes on frequently filtered columns:
   ```sql
   CREATE INDEX idx_portfolio_metrics_date ON portfolio_metrics(portfolio_id, metric_date DESC);
   ```
2. Partition large tables by date
3. Archive old transaction data

**Large dataset handling**:
1. Use date filters in queries
2. Aggregate historical metrics
3. Implement data retention policies

---

## 📝 License

This project is provided as-is for educational and personal use.

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional risk metrics (Value at Risk, Conditional Value at Risk)
- Machine learning portfolio optimization
- Multi-currency support
- Mobile app interface
- Real-time streaming data

---

## 📧 Support

For issues or questions:
1. Check troubleshooting section
2. Review PostgreSQL and yfinance documentation
3. Check application logs in `logs/` directory

---

**Last Updated**: February 2026  
**Version**: 1.0
