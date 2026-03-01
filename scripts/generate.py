#!/usr/bin/env python3
"""
Generate static HTML site from JSON data.
Hand-drawn sketch aesthetic - contemporary + classic.
"""

import json
from pathlib import Path
from datetime import datetime, date

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PUBLIC_DIR = PROJECT_ROOT

# Ensure public dir exists
PUBLIC_DIR.mkdir(exist_ok=True)

def load_json(filename):
    """Load JSON data file."""
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def calculate_holding_period(entry_date_str):
    """Calculate holding period from entry date."""
    entry = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
    today = date.today()
    delta = today - entry
    
    years = delta.days // 365
    months = (delta.days % 365) // 30
    
    if years > 0:
        return f"{years}y {months}m"
    elif months > 0:
        return f"{months}m"
    else:
        return f"{delta.days}d"

def calculate_return(entry_price, current_price):
    """Calculate return percentage."""
    if not current_price:
        return None
    return ((current_price - entry_price) / entry_price) * 100

def generate_holdings_page(holdings_data):
    """Generate long-term holdings page."""
    portfolio = holdings_data["portfolio"]
    performance = holdings_data.get("performance", {})
    last_updated = holdings_data["last_updated"]
    inception = holdings_data.get("portfolio_inception", "N/A")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio | enhaq.capital</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'EB Garamond', serif;
            background: #faf8f5;
            color: #2c2c2c;
            line-height: 1.7;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        h1 {{
            font-family: 'Caveat', cursive;
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }}
        
        h2 {{
            font-family: 'Crimson Text', serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid #2c2c2c;
            padding-bottom: 0.5rem;
        }}
        
        .subtitle {{
            font-family: 'Crimson Text', serif;
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-style: italic;
        }}
        
        .meta {{
            font-size: 0.9rem;
            color: #999;
            margin-bottom: 3rem;
        }}
        
        nav {{
            margin: 2rem 0;
            border-top: 1px solid #ccc;
            border-bottom: 1px solid #ccc;
            padding: 1rem 0;
        }}
        
        nav a {{
            font-family: 'Crimson Text', serif;
            text-decoration: none;
            color: #2c2c2c;
            margin-right: 2rem;
            font-size: 1.1rem;
            border-bottom: 2px solid transparent;
            padding-bottom: 2px;
            transition: border-color 0.2s;
        }}
        
        nav a:hover {{
            border-bottom: 2px solid #2c2c2c;
        }}
        
        nav a.active {{
            border-bottom: 2px solid #2c2c2c;
            font-weight: 600;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .metric {{
            border: 1px solid #d4d4d4;
            padding: 1.5rem;
            background: white;
        }}
        
        .metric-label {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: 500;
            color: #2c2c2c;
        }}
        
        .metric-value.positive {{
            color: #2d5016;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: white;
            border: 1px solid #d4d4d4;
        }}
        
        thead {{
            border-bottom: 2px solid #2c2c2c;
        }}
        
        th {{
            text-align: left;
            padding: 1rem;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
        }}
        
        th.right {{
            text-align: right;
        }}
        
        td {{
            padding: 1rem;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        td.right {{
            text-align: right;
        }}
        
        tbody tr:hover {{
            background: #fafafa;
        }}
        
        .ticker {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 0.95rem;
        }}
        
        .category {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border: 1px solid #ccc;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .positive {{
            color: #2d5016;
        }}
        
        .negative {{
            color: #8b0000;
        }}
        
        .summary {{
            margin: 3rem 0;
            padding: 2rem;
            border: 1px solid #d4d4d4;
            background: white;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 1.5rem;
        }}
        
        .summary-item {{
            border-left: 3px solid #2c2c2c;
            padding-left: 1rem;
        }}
        
        .summary-label {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        
        .summary-value {{
            font-size: 1.8rem;
            font-weight: 500;
        }}
        
        .summary-note {{
            font-size: 0.8rem;
            color: #999;
            margin-top: 0.25rem;
        }}
        
        footer {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #ccc;
            text-align: center;
            font-size: 0.85rem;
            color: #999;
        }}
        
        footer p {{
            margin: 0.5rem 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <h1>Portfolio</h1>
            <p class="subtitle">Long-term concentrated positions</p>
            <p class="meta">As of {last_updated} · Inception {inception}</p>
        </header>

        <!-- Navigation -->
        <nav>
            <a href="index.html" class="active">Holdings</a>
            <a href="options.html">Options</a>
        </nav>

        <!-- Performance Metrics -->
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">YTD Return</div>
                <div class="metric-value positive">+{performance.get('ytd_return', 0):.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">1-Year Return</div>
                <div class="metric-value positive">+{performance.get('one_year_return', 0):.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Since Inception</div>
                <div class="metric-value positive">+{performance.get('since_inception_return', 0):.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Annualized IRR</div>
                <div class="metric-value">{performance.get('annualized_irr', 0):.1f}%</div>
            </div>
        </div>

        <!-- Holdings Table -->
        <h2>Current Positions</h2>
        <table>
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Geography</th>
                    <th class="right">Allocation</th>
                    <th class="right">Return</th>
                    <th class="right">Holding Period</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for holding in portfolio:
        holding_return = calculate_return(holding["entry_price"], holding.get("current_price"))
        holding_period = calculate_holding_period(holding["entry_date"])
        return_class = "positive" if holding_return and holding_return > 0 else "negative"
        return_sign = "+" if holding_return and holding_return > 0 else ""
        
        html += f"""
                <tr>
                    <td class="ticker">{holding['ticker']}</td>
                    <td>{holding['name']}</td>
                    <td><span class="category">{holding['category']}</span></td>
                    <td>{holding.get('geography', 'N/A')}</td>
                    <td class="right"><strong>{holding['allocation_pct']:.1f}%</strong></td>
                    <td class="right {return_class}"><strong>{return_sign}{holding_return:.1f}%</strong></td>
                    <td class="right">{holding_period}</td>
                </tr>
"""
    
    html += f"""
            </tbody>
        </table>

        <!-- Summary -->
        <div class="summary">
            <h2>Portfolio Characteristics</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-label">Total Positions</div>
                    <div class="summary-value">{len(portfolio)}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Concentration</div>
                    <div class="summary-value">High</div>
                    <div class="summary-note">Top 3: {sum(h['allocation_pct'] for h in portfolio[:3]):.0f}%</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Investment Horizon</div>
                    <div class="summary-value">20+ years</div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer>
            <p>Past performance does not guarantee future results.</p>
            <p>This portfolio tracker is for informational purposes only.</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

def generate_trades_page(trades_data):
    """Generate options trades page."""
    # Simplified for now - similar aesthetic
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Options | enhaq.capital</title>
</head>
<body>
<p>Options page - coming soon</p>
</body>
</html>"""

def main():
    print("🔨 Generating portfolio site...")
    
    # Load data
    holdings_data = load_json("holdings.json")
    trades_data = load_json("trades.json")
    
    # Generate pages
    holdings_html = generate_holdings_page(holdings_data)
    trades_html = generate_trades_page(trades_data)
    
    # Write to root
    with open(PUBLIC_DIR / "index.html", "w") as f:
        f.write(holdings_html)
    
    with open(PUBLIC_DIR / "options.html", "w") as f:
        f.write(trades_html)
    
    print(f"✅ Site generated:")
    print(f"   - {PUBLIC_DIR / 'index.html'}")
    print(f"   - {PUBLIC_DIR / 'options.html'}")

if __name__ == "__main__":
    main()
