#!/usr/bin/env python3
"""
Generate bear-signals.html from bear_signals.json
"""

import json
from datetime import datetime

def load_data():
    with open('/data/.openclaw/workspace/bear-signals-repo/data/bear_signals.json', 'r') as f:
        return json.load(f)

def generate_html(data):
    last_updated = datetime.fromisoformat(data['last_updated']).strftime('%B %d, %Y at %I:%M %p UTC')
    
    market = data['market_summary']
    summary = data['summary']
    indicators = data['indicators']
    
    # Determine status
    pct = summary['percentage']
    if pct >= 70:
        status_text = "BEAR MARKET BOTTOM LIKELY"
        status_class = "signal-strong"
    elif pct >= 50:
        status_text = "Moderate signals detected"
        status_class = "signal-moderate"
    else:
        status_text = "Bull market (normal)"
        status_class = "signal-normal"
    
    # Generate indicator rows
    indicator_rows = ""
    for i, ind in enumerate(indicators, 1):
        status_icon = "✓" if ind['met'] else "—"
        row_class = "row-met" if ind['met'] else ""
        
        note_html = f'<div class="ind-note">{ind.get("note", "")}</div>' if ind.get("note") else ""
        
        indicator_rows += f"""
        <tr class="{row_class}">
            <td class="ind-num">{i}</td>
            <td class="ind-check">{status_icon}</td>
            <td class="ind-name"><strong>{ind['name']}</strong><br><span class="ind-desc">{ind['description']}</span>{note_html}</td>
            <td class="ind-val">{ind['value']}</td>
            <td class="ind-thresh">{ind['threshold']}</td>
        </tr>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bear Market Signals | enhaq capital</title>
    <meta name="description" content="Real-time bear market bottom indicators – market-wide technical oversold signals">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'EB Garamond', serif;
            background: #ffffff;
            color: #1a1a1a;
            line-height: 1.7;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .site-header {{ margin-bottom: 1.5rem; }}
        h1 {{
            font-family: 'Caveat', cursive;
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0;
        }}
        h2 {{
            font-family: 'Crimson Text', serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid #2c2c2c;
            padding-bottom: 0.5rem;
        }}
        nav {{
            margin: 1.5rem 0;
            border-bottom: 1px solid #ccc;
            padding-bottom: 1rem;
        }}
        nav a {{
            font-family: 'Crimson Text', serif;
            text-decoration: none;
            color: #2c2c2c;
            margin-right: 2rem;
            font-size: 1.1rem;
            border-bottom: 2px solid transparent;
            padding-bottom: 2px;
        }}
        nav a:hover {{ border-bottom: 2px solid #2c2c2c; }}
        nav a.active {{ border-bottom: 2px solid #2c2c2c; font-weight: 600; }}
        .page-tagline {{
            font-family: 'Crimson Text', serif;
            font-size: 1.1rem;
            color: #666;
            font-style: italic;
            margin: 0 0 2rem 0;
            padding: 1.5rem 0;
            border-bottom: 1px solid #e5e5e5;
        }}
        
        .signal-banner {{
            text-align: center;
            padding: 2rem;
            margin: 2rem 0;
            border: 2px solid #2c2c2c;
            font-family: 'Crimson Text', serif;
            font-size: 1.8rem;
            font-weight: 600;
        }}
        .signal-strong {{ background: #ffe5e5; border-color: #cc0000; color: #cc0000; }}
        .signal-moderate {{ background: #fff4e5; border-color: #cc8800; color: #cc8800; }}
        .signal-normal {{ background: #f0f0f0; border-color: #666; color: #666; }}
        
        .progress-section {{
            margin: 2rem 0;
            padding: 2rem;
            border: 1px solid #e5e5e5;
        }}
        .progress-label {{
            font-family: 'Crimson Text', serif;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #f0f0f0;
            border: 1px solid #ccc;
            position: relative;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: #2c2c2c;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 500;
            font-size: 0.9rem;
        }}
        
        .market-summary {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 2rem 0;
            padding: 2rem;
            border: 1px solid #e5e5e5;
        }}
        .market-card {{
            text-align: center;
        }}
        .market-label {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        .market-value {{
            font-size: 1.8rem;
            font-weight: 500;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            font-size: 0.95rem;
        }}
        thead {{
            border-bottom: 2px solid #2c2c2c;
        }}
        th {{
            font-family: 'Crimson Text', serif;
            font-weight: 600;
            padding: 0.75rem 0.5rem;
            text-align: left;
        }}
        td {{
            padding: 1rem 0.5rem;
            border-bottom: 1px solid #e5e5e5;
            vertical-align: top;
        }}
        .row-met {{
            background: #f9f9f9;
        }}
        .ind-num {{
            width: 40px;
            text-align: center;
            color: #999;
        }}
        .ind-check {{
            width: 40px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
        }}
        .row-met .ind-check {{
            color: #2c2c2c;
        }}
        .ind-name {{
            min-width: 200px;
        }}
        .ind-desc {{
            font-size: 0.85rem;
            color: #666;
        }}
        .ind-note {{
            font-size: 0.8rem;
            color: #999;
            font-style: italic;
            margin-top: 0.25rem;
        }}
        .ind-val {{
            color: #2c2c2c;
        }}
        .ind-thresh {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .methodology {{
            margin: 3rem 0;
            padding: 2rem;
            border: 1px solid #e5e5e5;
            background: #fafafa;
        }}
        .methodology h2 {{
            margin-top: 0;
        }}
        .methodology ul {{
            margin: 1rem 0 1rem 1.5rem;
            line-height: 1.9;
        }}
        .methodology li {{
            margin-bottom: 0.5rem;
        }}
        
        .footer {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #e5e5e5;
            text-align: center;
            color: #999;
            font-size: 0.9rem;
        }}
        .footer a {{
            color: #666;
            text-decoration: none;
            border-bottom: 1px solid #ccc;
        }}
        .footer a:hover {{
            border-bottom: 1px solid #2c2c2c;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="site-header">
            <h1>enhaq capital</h1>
        </header>
        
        <nav>
            <a href="index.html">Home</a>
            <a href="holdings.html">Holdings</a>
            <a href="trades.html">Trades</a>
            <a href="bear-signals.html" class="active">Bear Signals</a>
        </nav>
        
        <div class="page-tagline">
            Real-time bear market bottom indicators – market-wide technical oversold signals
        </div>
        
        <div class="signal-banner {status_class}">
            {status_text}
        </div>
        
        <div class="progress-section">
            <div class="progress-label">Indicators Met: {summary['met_count']} of {summary['total_count']}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {pct}%;">
                    {pct}%
                </div>
            </div>
        </div>
        
        <div class="market-summary">
            <div class="market-card">
                <div class="market-label">S&P 500</div>
                <div class="market-value">{market['sp500']}</div>
            </div>
            <div class="market-card">
                <div class="market-label">VIX</div>
                <div class="market-value">{market['vix']}</div>
            </div>
            <div class="market-card">
                <div class="market-label">Drawdown</div>
                <div class="market-value">{market['drawdown_from_52w_high']}%</div>
            </div>
        </div>
        
        <h2>Indicator Breakdown</h2>
        
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th></th>
                    <th>Indicator</th>
                    <th>Current Value</th>
                    <th>Threshold</th>
                </tr>
            </thead>
            <tbody>
                {indicator_rows}
            </tbody>
        </table>
        
        <div class="methodology">
            <h2>Methodology</h2>
            <ul>
                <li><strong>Purpose:</strong> Identify high-probability bear market bottoms for deploying cash into quality compounders</li>
                <li><strong>Not predictive:</strong> Only tracks oversold conditions after a bear market has started (S&P -10% or more)</li>
                <li><strong>Buy signal:</strong> When 8-10 indicators are met simultaneously</li>
                <li><strong>Strategy:</strong> Pre-select quality stocks/ETFs during bull markets, buy heavily when signals trigger</li>
                <li><strong>Historical accuracy:</strong> Successfully signaled bottoms in Dec 2018, Mar-Apr 2020, Sep 2022, Apr 2025</li>
                <li><strong>Risk:</strong> Lost decade scenarios (prolonged secular bear markets) are not covered by these indicators</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Last updated: {last_updated}</p>
            <p>Data sources: Yahoo Finance (S&P 500, Nasdaq, Dow Jones, VIX)</p>
            <p><a href="https://enhaq.com">enhaq.com</a></p>
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    print("Loading data...")
    data = load_data()
    
    print("Generating HTML...")
    html = generate_html(data)
    
    output_path = '/data/.openclaw/workspace/bear-signals-repo/bear-signals.html'
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✓ HTML generated: {output_path}")

if __name__ == "__main__":
    main()
