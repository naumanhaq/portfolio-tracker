#!/usr/bin/env python3
"""
Complete 3-page generator with SEO + risk columns
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

def seo_meta(page="home"):
    meta = {
        "home": {
            "title": "enhaq.capital – Long what survives, short what doesn't",
            "description": "Concentrated equity positions and volatility strategies. Portfolio commentary and trade transparency.",
        },
        "holdings": {
            "title": "Holdings – enhaq.capital",
            "description": "Long-term concentrated positions in enduring businesses. Performance metrics and portfolio composition.",
        },
        "trades": {
            "title": "Trades – enhaq.capital",
            "description": "Options trade log. Volatility-based strategies with full transparency on structure, risk, and outcomes.",
        }
    }
    
    m = meta.get(page, meta["home"])
    
    return f"""<meta name="description" content="{m['description']}">
    <meta property="og:title" content="{m['title']}">
    <meta property="og:description" content="{m['description']}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">"""

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

def page_header(page_type="home"):
    taglines = {
        "home": "Long what survives, short what doesn't.",
        "holdings": "Concentrated positions in enduring businesses.",
        "trades": "Volatility trades. Short duration, asymmetric payoff."
    }
    
    return f"""
        <header class="site-header">
            <h1>enhaq capital</h1>
        </header>
        
        {nav_html(page_type)}
        
        <div class="page-tagline">
            {taglines.get(page_type, "")}
        </div>
"""

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
        .site-header { margin-bottom: 1.5rem; }
        h1 {
            font-family: 'Caveat', cursive;
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0;
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
            margin: 1.5rem 0;
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
        .page-tagline {
            font-family: 'Crimson Text', serif;
            font-size: 1.1rem;
            color: #666;
            font-style: italic;
            margin: 0 0 3rem 0;
            padding: 1.5rem 0;
            border-bottom: 1px solid #e5e5e5;
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
    <title>enhaq.capital – Long what survives, short what doesn't</title>
    {seo_meta("home")}
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
        .stat-note {{ font-size: 0.75rem; color: #999; margin-top: 0.25rem; }}
    </style>
</head>
<body>
    <div class="container">
        {page_header("home")}
        <div class="quick-stats">
            <div>
                <div class="stat-label">YTD Return</div>
                <div class="stat-value">+{performance.get('ytd_return', 0):.1f}%</div>
                <div class="stat-note">Combined (equity + vol)</div>
            </div>
            <div>
                <div class="stat-label">Since Inception</div>
                <div class="stat-value">+{performance.get('since_inception_return', 0):.1f}%</div>
                <div class="stat-note">Combined portfolio</div>
            </div>
            <div>
                <div class="stat-label">Annualized IRR</div>
                <div class="stat-value">{performance.get('annualized_irr', 0):.1f}%</div>
                <div class="stat-note">Time-weighted</div>
            </div>
        </div>
"""
    
    for post in posts:
        paragraphs = post["content"].split("\n\n")
        content_html = "\n".join(f"<p>{p}</p>" for p in paragraphs if p.strip())
        date_html = f'<div class="post-date">{post["date"]}</div>' if post.get("date") else ''
        html += f"""
        <article class="post">
            {date_html}
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
    <title>Holdings – enhaq.capital</title>
    {seo_meta("holdings")}
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {base_styles()}
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
        {page_header("holdings")}
        <p class="meta" style="margin-top: -2rem; margin-bottom: 2rem;">As of {last_updated} · Inception {inception}</p>
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
    <title>Trades – enhaq.capital</title>
    {seo_meta("trades")}
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {base_styles()}
        .meta {{ font-size: 0.9rem; color: #999; margin-bottom: 3rem; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin: 2rem 0; }}
        .metric {{ border: 1px solid #e5e5e5; padding: 1.5rem; }}
        .metric-label {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; margin-bottom: 0.5rem; }}
        .metric-value {{ font-size: 2rem; font-weight: 500; }}
        table {{ width: 100%; border-collapse: collapse; margin: 2rem 0; border: 1px solid #e5e5e5; font-size: 0.9rem; }}
        thead {{ border-bottom: 2px solid #2c2c2c; }}
        th {{ text-align: left; padding: 0.75rem; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; }}
        th.right {{ text-align: right; }}
        td {{ padding: 0.75rem; border-bottom: 1px solid #f0f0f0; }}
        td.right {{ text-align: right; }}
        tbody tr {{ cursor: pointer; }}
        tbody tr:hover {{ background: #f9f9f9; }}
        .ticker {{ font-family: 'Courier New', monospace; font-weight: bold; }}
        .status {{ display: inline-block; padding: 0.25rem 0.5rem; border: 1px solid; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        .status.open {{ border-color: #2d5016; color: #2d5016; }}
        .status.closed {{ border-color: #666; color: #666; }}
        .positive {{ color: #2d5016; }}
        .negative {{ color: #8b0000; }}
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
        {page_header("trades")}
        <p class="meta" style="margin-top: -2rem; margin-bottom: 2rem;">As of {last_updated}</p>
        
        <div class="metrics">
            <div class="metric"><div class="metric-label">Total Trades</div><div class="metric-value">{len(trades)}</div></div>
            <div class="metric"><div class="metric-label">Win Rate</div><div class="metric-value">{performance.get('win_rate', 0):.0f}%</div></div>
            <div class="metric"><div class="metric-label">Avg Return</div><div class="metric-value">{performance.get('avg_return', 0):.1f}%</div></div>
            <div class="metric"><div class="metric-label">Total P&L</div><div class="metric-value">${performance.get('total_pnl', 0):,.0f}</div></div>
        </div>
        
        <h2>Trade Log</h2>
        <table><thead><tr>
            <th>ID</th>
            <th>Ticker</th>
            <th>Type</th>
            <th>Entry</th>
            <th>Status</th>
            <th class="right">Max Loss</th>
            <th class="right">Max Profit</th>
            <th class="right">Actual P&L</th>
        </tr></thead><tbody>
"""
    
    for trade in trades:
        status_class = "open" if trade["status"] == "open" else "closed"
        max_loss = trade['structure'].get('max_loss', 0)
        profit_pot = trade['structure'].get('profit_potential', 0)
        actual_pnl = trade.get('realized_pnl', 0) or 0
        pnl_class = "positive" if actual_pnl > 0 else ("negative" if actual_pnl < 0 else "")
        pnl_sign = "+" if actual_pnl > 0 else ""
        
        html += f"""
            <tr onclick="toggleDetail('{trade['id']}')">
                <td>{trade['id']}</td>
                <td class="ticker">{trade['ticker']}</td>
                <td>{trade['trade_type']}</td>
                <td>{trade['entry_date']}</td>
                <td><span class="status {status_class}">{trade['status']}</span></td>
                <td class="right negative">-${max_loss:.0f}</td>
                <td class="right positive">+${profit_pot:.0f}</td>
                <td class="right {pnl_class}"><strong>{pnl_sign}${actual_pnl:.0f}</strong></td>
            </tr>
            <tr class="detail-row" id="detail-{trade['id']}">
                <td colspan="8" class="detail-cell">
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
                            <div class="section-title">Risk Profile</div>
                            <div class="structure">
                                Max Loss: ${max_loss:.0f}<br>
                                Max Profit: ${profit_pot:.0f}<br>
                                R:R Ratio: {(profit_pot/max_loss if max_loss > 0 else 0):.2f}:1
                            </div>
                        </div>
                        <div class="detail-section">
                            <div class="section-title">Vol Metrics</div>
                            <div class="structure">
                                IV%: {trade['moontower_metrics']['iv_percentile']}<br>
                                VRP: {trade['moontower_metrics']['vrp']}<br>
                                RV%: {trade['moontower_metrics']['rv_percentile']}<br>
                                Term: {trade['moontower_metrics']['term_structure']}
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
        function toggleDetail(tradeId) {
            const row = document.getElementById('detail-' + tradeId);
            row.classList.toggle('show');
        }
    </script>
</body>
</html>
"""
    return html

def main():
    print("🔨 Generating complete site...")
    
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
    
    print("✅ Complete site generated:")
    print("   - index.html (SEO + combined returns)")
    print("   - holdings.html (SEO)")
    print("   - trades.html (SEO + risk columns: Max Loss | Max Profit | Actual P&L)")

if __name__ == "__main__":
    main()
