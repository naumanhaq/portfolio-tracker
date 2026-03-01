#!/usr/bin/env python3
"""
One-time fix: Recalculate entry_price from unrealized_pnl
Uses IBKR's actual cost basis data instead of current price
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def save_json(filename, data):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)

def fix_entry_prices():
    print("🔧 Recalculating entry prices from cost basis...")
    
    holdings_data = load_json("holdings.json")
    
    fixed = 0
    for holding in holdings_data["portfolio"]:
        current_value = holding.get("current_value", 0)
        unrealized_pnl = holding.get("unrealized_pnl", 0)
        shares = holding.get("shares", 0)
        
        if shares == 0:
            print(f"   ⚠️  {holding['ticker']}: No shares (skipping)")
            continue
        
        # Cost basis = market value - unrealized P&L
        cost_basis_total = current_value - unrealized_pnl
        cost_basis_per_share = cost_basis_total / shares
        
        old_entry = holding.get("entry_price", 0)
        holding["entry_price"] = cost_basis_per_share
        
        # Calculate actual return
        current_price = holding.get("current_price", 0)
        return_pct = ((current_price - cost_basis_per_share) / cost_basis_per_share * 100) if cost_basis_per_share > 0 else 0
        
        print(f"   ✓ {holding['ticker']}: {cost_basis_per_share:.2f} (was {old_entry:.2f}) → Return: {return_pct:+.1f}%")
        fixed += 1
    
    save_json("holdings.json", holdings_data)
    print(f"\n✅ Fixed {fixed} entry prices using IBKR cost basis")

if __name__ == "__main__":
    fix_entry_prices()
