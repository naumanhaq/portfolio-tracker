# Valuation Framework: Reverse DCF + 3 Ps

## Overview

This framework combines **two independent signals** to determine when and what to buy:

1. **Broad Market Signal:** Bear Market Bottom Indicators (11 technical signals)
2. **Individual Stock Signal:** Reverse DCF + 3 Ps Framework (valuation analysis per ticker)

**Both must align for deployment.**

---

## The Two-Signal System

### Signal 1: Bear Market Indicators (Broad)

**Purpose:** Tells you WHEN to deploy cash (market timing)

**Threshold:**
- **8+ indicators met:** Deploy cash heavily
- **7 indicators:** Partial deployment (optional)
- **<7 indicators:** Stay in cash accumulation mode

**Current Status:** 1/11 indicators (bull market, no deployment)

**See:** [enhaq.capital/bear-signals.html](https://enhaq.capital/bear-signals.html)

---

### Signal 2: Reverse DCF (Individual Stock)

**Purpose:** Tells you WHAT to buy and at what price (valuation discipline)

**Framework:** Professor Damodaran's "3 Ps" (Possible, Plausible, Probable)

**Workflow:**
1. **Reverse DCF:** Calculate implied growth rate to justify current price
2. **Multiple Compression:** Stress-test if valuation compresses to "mature" levels
3. **3 Ps Assessment:** Is the implied growth Possible? Plausible? Probable?
4. **Entry/Exit Triggers:** Define buy/hold/sell zones based on Probable vs. Implied

**Philosophy:** Price ≠ Value. Decode the market's assumptions, then assess if they're realistic.

---

## Reverse DCF Calculation

### Step 1: Implied Growth Rate

**Formula (simplified):**
```
Current Price = FCF₀ × (1 + g)^10 × Terminal Multiple / (1 + WACC)^10
```

**Solve for g** — this is the "Implied Growth" the market expects.

**Example (CSU):**
- Current price: CAD 2,520
- Current multiple: 35x P/FCF
- Implied 10-year FCF CAGR: **12-14%**
- Market expects: CSU grows FCF at 12-14% annually for 10 years, then 3% perpetually

---

### Step 2: Multiple Compression Scenario

**Question:** What if the premium valuation compresses?

**Example (CSU):**
- Current: 35x P/FCF
- Mature scenario: 25x P/FCF (mature VMS multiple)
- **Breakeven CAGR: 16-18%**
- Need 16-18% growth just to break even if multiple compresses

**This stress-tests your downside risk.**

---

## The 3 Ps Framework

### Possible: Is the TAM Large Enough?

**Question:** Can the company grow at the implied rate without running out of market?

**Example (CSU):**
- ✅ Yes. VMS TAM $50B+, expanding (cloud migration, vertical deepening)
- No ceiling in sight for 10+ years

---

### Plausible: Is There a Logical Pathway?

**Question:** Can the company realistically execute? (pricing power, margins, capital allocation)

**Example (CSU):**
- ✅ Yes. Historical 20%+ FCF growth (2010-2020)
- M&A pipeline robust, pricing power intact
- Decentralized model scales without bureaucracy

---

### Probable: What's the Base Case?

**Question:** Given track record and structural moats, what's most likely?

**Example (CSU):**
- **Base case: 15% FCF CAGR**
- Bull case: 18%
- Bear case: 12%
- **Probable: 15-18%**

---

## Comparison: Probable vs. Implied

**Decision Matrix:**

| Scenario | Action |
|---|---|
| **Probable > Implied by 20%+** | Strong BUY (undervalued) |
| **Probable ≈ Implied (±10%)** | HOLD (fairly valued) |
| **Implied > Probable by 20%+** | SELL (overvalued) |

**Example (CSU):**
- Probable: 15-18%
- Implied: 12-14%
- **Assessment:** Probable > Implied by ~20%
- **Signal:** Fairly valued to slightly undervalued

---

## Entry / Exit Triggers

### Buy Trigger

**Two conditions (OR logic):**
1. **Valuation trigger:** Price drops enough that Probable > Implied by 30%+
2. **Market trigger:** 8+ bear signals + price < Fair Value

**Example (CSU):**
- **BUY:** Price < CAD 2,200 (Probable 20%+ above Implied) **OR** 8+ bear signals

---

### Hold Range

**When:** Probable ≈ Implied (±20%)

**Example (CSU):**
- **HOLD:** CAD 2,200 - 3,000
- Fair value range, wait for better entry or market dislocation

---

### Sell Trigger

**When:** Implied > Probable significantly (market expects unrealistic growth)

**Example (CSU):**
- **SELL:** Price > CAD 3,500 (P/FCF >40x, Implied >20%, unsustainable for VMS)

---

## Deployment Logic

### Scenario 1: Bull Market (Current)

- Bear signals: 1/11
- CSU signal: HOLD (fairly valued)
- **Action:** Accumulate cash, monitor both signals

### Scenario 2: Bear Market + Fair Valuation

- Bear signals: 9/11 ✅
- CSU signal: HOLD (still fairly valued despite market crash)
- **Action:** Deploy into CSU (market signal overrides individual signal)
- **Rationale:** Quality compounder at reasonable price during panic

### Scenario 3: Bull Market + Deep Undervaluation

- Bear signals: 2/11
- CSU signal: BUY (price crashed 40%, Probable >> Implied)
- **Action:** Buy CSU (individual signal sufficient)
- **Rationale:** Company-specific dislocation, not market-wide

### Scenario 4: Bear Market + Both Signals Align

- Bear signals: 9/11 ✅
- CSU signal: BUY (price < 2,200) ✅
- **Action:** Deploy heavily into CSU
- **Rationale:** Maximum conviction — market timing + valuation align

---

## How to Use This

### 1. During Bull Markets (Now)

**Tasks:**
- Monitor bear signals daily (automated)
- Update reverse DCF valuations quarterly
- Build/maintain watchlist
- Accumulate cash

**Script to update valuations:**
```bash
cd /data/.openclaw/workspace/bear-signals-repo
python3 scripts/calculate_reverse_dcf.py TICKER
```

---

### 2. When 8+ Bear Signals Trigger

**Tasks:**
- Review all watchlist positions
- Prioritize by:
  1. Positions with BUY signals (Probable >> Implied)
  2. Existing holdings with "Add on dip" flag
  3. High Fisher scores + Lindy years
- Deploy cash heavily (not DCA)

**Example allocation ($100k):**
- 50% → Broad ETFs (VWRA, SPY, QQQ)
- 50% → Individual stocks with BUY signals

---

### 3. After Deployment

**Tasks:**
- Stop monitoring bear signals (don't chase)
- Return to cash accumulation mode
- Let positions compound
- Update reverse DCF quarterly to track if thesis holds

---

## Tools & Scripts

### Calculate Reverse DCF (Interactive)
```bash
python3 scripts/calculate_reverse_dcf.py CSU
```
- Guides you through:
  - Current price & multiple
  - Implied growth calculation
  - Multiple compression scenario
  - 3 Ps assessment
  - Entry/exit triggers
- Outputs JSON to paste into watchlist.json

### Update Watchlist HTML
```bash
python3 scripts/generate_watchlist_html.py
```
- Regenerates watchlist.html from watchlist.json
- Run after editing valuation data

### Full Update & Deploy
```bash
bash scripts/update_and_deploy.sh
```
- Collects bear signals
- Generates all HTML pages
- Pushes to GitHub Pages

---

## Examples

### CSU (Constellation Software)

**Current Status:**
- Price: CAD 2,520
- Multiple: 35x P/FCF
- Implied: 12-14% FCF CAGR
- Probable: 15-18% FCF CAGR
- **Signal:** HOLD (wait for 8+ bear signals or price < 2,200)

### RMS (Hermès)

**Current Status:**
- Price: EUR 2,350
- Multiple: 55x P/E
- Implied: 8-10% EPS CAGR
- Probable: 10-12% EPS CAGR
- **Signal:** HOLD (fairly valued, luxury premium justified)

### MSFT (Microsoft)

**Current Status:**
- Price: USD 445
- Multiple: 38x P/E
- Implied: 12-14% EPS CAGR
- Probable: 14-16% EPS CAGR
- **Signal:** WAIT (not buying unless 8+ bear signals)

---

## Philosophy

**Two-dimensional risk management:**

1. **Time risk:** Am I buying at the right time? (Bear signals)
2. **Price risk:** Am I buying at the right price? (Reverse DCF)

**Both dimensions must align for maximum conviction deployment.**

**When only one aligns:**
- Bear signals alone → Deploy into fair-valued quality (reasonable)
- Valuation alone → Opportunistic single-stock buy (higher risk)

**When both align:**
- Maximum deployment (highest conviction)

---

## Maintenance

**Quarterly:**
- Update reverse DCF for all owned positions
- Recalculate implied growth rates (prices change)
- Reassess 3 Ps (business performance changes)
- Adjust entry/exit triggers

**Weekly:**
- Check bear signals (automated)
- Monitor position prices vs. triggers

**Daily:**
- Bear signals auto-update at 9 PM UAE
- Telegram alerts if 8+ indicators trigger

---

## References

- **Aswath Damodaran:** Narrative and Numbers, reverse DCF methodology
- **Bear Market Framework:** Based on multi-decade backtesting (2018, 2020, 2022, 2025 bottoms)
- **Fisher 15-Point Quality:** Common Stocks and Uncommon Profits
- **Lindy Effect:** Nassim Taleb, Antifragile

---

**Live Dashboard:** https://enhaq.capital/watchlist.html
