#!/usr/bin/env python3
"""
Generate static HTML site from JSON data.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Output to root for GitHub Pages / Cloudflare
PUBLIC_DIR = PROJECT_ROOT

# Ensure public dir exists
PUBLIC_DIR.mkdir(exist_ok=True)

def load_json(filename):
    """Load JSON data file."""
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def generate_holdings_page(holdings_data):
    """Generate long-term holdings page."""
    portfolio = holdings_data["portfolio"]
    last_updated = holdings_data["last_updated"]
    
    # Calculate totals (will be updated when we add current prices)
    total_cost = sum(h["entry_price"] * h["shares"] for h in portfolio if h["currency"] == "EUR")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Long-Term Portfolio | enhaq.online</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <!-- Header -->
        <header class="mb-8">
            <h1 class="text-4xl font-bold mb-2">Long-Term Portfolio</h1>
            <p class="text-gray-600">Fisher Quality Growth + Lindy Survival</p>
            <p class="text-sm text-gray-500 mt-2">Last updated: {last_updated}</p>
        </header>

        <!-- Navigation -->
        <nav class="mb-8 flex gap-4">
            <a href="index.html" class="px-4 py-2 bg-blue-600 text-white rounded">Long-Term</a>
            <a href="options.html" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Options Trades</a>
        </nav>

        <!-- Holdings Table -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
            <table class="w-full">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="px-4 py-3 text-left">Ticker</th>
                        <th class="px-4 py-3 text-left">Name</th>
                        <th class="px-4 py-3 text-left">Category</th>
                        <th class="px-4 py-3 text-right">Entry Date</th>
                        <th class="px-4 py-3 text-right">Entry Price</th>
                        <th class="px-4 py-3 text-right">Shares</th>
                        <th class="px-4 py-3 text-right">Cost Basis</th>
                    </tr>
                </thead>
                <tbody class="divide-y">
"""
    
    for holding in portfolio:
        cost_basis = holding["entry_price"] * holding["shares"]
        html += f"""
                    <tr class="hover:bg-gray-50 cursor-pointer" onclick="toggleDetails('{holding['ticker']}')">
                        <td class="px-4 py-3 font-mono font-bold">{holding['ticker']}</td>
                        <td class="px-4 py-3">{holding['name']}</td>
                        <td class="px-4 py-3"><span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">{holding['category']}</span></td>
                        <td class="px-4 py-3 text-right">{holding['entry_date']}</td>
                        <td class="px-4 py-3 text-right font-mono">€{holding['entry_price']:,.2f}</td>
                        <td class="px-4 py-3 text-right">{holding['shares']}</td>
                        <td class="px-4 py-3 text-right font-mono">€{cost_basis:,.2f}</td>
                    </tr>
                    <tr id="details-{holding['ticker']}" class="hidden bg-gray-50">
                        <td colspan="7" class="px-4 py-4">
                            <div class="space-y-4">
                                <div>
                                    <h3 class="font-bold mb-2">Investment Thesis</h3>
                                    <p class="text-gray-700">{holding['thesis']}</p>
                                </div>
                                <div>
                                    <h3 class="font-bold mb-2">Valuation Notes</h3>
                                    <p class="text-gray-700">{holding['valuation_notes']}</p>
                                </div>
                                <div>
                                    <h3 class="font-bold mb-2">Thesis Evolution</h3>
"""
        for note in holding["thesis_evolution"]:
            html += f"""
                                    <div class="mb-2">
                                        <span class="text-sm font-mono text-gray-600">{note['date']}</span>
                                        <p class="text-gray-700">{note['note']}</p>
                                    </div>
"""
        html += """
                                </div>
                            </div>
                        </td>
                    </tr>
"""
    
    html += f"""
                </tbody>
            </table>
        </div>

        <!-- Summary -->
        <div class="mt-8 bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-bold mb-4">Portfolio Summary</h2>
            <div class="grid grid-cols-3 gap-4">
                <div>
                    <p class="text-gray-600 text-sm">Total Holdings</p>
                    <p class="text-2xl font-bold">{len(portfolio)}</p>
                </div>
                <div>
                    <p class="text-gray-600 text-sm">Total Cost Basis</p>
                    <p class="text-2xl font-bold">€{total_cost:,.2f}</p>
                </div>
                <div>
                    <p class="text-gray-600 text-sm">Target Horizon</p>
                    <p class="text-2xl font-bold">20+ years</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function toggleDetails(ticker) {{
            const row = document.getElementById('details-' + ticker);
            row.classList.toggle('hidden');
        }}
    </script>
</body>
</html>
"""
    
    return html

def generate_trades_page(trades_data):
    """Generate options trades page."""
    trades = trades_data["trades"]
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
    <title>Options Trades | enhaq.online</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <!-- Header -->
        <header class="mb-8">
            <h1 class="text-4xl font-bold mb-2">Options Trades</h1>
            <p class="text-gray-600">Moontower Vol Framework</p>
            <p class="text-sm text-gray-500 mt-2">Last updated: {last_updated}</p>
        </header>

        <!-- Navigation -->
        <nav class="mb-8 flex gap-4">
            <a href="index.html" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Long-Term</a>
            <a href="options.html" class="px-4 py-2 bg-blue-600 text-white rounded">Options Trades</a>
        </nav>

        <!-- Stats -->
        <div class="mb-8 grid grid-cols-3 gap-4">
            <div class="bg-white rounded-lg shadow p-4">
                <p class="text-gray-600 text-sm">Total Trades</p>
                <p class="text-3xl font-bold">{total_trades}</p>
            </div>
            <div class="bg-white rounded-lg shadow p-4">
                <p class="text-gray-600 text-sm">Open</p>
                <p class="text-3xl font-bold text-blue-600">{open_trades}</p>
            </div>
            <div class="bg-white rounded-lg shadow p-4">
                <p class="text-gray-600 text-sm">Closed</p>
                <p class="text-3xl font-bold text-gray-600">{closed_trades}</p>
            </div>
        </div>

        <!-- Trades -->
        <div class="space-y-4">
"""
    
    for trade in trades:
        status_color = "bg-green-100 text-green-800" if trade["status"] == "open" else "bg-gray-100 text-gray-800"
        
        html += f"""
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <h3 class="text-xl font-bold">{trade['ticker']} - {trade['classification']}</h3>
                        <p class="text-sm text-gray-600">Trade ID: {trade['id']} | Type: {trade['trade_type']}</p>
                    </div>
                    <span class="px-3 py-1 {status_color} rounded text-sm font-semibold">{trade['status'].upper()}</span>
                </div>
                
                <div class="grid grid-cols-2 gap-6 mb-4">
                    <div>
                        <h4 class="font-bold mb-2">Entry Thesis</h4>
                        <p class="text-gray-700">{trade['entry_thesis']}</p>
                    </div>
                    <div>
                        <h4 class="font-bold mb-2">Structure</h4>
                        <p class="text-gray-700 font-mono text-sm">
                            Long: {trade['structure']['long']}<br>
                            Short: {trade['structure']['short']}<br>
                            Net Debit: ${trade['structure']['net_debit']:.2f}
                        </p>
                    </div>
                </div>
                
                <div class="grid grid-cols-2 gap-6 mb-4">
                    <div>
                        <h4 class="font-bold mb-2">Moontower Metrics</h4>
                        <div class="text-sm space-y-1">
                            <p>IV%: {trade['moontower_metrics']['iv_percentile']}</p>
                            <p>VRP: {trade['moontower_metrics']['vrp']}</p>
                            <p>RV%: {trade['moontower_metrics']['rv_percentile']}</p>
                            <p>Term Structure: {trade['moontower_metrics']['term_structure']}</p>
                        </div>
                    </div>
                    <div>
                        <h4 class="font-bold mb-2">Greeks at Entry</h4>
                        <div class="text-sm space-y-1 font-mono">
                            <p>Delta: {trade['greeks_at_entry']['delta']}</p>
                            <p>Theta: {trade['greeks_at_entry']['theta']}</p>
                            <p>Vega: {trade['greeks_at_entry']['vega']}</p>
                        </div>
                    </div>
                </div>
                
                <div class="grid grid-cols-2 gap-6">
                    <div>
                        <h4 class="font-bold mb-2">Expected Outcome</h4>
                        <p class="text-gray-700">{trade['expected_outcome']}</p>
                    </div>
                    <div>
                        <h4 class="font-bold mb-2">Actual Outcome</h4>
                        <p class="text-gray-700">{trade['actual_outcome'] or 'Pending (trade open)'}</p>
                    </div>
                </div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    print("🔨 Generating portfolio site...")
    
    # Load data
    holdings_data = load_json("holdings.json")
    trades_data = load_json("trades.json")
    
    # Generate pages
    holdings_html = generate_holdings_page(holdings_data)
    trades_html = generate_trades_page(trades_data)
    
    # Write to public/
    with open(PUBLIC_DIR / "index.html", "w") as f:
        f.write(holdings_html)
    
    with open(PUBLIC_DIR / "options.html", "w") as f:
        f.write(trades_html)
    
    print(f"✅ Site generated:")
    print(f"   - {PUBLIC_DIR / 'index.html'}")
    print(f"   - {PUBLIC_DIR / 'options.html'}")
    print(f"\nOpen in browser: file://{PUBLIC_DIR / 'index.html'}")

if __name__ == "__main__":
    main()
