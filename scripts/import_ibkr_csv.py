#!/usr/bin/env python3
"""
Import position data from IBKR Portfolio Analyst CSV
Updates holdings.json with actual cost basis and returns
"""

import json
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def save_json(filename, data):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)

def parse_ibkr_csv(csv_path):
    """Extract position data from IBKR Portfolio Analyst CSV"""
    positions = {}
    performance = {}
    
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            
            section = row[0]
            data_type = row[1]
            
            # Extract performance metrics
            if section == "Key Statistics" and data_type == "Data":
                # Row: BeginningNAV,EndingNAV,CumulativeReturn,1MonthReturn,...,YTD,...
                try:
                    cumulative_return = float(row[4]) if len(row) > 4 and row[4] else 0
                    performance["since_inception_return"] = cumulative_return
                except:
                    pass
            
            # Extract benchmark comparison for YTD, 1Y returns
            if section == "Historical Performance Benchmark Comparison" and data_type == "Data":
                if len(row) > 1 and row[2] == "U4407190":  # Account line
                    try:
                        # Row: Account, MTD, QTD, YTD, 1Year, 3Year, 5Year, Since Inception
                        ytd = float(row[5]) if len(row) > 5 and row[5] else 0
                        one_year = float(row[6]) if len(row) > 6 and row[6] else 0
                        performance["ytd_return"] = ytd
                        performance["one_year_return"] = one_year
                    except:
                        pass
            
            # Extract position data
            if section == "Open Position Summary" and data_type == "Data":
                if len(row) < 14:
                    continue
                
                # Skip "Total" rows
                if row[2] == "Total":
                    continue
                
                # Row: [0]=Section, [1]=Type, [2]=Date, [3]=FinancialInstrument,
                #      [4]=Currency, [5]=Symbol, [6]=Description, [7]=Sector,
                #      [8]=Quantity, [9]=ClosePrice, [10]=Value, [11]=CostBasis,
                #      [12]=UnrealizedP&L, [13]=FXRate
                symbol = row[5].strip()
                
                # Skip empty symbols
                if not symbol:
                    continue
                
                try:
                    quantity = float(row[8].strip()) if row[8].strip() else 0
                    close_price = float(row[9].strip()) if row[9].strip() else 0
                    value = float(row[10].strip()) if row[10].strip() else 0
                    cost_basis = float(row[11].strip()) if row[11].strip() else 0
                    unrealized_pnl = float(row[12].strip()) if row[12].strip() else 0
                    currency = row[4].strip()
                except ValueError:
                    continue
                
                # Calculate entry price from cost basis
                entry_price = abs(cost_basis / quantity) if quantity != 0 else close_price
                
                positions[symbol] = {
                    "current_price": close_price,
                    "entry_price": entry_price,
                    "shares": abs(quantity),
                    "current_value": value,
                    "unrealized_pnl": unrealized_pnl,
                    "cost_basis": cost_basis,
                    "currency": currency
                }
    
    return positions, performance

def update_holdings_from_csv(csv_path):
    print("📊 Importing IBKR Portfolio Analyst data...")
    
    positions, performance = parse_ibkr_csv(csv_path)
    
    print(f"\nFound {len(positions)} positions in CSV")
    print(f"Performance: YTD {performance.get('ytd_return', 0):.2f}%, 1Y {performance.get('one_year_return', 0):.2f}%, Since Inception {performance.get('since_inception_return', 0):.2f}%")
    
    holdings_data = load_json("holdings.json")
    
    # Update existing holdings
    updated = 0
    for holding in holdings_data["portfolio"]:
        ticker = holding["ticker"]
        
        if ticker in positions:
            pos = positions[ticker]
            holding["entry_price"] = pos["entry_price"]
            holding["current_price"] = pos["current_price"]
            holding["shares"] = pos["shares"]
            holding["current_value"] = pos["current_value"]
            holding["unrealized_pnl"] = pos["unrealized_pnl"]
            
            # Calculate return %
            return_pct = (pos["unrealized_pnl"] / abs(pos["cost_basis"]) * 100) if pos["cost_basis"] != 0 else 0
            
            print(f"   ✓ {ticker}: Entry ${pos['entry_price']:.2f} → Current ${pos['current_price']:.2f} ({return_pct:+.1f}%)")
            updated += 1
        else:
            print(f"   ⚠️  {ticker}: Not found in CSV")
    
    # Update performance metrics
    holdings_data["performance"] = {
        "ytd_return": performance.get("ytd_return", 0),
        "one_year_return": performance.get("one_year_return", 0),
        "since_inception_return": performance.get("since_inception_return", 0),
        "annualized_irr": performance.get("since_inception_return", 0) / 5.5  # Rough approximation
    }
    
    save_json("holdings.json", holdings_data)
    
    print(f"\n✅ Updated {updated} holdings with cost basis and returns")
    print(f"✅ Updated performance metrics")
    print(f"\n⚠️  Entry dates still need manual correction (see data/entry_dates_template.csv)")

if __name__ == "__main__":
    csv_file = DATA_DIR / "portfolio_from_drive.csv"
    if not csv_file.exists():
        print(f"❌ CSV not found: {csv_file}")
    else:
        update_holdings_from_csv(csv_file)
