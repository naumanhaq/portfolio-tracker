#!/usr/bin/env python3
"""
Send portfolio update notification to Telegram
Called after successful IBKR sync
"""

import sys
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def format_notification():
    """Generate portfolio update notification"""
    
    # Load current data
    try:
        with open(DATA_DIR / "holdings_snapshot.json") as f:
            snapshot = json.load(f)
        
        account_value = snapshot.get("account_value", 0)
        as_of = snapshot.get("as_of_date", "unknown")
        
        # Get stock count
        stock_count = len(snapshot["positions"]["stocks"])
        option_count = len(snapshot["positions"]["options"])
        etf_count = len(snapshot["positions"]["etfs"])
        
        message = f"""📊 Portfolio Updated

💰 Account Value: ${account_value:,.2f}
📅 As of: {as_of}

Holdings:
• {stock_count} stocks
• {etf_count} ETFs  
• {option_count} options

🌐 enhaq.capital"""
        
        return message
        
    except Exception as e:
        return f"❌ Portfolio sync completed but notification failed: {e}"

if __name__ == "__main__":
    print(format_notification())
