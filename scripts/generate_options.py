# Insert into generate.py - options page with table view + performance

def generate_trades_page(trades_data):
    """Generate options trades page with table summary + expandable detail."""
    trades = trades_data["trades"]
    performance = trades_data.get("performance", {})
    last_updated = trades_data["last_updated"]
    
    # Stats
    total_trades = len(trades)
    open_trades = len([t for t in trades if t["status"] == "open"])
    closed_trades = len([t for t in trades if t["status"] == "closed"])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Options | enhaq.capital</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
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
        
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        h1 {{
            font-family: 'Caveat', cursive;
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
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
            font-style: italic;
        }}
        
        .meta {{ font-size: 0.9rem; color: #999; margin-bottom: 3rem; }}
        
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
        }}
        
        nav a:hover {{ border-bottom: 2px solid #2c2c2c; }}
        nav a.active {{ border-bottom: 2px solid #2c2c2c; font-weight: 600; }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .metric {{
            border: 1px solid #e5e5e5;
            padding: 1.5rem;
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
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: #ffffff;
            border: 1px solid #e5e5e5;
        }}
        
        thead {{ border-bottom: 2px solid #2c2c2c; }}
        
        th {{
            text-align: left;
            padding: 1rem;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
        }}
        
        th.right {{ text-align: right; }}
        
        td {{
            padding: 1rem;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        td.right {{ text-align: right; }}
        
        tbody tr {{ cursor: pointer; }}
        tbody tr:hover {{ background: #f9f9f9; }}
        
        .ticker {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }}
        
        .status {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border: 1px solid;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .status.open {{ border-color: #2d5016; color: #2d5016; }}
        .status.closed {{ border-color: #666; color: #666; }}
        
        .positive {{ color: #2d5016; }}
        .negative {{ color: #8b0000; }}
        
        .detail-row {{
            display: none;
        }}
        
        .detail-row.show {{
            display: table-row;
        }}
        
        .detail-cell {{
            padding: 2rem;
            background: #f9f9f9;
            border-bottom: 2px solid #e5e5e5;
        }}
        
        .detail-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }}
        
        .detail-section {{
            margin-bottom: 1.5rem;
        }}
        
        .section-title {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .structure {{
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.8;
        }}
        
        footer {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #ccc;
            text-align: center;
            font-size: 0.85rem;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Options</h1>
            <p class="subtitle">Volatility-based strategies</p>
            <p class="meta">As of {last_updated}</p>
        </header>

        <nav>
            <a href="index.html">Holdings</a>
            <a href="options.html" class="active">Options</a>
        </nav>

        <!-- Performance Metrics -->
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">Total Trades</div>
                <div class="metric-value">{total_trades}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Win Rate</div>
                <div class="metric-value">{performance.get('win_rate', 0):.0f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Avg Return</div>
                <div class="metric-value">{performance.get('avg_return', 0):.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Total P&L</div>
                <div class="metric-value">${performance.get('total_pnl', 0):,.0f}</div>
            </div>
        </div>

        <!-- Trade Summary Table -->
        <h2>Trade Log</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Ticker</th>
                    <th>Type</th>
                    <th>Classification</th>
                    <th>Entry Date</th>
                    <th>Status</th>
                    <th class="right">Net Debit</th>
                    <th class="right">P&L</th>
                    <th class="right">Return</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for trade in trades:
        status_class = "open" if trade["status"] == "open" else "closed"
        pnl = trade.get("realized_pnl", 0) or 0
        return_pct = trade.get("return_pct", 0) or 0
        pnl_class = "positive" if pnl > 0 else ("negative" if pnl < 0 else "")
        pnl_sign = "+" if pnl > 0 else ""
        return_sign = "+" if return_pct > 0 else ""
        
        html += f"""
                <tr onclick="toggleDetail('{trade['id']}')">
                    <td>{trade['id']}</td>
                    <td class="ticker">{trade['ticker']}</td>
                    <td>{trade['trade_type']}</td>
                    <td>{trade['classification']}</td>
                    <td>{trade['entry_date']}</td>
                    <td><span class="status {status_class}">{trade['status']}</span></td>
                    <td class="right">${trade['structure']['net_debit']:.2f}</td>
                    <td class="right {pnl_class}"><strong>{pnl_sign}${pnl:.2f}</strong></td>
                    <td class="right {pnl_class}"><strong>{return_sign}{return_pct:.1f}%</strong></td>
                </tr>
                <tr class="detail-row" id="detail-{trade['id']}">
                    <td colspan="9" class="detail-cell">
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
            </tbody>
        </table>

        <footer>
            <p>Options trading involves substantial risk and is not suitable for all investors.</p>
        </footer>
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
