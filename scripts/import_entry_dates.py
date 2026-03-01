#!/usr/bin/env python3
"""
Import actual entry dates from CSV
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

def import_entry_dates(csv_path):
    print("📅 Importing entry dates...")
    
    holdings_data = load_json("holdings.json")
    
    # Build a lookup map
    ticker_map = {h["ticker"]: h for h in holdings_data["portfolio"]}
    
    updated = 0
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = row["ticker"]
            new_date = row["entry_date"]
            
            if ticker in ticker_map and new_date != "2026-03-01":
                ticker_map[ticker]["entry_date"] = new_date
                print(f"   ✓ {ticker}: {new_date}")
                updated += 1
    
    save_json("holdings.json", holdings_data)
    print(f"\n✅ Updated {updated} entry dates")

if __name__ == "__main__":
    csv_file = DATA_DIR / "entry_dates.csv"
    if not csv_file.exists():
        print("❌ No entry_dates.csv found")
        print("📋 Template created at data/entry_dates_template.csv")
        print("   → Copy to data/entry_dates.csv and fill in actual dates")
    else:
        import_entry_dates(csv_file)
