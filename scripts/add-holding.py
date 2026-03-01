#!/usr/bin/env python3
"""
Add a new holding to the portfolio.
"""

import json
import argparse
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).parent.parent
HOLDINGS_FILE = PROJECT_ROOT / "data/holdings.json"

def main():
    parser = argparse.ArgumentParser(description="Add new holding to portfolio")
    parser.add_argument("--ticker", required=True, help="Ticker symbol")
    parser.add_argument("--name", required=True, help="Company name")
    parser.add_argument("--category", required=True, help="Category (e.g., 'Luxury - Lindy')")
    parser.add_argument("--entry-date", required=True, help="Entry date (YYYY-MM-DD)")
    parser.add_argument("--entry-price", type=float, required=True, help="Entry price")
    parser.add_argument("--shares", type=int, required=True, help="Number of shares")
    parser.add_argument("--currency", default="EUR", help="Currency (default: EUR)")
    parser.add_argument("--thesis", required=True, help="Investment thesis")
    parser.add_argument("--valuation-notes", default="", help="Valuation notes")
    
    args = parser.parse_args()
    
    # Load existing data
    with open(HOLDINGS_FILE) as f:
        data = json.load(f)
    
    # Create new holding
    new_holding = {
        "ticker": args.ticker,
        "name": args.name,
        "category": args.category,
        "entry_date": args.entry_date,
        "entry_price": args.entry_price,
        "shares": args.shares,
        "currency": args.currency,
        "thesis": args.thesis,
        "thesis_evolution": [
            {
                "date": args.entry_date,
                "note": "Initial entry."
            }
        ],
        "valuation_notes": args.valuation_notes or "N/A",
        "add_trim_signals": [],
        "current_price": None,
        "current_value": None,
        "unrealized_pnl": None
    }
    
    # Add to portfolio
    data["portfolio"].append(new_holding)
    data["last_updated"] = str(date.today())
    
    # Save
    with open(HOLDINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Added {args.ticker} to portfolio")
    print(f"   Cost basis: {args.currency}{args.entry_price * args.shares:,.2f}")

if __name__ == "__main__":
    main()
