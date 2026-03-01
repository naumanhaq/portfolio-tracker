#!/usr/bin/env python3
"""
Move option positions from holdings.json to trades.json
"""

import json
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def save_json(filename, data):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)

def is_option_ticker(ticker):
    """Detect option tickers by pattern (spaces, expiry dates, strike prices)"""
    # Options have format like: "UBER  260515C00085000"
    # Stock tickers are simple: "UBER", "BRK B", etc.
    return bool(re.search(r'\d{6}[CP]\d{8}', ticker))

def parse_option_ticker(ticker):
    """Extract underlying, expiry, type, strike from option ticker"""
    # Example: "UBER  260515C00085000"
    # Format: TICKER YYMMDDCT00000000 where C/P = call/put, strike in cents
    parts = ticker.split()
    if len(parts) < 2:
        return None
    
    underlying = parts[0]
    option_code = parts[1]
    
    if len(option_code) < 15:
        return None
    
    expiry_str = option_code[:6]  # YYMMDD
    option_type = option_code[6]  # C or P
    strike_cents = int(option_code[7:])
    
    # Parse expiry
    year = 2000 + int(expiry_str[:2])
    month = int(expiry_str[2:4])
    day = int(expiry_str[4:6])
    expiry = f"{year}-{month:02d}-{day:02d}"
    
    # Parse strike
    strike = strike_cents / 1000.0
    
    return {
        "underlying": underlying,
        "expiry": expiry,
        "type": "Call" if option_type == "C" else "Put",
        "strike": strike
    }

def move_options():
    print("🔄 Moving options from holdings to trades...")
    
    holdings_data = load_json("holdings.json")
    trades_data = load_json("trades.json")
    
    stocks = []
    options_moved = 0
    
    for holding in holdings_data["portfolio"]:
        ticker = holding["ticker"]
        
        if is_option_ticker(ticker):
            print(f"   → Moving option: {ticker}")
            
            option_info = parse_option_ticker(ticker)
            if not option_info:
                print(f"      ⚠️  Could not parse option ticker format")
                continue
            
            # Create trade entry
            trade_id = f"opt-{len(trades_data['trades']) + 1:03d}"
            
            # Determine if long or short based on current_value sign
            position_type = "Long" if holding.get("current_value", 0) > 0 else "Short"
            
            trade_entry = {
                "id": trade_id,
                "ticker": option_info["underlying"],
                "trade_type": f"{option_info['type']} Option",
                "classification": "TBD",  # User needs to classify (P1-P4)
                "entry_date": holding["entry_date"],
                "status": "open",
                "entry_thesis": "Add thesis",
                "structure": {
                    "long": f"{option_info['underlying']} {option_info['expiry']} ${option_info['strike']} {option_info['type']}" if position_type == "Long" else "N/A",
                    "short": f"{option_info['underlying']} {option_info['expiry']} ${option_info['strike']} {option_info['type']}" if position_type == "Short" else "N/A",
                    "net_debit": abs(holding.get("entry_price", 0)),
                    "max_loss": abs(holding.get("current_value", 0)) if position_type == "Long" else 0,  # TBD for short
                    "profit_potential": 0  # TBD
                },
                "moontower_metrics": {
                    "iv_percentile": "TBD",
                    "vrp": "TBD",
                    "rv_percentile": "TBD",
                    "term_structure": "TBD"
                },
                "greeks": {
                    "delta": 0,
                    "gamma": 0,
                    "theta": 0,
                    "vega": 0
                },
                "expected_outcome": "Add expected outcome",
                "actual_outcome": None,
                "realized_pnl": holding.get("unrealized_pnl", 0)
            }
            
            trades_data["trades"].append(trade_entry)
            options_moved += 1
        else:
            # Keep stock positions
            stocks.append(holding)
    
    # Update holdings to only contain stocks
    holdings_data["portfolio"] = stocks
    
    # Save updated files
    save_json("holdings.json", holdings_data)
    save_json("trades.json", trades_data)
    
    print(f"\n✅ Moved {options_moved} options to trades.json")
    print(f"✅ {len(stocks)} stock positions remain in holdings.json")

if __name__ == "__main__":
    move_options()
