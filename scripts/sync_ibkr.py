#!/usr/bin/env python3
"""
Sync portfolio data from Interactive Brokers Flex Query
Updates holdings.json with current prices and positions
"""

import os
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date
import urllib.request
import urllib.parse

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SECRETS_DIR = PROJECT_ROOT / ".secrets"
HOLDINGS_FILE = DATA_DIR / "holdings.json"
IBKR_ENV = SECRETS_DIR / "ibkr.env"

# Load credentials
def load_credentials():
    """Load IBKR credentials from .secrets/ibkr.env"""
    if not IBKR_ENV.exists():
        print(f"❌ IBKR credentials not found at {IBKR_ENV}")
        return None, None
    
    creds = {}
    with open(IBKR_ENV) as f:
        for line in f:
            if '=' in line:
                key, val = line.strip().split('=', 1)
                creds[key] = val
    
    return creds.get('IBKR_QUERY_ID'), creds.get('IBKR_TOKEN')

def request_flex_report(query_id, token):
    """Request Flex Query execution and return reference code"""
    url = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest"
    params = {
        't': token,
        'q': query_id,
        'v': '3'
    }
    
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    print(f"📡 Requesting Flex Query {query_id}...")
    
    try:
        with urllib.request.urlopen(full_url) as response:
            xml_data = response.read().decode('utf-8')
            
        # Parse response
        root = ET.fromstring(xml_data)
        
        # Check for error
        if root.tag == 'Status':
            error_code = root.find('ErrorCode')
            error_msg = root.find('ErrorMessage')
            if error_code is not None:
                print(f"❌ IBKR Error {error_code.text}: {error_msg.text}")
                return None
        
        # Get reference code
        ref_code_elem = root.find('.//ReferenceCode')
        if ref_code_elem is not None:
            ref_code = ref_code_elem.text
            print(f"✅ Request accepted. Reference code: {ref_code}")
            return ref_code
        else:
            print(f"❌ No reference code in response")
            return None
    
    except Exception as e:
        print(f"❌ Error requesting report: {e}")
        return None

def fetch_flex_report(ref_code, token, max_attempts=10):
    """Fetch Flex Query report using reference code"""
    url = "https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement"
    params = {
        't': token,
        'q': ref_code,
        'v': '3'
    }
    
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    print(f"📥 Fetching report (ref: {ref_code})...")
    
    for attempt in range(max_attempts):
        try:
            with urllib.request.urlopen(full_url) as response:
                xml_data = response.read().decode('utf-8')
            
            root = ET.fromstring(xml_data)
            
            # Check for error
            if root.tag == 'Status':
                error_code = root.find('ErrorCode')
                error_msg = root.find('ErrorMessage')
                
                if error_code is not None:
                    code = error_code.text
                    msg = error_msg.text if error_msg is not None else "Unknown error"
                    
                    # Error code 1019 = report not ready yet
                    if code == '1019':
                        print(f"   ⏳ Report not ready yet (attempt {attempt + 1}/{max_attempts}), waiting 3s...")
                        time.sleep(3)
                        continue
                    else:
                        print(f"❌ IBKR Error {code}: {msg}")
                        return None
            
            # If we got here, report is ready
            print("✅ Report downloaded successfully")
            return root
        
        except Exception as e:
            print(f"❌ Error fetching report: {e}")
            return None
    
    print(f"❌ Report not ready after {max_attempts} attempts")
    return None

def parse_positions(flex_report):
    """Parse open positions from Flex Query XML"""
    positions = []
    
    # Find OpenPositions section
    for position in flex_report.findall('.//OpenPosition'):
        symbol = position.get('symbol')
        quantity = float(position.get('position', 0))
        market_price = float(position.get('markPrice', 0))
        market_value = float(position.get('positionValue', 0))
        unrealized_pnl = float(position.get('fifoPnlUnrealized', 0))  # IBKR uses fifoPnlUnrealized, not unrealizedPnL
        asset_class = position.get('assetCategory', 'STK')
        currency = position.get('currency', 'USD')
        
        positions.append({
            'symbol': symbol,
            'quantity': quantity,
            'market_price': market_price,
            'market_value': market_value,
            'unrealized_pnl': unrealized_pnl,
            'asset_class': asset_class,
            'currency': currency
        })
    
    return positions

def update_holdings(positions):
    """
    Update holdings.json with IBKR equity positions
    - Auto-imports STOCKS (STK) only
    - Ignores OPTIONS (OPT) - those belong in trades
    - Updates existing + imports new equity positions
    """
    # Load existing holdings
    with open(HOLDINGS_FILE) as f:
        data = json.load(f)
    
    # Filter: STOCKS only (STK), ignore options (OPT)
    stock_positions = [p for p in positions if p['asset_class'] == 'STK']
    
    # Existing tickers lookup
    existing = {h['ticker'].split('.')[0]: h for h in data['portfolio']}
    
    total_value = 0
    updated = 0
    imported = []
    
    # Process all stock positions
    for ibkr_pos in stock_positions:
        symbol = ibkr_pos['symbol']
        ticker_base = symbol.split('.')[0]
        
        if ticker_base in existing or symbol in existing:
            # Update existing
            holding = existing.get(symbol) or existing.get(ticker_base)
            holding['current_price'] = ibkr_pos['market_price']
            holding['shares'] = ibkr_pos['quantity']
            holding['current_value'] = ibkr_pos['market_value']
            holding['unrealized_pnl'] = ibkr_pos['unrealized_pnl']
            total_value += abs(ibkr_pos['market_value'])
            updated += 1
            print(f"   ✓ {symbol}: {ibkr_pos['currency']}{ibkr_pos['market_price']:.2f} × {ibkr_pos['quantity']:.0f}")
        else:
            # Auto-import new equity position
            # Calculate actual cost basis from unrealized P&L
            cost_basis_total = ibkr_pos['market_value'] - ibkr_pos['unrealized_pnl']
            cost_basis_per_share = cost_basis_total / ibkr_pos['quantity'] if ibkr_pos['quantity'] != 0 else ibkr_pos['market_price']
            
            new_holding = {
                "ticker": symbol,
                "name": symbol,
                "category": "Equity",
                "geography": "TBD",
                "entry_date": str(date.today()),
                "entry_price": cost_basis_per_share,
                "current_price": ibkr_pos['market_price'],
                "allocation_pct": 0,
                "shares": ibkr_pos['quantity'],
                "currency": ibkr_pos['currency'],
                "thesis": "Add investment thesis",
                "thesis_evolution": [],
                "add_trim_signals": [],
                "current_value": ibkr_pos['market_value'],
                "unrealized_pnl": ibkr_pos['unrealized_pnl']
            }
            data['portfolio'].append(new_holding)
            imported.append(symbol)
            total_value += abs(ibkr_pos['market_value'])
            print(f"   ✨ {symbol}: imported ({ibkr_pos['quantity']:.0f} shares)")
    
    # Calculate allocation %
    for holding in data['portfolio']:
        if holding.get('current_value') and total_value > 0:
            holding['allocation_pct'] = (abs(holding['current_value']) / total_value) * 100
    
    data['last_updated'] = str(date.today())
    
    # Save
    with open(HOLDINGS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ {updated} updated, {len(imported)} imported")
    print(f"   Total equity value: ${total_value:,.0f}")
    if imported:
        print(f"   New: {', '.join(imported)}")
    
    return data

def main():
    print("🔄 Syncing portfolio from Interactive Brokers...\n")
    
    # Load credentials
    query_id, token = load_credentials()
    if not query_id or not token:
        print("❌ Missing IBKR credentials")
        return
    
    # Request report
    ref_code = request_flex_report(query_id, token)
    if not ref_code:
        return
    
    # Wait a moment for report generation
    print("   Waiting 3 seconds for report generation...")
    time.sleep(3)
    
    # Fetch report
    flex_report = fetch_flex_report(ref_code, token)
    if flex_report is None:
        return
    
    # Parse positions
    positions = parse_positions(flex_report)
    print(f"\n📊 Found {len(positions)} positions in IBKR:")
    for p in positions:
        print(f"   {p['symbol']}: {p['quantity']} @ ${p['market_price']:.2f} = ${p['market_value']:,.2f}")
    
    # Update holdings
    print(f"\n💾 Updating holdings.json...")
    update_holdings(positions)
    
    print("\n✅ Sync complete!")
    print("\n🔨 Regenerating site...")
    os.system(f"cd {PROJECT_ROOT} && python3 scripts/generate.py")
    
    print("\n✅ Done! Site updated with latest positions.")

if __name__ == "__main__":
    main()
