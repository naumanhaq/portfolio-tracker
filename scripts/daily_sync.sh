#!/bin/bash
# Daily IBKR portfolio sync with Telegram notification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/logs/sync_$(date +%Y%m%d).log"

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

# Run sync and capture output
echo "========================================" >> "$LOG_FILE"
echo "Sync started: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

cd "$PROJECT_ROOT"
python3 scripts/sync_ibkr.py >> "$LOG_FILE" 2>&1

SYNC_STATUS=$?

if [ $SYNC_STATUS -eq 0 ]; then
    echo "✅ Sync completed successfully" >> "$LOG_FILE"
    
    # Check for changes
    if git diff --quiet data/holdings.json; then
        echo "ℹ️  No changes detected" >> "$LOG_FILE"
    else
        echo "📊 Changes detected, committing..." >> "$LOG_FILE"
        
        # Commit and push changes
        git add data/holdings.json holdings.html index.html
        git commit -m "Auto-update: IBKR sync $(date +%Y-%m-%d)"
        git push origin main >> "$LOG_FILE" 2>&1
        
        echo "✅ Changes deployed to enhaq.capital" >> "$LOG_FILE"
        
        # Trigger Telegram notification via OpenClaw
        echo "PORTFOLIO_UPDATED" > /tmp/portfolio_update_trigger
    fi
else
    echo "❌ Sync failed with status $SYNC_STATUS" >> "$LOG_FILE"
    echo "PORTFOLIO_SYNC_FAILED" > /tmp/portfolio_update_trigger
fi

echo "========================================" >> "$LOG_FILE"
echo "Sync ended: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
