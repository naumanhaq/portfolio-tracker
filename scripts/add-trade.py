#!/usr/bin/env python3
"""
Add a new options trade.
"""

import json
import argparse
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).parent.parent
TRADES_FILE = PROJECT_ROOT / "data/trades.json"

def main():
    parser = argparse.ArgumentParser(description="Add new options trade")
    parser.add_argument("--ticker", required=True, help="Underlying ticker")
    parser.add_argument("--type", required=True, choices=["P1", "P2", "P3", "P4"], 
                        help="Moontower trade type (P1=Long Cal, P2=Sell Vol, P3=Buy Vol, P4=Short Cal)")
    parser.add_argument("--classification", required=True, help="Trade classification (e.g., 'Long Calendar')")
    parser.add_argument("--entry-date", required=True, help="Entry date (YYYY-MM-DD)")
    parser.add_argument("--thesis", required=True, help="Entry thesis")
    parser.add_argument("--long", required=True, help="Long leg description")
    parser.add_argument("--short", required=True, help="Short leg description")
    parser.add_argument("--net-debit", type=float, required=True, help="Net debit/credit")
    parser.add_argument("--iv-pct", type=int, help="IV percentile")
    parser.add_argument("--vrp", type=float, help="Volatility risk premium")
    parser.add_argument("--rv-pct", type=int, help="RV percentile")
    parser.add_argument("--term-structure", help="Term structure (flat/steep/inverted)")
    
    args = parser.parse_args()
    
    # Load existing data
    with open(TRADES_FILE) as f:
        data = json.load(f)
    
    # Generate trade ID
    existing_ids = [t["id"] for t in data["trades"]]
    next_num = len(existing_ids) + 1
    trade_id = f"T{next_num:03d}"
    
    # Create new trade
    new_trade = {
        "id": trade_id,
        "ticker": args.ticker,
        "trade_type": args.type,
        "classification": args.classification,
        "entry_date": args.entry_date,
        "exit_date": None,
        "status": "open",
        "entry_thesis": args.thesis,
        "structure": {
            "long": args.long,
            "short": args.short,
            "net_debit": args.net_debit
        },
        "greeks_at_entry": {
            "delta": None,
            "theta": None,
            "vega": None
        },
        "expected_outcome": "TBD - add later",
        "actual_outcome": None,
        "realized_pnl": None,
        "lessons": [],
        "moontower_metrics": {
            "iv_percentile": args.iv_pct,
            "vrp": args.vrp,
            "rv_percentile": args.rv_pct,
            "term_structure": args.term_structure
        }
    }
    
    # Add to trades
    data["trades"].append(new_trade)
    data["last_updated"] = str(date.today())
    
    # Save
    with open(TRADES_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Added trade {trade_id}: {args.ticker} {args.classification}")
    print(f"   Net debit: ${args.net_debit:.2f}")

if __name__ == "__main__":
    main()
