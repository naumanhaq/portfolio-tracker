# Portfolio Tracker - Quick Start

## What's Built

✅ **Static site generator** (JSON → HTML with Tailwind CSS)
✅ **Two pages:**
   - `/index.html` — Long-term portfolio tracker
   - `/options.html` — Options trades log
✅ **Helper scripts** for adding data
✅ **Sample data** (Hermès holding + SPY calendar spread)
✅ **Deploy script** (needs Hostinger credentials)

## Preview the Site

```bash
cd ~/.openclaw/workspace/portfolio-tracker
python3 scripts/generate.py
```

Then open in browser:
- `file://~/.openclaw/workspace/portfolio-tracker/public/index.html`

Or use a simple HTTP server:
```bash
cd public/
python3 -m http.server 8000
# Visit: http://localhost:8000
```

## Add Data

### Add a Long-Term Holding

```bash
python3 scripts/add-holding.py \
  --ticker "RACE.MI" \
  --name "Ferrari N.V." \
  --category "Luxury - Lindy" \
  --entry-date "2025-11-20" \
  --entry-price 420.00 \
  --shares 50 \
  --currency "EUR" \
  --thesis "Enduring luxury brand. Scarcity model + pricing power. Fisher quality growth." \
  --valuation-notes "Premium multiple acceptable for 20-year hold."
```

### Add an Options Trade

```bash
python3 scripts/add-trade.py \
  --ticker "SPY" \
  --type "P1" \
  --classification "Long Calendar" \
  --entry-date "2026-03-01" \
  --thesis "IV at 15th percentile, term structure flat. Buying near-term vol cheap." \
  --long "SPY Mar 14 560C" \
  --short "SPY Apr 18 560C" \
  --net-debit 320.00 \
  --iv-pct 15 \
  --vrp -1.8 \
  --rv-pct 20 \
  --term-structure "flat"
```

After adding data, regenerate the site:
```bash
python3 scripts/generate.py
```

## Edit Data Manually

Edit JSON files directly:
- `data/holdings.json` — Long-term positions
- `data/trades.json` — Options trades

Then regenerate:
```bash
python3 scripts/generate.py
```

## Deploy to Hostinger

### Step 1: Configure Credentials

Edit `scripts/deploy.sh` and add your Hostinger details:
```bash
HOST='ftp.yourdomain.com'
USER='your_ftp_username'
PASS='your_ftp_password'
REMOTE_DIR='/public_html/portfolio.enhaq.online'
```

Or use SFTP with SSH keys (more secure).

### Step 2: Deploy

```bash
./scripts/deploy.sh
```

### Manual Deployment

1. Generate site: `python3 scripts/generate.py`
2. Upload `public/` folder contents to your Hostinger subdomain root
3. Done!

## Next Steps

### Phase 2: IBKR Integration

Auto-sync positions from Interactive Brokers using Flex Queries:
1. Set up Flex Query in IBKR
2. Add Python script to fetch daily
3. Update `current_price`, `unrealized_pnl` in holdings.json
4. Cron job: daily sync + regenerate

### Future Enhancements

- Add P&L charts (Chart.js or Plotly)
- Trade statistics page (win rate, avg R:R)
- Export to CSV
- Dark mode toggle
- Mobile-responsive improvements

## Data Structure

### Holdings JSON Schema

```json
{
  "ticker": "RMS.PA",
  "name": "Hermès International",
  "category": "Luxury - Lindy",
  "entry_date": "2024-06-15",
  "entry_price": 2100.00,
  "shares": 10,
  "currency": "EUR",
  "thesis": "Your investment thesis here",
  "thesis_evolution": [
    {
      "date": "2024-06-15",
      "note": "Initial entry note"
    }
  ],
  "valuation_notes": "Valuation commentary",
  "add_trim_signals": [],
  "current_price": null,
  "current_value": null,
  "unrealized_pnl": null
}
```

### Trades JSON Schema

```json
{
  "id": "T001",
  "ticker": "SPY",
  "trade_type": "P1",
  "classification": "Long Calendar",
  "entry_date": "2026-02-01",
  "exit_date": null,
  "status": "open",
  "entry_thesis": "Why you entered",
  "structure": {
    "long": "Long leg description",
    "short": "Short leg description",
    "net_debit": 250.00
  },
  "greeks_at_entry": {
    "delta": 0.05,
    "theta": -15.00,
    "vega": 45.00
  },
  "expected_outcome": "What you expected to happen",
  "actual_outcome": null,
  "realized_pnl": null,
  "lessons": [],
  "moontower_metrics": {
    "iv_percentile": 12,
    "vrp": -2.5,
    "rv_percentile": 18,
    "term_structure": "flat"
  }
}
```

## Questions?

- Check README.md for overview
- Inspect `scripts/generate.py` to understand templating
- Edit `data/*.json` to customize data
