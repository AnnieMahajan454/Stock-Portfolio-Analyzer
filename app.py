from flask import Flask, render_template
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Sample portfolio data
portfolio_data = {
    "portfolio_name": "Tech Growth Portfolio",
    "total_value": 28750.00,
    "total_invested": 25400.00,
    "total_gain": 3350.00,
    "total_return_pct": 13.19,
    "sharpe_ratio": 1.42,
    "annual_volatility": 0.182,
    "max_drawdown": -0.125,
    
    "holdings": [
        {
            "ticker": "AAPL",
            "company": "Apple Inc.",
            "shares": 10,
            "purchase_price": 150.00,
            "current_price": 178.50,
            "current_value": 1785.00,
            "gain_loss": 285.00,
            "gain_loss_pct": 19.0,
            "sector": "Technology"
        },
        {
            "ticker": "MSFT",
            "company": "Microsoft Corp.",
            "shares": 5,
            "purchase_price": 300.00,
            "current_price": 326.00,
            "current_value": 1630.00,
            "gain_loss": 130.00,
            "gain_loss_pct": 21.7,
            "sector": "Technology"
        },
        {
            "ticker": "GOOGL",
            "company": "Alphabet Inc.",
            "shares": 8,
            "purchase_price": 2800.00,
            "current_price": 3150.00,
            "current_value": 25200.00,
            "gain_loss": 2800.00,
            "gain_loss_pct": 12.5,
            "sector": "Technology"
        }
    ],
    
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
        {"date": "2024-08-01", "value": 28750, "return": 13.19, "volatility": 0.182}
    ]
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', data=json.dumps(portfolio_data))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
