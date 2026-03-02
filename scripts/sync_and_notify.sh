#!/bin/bash
# Portfolio sync with notification
# Run this daily at 9 AM Dubai time

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "📊 Starting IBKR portfolio sync..."

# Run sync
if python3 scripts/sync_ibkr.py; then
    echo "✅ Sync successful"
    
    # Check if there are changes to commit
    if ! git diff --quiet data/holdings.json holdings.html; then
        # Commit and push
        git add data/holdings.json holdings.html index.html
        git commit -m "Auto-update: IBKR sync $(date +%Y-%m-%d)"
        git push origin main
        
        echo "✅ Changes deployed to enhaq.capital"
        
        # Output notification message (OpenClaw will capture this)
        python3 scripts/notify_telegram.py
    else
        echo "ℹ️  No changes detected"
    fi
else
    echo "❌ Sync failed"
    exit 1
fi
