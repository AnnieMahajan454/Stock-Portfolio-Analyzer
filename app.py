from flask import Flask, render_template
import json
from datetime import datetime, timedelta
import os
import sqlite3
import numpy as np
from dotenv import load_dotenv

# Try to import yfinance and psycopg2 (optional)
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Database configuration
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' or 'postgresql'
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'portfolio.db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Portfolio holdings (used to fetch live data)
HOLDINGS = [
    {"ticker": "AAPL", "shares": 10, "purchase_price": 150.00, "purchase_date": "2024-01-15"},
    {"ticker": "MSFT", "shares": 5, "purchase_price": 300.00, "purchase_date": "2024-02-10"},
    {"ticker": "GOOGL", "shares": 8, "purchase_price": 2800.00, "purchase_date": "2024-03-05"}
]

def get_database_connection():
    """Get database connection - tries PostgreSQL first, falls back to SQLite"""
    if DB_TYPE == 'postgresql' and PSYCOPG2_AVAILABLE:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("✓ Connected to PostgreSQL")
            return conn, 'postgresql'
        except Exception as e:
            print(f"⚠ PostgreSQL connection failed: {e}. Falling back to SQLite.")
    
    # Fall back to SQLite
    if os.path.exists('portfolio.db'):
        try:
            conn = sqlite3.connect('portfolio.db')
            conn.row_factory = sqlite3.Row
            print("✓ Connected to SQLite")
            return conn, 'sqlite'
        except Exception as e:
            print(f"⚠ SQLite connection failed: {e}")
    
    return None, None

def get_live_prices():
    """Fetch live stock prices from yfinance"""
    if not YFINANCE_AVAILABLE:
        return get_sample_prices()
    
    try:
        prices = {}
        for holding in HOLDINGS:
            ticker = holding['ticker']
            data = yf.Ticker(ticker)
            price = data.info.get('currentPrice') or data.info.get('regularMarketPrice')
            if price:
                prices[ticker] = float(price)
            else:
                prices[ticker] = holding['purchase_price']  # Fallback
        print(f"✓ Fetched live prices: {prices}")
        return prices
    except Exception as e:
        print(f"⚠ Error fetching live prices: {e}. Using sample data.")
        return get_sample_prices()

def get_sample_prices():
    """Fallback sample prices"""
    return {
        "AAPL": 178.50,
        "MSFT": 326.00,
        "GOOGL": 3150.00
    }

def get_portfolio_data():
    """Build portfolio data with live prices"""
    live_prices = get_live_prices()
    
    holdings = []
    total_value = 0
    total_invested = 0
    
    for holding in HOLDINGS:
        ticker = holding['ticker']
        shares = holding['shares']
        purchase_price = holding['purchase_price']
        current_price = live_prices.get(ticker, purchase_price)
        
        current_value = shares * current_price
        invested = shares * purchase_price
        gain_loss = current_value - invested
        gain_loss_pct = (gain_loss / invested * 100) if invested > 0 else 0
        
        total_value += current_value
        total_invested += invested
        
        stock_names = {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corp.",
            "GOOGL": "Alphabet Inc."
        }
        
        holdings.append({
            "ticker": ticker,
            "company": stock_names.get(ticker, ticker),
            "shares": shares,
            "purchase_price": round(purchase_price, 2),
            "current_price": round(current_price, 2),
            "current_value": round(current_value, 2),
            "gain_loss": round(gain_loss, 2),
            "gain_loss_pct": round(gain_loss_pct, 2),
            "sector": "Technology"
        })
    
    total_gain = total_value - total_invested
    total_return_pct = (total_gain / total_invested * 100) if total_invested > 0 else 0
    
    # Calculate metrics (simplified)
    sharpe_ratio = 1.42
    annual_volatility = 0.182
    max_drawdown = -0.125
    
    portfolio_data = {
        "portfolio_name": "Tech Growth Portfolio",
        "total_value": round(total_value, 2),
        "total_invested": round(total_invested, 2),
        "total_gain": round(total_gain, 2),
        "total_return_pct": round(total_return_pct, 2),
        "sharpe_ratio": sharpe_ratio,
        "annual_volatility": annual_volatility,
        "max_drawdown": max_drawdown,
        
        "holdings": holdings,
        
        "transactions": [
            {"date": "2024-01-15", "ticker": "AAPL", "action": "BUY", "shares": 10, "price": 150.00, "total": 1500.00},
            {"date": "2024-02-10", "ticker": "MSFT", "action": "BUY", "shares": 5, "price": 300.00, "total": 1500.00},
            {"date": "2024-03-05", "ticker": "GOOGL", "action": "BUY", "shares": 8, "price": 2800.00, "total": 22400.00},
            {"date": "2024-04-20", "ticker": "AAPL", "action": "BUY", "shares": 2, "price": 155.00, "total": 310.00},
            {"date": "2024-08-12", "ticker": "MSFT", "action": "BUY", "shares": 1, "price": 310.00, "total": 310.00}
        ],
        
        "metrics_history": [
            {"date": "2024-01-01", "value": 25400, "return": 0, "volatility": 0.15},
            {"date": "2024-02-01", "value": 25920, "return": 2.05, "volatility": 0.162},
            {"date": "2024-03-01", "value": 26850, "return": 5.71, "volatility": 0.168},
            {"date": "2024-04-01", "value": 26500, "return": 4.34, "volatility": 0.175},
            {"date": "2024-05-01", "value": 27200, "return": 7.09, "volatility": 0.178},
            {"date": "2024-06-01", "value": 27850, "return": 9.58, "volatility": 0.180},
            {"date": "2024-07-01", "value": 28200, "return": 11.02, "volatility": 0.181},
            {"date": "2024-08-01", "value": round(total_value, 2), "return": round(total_return_pct, 2), "volatility": 0.182}
        ]
    }
    
    return portfolio_data

@app.route('/')
def dashboard():
    portfolio_data = get_portfolio_data()
    return render_template('dashboard.html', data=json.dumps(portfolio_data))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
