#!/usr/bin/env python3
"""
Enrich holdings with category and geography based on ticker knowledge
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Mapping ticker → (category, geography, full_name)
TICKER_MAP = {
    # US Stocks
    "RACE": ("Luxury Auto", "Europe", "Ferrari N.V."),
    "UBER": ("Technology", "USA", "Uber Technologies"),
    "GOOGL": ("Technology", "USA", "Alphabet Inc."),
    "IAU": ("Commodities", "Global", "iShares Gold Trust"),
    "IBIT": ("Alternative Assets", "USA", "iShares Bitcoin Trust"),
    "VWRA": ("Global Equity", "Global", "Vanguard FTSE All-World"),
    "IGV": ("Technology", "USA", "iShares Expanded Tech-Software ETF"),
    "CPRT": ("Industrials", "USA", "Copart Inc."),
    "BRK B": ("Financials", "USA", "Berkshire Hathaway Class B"),
    "ADBE": ("Technology", "USA", "Adobe Inc."),
    "BRBR": ("Financials", "USA", "BellRing Brands"),
    "MU": ("Technology", "USA", "Micron Technology"),
    "QXO": ("Industrials", "USA", "QXO Inc."),
    "SCZM": ("Equities", "Emerging Markets", "SCZM ETF"),
    "SLV": ("Commodities", "Global", "iShares Silver Trust"),
    "SSRM": ("Materials", "Canada", "SSR Mining"),
    "U.U": ("Technology", "USA", "Unity Software"),
    
    # Canadian Stocks
    "CSU": ("Technology", "Canada", "Constellation Software"),
    "LMN": ("Technology", "Canada", "Lumine Group"),
    "TOI": ("Technology", "Canada", "Topicus.com"),
    
    # European Stocks (EUR currency)
    "CHG": ("Luxury Goods", "Europe", "Compagnie Financière Richemont (Cartier)"),
    "EXO": ("Luxury Goods", "Europe", "Exor N.V."),
    "RMS": ("Luxury Goods", "Europe", "Hermès International"),
    "SLm": ("Technology", "Europe", "SLM Solutions"),
}

def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def save_json(filename, data):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)

def enrich_holdings():
    print("📊 Enriching holdings with category and geography...")
    
    holdings_data = load_json("holdings.json")
    updated_count = 0
    
    for holding in holdings_data["portfolio"]:
        ticker = holding["ticker"]
        
        # Skip options (we'll handle those separately)
        if any(char in ticker for char in [" ", "P", "C"]) and len(ticker) > 10:
            # This looks like an option ticker - skip for now
            holding["category"] = "Options"
            holding["geography"] = "N/A"
            continue
        
        if ticker in TICKER_MAP:
            category, geography, full_name = TICKER_MAP[ticker]
            holding["category"] = category
            holding["geography"] = geography
            holding["name"] = full_name
            updated_count += 1
            print(f"   ✓ {ticker}: {category} | {geography} | {full_name}")
        else:
            print(f"   ⚠️  {ticker}: No mapping found (keeping TBD)")
    
    save_json("holdings.json", holdings_data)
    print(f"\n✅ Updated {updated_count} holdings")
    print("⚠️  Options tickers marked as 'Options' category - move to trades.json separately")

if __name__ == "__main__":
    enrich_holdings()
