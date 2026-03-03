#!/usr/bin/env python3
"""
Generate watchlist.html from watchlist.json
"""

import json
from datetime import datetime

def load_data():
    with open('/data/.openclaw/workspace/bear-signals-repo/data/watchlist.json', 'r') as f:
        return json.load(f)

def generate_html(data):
    last_updated = data['last_updated']
    
    # Generate category sections
    category_sections = ""
    
    for category in data['categories']:
        cat_name = category['name']
        cat_alloc = category['allocation_target_pct']
        cat_rationale = category['rationale']
        
        # Generate position rows
        position_rows = ""
        for pos in category['positions']:
            status_badge = "owned" if pos['status'] == "owned" else "watch"
            status_class = "status-owned" if pos['status'] == "owned" else "status-watch"
            status_text = "Currently Owned" if pos['status'] == "owned" else "Watchlist"
            
            current_alloc = pos['current_allocation_pct']
            target_alloc = pos['target_allocation_pct']
            alloc_display = f"{current_alloc}% → {target_alloc}%" if pos['status'] == "owned" else f"{target_alloc}%"
            
            fisher_display = pos.get('fisher_score', 'N/A')
            lindy_display = f"{pos.get('lindy_years', 'N/A')} years" if pos.get('lindy_years') else 'N/A'
            
            notes_html = ""
            if pos.get('notes'):
                notes_html = f'<div class="pos-notes">📝 {pos["notes"]}</div>'
            
            add_on_dip_html = ""
            if pos.get('add_on_dip'):
                add_on_dip_html = '<span class="add-flag">✓ Add on dip</span>'
            
            # Valuation section (if present)
            valuation_html = ""
            if pos.get('valuation'):
                val = pos['valuation']
                
                # Determine signal color
                signal = val.get('entry_exit_trigger', {}).get('current_signal', '')
                if 'BUY' in signal.upper():
                    signal_class = 'signal-buy'
                elif 'SELL' in signal.upper():
                    signal_class = 'signal-sell'
                elif 'HOLD' in signal.upper():
                    signal_class = 'signal-hold'
                else:
                    signal_class = 'signal-wait'
                
                reverse_dcf = val.get('reverse_dcf', {})
                compression = val.get('multiple_compression_scenario', {})
                three_ps = val.get('three_ps', {})
                triggers = val.get('entry_exit_trigger', {})
                
                valuation_html = f'''
                <div class="valuation-section">
                    <div class="valuation-header">Valuation Analysis (Reverse DCF + 3 Ps)</div>
                    
                    <div class="valuation-grid">
                        <div class="val-box">
                            <div class="val-label">Current Price</div>
                            <div class="val-value">{val.get('current_price_cad') or val.get('current_price_usd') or val.get('current_price_eur', 'N/A')}</div>
                            <div class="val-sublabel">{val.get('current_multiple', '')}</div>
                        </div>
                        <div class="val-box">
                            <div class="val-label">Implied Growth (10Y)</div>
                            <div class="val-value">{reverse_dcf.get('implied_fcf_cagr_10y') or reverse_dcf.get('implied_eps_cagr_10y', 'N/A')}</div>
                            <div class="val-sublabel">Market expectation</div>
                        </div>
                        <div class="val-box">
                            <div class="val-label">Probable Growth</div>
                            <div class="val-value">{three_ps.get('probable', 'N/A')[:20]}</div>
                            <div class="val-sublabel">Base case estimate</div>
                        </div>
                    </div>
                    
                    <div class="reverse-dcf-detail">
                        <div class="detail-row-val">
                            <strong>Reverse DCF:</strong> {reverse_dcf.get('interpretation', '')}
                        </div>
                        <div class="detail-row-val">
                            <strong>Multiple Compression:</strong> {compression.get('interpretation', '')}
                        </div>
                    </div>
                    
                    <div class="three-ps-section">
                        <div class="ps-title">The 3 Ps Framework</div>
                        <div class="ps-item"><strong>Possible:</strong> {three_ps.get('possible', '')}</div>
                        <div class="ps-item"><strong>Plausible:</strong> {three_ps.get('plausible', '')}</div>
                        <div class="ps-item"><strong>Probable:</strong> {three_ps.get('probable', '')}</div>
                        <div class="ps-assessment">{three_ps.get('assessment', '')}</div>
                    </div>
                    
                    <div class="entry-exit-triggers">
                        <div class="trigger-title">Entry / Exit Triggers</div>
                        <div class="trigger-grid">
                            <div class="trigger-item trigger-buy">
                                <div class="trigger-label">BUY</div>
                                <div class="trigger-value">{triggers.get('buy', 'N/A')}</div>
                            </div>
                            <div class="trigger-item trigger-hold">
                                <div class="trigger-label">HOLD</div>
                                <div class="trigger-value">{triggers.get('hold', 'N/A')}</div>
                            </div>
                            <div class="trigger-item trigger-sell">
                                <div class="trigger-label">SELL</div>
                                <div class="trigger-value">{triggers.get('sell', 'N/A')}</div>
                            </div>
                        </div>
                        <div class="current-signal {signal_class}">
                            <strong>Current Signal:</strong> {triggers.get('current_signal', 'N/A')}
                        </div>
                    </div>
                    
                    <div class="val-updated">Last updated: {val.get('last_updated', 'N/A')}</div>
                </div>
                '''
            
            position_rows += f'''
            <tr class="position-row clickable-row" onclick="togglePositionDetail('{pos['ticker']}')">
                <td class="pos-ticker">
                    <strong>{pos['ticker']}</strong>
                    <div class="{status_class}">{status_text}</div>
                </td>
                <td class="pos-name">
                    {pos['name']}
                    <div class="pos-geo">{pos['geography']}</div>
                </td>
                <td class="pos-alloc">{alloc_display}</td>
                <td class="pos-trigger">{pos['entry_trigger']}</td>
            </tr>
            <tr class="detail-row" id="detail-{pos['ticker']}" style="display: none;">
                <td colspan="4" class="detail-cell">
                    <div class="pos-detail">
                        <div class="detail-section">
                            <div class="detail-label">Investment Thesis</div>
                            <div class="detail-content">{pos['thesis']}</div>
                        </div>
                        <div class="detail-metrics">
                            <div class="detail-metric">
                                <div class="metric-label">Fisher Score</div>
                                <div class="metric-value">{fisher_display}</div>
                            </div>
                            <div class="detail-metric">
                                <div class="metric-label">Lindy Test</div>
                                <div class="metric-value">{lindy_display}</div>
                            </div>
                            <div class="detail-metric">
                                <div class="metric-label">Target Weight</div>
                                <div class="metric-value">{target_alloc}%</div>
                            </div>
                        </div>
                        {add_on_dip_html}
                        {notes_html}
                        {valuation_html}
                    </div>
                </td>
            </tr>
            '''
        
        category_sections += f'''
        <div class="category-section">
            <div class="category-header">
                <span class="category-title">{cat_name}</span>
                <span class="category-allocation">{cat_alloc}% target allocation</span>
            </div>
            <div class="category-rationale">{cat_rationale}</div>
            
            <table class="watchlist-table">
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Company</th>
                        <th>Allocation</th>
                        <th>Entry Trigger</th>
                    </tr>
                </thead>
                <tbody>
                    {position_rows}
                </tbody>
            </table>
        </div>
        '''
    
    # Deployment notes
    notes_list = "\n".join([f"<li>{note}</li>" for note in data['deployment_notes']])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watchlist | enhaq capital</title>
    <meta name="description" content="Pre-selected quality compounders for bear market deployment. Select now, buy when signals fire.">
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
        
        .philosophy-box {{
            background: #f8f9fa;
            border: 1px solid #e5e5e5;
            padding: 2rem;
            margin: 2rem 0;
            border-left: 4px solid #2c2c2c;
        }}
        .philosophy-box h3 {{
            font-family: 'Crimson Text', serif;
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }}
        
        .category-section {{
            margin: 3rem 0;
        }}
        .category-header {{
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #2c2c2c;
        }}
        .category-title {{
            font-family: 'Crimson Text', serif;
            font-size: 1.3rem;
            font-weight: 600;
        }}
        .category-allocation {{
            font-size: 1rem;
            color: #666;
            margin-left: 1rem;
        }}
        .category-rationale {{
            font-size: 0.95rem;
            color: #666;
            font-style: italic;
            margin: 0.75rem 0 1.5rem 0;
        }}
        
        .watchlist-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            border: 1px solid #e5e5e5;
        }}
        .watchlist-table thead {{
            border-bottom: 2px solid #2c2c2c;
        }}
        .watchlist-table th {{
            text-align: left;
            padding: 0.75rem;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
        }}
        .watchlist-table td {{
            padding: 1rem 0.75rem;
            border-bottom: 1px solid #f0f0f0;
        }}
        .position-row {{
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        .position-row:hover {{
            background: #f5f5f5 !important;
        }}
        .position-row.expanded {{
            background: #fafafa !important;
        }}
        
        .pos-ticker {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 1rem;
        }}
        .status-owned, .status-watch {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.25rem;
            font-weight: 600;
        }}
        .status-owned {{
            color: #2d5016;
        }}
        .status-watch {{
            color: #666;
        }}
        .pos-geo {{
            font-size: 0.85rem;
            color: #999;
            margin-top: 0.25rem;
        }}
        .pos-alloc {{
            font-weight: 500;
        }}
        .pos-trigger {{
            font-size: 0.9rem;
            color: #666;
        }}
        
        .detail-row {{
            background: #fafafa;
        }}
        .detail-cell {{
            padding: 0 !important;
        }}
        .pos-detail {{
            padding: 1.5rem 2rem;
            border-left: 4px solid #2c2c2c;
            background: #f8f9fa;
        }}
        .detail-section {{
            margin-bottom: 1.5rem;
        }}
        .detail-label {{
            font-family: 'Crimson Text', serif;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        .detail-content {{
            font-size: 0.95rem;
            line-height: 1.7;
            color: #444;
        }}
        .detail-metrics {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1.5rem 0;
            padding: 1rem;
            background: white;
            border: 1px solid #e5e5e5;
        }}
        .detail-metric {{
            text-align: center;
        }}
        .metric-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #999;
            margin-bottom: 0.25rem;
        }}
        .metric-value {{
            font-size: 1.3rem;
            font-weight: 500;
            color: #2c2c2c;
        }}
        .add-flag {{
            display: inline-block;
            background: #e8f5e9;
            color: #2d5016;
            padding: 0.25rem 0.75rem;
            border-radius: 3px;
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 1rem;
        }}
        .pos-notes {{
            margin-top: 1rem;
            padding: 0.75rem;
            background: #fff3cd;
            border-left: 3px solid #856404;
            font-size: 0.9rem;
            color: #856404;
        }}
        
        .valuation-section {{
            margin-top: 2rem;
            padding: 2rem;
            background: white;
            border: 2px solid #2c2c2c;
        }}
        .valuation-header {{
            font-family: 'Crimson Text', serif;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #2c2c2c;
        }}
        .valuation-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        .val-box {{
            background: #f8f9fa;
            padding: 1rem;
            border: 1px solid #e5e5e5;
            text-align: center;
        }}
        .val-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        .val-value {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #2c2c2c;
            margin-bottom: 0.25rem;
        }}
        .val-sublabel {{
            font-size: 0.8rem;
            color: #999;
        }}
        .reverse-dcf-detail {{
            margin: 1.5rem 0;
            padding: 1rem;
            background: #f8f9fa;
            border-left: 3px solid #666;
        }}
        .detail-row-val {{
            margin: 0.5rem 0;
            font-size: 0.9rem;
            line-height: 1.6;
        }}
        .three-ps-section {{
            margin: 1.5rem 0;
            padding: 1.5rem;
            background: #f8f9fa;
            border: 1px solid #e5e5e5;
        }}
        .ps-title {{
            font-family: 'Crimson Text', serif;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }}
        .ps-item {{
            margin: 0.75rem 0;
            font-size: 0.9rem;
            line-height: 1.6;
        }}
        .ps-assessment {{
            margin-top: 1rem;
            padding: 0.75rem;
            background: white;
            border-left: 3px solid #2c2c2c;
            font-weight: 500;
        }}
        .entry-exit-triggers {{
            margin: 1.5rem 0;
            padding: 1.5rem;
            background: #fafafa;
            border: 1px solid #e5e5e5;
        }}
        .trigger-title {{
            font-family: 'Crimson Text', serif;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }}
        .trigger-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        .trigger-item {{
            padding: 1rem;
            border: 2px solid;
            background: white;
        }}
        .trigger-buy {{
            border-color: #2d5016;
        }}
        .trigger-hold {{
            border-color: #666;
        }}
        .trigger-sell {{
            border-color: #8b0000;
        }}
        .trigger-label {{
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        .trigger-buy .trigger-label {{
            color: #2d5016;
        }}
        .trigger-hold .trigger-label {{
            color: #666;
        }}
        .trigger-sell .trigger-label {{
            color: #8b0000;
        }}
        .trigger-value {{
            font-size: 0.85rem;
            line-height: 1.5;
            color: #444;
        }}
        .current-signal {{
            padding: 1rem;
            font-size: 1rem;
            text-align: center;
            border: 2px solid;
            font-weight: 600;
        }}
        .signal-buy {{
            background: #e8f5e9;
            border-color: #2d5016;
            color: #2d5016;
        }}
        .signal-hold {{
            background: #f5f5f5;
            border-color: #666;
            color: #666;
        }}
        .signal-sell {{
            background: #ffebee;
            border-color: #8b0000;
            color: #8b0000;
        }}
        .signal-wait {{
            background: #fff3cd;
            border-color: #856404;
            color: #856404;
        }}
        .val-updated {{
            margin-top: 1rem;
            font-size: 0.8rem;
            color: #999;
            text-align: right;
        }}
        
        .deployment-notes {{
            margin: 3rem 0;
            padding: 2rem;
            background: #f8f9fa;
            border: 1px solid #e5e5e5;
        }}
        .deployment-notes h2 {{
            margin-top: 0;
        }}
        .deployment-notes ul {{
            margin: 1rem 0 0 1.5rem;
            line-height: 1.9;
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
            <a href="bear-signals.html">Bear Signals</a>
            <a href="watchlist.html" class="active">Watchlist</a>
        </nav>
        
        <div class="page-tagline">
            Pre-selected quality compounders. Select now, buy when signals fire.
        </div>
        
        <div class="philosophy-box">
            <h3>Deployment Philosophy</h3>
            <p>{data['description']}</p>
            <p style="margin-top: 0.75rem;"><strong>{data['deployment_philosophy']}</strong></p>
        </div>
        
        {category_sections}
        
        <div class="deployment-notes">
            <h2>Deployment Notes</h2>
            <ul>
                {notes_list}
            </ul>
        </div>
        
        <div class="footer">
            <p>Last updated: {last_updated}</p>
            <p><a href="https://enhaq.com">enhaq.com</a></p>
        </div>
    </div>
    
    <script>
        function togglePositionDetail(ticker) {{
            const detailRow = document.getElementById('detail-' + ticker);
            const positionRow = detailRow.previousElementSibling;
            
            if (detailRow.style.display === 'none') {{
                // Close all other details
                document.querySelectorAll('.detail-row').forEach(row => {{
                    row.style.display = 'none';
                }});
                document.querySelectorAll('.position-row').forEach(row => {{
                    row.classList.remove('expanded');
                }});
                
                // Open this one
                detailRow.style.display = 'table-row';
                positionRow.classList.add('expanded');
            }} else {{
                // Close this one
                detailRow.style.display = 'none';
                positionRow.classList.remove('expanded');
            }}
        }}
    </script>
</body>
</html>'''
    
    return html

def main():
    print("Loading watchlist data...")
    data = load_data()
    
    print("Generating HTML...")
    html = generate_html(data)
    
    output_path = '/data/.openclaw/workspace/bear-signals-repo/watchlist.html'
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✓ Watchlist HTML generated: {output_path}")

if __name__ == "__main__":
    main()
