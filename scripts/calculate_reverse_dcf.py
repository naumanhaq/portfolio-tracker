#!/usr/bin/env python3
"""
Reverse DCF Calculator
Calculate implied growth rates to justify current stock price

Usage:
    python3 calculate_reverse_dcf.py TICKER

Interactive prompts will guide you through:
1. Current price & multiple
2. Terminal assumptions (growth, WACC)
3. Multiple compression scenario
4. 3 Ps assessment
5. Entry/exit triggers

Output: Updates watchlist.json with valuation data
"""

import json
import sys
from datetime import datetime

def calculate_implied_cagr():
    """
    Simplified reverse DCF calculator
    
    Formula (approximation):
    Current Price = FCF0 * (1 + g)^10 * Terminal Multiple / (1 + WACC)^10
    
    Solve for g (implied growth rate)
    """
    print("\n=== Reverse DCF Calculator ===")
    print("This calculates the implied growth rate embedded in the current price.\n")
    
    current_price = float(input("Current stock price: "))
    current_multiple = float(input("Current multiple (P/E or P/FCF): "))
    fcf_or_eps = float(input("Current FCF or EPS per share: "))
    
    terminal_growth = float(input("Terminal growth rate (default 3%): ") or 3) / 100
    wacc = float(input("WACC / discount rate (default 9%): ") or 9) / 100
    years = int(input("Forecast period (default 10 years): ") or 10)
    
    # Simplified calculation (assuming constant multiple at end)
    # current_price ≈ fcf_or_eps * (1 + g)^years * current_multiple / (1 + wacc)^years
    
    # Solving for g:
    discount_factor = (1 + wacc) ** years
    target_fcf_eps = current_price * discount_factor / current_multiple
    
    implied_cagr = (target_fcf_eps / fcf_or_eps) ** (1 / years) - 1
    
    print(f"\n✓ Implied {years}-year CAGR: {implied_cagr * 100:.1f}%")
    print(f"  (This is what the market expects to justify current price of {current_price})")
    
    # Multiple compression scenario
    print("\n--- Multiple Compression Scenario ---")
    mature_multiple = float(input(f"Mature multiple in {years} years (e.g., 25 for 25x): "))
    
    target_fcf_eps_compressed = current_price * discount_factor / mature_multiple
    breakeven_cagr = (target_fcf_eps_compressed / fcf_or_eps) ** (1 / years) - 1
    
    print(f"\n✓ Breakeven CAGR with compression: {breakeven_cagr * 100:.1f}%")
    print(f"  (Need this growth just to break even if multiple compresses to {mature_multiple}x)")
    
    return {
        "implied_cagr": round(implied_cagr * 100, 1),
        "breakeven_cagr_compressed": round(breakeven_cagr * 100, 1),
        "terminal_growth": terminal_growth * 100,
        "wacc": wacc * 100,
        "mature_multiple": mature_multiple
    }

def get_three_ps():
    """Interactive 3 Ps assessment"""
    print("\n=== The 3 Ps Framework ===")
    print("Assess whether the implied growth is achievable.\n")
    
    possible = input("POSSIBLE: Is the TAM large enough? (Yes/No + rationale): ")
    plausible = input("PLAUSIBLE: Is there a logical pathway to get there? (Yes/No + rationale): ")
    probable_input = input("PROBABLE: What's your base case growth estimate? (e.g., 12-15% CAGR): ")
    
    probable_low = float(input("  Base case (low): ") or 0)
    probable_high = float(input("  Base case (high): ") or 0)
    probable_range = f"{probable_low}-{probable_high}%"
    
    assessment = input("\nFinal assessment (Probable vs. Implied): ")
    
    return {
        "possible": possible,
        "plausible": plausible,
        "probable": f"{probable_range} CAGR. {probable_input}",
        "assessment": assessment
    }

def get_entry_exit_triggers(current_price, implied_cagr, probable_range):
    """Define entry/exit triggers"""
    print("\n=== Entry / Exit Triggers ===")
    print(f"Current price: {current_price}")
    print(f"Implied growth: {implied_cagr}%")
    print(f"Probable growth: {probable_range}\n")
    
    buy_trigger = input("BUY trigger (price level + conditions): ")
    hold_range = input("HOLD range (e.g., 2200-3000): ")
    sell_trigger = input("SELL trigger (price level + conditions): ")
    current_signal = input("Current signal (BUY/HOLD/SELL/WAIT + brief rationale): ")
    
    return {
        "buy": buy_trigger,
        "hold": hold_range,
        "sell": sell_trigger,
        "current_signal": current_signal
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 calculate_reverse_dcf.py TICKER")
        print("Example: python3 calculate_reverse_dcf.py CSU")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    
    print(f"\n🔍 Calculating valuation for {ticker}...")
    
    # Get current price info
    current_price = input(f"\nCurrent price for {ticker}: ")
    current_multiple_str = input(f"Current multiple (e.g., 'P/E ~35x' or 'P/FCF ~40x'): ")
    
    # Calculate reverse DCF
    dcf_results = calculate_implied_cagr()
    
    # Get 3 Ps assessment
    three_ps = get_three_ps()
    
    # Get entry/exit triggers
    triggers = get_entry_exit_triggers(
        current_price, 
        dcf_results['implied_cagr'],
        three_ps['probable']
    )
    
    # Build valuation object
    valuation = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "current_price_usd": current_price,  # Adjust currency key as needed
        "current_multiple": current_multiple_str,
        "reverse_dcf": {
            "implied_eps_cagr_10y": f"{dcf_results['implied_cagr']:.0f}%",
            "terminal_growth": f"{dcf_results['terminal_growth']}%",
            "wacc": f"{dcf_results['wacc']}%",
            "interpretation": f"Market expects {dcf_results['implied_cagr']:.0f}% growth for 10 years."
        },
        "multiple_compression_scenario": {
            "mature_multiple": f"{dcf_results['mature_multiple']:.0f}x",
            "breakeven_cagr": f"{dcf_results['breakeven_cagr_compressed']:.0f}%",
            "interpretation": f"Need {dcf_results['breakeven_cagr_compressed']:.0f}% growth if multiple compresses."
        },
        "three_ps": three_ps,
        "entry_exit_trigger": triggers
    }
    
    # Print summary
    print("\n" + "="*60)
    print(f"VALUATION SUMMARY FOR {ticker}")
    print("="*60)
    print(json.dumps(valuation, indent=2))
    print("="*60)
    
    # Ask to save
    save = input("\n💾 Add this to watchlist.json? (y/n): ")
    if save.lower() == 'y':
        print("\n⚠️  Manual step required:")
        print(f"1. Open data/watchlist.json")
        print(f"2. Find the position for {ticker}")
        print(f"3. Add/update the 'valuation' field with the JSON above")
        print(f"4. Run: python3 scripts/generate_watchlist_html.py")
        print(f"5. Commit and push to GitHub")

if __name__ == "__main__":
    main()
