# Portfolio Tracker - enhaq.online

Static site for tracking long-term investments and options trades.

## Structure

- `data/` — JSON data files
  - `holdings.json` — Long-term portfolio positions
  - `trades.json` — Options trades log
- `templates/` — HTML templates
- `scripts/` — Python generators + utilities
- `public/` — Generated HTML (deploy this)

## Usage

**Generate site:**
```bash
python3 scripts/generate.py
```

**Add new holding:**
```bash
python3 scripts/add-holding.py --ticker RACE --entry-date 2025-01-15 --shares 100 --price 450.00
```

**Add new trade:**
```bash
python3 scripts/add-trade.py --ticker SPY --type P1 --structure "Long Calendar" --entry-date 2026-02-01
```

**Deploy:**
```bash
./scripts/deploy.sh
```

## Deployment

- Domain: portfolio.enhaq.online (subdomain on Hostinger)
- Method: FTP/SFTP upload of `public/` folder
- Automated: Cron or manual after updates

## Future: IBKR Integration

Phase 2: Flex Query automation to sync positions daily.
