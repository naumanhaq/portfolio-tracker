#!/usr/bin/env python3
"""
Complete 3-page generator:
- index.html: Landing/blog
- holdings.html: Portfolio tracker
- trades.html: Options log
"""

import json
from pathlib import Path
from datetime import datetime, date

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PUBLIC_DIR = PROJECT_ROOT
PUBLIC_DIR.mkdir(exist_ok=True)

def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def calculate_holding_period(entry_date_str):
    entry = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
    today = date.today()
    delta = today - entry
    years = delta.days // 365
    months = (delta.days % 365) // 30
    return f"{years}y {months}m" if years > 0 else (f"{months}m" if months > 0 else f"{delta.days}d")

def calculate_return(entry_price, current_price):
    if not current_price:
        return None
    return ((current_price - entry_price) / entry_price) * 100

def nav_html(active="home"):
    pages = [
        ("home", "Home", "index.html"),
        ("holdings", "Holdings", "holdings.html"),
        ("trades", "Trades", "trades.html")
    ]
    nav = '<nav>\n'
    for key, label, url in pages:
        active_class = ' class="active"' if key == active else ''
        nav += f'            <a href="{url}"{active_class}>{label}</a>\n'
    nav += '        </nav>'
    return nav

def base_styles():
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'EB Garamond', serif;
            background: #ffffff;
            color: #1a1a1a;
            line-height: 1.7;
            padding: 40px 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 {
            font-family: 'Caveat', cursive;
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        h2 {
            font-family: 'Crimson Text', serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid #2c2c2c;
            padding-bottom: 0.5rem;
        }
        nav {
            margin: 0 0 3rem 0;
            border-bottom: 1px solid #ccc;
            padding-bottom: 1rem;
        }
        nav a {
            font-family: 'Crimson Text', serif;
            text-decoration: none;
            color: #2c2c2c;
            margin-right: 2rem;
            font-size: 1.1rem;
            border-bottom: 2px solid transparent;
            padding-bottom: 2px;
        }
        nav a:hover { border-bottom: 2px solid #2c2c2c; }
        nav a.active { border-bottom: 2px solid #2c2c2c; font-weight: 600; }
        footer {
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #ccc;
            text-align: center;
            font-size: 0.85rem;
            color: #999;
        }
"""

def generate_index(posts_data, holdings_data):
    posts = posts_data["posts"]
    performance = holdings_data.get("performance", {})
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>enhaq.capital</title>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {base_styles()}
        .post {{ margin: 3rem 0; padding-bottom: 3rem; border-bottom: 1px solid #e5e5e5; }}
        .post:last-child {{ border-bottom: none; }}
        .post-date {{ font-size: 0.9rem; color: #999; margin-bottom: 0.5rem; }}
        .post-title {{ font-family: 'Crimson Text', serif; font-size: 2rem; font-weight: 600; margin-bottom: 1rem; }}
        .post-content {{ font-size: 1.1rem; line-height: 1.8; }}
        .post-content p {{ margin-bottom: 1rem; }}
        .quick-stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0 3rem 0; padding: 2rem; border: 1px solid #e5e5e5; }}
        .stat-label {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 500; margin-top: 0.25rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header><h1>enhaq.capital</h1></header>
        {nav_html("home")}
        <div class="quick-stats">
            <div><div class="stat-label">YTD Return</div><div class="stat-value">+{performance.get('ytd_return', 0):.1f}%</div></div>
            <div><div class="stat-label">Since Inception</div><div class="stat-value">+{performance.get('since_inception_return', 0):.1f}%</div></div>
            <div><div class="stat-label">Annualized IRR</div><div class="stat-value">{performance.get('annualized_irr', 0):.1f}%</div></div>
        </div>
"""
    
    for post in posts:
        paragraphs = post["content"].split("\n\n")
        content_html = "\n".join(f"<p>{p}</p>" for p in paragraphs if p.strip())
        html += f"""
        <article class="post">
            <div class="post-date">{post['date']}</div>
            <h2 class="post-title">{post['title']}</h2>
            <div class="post-content">{content_html}</div>
        </article>
"""
    
    html += """
    </div>
</body>
</html>
"""
    return html

def generate_holdings(holdings_data):
    portfolio = holdings_data["portfolio"]
    performance = holdings_data.get("performance", {})
    last_updated = holdings_data["last_updated"]
    inception = holdings_data.get("portfolio_inception", "N/A")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holdings | enhaq.capital</title>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {base_styles()}
        .subtitle {{ font-family: 'Crimson Text', serif; font-size: 1.2rem; color: #666; font-style: italic; }}
        .meta {{ font-size: 0.9rem; color: #999; margin-bottom: 3rem; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin: 2rem 0; }}
        .metric {{ border: 1px solid #e5e5e5; padding: 1.5rem; }}
        .metric-label {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; margin-bottom: 0.5rem; }}
        .metric-value {{ font-size: 2rem; font-weight: 500; }}
        .metric-value.positive {{ color: #2d5016; }}
        table {{ width: 100%; border-collapse: collapse; margin: 2rem 0; border: 1px solid #e5e5e5; }}
        thead {{ border-bottom: 2px solid #2c2c2c; }}
        th {{ text-align: left; padding: 1rem; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; }}
        th.right {{ text-align: right; }}
        td {{ padding: 1rem; border-bottom: 1px solid #f0f0f0; }}
        td.right {{ text-align: right; }}
        tbody tr:hover {{ background: #f9f9f9; }}
        .ticker {{ font-family: 'Courier New', monospace; font-weight: bold; }}
        .category {{ display: inline-block; padding: 0.25rem 0.5rem; border: 1px solid #ccc; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        .positive {{ color: #2d5016; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Portfolio</h1>
            <p class="subtitle">Long-term concentrated positions</p>
            <p class="meta">As of {last_updated} · Inception {inception}</p>
        </header>
        {nav_html("holdings")}
        <div class="metrics">
            <div class="metric"><div class="metric-label">YTD Return</div><div class="metric-value positive">+{performance.get('ytd_return', 0):.1f}%</div></div>
            <div class="metric"><div class="metric-label">1-Year Return</div><div class="metric-value positive">+{performance.get('one_year_return', 0):.1f}%</div></div>
            <div class="metric"><div class="metric-label">Since Inception</div><div class="metric-value positive">+{performance.get('since_inception_return', 0):.1f}%</div></div>
            <div class="metric"><div class="metric-label">Annualized IRR</div><div class="metric-value">{performance.get('annualized_irr', 0):.1f}%</div></div>
        </div>
        <h2>Current Positions</h2>
        <table><thead><tr>
            <th>Ticker</th><th>Name</th><th>Category</th><th>Geography</th>
            <th class="right">Allocation</th><th class="right">Return</th><th class="right">Holding Period</th>
        </tr></thead><tbody>
"""
    
    for holding in portfolio:
        ret = calculate_return(holding["entry_price"], holding.get("current_price"))
        period = calculate_holding_period(holding["entry_date"])
        ret_sign = "+" if ret and ret > 0 else ""
        
        html += f"""
            <tr>
                <td class="ticker">{holding['ticker']}</td>
                <td>{holding['name']}</td>
                <td><span class="category">{holding['category']}</span></td>
                <td>{holding.get('geography', 'N/A')}</td>
                <td class="right"><strong>{holding['allocation_pct']:.1f}%</strong></td>
                <td class="right positive"><strong>{ret_sign}{ret:.1f}%</strong></td>
                <td class="right">{period}</td>
            </tr>
"""
    
    html += """
        </tbody></table>
    </div>
</body>
</html>
"""
    return html

def generate_trades(trades_data):
    trades = trades_data["trades"]
    performance = trades_data.get("performance", {})
    last_updated = trades_data["last_updated"]
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trades | enhaq.capital</title>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {base_styles()}
        .subtitle {{ font-family: 'Crimson Text', serif; font-size: 1.2rem; color: #666; font-style: italic; }}
        .meta {{ font-size: 0.9rem; color: #999; margin-bottom: 3rem; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin: 2rem 0; }}
        .metric {{ border: 1px solid #e5e5e5; padding: 1.5rem; }}
        .metric-label {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; margin-bottom: 0.5rem; }}
        .metric-value {{ font-size: 2rem; font-weight: 500; }}
        table {{ width: 100%; border-collapse: collapse; margin: 2rem 0; border: 1px solid #e5e5e5; }}
        thead {{ border-bottom: 2px solid #2c2c2c; }}
        th {{ text-align: left; padding: 1rem; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; }}
        th.right {{ text-align: right; }}
        td {{ padding: 1rem; border-bottom: 1px solid #f0f0f0; }}
        td.right {{ text-align: right; }}
        tbody tr {{ cursor: pointer; }}
        tbody tr:hover {{ background: #f9f9f9; }}
        .ticker {{ font-family: 'Courier New', monospace; font-weight: bold; }}
        .status {{ display: inline-block; padding: 0.25rem 0.5rem; border: 1px solid; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        .status.open {{ border-color: #2d5016; color: #2d5016; }}
        .status.closed {{ border-color: #666; color: #666; }}
        .detail-row {{ display: none; }}
        .detail-row.show {{ display: table-row; }}
        .detail-cell {{ padding: 2rem; background: #f9f9f9; border-bottom: 2px solid #e5e5e5; }}
        .detail-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
        .detail-section {{ margin-bottom: 1.5rem; }}
        .section-title {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; margin-bottom: 0.5rem; font-weight: 600; }}
        .structure {{ font-family: 'Courier New', monospace; font-size: 0.9rem; line-height: 1.8; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Options</h1>
            <p class="subtitle">Volatility-based strategies</p>
            <p class="meta">As of {last_updated}</p>
        </header>
        {nav_html("trades")}
        <div class="metrics">
            <div class="metric"><div class="metric-label">Total Trades</div><div class="metric-value">{len(trades)}</div></div>
            <div class="metric"><div class="metric-label">Win Rate</div><div class="metric-value">{performance.get('win_rate', 0):.0f}%</div></div>
            <div class="metric"><div class="metric-label">Avg Return</div><div class="metric-value">{performance.get('avg_return', 0):.1f}%</div></div>
            <div class="metric"><div class="metric-label">Total P&L</div><div class="metric-value">${performance.get('total_pnl', 0):,.0f}</div></div>
        </div>
        <h2>Trade Log</h2>
        <table><thead><tr>
            <th>ID</th><th>Ticker</th><th>Type</th><th>Classification</th>
            <th>Entry Date</th><th>Status</th><th class="right">Net Debit</th>
        </tr></thead><tbody>
"""
    
    for trade in trades:
        status_class = "open" if trade["status"] == "open" else "closed"
        html += f"""
            <tr onclick="toggleDetail('{trade['id']}')">
                <td>{trade['id']}</td>
                <td class="ticker">{trade['ticker']}</td>
                <td>{trade['trade_type']}</td>
                <td>{trade['classification']}</td>
                <td>{trade['entry_date']}</td>
                <td><span class="status {status_class}">{trade['status']}</span></td>
                <td class="right">${trade['structure']['net_debit']:.2f}</td>
            </tr>
            <tr class="detail-row" id="detail-{trade['id']}">
                <td colspan="7" class="detail-cell">
                    <div class="detail-grid">
                        <div class="detail-section">
                            <div class="section-title">Entry Thesis</div>
                            <p>{trade['entry_thesis']}</p>
                        </div>
                        <div class="detail-section">
                            <div class="section-title">Structure</div>
                            <div class="structure">
                                Long: {trade['structure']['long']}<br>
                                Short: {trade['structure']['short']}<br>
                                Net Debit: ${trade['structure']['net_debit']:.2f}
                            </div>
                        </div>
                    </div>
                    <div class="detail-grid">
                        <div class="detail-section">
                            <div class="section-title">Vol Metrics</div>
                            <div class="structure">
                                IV%: {trade['moontower_metrics']['iv_percentile']}<br>
                                VRP: {trade['moontower_metrics']['vrp']}<br>
                                RV%: {trade['moontower_metrics']['rv_percentile']}<br>
                                Term: {trade['moontower_metrics']['term_structure']}
                            </div>
                        </div>
                        <div class="detail-section">
                            <div class="section-title">Greeks at Entry</div>
                            <div class="structure">
                                Delta: {trade['greeks_at_entry']['delta']}<br>
                                Theta: {trade['greeks_at_entry']['theta']}<br>
                                Vega: {trade['greeks_at_entry']['vega']}
                            </div>
                        </div>
                    </div>
                    <div class="detail-grid">
                        <div class="detail-section">
                            <div class="section-title">Expected Outcome</div>
                            <p>{trade['expected_outcome']}</p>
                        </div>
                        <div class="detail-section">
                            <div class="section-title">Actual Outcome</div>
                            <p>{trade['actual_outcome'] or 'Pending (trade open)'}</p>
                        </div>
                    </div>
                </td>
            </tr>
"""
    
    html += """
        </tbody></table>
    </div>
    <script>
        function toggleDetail(tradeId) {{
            const row = document.getElementById('detail-' + tradeId);
            row.classList.toggle('show');
        }}
    </script>
</body>
</html>
"""
    return html

def main():
    print("🔨 Generating 3-page site...")
    
    holdings_data = load_json("holdings.json")
    trades_data = load_json("trades.json")
    posts_data = load_json("posts.json")
    
    index_html = generate_index(posts_data, holdings_data)
    holdings_html = generate_holdings(holdings_data)
    trades_html = generate_trades(trades_data)
    
    with open(PUBLIC_DIR / "index.html", "w") as f:
        f.write(index_html)
    with open(PUBLIC_DIR / "holdings.html", "w") as f:
        f.write(holdings_html)
    with open(PUBLIC_DIR / "trades.html", "w") as f:
        f.write(trades_html)
    
    print("✅ Site generated:")
    print(f"   - {PUBLIC_DIR / 'index.html'}")
    print(f"   - {PUBLIC_DIR / 'holdings.html'}")
    print(f"   - {PUBLIC_DIR / 'trades.html'}")

if __name__ == "__main__":
    main()
