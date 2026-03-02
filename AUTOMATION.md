# Portfolio Automation

## Daily Sync Setup

The portfolio automatically syncs with Interactive Brokers daily and updates enhaq.capital.

### How it works

1. **Fetch data:** Pulls latest positions from IBKR Flex Query
2. **Update files:** Updates `data/holdings.json` with current prices
3. **Regenerate site:** Runs `generate.py` to update HTML
4. **Deploy:** Commits and pushes to GitHub (auto-deploys via GitHub Pages)
5. **Notify:** Sends Telegram message if changes detected

### Manual run

```bash
cd /data/.openclaw/workspace/portfolio-tracker
./scripts/sync_and_notify.sh
```

### Schedule with OpenClaw

To set up daily automation at 9 AM Dubai time (5 AM UTC):

```bash
# Add to HEARTBEAT.md or create a scheduled session
# Or use system cron if available:
0 5 * * * cd /data/.openclaw/workspace/portfolio-tracker && ./scripts/sync_and_notify.sh
```

### Telegram Notification

After successful sync with changes, sends message:
```
📊 Portfolio Updated

💰 Account Value: $XXX,XXX.XX
📅 As of: YYYY-MM-DD

Holdings:
• XX stocks
• X ETFs
• XX options

🌐 enhaq.capital
```

### Configuration

IBKR credentials stored in `.secrets/ibkr.env`:
```
IBKR_QUERY_ID=1420225
IBKR_TOKEN=238296570310971839485828
```

### Logs

Sync logs stored in `logs/sync_YYYYMMDD.log`

### Troubleshooting

**Sync fails:**
- Check IBKR credentials in `.secrets/ibkr.env`
- Verify Flex Query is active in IBKR portal
- Check logs for error details

**No Telegram notification:**
- Verify OpenClaw Telegram is configured: `openclaw status`
- Test notification manually: `python3 scripts/notify_telegram.py`

**Site not updating:**
- Check GitHub push succeeded: `git log -1`
- Verify GitHub Pages is enabled in repo settings
- Wait 1-2 minutes for deploy

## Return Calculation Fix (2026-03-02)

**Issue:** Returns were using first purchase price instead of average cost basis.

**Fix:** Now uses IBKR's actual cost basis (accounts for multiple buys/sells).

Example - ADBE:
- First buy: $495 (Apr 2024)
- Had 8 buys, then sold 100 shares
- Actual avg cost: $308.94
- Correct return: -15.1% (not -47%)

All positions now show accurate returns based on IBKR cost basis.
